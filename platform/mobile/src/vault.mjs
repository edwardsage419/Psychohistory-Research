/** Same-install encrypted storage. The authorization ledger is never included in a backup. */
const enc = new TextEncoder();
const dec = new TextDecoder('utf-8', { fatal: true });
const DB = 'psychohistory-mobile-v01-dev';
const SLOT = 'sealed-session';
const LEDGER = 'authorization';
const LEGACY_FORMAT = 'psychohistory-mobile-v01-dev';
const VAULT_FORMAT = 'psychohistory-mobile-v01-vault';
const ITERATIONS = 310000;
const KDF = 'PBKDF2-SHA256';
const CIPHER = 'AES-256-GCM';
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;

function bytesToB64(bytes) {
  const chunks = [];
  for (let start = 0; start < bytes.length; start += 8192) {
    chunks.push(String.fromCharCode(...bytes.subarray(start, start + 8192)));
  }
  return btoa(chunks.join(''));
}

function readBase64(text) {
  if (typeof text !== 'string') throw new Error('加密记录已损坏');
  let binary;
  try { binary = atob(text); } catch { throw new Error('加密记录已损坏'); }
  if (btoa(binary) !== text) throw new Error('加密记录已损坏');
  return Uint8Array.from(binary, character => character.charCodeAt(0));
}

function cryptoApi() {
  if (!globalThis.isSecureContext && typeof window !== 'undefined') throw new Error('加密存储必须使用可信 HTTPS 或本机安全来源');
  if (!globalThis.crypto?.subtle) throw new Error('当前环境没有可用的 WebCrypto');
  return globalThis.crypto;
}

async function makeKey(password, salt) {
  const c = cryptoApi();
  if (typeof password !== 'string' || password.length < 12) throw new Error('存储口令至少需要 12 个字符');
  const material = await c.subtle.importKey('raw', enc.encode(password), 'PBKDF2', false, ['deriveKey']);
  return c.subtle.deriveKey({ name: 'PBKDF2', salt, iterations: ITERATIONS, hash: 'SHA-256' }, material,
    { name: 'AES-GCM', length: 256 }, false, ['encrypt', 'decrypt']);
}

function additionalData(envelope) {
  return enc.encode(envelope.format === VAULT_FORMAT
    ? JSON.stringify([VAULT_FORMAT, envelope.epoch, envelope.generation])
    : `${LEGACY_FORMAT}:local-vault`);
}

async function seal(value, password, version) {
  const serialized = JSON.stringify(value);
  if (serialized === undefined) throw new Error('没有可加密的记录');
  const c = cryptoApi();
  const salt = c.getRandomValues(new Uint8Array(16));
  const iv = c.getRandomValues(new Uint8Array(12));
  const envelope = {
    format: version ? VAULT_FORMAT : LEGACY_FORMAT,
    kdf: KDF,
    iterations: ITERATIONS,
    cipher: CIPHER,
    ...version,
    salt: bytesToB64(salt),
    iv: bytesToB64(iv),
  };
  const key = await makeKey(password, salt);
  const ciphertext = await c.subtle.encrypt({ name: 'AES-GCM', iv, additionalData: additionalData(envelope) },
    key, enc.encode(serialized));
  return { ...envelope, ciphertext: bytesToB64(new Uint8Array(ciphertext)) };
}

function inspectEnvelope(input, format) {
  if (!input || typeof input !== 'object' || Array.isArray(input)) throw new Error('加密记录格式无效');
  const fields = ['format', 'kdf', 'iterations', 'cipher', 'salt', 'iv', 'ciphertext'];
  if (format === VAULT_FORMAT) fields.splice(4, 0, 'epoch', 'generation');
  if (Object.keys(input).length !== fields.length || fields.some(field => !Object.hasOwn(input, field))) {
    throw new Error('未知或不兼容的加密记录版本');
  }
  const envelope = Object.fromEntries(fields.map(field => [field, input[field]]));
  if (envelope.format !== format || envelope.kdf !== KDF || envelope.iterations !== ITERATIONS || envelope.cipher !== CIPHER) {
    throw new Error('未知或不兼容的加密记录版本');
  }
  if (format === VAULT_FORMAT && (!isVersionId(envelope.epoch) || !isVersionId(envelope.generation))) {
    throw new Error('备份缺少有效的授权版本');
  }
  const salt = readBase64(envelope.salt);
  const iv = readBase64(envelope.iv);
  const ciphertext = readBase64(envelope.ciphertext);
  if (salt.length !== 16 || iv.length !== 12 || ciphertext.length < 17) throw new Error('加密记录已损坏');
  return { envelope, salt, iv, ciphertext };
}

async function unseal({ envelope, salt, iv, ciphertext }, password) {
  const key = await makeKey(password, salt);
  try {
    const plain = await cryptoApi().subtle.decrypt({ name: 'AES-GCM', iv, additionalData: additionalData(envelope) }, key, ciphertext);
    return JSON.parse(dec.decode(plain));
  } catch { throw new Error('口令错误或密文被修改，拒绝读取'); }
}

// Standalone prototype envelopes stay readable through this primitive. The vault never imports them.
export function encryptRecord(value, password) { return seal(value, password); }
export async function decryptRecord(blob, password) { return unseal(inspectEnvelope(blob, LEGACY_FORMAT), password); }

function openDb(create) {
  return new Promise((resolve, reject) => {
    if (!globalThis.indexedDB) { reject(new Error('当前浏览器不支持本地记录')); return; }
    const request = globalThis.indexedDB.open(DB, 1);
    let missing = false;
    request.onupgradeneeded = () => {
      if (create) {
        request.result.createObjectStore('records');
      } else {
        missing = true;
        request.transaction.abort();
      }
    };
    request.onerror = () => {
      if (missing) resolve(undefined);
      else reject(new Error('无法打开本地记录，可能被系统清理'));
    };
    request.onsuccess = () => {
      const db = request.result;
      db.onversionchange = () => db.close();
      resolve(db);
    };
  });
}

async function transact(mode, action, { create = false } = {}) {
  const db = await openDb(create);
  if (!db) {
    if (mode === 'readonly') return undefined;
    throw new Error('本地记录或授权已改变，请重新读取后再操作');
  }
  try {
    return await new Promise((resolve, reject) => {
      const tx = db.transaction('records', mode, { durability: 'strict' });
      let result;
      let failure;
      const complete = value => { result = value; };
      const abort = error => {
        failure = error;
        tx.abort();
      };
      tx.oncomplete = () => resolve(result);
      tx.onabort = () => reject(failure ?? new Error('存储事务失败，可能是配额已满或存储已清理'));
      try { action(tx.objectStore('records'), complete, abort); } catch (error) { abort(error); }
    });
  } finally { db.close(); }
}

function withRequest(request, action, abort) {
  request.onsuccess = () => {
    try { action(request.result); } catch (error) { abort(error); }
  };
}

async function readVault() {
  return await transact('readonly', (store, complete, abort) => {
    const authorization = store.get(LEDGER);
    const ciphertext = store.get(SLOT);
    withRequest(ciphertext, record => complete({ record, authorization: authorization.result }), abort);
  }) ?? {};
}

function isVersionId(value) {
  return typeof value === 'string' && UUID.test(value);
}

function readAuthorization(authorization) {
  if (authorization === undefined) return undefined;
  if (authorization?.status === 'revoked' && isVersionId(authorization.epoch)) return authorization;
  if (authorization?.status === 'active' && isVersionId(authorization.epoch) && isVersionId(authorization.generation) &&
      typeof authorization.digest === 'string' && /^[A-Za-z0-9+/]{43}=$/.test(authorization.digest)) return authorization;
  throw new Error('本地授权记录损坏，请先删除并撤回授权');
}

function assertUnchanged(expected, current) {
  if (expected?.status !== current?.status || expected?.epoch !== current?.epoch ||
      expected?.generation !== current?.generation || expected?.digest !== current?.digest) {
    throw new Error('本地记录或授权已改变，请重新读取后再操作');
  }
}

async function verifyUnchanged(expected) {
  const authorization = await transact('readonly', (store, complete, abort) => {
    withRequest(store.get(LEDGER), complete, abort);
  });
  assertUnchanged(expected, readAuthorization(authorization));
}

function commitRecord(expected, envelope, replacement) {
  // Encryption and authentication run before opening this transaction. The comparison
  // and both writes run in one readwrite transaction across all tabs of this origin.
  return transact('readwrite', (store, complete, abort) => {
    withRequest(store.get(LEDGER), current => {
      assertUnchanged(expected, readAuthorization(current));
      store.put(envelope, SLOT);
      if (replacement) store.put(replacement, LEDGER);
    }, abort);
  }, { create: expected === undefined && replacement !== undefined });
}

async function fingerprint(envelope) {
  const bytes = await cryptoApi().subtle.digest('SHA-256', enc.encode(JSON.stringify(envelope)));
  return bytesToB64(new Uint8Array(bytes));
}

async function matchesAuthorization(envelope, authorization) {
  return authorization?.status === 'active' && envelope.epoch === authorization.epoch &&
    envelope.generation === authorization.generation && await fingerprint(envelope) === authorization.digest;
}

async function inspectAuthorizedRecord(record, authorization) {
  if (authorization?.status !== 'active' || record === undefined) return undefined;
  let inspected;
  try { inspected = inspectEnvelope(record, VAULT_FORMAT); } catch { return undefined; }
  if (await matchesAuthorization(inspected.envelope, authorization)) return inspected;
  return undefined;
}

function requireRecord(inspected) {
  if (!inspected) throw new Error('没有可读取的已授权记录');
  return inspected;
}

export async function localRecordStatus() {
  const state = await readVault();
  const authorization = readAuthorization(state.authorization);
  if (authorization?.status !== 'active') return 'missing';
  const inspected = await inspectAuthorizedRecord(state.record, authorization);
  return inspected ? 'available' : 'recoverable';
}

export async function saveAuthorizedRecord(value, password, authorized, { expectedGeneration } = {}) {
  if (authorized !== true) throw new Error('需要明确授权后才能持久化');
  const state = await readVault();
  const authorization = readAuthorization(state.authorization);
  const active = authorization?.status === 'active';
  if (expectedGeneration !== undefined && expectedGeneration !== (active ? authorization.generation : null)) {
    throw new Error('本地记录或授权已改变，请重新读取后再操作');
  }
  if (active) {
    const inspected = requireRecord(await inspectAuthorizedRecord(state.record, authorization));
    await unseal(inspected, password);
  }
  const c = cryptoApi();
  const version = { epoch: active ? authorization.epoch : c.randomUUID(), generation: c.randomUUID() };
  const envelope = await seal(value, password, version);
  const replacement = { status: 'active', ...version, digest: await fingerprint(envelope) };
  await commitRecord(authorization, envelope, replacement);
}

export async function loadAuthorizedRecordWithVersion(password) {
  const state = await readVault();
  const authorization = readAuthorization(state.authorization);
  const inspected = requireRecord(await inspectAuthorizedRecord(state.record, authorization));
  const value = await unseal(inspected, password);
  await verifyUnchanged(authorization);
  return { value, generation: authorization.generation };
}

export async function loadAuthorizedRecord(password) {
  const { value } = await loadAuthorizedRecordWithVersion(password);
  return value;
}

export async function exportEncryptedBlob() {
  const state = await readVault();
  const authorization = readAuthorization(state.authorization);
  const { envelope } = requireRecord(await inspectAuthorizedRecord(state.record, authorization));
  await verifyUnchanged(authorization);
  return JSON.stringify(envelope, null, 2);
}

export async function restoreEncryptedBlob(serialized, password, confirmed) {
  if (confirmed !== true) throw new Error('需要明确确认后才能恢复备份');
  let blob;
  try { blob = typeof serialized === 'string' ? JSON.parse(serialized) : serialized; }
  catch { throw new Error('备份不是有效的 JSON 文件'); }
  const inspected = inspectEnvelope(blob, VAULT_FORMAT);
  const { authorization: storedAuthorization } = await readVault();
  const authorization = readAuthorization(storedAuthorization);
  if (!await matchesAuthorization(inspected.envelope, authorization)) {
    throw new Error('备份与当前本地授权不匹配，无法恢复');
  }
  await unseal(inspected, password);
  await commitRecord(authorization, inspected.envelope);
}

export async function removeLocalRecord() {
  const revoked = { status: 'revoked', epoch: cryptoApi().randomUUID() };
  await transact('readwrite', store => {
    store.put(revoked, LEDGER);
    store.delete(SLOT);
  }, { create: true });
}
