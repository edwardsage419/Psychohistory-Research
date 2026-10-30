# F009 phase18: low-cardinality appeal audit hashes and residual linkability

UTC 2026-10-30. Track privacy_safety. Weekly theme F009 continued with a new bounded phase. Target (privacy_safety,F009,phase18,small-domain-hash-dictionary-and-retention). Status COMPLETE_BOUNDED_PRIMARY_GUIDANCE_PLUS_SYNTHETIC_TEST.

## English primary standards and status

* UK ICO, Pseudonymisation guidance, accessed 2026-10-30: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/pseudonymisation/ . Pseudonymised information can remain personal data; simple unsalted hashes are vulnerable to guessing. The ICO discusses appropriate cryptographic protection and linkage.
* EDPB Guidelines 01/2025 on Pseudonymisation, published as a version for public consultation, accessed 2026-10-30: https://www.edpb.europa.eu/public-consultations/guidelines-012025-on-pseudonymisation_en . The summary explains that linkable pseudonymised information remains personal data. This source is a consultation draft and is not treated as final binding law.
* OWASP Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html . Minimise sensitive identifiers and secrets in logs, prevent tampering, protect access, and define retention and disposal.
* NIST SP 800-63B-4: https://pages.nist.gov/800-63-4/sp800-63b.html . Recovery events require notification, but the standard does not establish a universal 30-day or 90-day appeal retention period.

## Actually executed synthetic SHA256 and HMAC experiment

Executed archived standard-library Python 3.13.5 `research/privacy_safety/f009_phase18_small_domain_hash_20261030.py`. Eight assertions PASS. Built 16 fictional audit states as four generic appeal labels OPEN/PENDING/REVIEW/CLOSED crossed with four relative day buckets 0/1/2/3. Computed SHA256 of each label and SHA256 of a known fixed public-salt prefix plus each label. An attacker who knows the 16-state vocabulary can enumerate all candidates offline: 16/16 unsalted hashes and 16/16 public-salted hashes are recoverable by exact dictionary lookup. A demonstration HMAC-SHA256 with a secret key has 0/16 matches under a deliberately wrong guessed key.

The experiment illustrates a tiny-domain offline dictionary, not a SHA256 collision, cryptographic break, real re-identification, or evidence that secret-key HMAC is always secure. A private HMAC key must be protected, rotated and destroyed appropriately. Pseudonymised records may still be linkable, and their personal-data legal classification depends on circumstances and jurisdiction.

## Candidate future safety controls, no implementation authorization

Keep detailed appeal evidence in a separate, access-controlled store with a documented purpose and review/deletion schedule. Use a minimal opaque event reference in the main log, with short retention and separate access controls; avoid stable globally reused user hashes. When keyed commitments are justified, bind purpose, key version and expiry, and plan key erasure without promising that deletion of a key removes all copies. Preserve narrowly justified evidence during a genuine pending appeal, but require periodic independent review to prevent indefinite retention via repeated spurious disputes. Log denial or appeal states without raw account secrets, health, relationship or financial content. Provide human challenge/override and make missing revocation evidence explicit. These are research proposals, not adopted security requirements or legal advice.

Evidence: PRIMARY_REGULATORY_GUIDANCE + OWASP_STANDARD_GUIDANCE + INTERNAL_NONBLIND_SYNTHETIC_ENGINEERING. No actual user data, live credentials, emails, crypto attack, app implementation or external evaluation. New E2=0, E3=0. No paid service, cloud compute, CI or API. Next phase19: evaluate scoped pseudonym rotation and deletion of cross-archive link tables using an artificial threat model.
