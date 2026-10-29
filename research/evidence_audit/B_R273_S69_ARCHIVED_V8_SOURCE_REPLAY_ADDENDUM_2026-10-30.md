# B addendum: R273 S69 archived source V8 replay

Date: 2026-10-30 Asia/Singapore. After the main B audit, the actual GitHub archived files were re-read from main and their calculation functions executed in the V8 tool runtime.

Remote R source blob a40f9b04d99e264fa854438dbac77974c8eb5b1a. Remote B grouped oracle blob dece06a95ada9ede465a9bf63f056bc7935374bf. Remote exact JSON blob 78eeeaaceb082befd99284e4335519e857eb0d6c, 5761 UTF-8 characters. Remote full CSV blob 9d0488797e3ac362b011a0b3a9868c5ccd914dbb, 23635 UTF-8 characters.

The exact archived R function generated JSON whose pretty-printed text equals the entire persisted JSON byte-for-byte in the tool's UTF-8 representation, and CSV equals the entire persisted CSV. The exact archived B function independently verified all 9 worlds, 135 grouped cells and 158 persisted receipt fields. Both operations returned PASS. No source changes were needed. This is V8 execution of archived calculation functions, not the original Node CLI entrypoint; Node native CLI remains NOT_RUN. It is an internal, nonblind programmatic replay, not external independent reproduction. No CI was dispatched and no fee-bearing service was invoked.
