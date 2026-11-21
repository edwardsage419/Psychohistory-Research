# Psychohistory Mobile v0.1 engineering bootstrap

Status: **PARTIAL / NOT ACCEPTED**. Owner-authorized full development is tracked in GitHub issue #58. This folder is an independently runnable offline architecture and two initial mathematical candidate methods, **not a fully portable Platform v0.5**.

## Goal

An independent iPhone-local personal intelligent decision assistant. After an initial secure HTTPS installation, computation and explicitly authorized personal records must work even when the phone is offline and the Mac is powered down. Its architecture must reuse Platform v0.5 model identities and reproducible contracts. Future upgrades must preserve the user's final choice, privacy and permission boundaries.

## What works in this bootstrap

* No dependency on Python, remote API, installed npm dependencies, or a running Mac for **prototype** mathematical operations.
* Browser-local rational arithmetic for finite point-utility scenario minimax regret and two-stage finite-signal information value, conditional on user-supplied data. Hard constraints distinguish ACCEPT, REJECT and UNRESOLVED.
* An open natural-language question field with explicitly labeled, manual structured JSON fallback. **No autonomous NLP and no full model orchestration yet.**
* Local password-protected AES-GCM encryption and IndexedDB storage after explicit consent; encrypted export. No plaintext records are written into CacheStorage.
* Service Worker precaches public application files for offline Home Screen use after successful HTTPS installation.

## Known gaps blocking release

* Mobile-ported full Platform v0.5 decision contract, model registry, interval and dependency robust analysis, deadline/time, full UI workflow, historical review/restore and preferences are NOT implemented. The present point-utility math is an engineering candidate pending cross-language independent parity.
* **Do not use as a production personal archive.** Revocation ledger, rollback rejection, signed backup migration from Platform v0.5, secured encrypted import/restore, session cleanup/OS caching boundaries and comprehensive storage eviction handling are pending. An exported ciphertext blob currently has no safe app import path.
* Browser responsive checks, real iPhone Safari installed-app tests, offline cold-start and corrupted cache acceptance are NOT_RUN.
* PWA service workers and crypto require a secure context (HTTPS, or localhost for laptop preview). One-time app distribution on a trustworthy HTTPS origin requires separate owner approval. Do not publish, merge to main or transmit private data without authorization.
* Android, WKWebView, native SwiftUI, cross-device synchronization, external autonomous inference, internet retrieval, action execution and empirical personal effectiveness are out of scope of the bootstrap.

## Local preview and tests

Requires Node.js 22 or newer for Node built-in test runner. No extra npm dependencies.


test:

    cd platform/mobile
    npm test

preview (localhost is a potentially trustworthy origin):

    npm run preview

Then open http://127.0.0.1:8766 on the **same** computer. On iPhone an actual secure HTTPS origin is needed for reliable installation and service worker operation. A localhost URL on Mac is not accessible through iPhone's own localhost.

The app's initial demo numbers are **synthetic**. If a user replaces them with their own values, these remain unverified user inputs; the app makes no empirical probability claims. No confidential data may be included in public test fixtures or GitHub.

## Governance

* Parent project: edwardsage419/Psychohistory-Research.
* Fixed baseline: merge of Platform v0.5, commit 0e574a7c7077824bb700d5fa9c5654e39348fe79.
* Full task: https://github.com/edwardsage419/Psychohistory-Research/issues/58
* Free tools and no paid API or deployment. R073, PESEN v0.1 and frozen research unaffected.
* Once Codex picks up this branch, the entire v0.1 acceptance contract in issue #58 remains binding. The bootstrap passes only local self-tests.
