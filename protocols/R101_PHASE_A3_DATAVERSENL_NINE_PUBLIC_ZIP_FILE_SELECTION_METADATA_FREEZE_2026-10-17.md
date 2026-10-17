# R101 Phase A3: official DataverseNL public ZIP file identity and selection metadata freeze

Date: 2026-10-17. State: FROZEN_BEFORE_FIRST_FILENAME_METADATA_RETRIEVAL. PESEN v0.1 remains FROZEN.

Phase A2 has independently verified DOI 10.34894/EYFM5L through the first-party DataverseNL API, with 9 ZIP file entries and 43,631,177 cumulative reported bytes. It has not verified any archive payload bytes, raw human actors, opponents, actions, sessions, or scores. Earlier Phase A/A2 receipt contents and the initial failed DOI field receipt stay unchanged.

## Scope and one additional disclosure authorization

Retrieve only the exact previously frozen `https://dataverse.nl/api/datasets/:persistentId/?persistentId=doi%3A10.34894%2FEYFM5L` JSON metadata through the same HTTPS host-checked redirect handler and strict DOI validation. The former A2 summary suppressed public filenames and file IDs. This *new*, previously frozen Phase A3 permits releasing exactly the **already-public Dataverse archive filenames, numeric dataFile IDs, bytes, published checksum fields if present, and bounded sanitized public file description**. These are repository file-catalog identifiers, not participant identifiers or the identity of a research participant. Only release if all filenames conform to ASCII basename `[A-Za-z0-9_.() -]{1,120}`, no path separators or dot-only basename, and description is ASCII-printable, at most 300 characters, with no URL, email, path, or sensitive identifier patterns. If any description fails, omit its content and publish a boolean description withheld. Never publish original metadata JSON as a whole, auth tokens, access requests, file contents, or file-level dataset byte samples.

Require exactly the same DOI and nine registered ZIPs; require each numeric `dataFile.id` to be a positive integer unique across the catalog; `filesize` a nonnegative integer <=100 MB, sum 43,631,177 bytes; `filename` ZIP extension; `dataFile.storageIdentifier` or URL not emitted; no direct /api/access/datafile request yet.

## Research decision

Once the public file list is authenticated, select a single ZIP with published filename and descriptive metadata suggesting raw experimental behavioral observations and accompanying codebook. Rank by metadata *before downloading*. Reject ambiguous multiple equally plausible raw files and explicitly freeze any decision. File size or ordinal alone cannot prove the contents are human behavior. For the selected file, separately freeze its exact ID, byte size, access URL, download redirect whitelist, maximum decompressed byte count, expected official checksum when independently present, secure ZIP member name-only audit, and acceptable source schema. ZIP contents and participant actions remain uninspected in A3. No E1/E2 credit from an API listing or synthetic tests.

Tests first, real publisher API second, machine receipt committed back to main through GitHub Actions. Synthetic tests cover malicious filename, duplicate file ID, wrong DOI, unsupported extension, unsafe description, missing published files, unexpected total, and private metadata suppression. On any mismatch, fail closed and preserve the negative result. All past negative findings remain, no model tuning, no person-level linkage attempted.

R101 A3 can only raise source catalog specificity to E0 metadata identification. R073 and PESEN v0.1 model/scoring remain frozen.
