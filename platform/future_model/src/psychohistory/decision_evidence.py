"""Local conversational evidence, explicit corrections, and purpose restrictions.

The caller retains or authenticates the ledger server-side. Client-authored
claims may be passed to draft_claims, but neither a submitted ledger nor a
receipt supplied by itself establishes authority.
"""

from collections.abc import Callable, Iterable
from datetime import UTC, datetime
from hashlib import sha256
from typing import Annotated, Literal
import unicodedata

from pydantic import ConfigDict, Field, StringConstraints, field_validator, model_validator

from .contracts import canonical
from .decision_semantics import comparison
from .decision_state import Identity, InputModel, Kind, Text, TextLine

ClaimOrigin = Literal['USER', 'LOCAL_MODEL', 'RULES']
Purpose = Literal['save', 'personalization', 'research', 'training']
Digest = Annotated[str, StringConstraints(pattern=r'^[0-9a-f]{64}$')]
MAX_CLAIMS = 96
_PURPOSES = ('save', 'personalization', 'research', 'training')
_HARD_ROLES = {'constraint', 'strict_constraint'}


def _hash(value):
    return sha256(canonical(value).encode()).hexdigest()


def _time(value):
    if 'T' not in value:
        raise ValueError('Evidence timestamps must be ISO 8601 with a timezone')
    try:
        stamp = datetime.fromisoformat(value)
        if stamp.tzinfo is not None:
            return stamp.astimezone(UTC)
    except (ValueError, OverflowError):
        pass
    raise ValueError('Evidence timestamps must be ISO 8601 with a timezone')


def _now():
    return datetime.now(UTC).isoformat()


def _normalized(value):
    return unicodedata.normalize('NFC', value or '').strip()


class _Frozen(InputModel):
    model_config = ConfigDict(frozen=True)


class SourceMetadata(_Frozen):
    version: Text | None = None
    observed_at: Text | None = None
    population: Text | None = None
    scope: Text | None = None
    channel: Literal['user_self_report', 'separate_source'] | None = None
    source_identity: Text | None = None
    published_date: Text | None = None
    retrieved_at: Text | None = None


class ClaimInput(_Frozen):
    kind: Kind
    field: Text
    subject: TextLine
    value: TextLine
    unit: TextLine
    source: TextLine
    role: TextLine = ''
    metadata: SourceMetadata | None = None

    @model_validator(mode='after')
    def known_claim_has_value(self):
        if self.kind != 'unknown' and not self.value.strip():
            raise ValueError('A known claim requires a value')
        return self

    def content_sha256(self):
        return _hash(self.model_dump(mode='json'))

    def _duplicate_key(self):
        fields = (self.kind, self.field, self.subject, self.value, self.unit, self.source, self.role)
        metadata = self.metadata or SourceMetadata()
        return tuple(map(_normalized, (*fields, metadata.version, metadata.observed_at,
                                       metadata.population, metadata.scope, metadata.channel, metadata.source_identity,
                                       metadata.published_date, metadata.retrieved_at)))

    def _key(self):
        return _normalized(self.field), _normalized(self.subject)

    def _group_key(self):
        scope = self.metadata.scope if self.metadata else None
        basis = scope if self.role == 'scenario_score' and scope and scope.startswith('scenario-basis:') else None
        return (*self._key(), basis)

    def _comparison_scope(self):
        metadata = self.metadata or SourceMetadata()
        return tuple(map(_normalized, (self.unit, metadata.observed_at, metadata.population, metadata.scope)))

    def _supported(self):
        if self.kind == 'unknown' or not self.source.strip() or self.role == 'previous':
            return False
        return self.role != 'conditional' or self.field == 'move_if_onsite_max'


class OperatorProof(_Frozen):
    """Receipt authenticated by an operator verifier installed by the caller."""

    claim_id: Identity
    content_sha256: Digest
    issuer: Text
    verified_at: Text
    receipt: Text

    @field_validator('verified_at')
    @classmethod
    def check_time(cls, value):
        _time(value)
        return value


ProofVerifier = Callable[[OperatorProof], bool]


class EvidenceEntry(_Frozen):
    claim_id: Identity
    claim: ClaimInput
    origin: ClaimOrigin
    recorded_at: Text
    confirmed_at: Text | None = None
    supersedes: Identity | None = None
    operator_proof: OperatorProof | None = None


def _claim_id(claim, position):
    return _hash({'position': position, 'content_sha256': claim.content_sha256()})[:32]


def _validate_correction(candidate, prior):
    if prior.confirmed_at is None or prior.claim._group_key() != candidate.claim._group_key():
        raise ValueError('A correction must identify prior confirmed evidence about the same field and subject')
    old = prior.claim.metadata or SourceMetadata()
    new = candidate.claim.metadata or SourceMetadata()
    same_identity = old.source_identity == new.source_identity
    # A proposal cannot carry a proof. The correction can earn its own proof
    # after confirmation, but it cannot replace a separately verified quote.
    self_report = old.channel == new.channel == 'user_self_report' and prior.operator_proof is None
    same_source = _normalized(prior.claim.source) == _normalized(candidate.claim.source)
    if not same_identity or not (self_report or same_source) or (old.channel and new.channel and old.channel != new.channel):
        raise ValueError('Different sources must remain separate evidence')


def _proof_matches(entry, proof):
    return proof.claim_id == entry.claim_id and proof.content_sha256 == entry.claim.content_sha256()


def _proof_trusted(proof, verifier):
    if proof is None or verifier is None:
        return False
    try:
        return verifier(proof) is True
    except Exception:
        return False


class EvidenceLedger(_Frozen):
    entries: tuple[EvidenceEntry, ...] = Field(default=(), max_length=MAX_CLAIMS)

    @model_validator(mode='after')
    def coherent_history(self):
        seen = {}
        corrected = set()
        hard_constraints = set()
        for index, entry in enumerate(self.entries, 1):
            if entry.claim_id != _claim_id(entry.claim, index):
                raise ValueError('Evidence identity does not match its recorded content')
            recorded = _time(entry.recorded_at)
            if entry.confirmed_at is None:
                if entry.supersedes is not None or entry.operator_proof is not None:
                    raise ValueError('A proposal cannot correct or verify evidence')
            elif _time(entry.confirmed_at) < recorded:
                raise ValueError('Evidence confirmation predates its proposal')
            if entry.supersedes is not None:
                if entry.supersedes in corrected or entry.supersedes not in seen:
                    raise ValueError('Correction must refer to earlier, active evidence')
                prior = seen[entry.supersedes]
                _validate_correction(entry, prior)
                if entry.supersedes in hard_constraints:
                    if entry.claim.role not in _HARD_ROLES | {'revision'} or entry.claim.kind != 'fact':
                        raise ValueError('A hard constraint requires an explicit hard constraint revision')
                    # A bare revised number cannot silently turn a strict limit inclusive.
                    old_operator = comparison(prior.claim.source)
                    if entry.claim.role == 'revision' and (
                        prior.claim.role == 'strict_constraint' or old_operator in {'<', '>'}
                    ):
                        direction = old_operator[0] if old_operator in {'<', '>', '<=', '>='} else (
                            '>' if entry.claim.field.endswith('_min') else '<'
                        )
                        if comparison(entry.claim.source) not in {direction, direction + '='}:
                            raise ValueError('Revising a strict hard constraint requires an explicit comparison')
                    hard_constraints.add(entry.claim_id)
                if _time(entry.confirmed_at) < _time(prior.confirmed_at):
                    raise ValueError('Correction predates its original confirmation')
                corrected.add(entry.supersedes)
            if entry.claim.role in _HARD_ROLES:
                hard_constraints.add(entry.claim_id)
            if entry.operator_proof is not None and (
                not entry.claim._supported() or not _proof_matches(entry, entry.operator_proof)
            ):
                raise ValueError('Verification receipt does not match the sourced claim')
            seen[entry.claim_id] = entry
        return self

    def trace(self, *, verifier: ProofVerifier | None = None):
        superseded = {entry.supersedes for entry in self.entries if entry.supersedes is not None}
        by_field = {}
        entries = []
        for entry in self.entries:
            by_field.setdefault(entry.claim._group_key(), []).append(entry)
            proof = entry.operator_proof
            verified = _proof_trusted(proof, verifier)
            if entry.claim_id in superseded:
                status = 'SUPERSEDED'
            elif entry.confirmed_at is None:
                status = 'PROVISIONAL'
            elif verified:
                status = 'EXTERNALLY_VERIFIED'
            else:
                status = 'USER_CONFIRMED'
            trace = entry.model_dump(mode='json', exclude={'operator_proof'})
            if verified:
                trace['operator_verification'] = proof.model_dump(mode='json', include={'issuer', 'verified_at', 'content_sha256'})
            entries.append({**trace, 'status': status})
        return {'entries': entries, 'groups': [
            _group(field, subject, rows, superseded) for (field, subject, _), rows in by_field.items()
        ]}


def _group(field, subject, entries, superseded):
    active = [entry for entry in entries if entry.claim_id not in superseded and entry.confirmed_at is not None]
    proposed = [entry.claim_id for entry in entries if entry.confirmed_at is None]
    supported = [entry.claim for entry in active if entry.claim._supported()]
    value = unit = None
    if not supported:
        status = 'PROVISIONAL' if proposed and not active else 'UNKNOWN'
    elif len({claim._comparison_scope() for claim in supported}) > 1:
        status = 'INCOMPARABLE'
    elif len({_normalized(claim.value) for claim in supported}) > 1:
        status = 'CONFLICT'
    else:
        status = 'CONFIRMED'
        value = _normalized(supported[0].value)
        unit = _normalized(supported[0].unit) or None
    return {
        'field': field, 'subject': subject, 'status': status, 'value': value, 'unit': unit,
        'active_claim_ids': [entry.claim_id for entry in active], 'provisional_claim_ids': proposed,
        'claim_ids': [entry.claim_id for entry in entries],
    }


def draft_claims(ledger: EvidenceLedger, claims: Iterable[ClaimInput | dict], *, origin: ClaimOrigin = 'USER', dismissed: Iterable[str] = ()):
    """Add immutable, deduplicated proposals without changing current evidence."""
    if origin not in ('USER', 'LOCAL_MODEL', 'RULES'):
        raise ValueError('Unknown evidence origin')
    entries = list(ledger.entries)
    superseded = {entry.supersedes for entry in entries if entry.supersedes is not None}
    inactive = superseded | set(dismissed)
    known = {entry.claim._duplicate_key() for entry in entries if entry.claim_id not in inactive}
    for item in claims:
        claim = ClaimInput.model_validate(item)
        key = claim._duplicate_key()
        if key in known:
            continue
        if len(entries) >= MAX_CLAIMS:
            raise ValueError('The decision evidence ledger has reached its claim limit')
        entries.append(EvidenceEntry(claim_id=_claim_id(claim, len(entries) + 1), claim=claim,
                                     origin=origin, recorded_at=_now()))
        known.add(key)
    return EvidenceLedger(entries=tuple(entries))


def _replace_entry(ledger, claim_id, **changes):
    entries = tuple(entry.model_copy(update=changes) if entry.claim_id == claim_id else entry
                    for entry in ledger.entries)
    return EvidenceLedger(entries=entries)


def _find_entry(ledger, claim_id):
    try:
        return next(entry for entry in ledger.entries if entry.claim_id == claim_id)
    except StopIteration:
        raise ValueError('Unknown evidence claim') from None


def confirm_claim(ledger: EvidenceLedger, claim_id: str, *, mode='accept', supersedes: str | None = None):
    """Confirm an exact proposal or explicitly link a same-source correction."""
    if mode not in ('accept', 'correct') or (mode == 'correct') != (supersedes is not None):
        raise ValueError('Explicit corrections require the identity of the original claim')
    entry = _find_entry(ledger, claim_id)
    if entry.confirmed_at is not None:
        if entry.supersedes != supersedes:
            raise ValueError('A confirmed evidence entry is immutable')
        return ledger
    if entry.claim.role == 'revision' and mode == 'accept':
        superseded = {other.supersedes for other in ledger.entries if other.supersedes is not None}
        if any(other.confirmed_at is not None and other.claim_id not in superseded and other.claim._supported()
               and other.claim._key() == entry.claim._key() for other in ledger.entries):
            raise ValueError('A revision of existing evidence requires an explicit correction')
    return _replace_entry(ledger, claim_id, confirmed_at=_now(), supersedes=supersedes)


def verify_claim(ledger: EvidenceLedger, claim_id: str, proof: OperatorProof, *, verifier: ProofVerifier):
    """Attach only a proof accepted by a server-side trusted verifier."""
    entry = _find_entry(ledger, claim_id)
    if entry.confirmed_at is None or any(other.supersedes == claim_id for other in ledger.entries):
        raise ValueError('Only active confirmed evidence can be externally verified')
    if not isinstance(proof, OperatorProof) or not _proof_matches(entry, proof) or not entry.claim._supported():
        raise ValueError('Verification receipt does not match the sourced claim')
    if not _proof_trusted(proof, verifier):
        raise PermissionError('A trusted operator proof is required')
    if entry.operator_proof is not None and entry.operator_proof != proof:
        raise ValueError('A historical operator receipt is immutable')
    return _replace_entry(ledger, claim_id, operator_proof=proof)


class PurposeConsent(_Frozen):
    save: bool = Field(default=False, strict=True)
    personalization: bool = Field(default=False, strict=True)
    research: bool = Field(default=False, strict=True)
    training: bool = Field(default=False, strict=True)

    def allows(self, purpose: Purpose, *, active_save=False):
        return purpose == 'save' and self.save and active_save is True

    def status(self, *, active_save=False):
        return {purpose: {'requested': getattr(self, purpose), 'available': purpose == 'save',
                          'authorized': self.allows(purpose, active_save=active_save)} for purpose in _PURPOSES}
