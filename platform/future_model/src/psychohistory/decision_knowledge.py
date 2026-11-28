"""Offline discovery over fixed project notes. Search results confer no evidence authority."""
from collections import Counter, defaultdict
from copy import deepcopy
from functools import lru_cache
from hashlib import sha1, sha256
import json
import math
from pathlib import Path
import re
import unicodedata


VERSION = "offline-knowledge@1.1.0"
MANIFEST_PATH = Path("research/decision_hub/2026-11-24-method-corpus-index/corpus_index.json")
MANIFEST_BLOB = "6862d5a2cd3c7eb3f2da9a85d79c8b3386f2a102"
MANIFEST_SIZE = 154
POLICY_PATH = Path("docs/PUBLICATION_POLICY.md")
POLICY_BLOB = "319e9922bf2f05a66e69eaa504a76cd90ebee59a"
CORPUS_PATH = Path("research/decision_methods")
RANKING_SOURCE = "research/decision_hub/2026-11-24-content-method-retrieval/probe.js"
RANKING_BLOB = "7d78f8c89ac73a2228ddca40dd45ad8b02366554"
LICENCE = {
    "status": "NO_OPEN_LICENCE_DECLARED",
    "basis": POLICY_PATH.as_posix(),
    "distribution": "NO_ADDITIONAL_RIGHTS_GRANTED",
    "cited_external_works": "SEPARATE_RIGHTS_NOT_REVIEWED",
}
K1 = 1.2
B = 0.75
TOKEN = re.compile(r"[a-z]+[0-9]*|[\u3400-\u9fff]+")
ARCHIVE_DATE = re.compile(r"_(\d{4}-\d{2}-\d{2})\.md$")
BOUNDARY_HEADING = re.compile(r"assumption|applicab|limitation|failure|scope|假设|适用|局限|边界|失效|限制", re.I)
MAX_SOURCE_BYTES = 2 * 1024 * 1024


def _blob(raw):
    return sha1(f"blob {len(raw)}\0".encode("ascii") + raw, usedforsecurity=False).hexdigest()


def _read(root, relative):
    """Only read ordinary files inside the checkout, even in a damaged copy."""
    path = root / relative
    if path.resolve() != path or (path.exists() and not path.is_file()):
        raise OSError("source is not a regular checkout file")
    with path.open("rb") as stream:
        raw = stream.read(MAX_SOURCE_BYTES + 1)
    if len(raw) > MAX_SOURCE_BYTES:
        raise OSError("source exceeds size limit")
    return raw


def _verification(root, relative, expected_blob, expected_size=None):
    try:
        content = _read(root, relative)
    except FileNotFoundError:
        return {"path": str(relative), "expected_blob": expected_blob, "status": "MISSING"}, None
    except (OSError, RuntimeError):
        return {"path": str(relative), "expected_blob": expected_blob, "status": "UNREADABLE"}, None
    actual_blob = _blob(content)
    matches = actual_blob == expected_blob and (expected_size is None or len(content) == expected_size)
    return {
        "path": str(relative), "expected_blob": expected_blob,
        "actual_blob": actual_blob, "actual_size": len(content),
        "sha256": sha256(content).hexdigest(), "status": "VERIFIED" if matches else "CHANGED",
    }, content if matches else None


def _tokens(text):
    """Round 28 English tokens and Han bigrams, with Unicode width normalization."""
    for word in TOKEN.findall(unicodedata.normalize("NFKC", text).lower()):
        if word.isascii():
            if len(word) > 1:
                yield word
        else:
            for offset in range(len(word) - 1):
                yield word[offset:offset + 2]


def _excerpt(text, limit):
    return " ".join(text.split())[:limit]


def _header_excerpt(lines):
    for offset, line in enumerate(lines):
        if line.startswith("## ") and BOUNDARY_HEADING.search(line):
            for body_line in lines[offset + 1:]:
                if body_line.startswith("#"):
                    break
                if body_line.strip():
                    return _excerpt(body_line, 280)
    return None


def _make_card(row, content, snapshot):
    path = row["path"]
    date = ARCHIVE_DATE.search(path)
    title = next((line[2:] for line in content if line.startswith("# ")), Path(path).stem)
    boundary = _header_excerpt(content)
    return {
        "id": row["actual_blob"], "title": title, "theory": title,
        "path": path, "source": {"kind": "PROJECT_ARCHIVE", "path": path, "snapshot": snapshot},
        "version": row["actual_blob"], "date": date[1] if date else None,
        "date_kind": "ARCHIVE_FILENAME" if date else "UNKNOWN",
        "licence": dict(LICENCE), "fact_type": "PROJECT_RESEARCH_NOTE",
        "applicability_boundary": boundary,
        "applicability_status": "ARCHIVE_EXCERPT" if boundary else "UNKNOWN",
        "evidence_qualification": "RESEARCH_REFERENCE_ONLY",
        "scientific_acceptance": "NOT_INFERRED", "decision_evidence": "NOT_QUALIFIED",
        "linked_methods": list(row["linked_methods"]), "authority": "NONE",
    }


class KnowledgeIndex:
    """Immutable in-memory snapshot built from verified UTF-8 Markdown bodies."""

    def __init__(self, root):
        root = Path(root).resolve()
        self._root = root
        self._manifest, raw_manifest = _verification(root, MANIFEST_PATH, MANIFEST_BLOB)
        self._policy, policy = _verification(root, POLICY_PATH, POLICY_BLOB)
        self._rows = []
        self._edges = []
        self._methods = {}
        self._unlisted = []
        self._cards = []
        self._lines = []
        self._lengths = []
        self._postings = defaultdict(list)
        self._average_length = 0.0
        if raw_manifest is None:
            return

        manifest = json.loads(raw_manifest)
        snapshot = manifest["snapshot"]
        self._manifest["snapshot"] = snapshot
        self._methods = {method["key"]: method for method in manifest["methods"]}
        known_paths = {asset["path"] for asset in manifest["assets"]}
        assert len(known_paths) == len(manifest["assets"]) == MANIFEST_SIZE
        scope = root / CORPUS_PATH
        try:
            ordinary_scope = scope.resolve() == scope
        except (OSError, RuntimeError):
            ordinary_scope = False
        if ordinary_scope:
            self._unlisted = sorted(
                path.relative_to(root).as_posix() for path in scope.glob("*.md")
                if path.relative_to(root).as_posix() not in known_paths
            )
        relations = defaultdict(list)
        for relation in manifest["relations"]:
            relations[relation["path"]].append(relation)

        seen_blobs = {}
        by_path = {}
        for asset in manifest["assets"]:
            path = asset["path"]
            row, raw = _verification(root, Path(path), asset["blob"], asset["size"])
            row.update({
                "expected_size": asset["size"], "linked_methods": asset["linkedMethods"],
                "relations": relations[path], "licence": dict(LICENCE) if policy else {"status": "UNKNOWN"},
                "indexed": False, "duplicate_of": None, "token_count": 0, "historical_source_changes": [],
                "identity": row["status"],
            })
            by_path[path] = row
            self._rows.append(row)
            if raw is None:
                continue
            if asset["blob"] in seen_blobs:
                row.update(status="BYTE_DUPLICATE", duplicate_of=seen_blobs[asset["blob"]])
                continue
            seen_blobs[asset["blob"]] = path
            if not policy:
                row["status"] = "LICENCE_POLICY_UNVERIFIED"
                continue
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                row["status"] = "INVALID_UTF8"
                continue
            frequency = Counter(_tokens(text))
            if not frequency:
                row["status"] = "EMPTY_TEXT"
                continue
            length = sum(frequency.values())
            doc = len(self._cards)
            lines = tuple(text.splitlines())
            row.update(status="INDEXED", indexed=True, token_count=length)
            self._cards.append(_make_card(row, lines, snapshot))
            self._lines.append(lines)
            self._lengths.append(length)
            for term, count in frequency.items():
                self._postings[term].append((doc, count))

        if self._lengths:
            self._average_length = sum(self._lengths) / len(self._lengths)
        for method in manifest["methods"]:
            for source in method["sources"]:
                row = by_path[source["path"]]
                self._edges.append({
                    "method": method["key"], "path": source["path"],
                    "expected_current_blob": source["currentBlob"], "historical_blob": source["baselineBlob"],
                    "historical_status": source["status"], "checkout_status": row["status"],
                    "checkout_blob": row.get("actual_blob"),
                })
                if source["status"] == "CHANGED":
                    row["historical_source_changes"].append({
                        "method": method["key"], "historical_blob": source["baselineBlob"],
                        "manifest_blob": source["currentBlob"],
                    })

    @property
    def status(self):
        if not self._cards:
            return "UNAVAILABLE"
        if len(self._cards) == MANIFEST_SIZE and not self._unlisted:
            return "AVAILABLE"
        return "PARTIAL"

    def _controls_current(self):
        return all(
            _verification(self._root, path, blob)[0]["status"] == "VERIFIED"
            for path, blob in ((MANIFEST_PATH, MANIFEST_BLOB), (POLICY_PATH, POLICY_BLOB))
        )

    def report(self):
        statuses = Counter(row["status"] for row in self._rows)
        counts = {
            "expected": MANIFEST_SIZE, "indexed": len(self._cards),
            "identity_verified": sum(row["identity"] == "VERIFIED" for row in self._rows),
            "missing": statuses["MISSING"], "changed": statuses["CHANGED"], "unreadable": statuses["UNREADABLE"],
            "byte_duplicates": statuses["BYTE_DUPLICATE"], "invalid_utf8": statuses["INVALID_UTF8"],
            "licence_policy_unverified": statuses["LICENCE_POLICY_UNVERIFIED"],
            "empty_text": statuses["EMPTY_TEXT"], "unlisted": len(self._unlisted),
            "documented_duplicate_supplements": sum(
                relation["relation"].startswith("DUPLICATE_")
                for row in self._rows for relation in row["relations"]
            ),
            "source_edges": len(self._edges), "historical_source_changes": sum(
                edge["historical_status"] == "CHANGED" for edge in self._edges
            ),
            "body_bytes": sum(row["actual_size"] for row in self._rows if row["indexed"]),
            "tokens": sum(self._lengths), "unique_terms": len(self._postings),
        }
        return deepcopy({
            "version": VERSION, "status": self.status, "authority": "NONE",
            "snapshot_scope": "INDEX_BUILD_TIME",
            "manifest": self._manifest, "publication_policy": self._policy,
            "counts": counts, "documents": self._rows, "source_edges": self._edges,
            "unlisted_paths": self._unlisted,
            "ranking": {"algorithm": "BM25", "k1": K1, "b": B, "source": RANKING_SOURCE, "blob": RANKING_BLOB},
        })

    def search(self, query, limit=5):
        if not isinstance(query, str) or len(query) > 6000:
            raise ValueError("knowledge query must be text up to 6000 characters")
        if type(limit) is not int or not 1 <= limit <= 20:
            raise ValueError("knowledge search limit must be 1–20")
        result = {"version": VERSION, "status": self.status, "authority": "NONE",
                  "ranking": "BM25_BODY_LEXICAL_RELEVANCE", "hits": [], "omitted_stale_hits": 0}
        if not self._controls_current():
            return {**result, "status": "UNAVAILABLE"}
        terms = list(dict.fromkeys(_tokens(query)))
        scores = defaultdict(float)
        total = len(self._cards)
        for term in terms:
            postings = self._postings.get(term)
            if not postings:
                continue
            df = len(postings)
            idf = math.log1p((total - df + 0.5) / (df + 0.5))
            for doc, count in postings:
                norm = 1 - B + B * self._lengths[doc] / self._average_length
                scores[doc] += idf * count * (K1 + 1) / (count + K1 * norm)
        ranked = sorted(scores, key=lambda doc: (-scores[doc], self._cards[doc]["path"]))[:limit]
        term_set = set(terms)
        for doc in ranked:
            card = self._cards[doc]
            identity, _ = _verification(self._root, Path(card["path"]), card["version"])
            if identity["status"] != "VERIFIED":
                result["omitted_stale_hits"] += 1
                result["status"] = "PARTIAL"
                continue
            lines = self._lines[doc]
            line = max(lines, key=lambda value: len(term_set.intersection(_tokens(value))))
            result["hits"].append({"card": deepcopy(card), "relevance": scores[doc], "snippet": _excerpt(line, 240)})
        return result

    def method_sources(self, method):
        """Match native registered paths and versions to the archived exact source edges."""
        archived = self._methods.get(method.key)
        edges = []
        for edge in self._edges:
            if edge["method"] != method.key:
                continue
            current, _ = _verification(self._root, Path(edge["path"]), edge["expected_current_blob"])
            edges.append({**edge, "current_verification": current["status"]})
        native_paths = (method.sources,) if isinstance(method.sources, str) else method.sources
        matches = (archived and method.source_baseline == archived["sourceBaseline"]
                   and method.candidate_scope == archived["scope"]
                   and list(method.depends_on) == archived["declaredDependencies"]
                   and set(native_paths) == {edge["path"] for edge in edges})
        matched_bytes = all(
            edge["checkout_status"] in {"INDEXED", "BYTE_DUPLICATE"}
            and edge["checkout_blob"] == edge["expected_current_blob"]
            and edge["historical_status"] == "MATCH"
            and edge["current_verification"] == "VERIFIED"
            for edge in edges
        )
        return ("MATCHED_REFERENCE_ONLY" if matches and matched_bytes and self._controls_current()
                else "REVIEW_REQUIRED"), edges


@lru_cache(maxsize=1)
def local_knowledge():
    return KnowledgeIndex(Path(__file__).resolve().parents[4])


def discover_knowledge(goal, *, index=None, limit=5):
    from .decision_knowledge_planning import discover

    return discover(goal, index if index is not None else local_knowledge(), limit=limit)


def main():
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[4])
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("report", help="Report identity, indexing, licence and change status per document")
    search = commands.add_parser("search", help="Rank verified Markdown document bodies")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=5)
    discovery = commands.add_parser("discover", help="Plan evidence needs for a supported explicit goal")
    discovery.add_argument("goal")
    discovery.add_argument("--limit", type=int, default=5)
    arguments = parser.parse_args()
    index = KnowledgeIndex(arguments.root)
    if arguments.command == "report":
        result = index.report()
    elif arguments.command == "search":
        result = index.search(arguments.query, arguments.limit)
    else:
        result = discover_knowledge(arguments.goal, index=index, limit=arguments.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
