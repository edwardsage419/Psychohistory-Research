import * as vault from '/vault.mjs';

const password = 'synthetic offline vault passphrase';
const sample = { decisions: [{ id: 'a', title: 'synthetic confidential topic' }] };
const revised = { decisions: [{ id: 'b', title: 'second confidential topic' }] };
const results = [];

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

async function rejects(operation, message) {
  try {
    await operation();
  } catch (error) {
    if (error instanceof TypeError) throw error;
    return;
  }
  throw new Error(message);
}

async function check(name, body, { fresh = false } = {}) {
  try {
    if (!fresh) await vault.removeLocalRecord();
    await body();
    results.push({ name });
  } catch (error) {
    results.push({ name, error: error.stack });
  }
}

function deleteStorageSlot(slot) {
  return new Promise((resolve, reject) => {
    const opening = indexedDB.open('psychohistory-mobile-v01-dev', 1);
    opening.onerror = () => reject(opening.error);
    opening.onsuccess = () => {
      const db = opening.result;
      const transaction = db.transaction('records', 'readwrite');
      transaction.oncomplete = () => { db.close(); resolve(); };
      transaction.onabort = () => { db.close(); reject(transaction.error); };
      transaction.objectStore('records').delete(slot);
    };
  });
}

await check('Session-only inspection leaves a fresh install without a vault database', async () => {
  assert(await vault.localRecordStatus() === 'missing', 'A fresh profile reported saved data');
  await rejects(() => vault.loadAuthorizedRecord(password), 'Loading produced a record from an empty profile');
  await rejects(() => vault.saveAuthorizedRecord(sample, password, false), 'Saving succeeded without consent');
  const databases = await indexedDB.databases();
  assert(!databases.some(database => database.name === 'psychohistory-mobile-v01-dev'), 'Session-only operations created persistent storage');
  await vault.saveAuthorizedRecord(sample, password, true, { expectedGeneration: null });
  assert(await vault.localRecordStatus() === 'available', 'The first consent did not create a vault');
}, { fresh: true });

await check('Existing vault rejects overwrite with a different passphrase', async () => {
  await vault.saveAuthorizedRecord(sample, password, true);
  await rejects(() => vault.saveAuthorizedRecord(revised, 'unrelated synthetic passphrase', true), 'A wrong password overwrote an authorized record');
  const actual = await vault.loadAuthorizedRecord(password);
  assert(actual.decisions[0].id === 'a', 'Wrong-password save changed the active record');
});

await check('An encrypted backup restores only with explicit confirmation and the right passphrase', async () => {
  await vault.saveAuthorizedRecord(sample, password, true);
  const backup = await vault.exportEncryptedBlob();
  assert(!backup.includes(sample.decisions[0].title), 'Backup exposed decision text');
  await deleteStorageSlot('sealed-session');
  assert(await vault.localRecordStatus() === 'recoverable', 'The authorization ledger did not survive ciphertext loss');
  await rejects(() => vault.saveAuthorizedRecord(revised, password, true), 'An unauthenticated write replaced recoverable data');
  await rejects(() => vault.restoreEncryptedBlob(backup, password, false), 'Restore accepted without confirmation');
  await rejects(() => vault.restoreEncryptedBlob(backup, 'unrelated synthetic passphrase', true), 'Restore accepted the wrong passphrase');
  assert(await vault.localRecordStatus() === 'recoverable', 'Rejected restore changed stored state');
  await vault.restoreEncryptedBlob(backup, password, true);
  const actual = await vault.loadAuthorizedRecord(password);
  assert(actual.decisions[0].id === 'a', 'Restore did not reproduce the authorized record');
});

await check('A stale backup or writer cannot replace a newer authorized record', async () => {
  await vault.saveAuthorizedRecord(sample, password, true, { expectedGeneration: null });
  const backup = await vault.exportEncryptedBlob();
  const { generation } = await vault.loadAuthorizedRecordWithVersion(password);
  const updated = await Promise.allSettled([
    vault.saveAuthorizedRecord(revised, password, true, { expectedGeneration: generation }),
    vault.saveAuthorizedRecord({ decisions: [] }, password, true, { expectedGeneration: generation }),
  ]);
  assert(updated.filter(result => result.status === 'fulfilled').length === 1, 'A concurrent stale update was accepted');
  const latest = await vault.exportEncryptedBlob();
  await rejects(() => vault.restoreEncryptedBlob(backup, password, true), 'A stale backup replaced a newer record');
  assert(await vault.exportEncryptedBlob() === latest, 'The stale backup changed stored state');
});

await check('Revocation blocks backup recovery even after fresh consent', async () => {
  await vault.saveAuthorizedRecord(sample, password, true);
  const backup = await vault.exportEncryptedBlob();
  const { generation } = await vault.loadAuthorizedRecordWithVersion(password);
  await vault.removeLocalRecord();
  assert(await vault.localRecordStatus() === 'missing', 'Revocation left an active authorization');
  await rejects(() => vault.loadAuthorizedRecord(password), 'Revocation left a readable record');
  await rejects(() => vault.exportEncryptedBlob(), 'Revocation left an exportable record');
  await rejects(() => vault.restoreEncryptedBlob(backup, password, true), 'Revocation was bypassed');
  await rejects(() => vault.saveAuthorizedRecord(revised, password, true, { expectedGeneration: generation }), 'A stale writer reopened a revoked vault');
  await vault.saveAuthorizedRecord(revised, password, true, { expectedGeneration: null });
  await rejects(() => vault.restoreEncryptedBlob(backup, password, true), 'Fresh consent accepted a revoked backup');
});

await check('Revocation wins over a restore whose authentication finishes later', async () => {
  await vault.saveAuthorizedRecord(sample, password, true);
  const backup = await vault.exportEncryptedBlob();
  await deleteStorageSlot('sealed-session');

  // Pause after real WebCrypto authentication to place revocation before the commit.
  const decrypt = crypto.subtle.decrypt;
  const authentication = Promise.withResolvers();
  const commit = Promise.withResolvers();
  crypto.subtle.decrypt = async function (...args) {
    const plaintext = await decrypt.apply(this, args);
    authentication.resolve();
    await commit.promise;
    return plaintext;
  };
  try {
    const restore = vault.restoreEncryptedBlob(backup, password, true);
    await Promise.race([authentication.promise, restore]);
    await vault.removeLocalRecord();
    commit.resolve();
    await rejects(() => restore, 'An in-flight restore reversed revocation');
    assert(await vault.localRecordStatus() === 'missing', 'The revoked authorization became active');
  } finally {
    commit.resolve();
    crypto.subtle.decrypt = decrypt;
  }
});

await check('Lost authorization cannot be reconstituted from ciphertext or a backup', async () => {
  await vault.saveAuthorizedRecord(sample, password, true);
  const backup = await vault.exportEncryptedBlob();
  await deleteStorageSlot('authorization');
  assert(await vault.localRecordStatus() === 'missing', 'Ciphertext was treated as authorization');
  await rejects(() => vault.loadAuthorizedRecord(password), 'Orphan ciphertext was readable');
  await rejects(() => vault.exportEncryptedBlob(), 'Orphan ciphertext was exportable');
  await rejects(() => vault.restoreEncryptedBlob(backup, password, true), 'Backup reconstructed missing consent');
  await vault.saveAuthorizedRecord(revised, password, true, { expectedGeneration: null });
  await rejects(() => vault.restoreEncryptedBlob(backup, password, true), 'New consent inherited the lost authorization');
});

await check('Altered and incompatible backup files fail closed', async () => {
  await vault.saveAuthorizedRecord(sample, password, true);
  const backup = await vault.exportEncryptedBlob();
  const modified = JSON.parse(backup);
  modified.ciphertext = (modified.ciphertext[0] === 'A' ? 'B' : 'A') + modified.ciphertext.slice(1);
  await rejects(() => vault.restoreEncryptedBlob(modified, password, true), 'Altered ciphertext was accepted');
  await rejects(() => vault.restoreEncryptedBlob({ ...JSON.parse(backup), personal: 'unknown plaintext field' }, password, true), 'Unexpected plaintext metadata was accepted');
  const bootstrap = await vault.encryptRecord(sample, password);
  await rejects(() => vault.restoreEncryptedBlob(bootstrap, password, true), 'Legacy/bootstrap envelope was accepted');
  await rejects(() => vault.restoreEncryptedBlob('{"format":"psychohistory-platform-v0.5"}', password, true), 'Unsupported platform envelope was accepted');
  assert(await vault.exportEncryptedBlob() === backup, 'Rejected backup changed stored state');
});

await fetch('/results', { method: 'POST', body: JSON.stringify(results) });
