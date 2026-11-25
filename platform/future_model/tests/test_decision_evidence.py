from hashlib import sha256
import hmac

import pytest

from psychohistory.decision_evidence import (
    ClaimInput, EvidenceLedger, OperatorProof, PurposeConsent, confirm_claim, draft_claims, verify_claim,
)


def claim(value='10', source='Fictional offer letter', **changes):
    return dict(kind='fact', field='weekly_hours', subject='Offer A', value=value,
                unit='hours', source=source) | changes


def confirmed(*claims):
    ledger = draft_claims(EvidenceLedger(), claims, origin='USER')
    for entry in ledger.entries:
        ledger = confirm_claim(ledger, entry.claim_id)
    return ledger


def test_proposals_cannot_replace_confirmed_values_or_self_verify():
    original = confirmed(claim())
    updated = draft_claims(original, [claim('80', 'Fictional recruiter')], origin='LOCAL_MODEL')
    assert updated.trace()['groups'][0]['value'] == '10'
    assert updated.trace()['entries'][1]['status'] == 'PROVISIONAL'
    assert original.trace()['entries'][0]['status'] == 'USER_CONFIRMED'
    with pytest.raises(ValueError):
        ClaimInput.model_validate(claim(verification='external'))


def test_distinct_sources_conflict_without_overwriting_and_duplicate_delivery_is_idempotent():
    ledger = confirmed(claim())
    duplicate = draft_claims(ledger, [claim()], origin='RULES')
    assert duplicate == ledger
    alternate = draft_claims(ledger, [claim('12', 'Fictional handbook')], origin='USER')
    first, second = alternate.entries
    with pytest.raises(ValueError):
        confirm_claim(alternate, second.claim_id, mode='correct', supersedes=first.claim_id)
    explicit = confirm_claim(alternate, second.claim_id)
    row = explicit.trace()['groups'][0]
    assert row['status'] == 'CONFLICT'
    assert row['value'] is None
    assert set(row['active_claim_ids']) == {first.claim_id, second.claim_id}


def test_confirmed_explicit_correction_retains_the_old_evidence_as_superseded():
    ledger = confirmed(claim())
    drafted = draft_claims(ledger, [claim('11', metadata={'version': '2'})], origin='USER')
    first, second = drafted.entries
    edited = confirm_claim(drafted, second.claim_id, mode='correct', supersedes=first.claim_id)
    assert confirm_claim(edited, second.claim_id, mode='correct', supersedes=first.claim_id) == edited
    trace = edited.trace()
    assert trace['groups'][0]['value'] == '11'
    assert trace['entries'][0]['status'] == 'SUPERSEDED'
    assert trace['entries'][0]['claim']['value'] == '10'
    assert trace['entries'][1]['supersedes'] == first.claim_id


def test_explicit_conversational_correction_can_use_a_new_quoted_utterance():
    metadata = dict(channel='user_self_report', source_identity='current_user')
    ledger = confirmed(claim('10', 'I can do ten hours.', role='constraint', metadata=metadata))
    drafted = draft_claims(ledger, [claim('12', 'Correction to twelve hours.', role='revision', metadata=metadata)])
    first, second = drafted.entries
    with pytest.raises(ValueError):
        confirm_claim(drafted, second.claim_id)
    corrected = confirm_claim(drafted, second.claim_id, mode='correct', supersedes=first.claim_id)
    assert corrected.trace()['groups'][0]['value'] == '12'


def test_previous_and_conditional_claims_do_not_become_unconditional_evidence():
    ledger = confirmed(claim('10', role='constraint'), claim('15', role='previous'), claim('20', role='conditional'))
    row = ledger.trace()['groups'][0]
    assert row['value'] == '10'
    assert len(row['claim_ids']) == 3


def test_operator_verification_blocks_replacing_prior_verbatim_source_via_self_report():
    metadata = dict(channel='user_self_report', source_identity='current_user')
    ledger = confirmed(claim('10', 'Ten hours per week.', role='constraint', metadata=metadata))
    original = ledger.entries[0]
    proof = OperatorProof(claim_id=original.claim_id, content_sha256=original.claim.content_sha256(),
                          issuer='Example operator', verified_at='2026-11-24T00:00:00+00:00', receipt='proof')
    checked = verify_claim(ledger, original.claim_id, proof, verifier=lambda package: package == proof)

    drafted = draft_claims(checked, [claim('12', 'Correction to twelve hours.', role='revision', metadata=metadata)])
    with pytest.raises(ValueError):
        confirm_claim(drafted, drafted.entries[1].claim_id, mode='correct', supersedes=original.claim_id)


def test_a_corrected_self_report_can_receive_separate_operator_verification():
    metadata = dict(channel='user_self_report', source_identity='current_user')
    ledger = confirmed(claim('10', 'Ten hours per week.', role='constraint', metadata=metadata))
    drafted = draft_claims(ledger, [claim('12', 'Correction to twelve hours.', role='revision', metadata=metadata)])
    first, edited = drafted.entries
    accepted = confirm_claim(drafted, edited.claim_id, mode='correct', supersedes=first.claim_id)
    proof = OperatorProof(claim_id=edited.claim_id, content_sha256=edited.claim.content_sha256(),
                          issuer='Example operator', verified_at='2026-11-24T00:00:00+00:00', receipt='proof')
    authorized = lambda package: package == proof
    checked = verify_claim(accepted, edited.claim_id, proof, verifier=authorized)
    traces = checked.trace(verifier=authorized)['entries']
    assert traces[0]['status'] == 'SUPERSEDED'
    assert traces[1]['status'] == 'EXTERNALLY_VERIFIED'
    assert traces[1]['operator_verification']['issuer'] == 'Example operator'


def test_incomparable_units_and_population_are_retained_without_average():
    ledger = confirmed(
        claim(metadata={'population': 'City A staff', 'version': '1'}),
        claim('0.5', 'Fictional labor summary', unit='days', metadata={'population': 'City B staff'}),
    )
    row = ledger.trace()['groups'][0]
    assert row['status'] == 'INCOMPARABLE'
    assert row['value'] is None
    assert ledger.trace()['entries'][0]['claim']['metadata']['version'] == '1'


def test_unknown_without_source_cannot_become_eligible_after_confirmation():
    ledger = confirmed(claim('120', '', kind='estimate'))
    trace = ledger.trace()
    assert trace['groups'][0]['status'] == 'UNKNOWN'
    assert trace['groups'][0]['value'] is None
    assert trace['entries'][0]['status'] == 'USER_CONFIRMED'


def test_external_proof_binds_operator_to_exact_confirmed_claim_and_is_revalidated():
    ledger = confirmed(claim(metadata={
        'version': 'offer-v2', 'observed_at': '2026-11-23T09:00:00+00:00', 'population': 'example employees',
    }))
    entry = ledger.entries[0]
    key = b'fictional test key controlled by the operator'
    receipt = hmac.new(key, entry.claim.content_sha256().encode(), sha256).hexdigest()
    proof = OperatorProof(claim_id=entry.claim_id, content_sha256=entry.claim.content_sha256(),
                          issuer='Synthetic test operator', verified_at='2026-11-24T10:00:00+00:00', receipt=receipt)

    def valid(candidate):
        expected = hmac.new(key, candidate.content_sha256.encode(), sha256).hexdigest()
        return candidate.issuer == 'Synthetic test operator' and hmac.compare_digest(candidate.receipt, expected)

    forged = proof.model_copy(update={'content_sha256': '0' * 64})
    with pytest.raises(ValueError):
        verify_claim(ledger, entry.claim_id, forged, verifier=lambda _: True)
    with pytest.raises(PermissionError):
        verify_claim(ledger, entry.claim_id, proof, verifier=lambda _: False)
    checked = verify_claim(ledger, entry.claim_id, proof, verifier=valid)
    assert checked.trace()['entries'][0]['status'] == 'USER_CONFIRMED'
    status = checked.trace(verifier=valid)['entries'][0]
    assert status['status'] == 'EXTERNALLY_VERIFIED'
    assert status['claim']['metadata']['population'] == 'example employees'


def test_purpose_permission_defaults_closed_and_save_requires_live_consent():
    assert all(not receipt['authorized'] for receipt in PurposeConsent().status(active_save=True).values())
    requested = PurposeConsent(save=True, personalization=True, research=True, training=True)
    assert not requested.allows('save')
    assert requested.allows('save', active_save=True)
    for purpose in ('personalization', 'research', 'training'):
        assert requested.status(active_save=True)[purpose] == {
            'requested': True, 'available': False, 'authorized': False,
        }
    with pytest.raises(ValueError):
        PurposeConsent.model_validate({'save': 'true'})
