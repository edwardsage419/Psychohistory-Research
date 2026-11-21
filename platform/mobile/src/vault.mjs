/** Encrypted local prototype storage. Full v0.5 revocation / backup parity pending. */
const enc = new TextEncoder(), dec = new TextDecoder();
const AAD = enc.encode('psychohistory-mobile-v0.1-dev:local-vault');
const DB = 'psychohistory-mobile-v01-dev';
const SLOT = 'sealed-session';
const ITERATIONS = 310000;
function bytesToB64(bytes) { return btoa(String.fromCharCode(...bytes)); }
function b64ToBytes(text) { return Uint8Array.from(atob(text), c => c.charCodeAt(0)); }
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
export async function encryptRecord(value, password) {
  const c = cryptoApi(), salt = c.getRandomValues(new Uint8Array(16)), iv = c.getRandomValues(new Uint8Array(12));
  const key = await makeKey(password, salt);
  const ciphertext = await c.subtle.encrypt({ name: 'AES-GCM', iv, additionalData: AAD }, key, enc.encode(JSON.stringify(value)));
  return { format: 'psychohistory-mobile-v01-dev', kdf: 'PBKDF2-SHA256', iterations: ITERATIONS,
    cipher: 'AES-256-GCM', salt: bytesToB64(salt), iv: bytesToB64(iv), ciphertext: bytesToB64(new Uint8Array(ciphertext)) };
}
export async function decryptRecord(blob, password) {
  if (blob?.format !== 'psychohistory-mobile-v01-dev' || blob.kdf !== 'PBKDF2-SHA256' ||
      blob.iterations !== ITERATIONS || blob.cipher !== 'AES-256-GCM') throw new Error('未知或不兼容的加密记录版本');
  const salt = b64ToBytes(blob.salt), iv = b64ToBytes(blob.iv), ciphertext = b64ToBytes(blob.ciphertext);
  if (salt.length !== 16 || iv.length !== 12 || ciphertext.length < 17) throw new Error('加密记录已损坏');
  const key = await makeKey(password, salt);
  try {
    const plain = await cryptoApi().subtle.decrypt({ name: 'AES-GCM', iv, additionalData: AAD }, key, ciphertext);
    return JSON.parse(dec.decode(plain));
  } catch { throw new Error('口令错误或密文被修改，拒绝读取'); }
}
function openDb() {
  return new Promise((resolve, reject) => {
    if (!globalThis.indexedDB) { reject(new Error('当前浏览器不支持本地记录')); return; }
    const request = indexedDB.open(DB, 1);
    request.onupgradeneeded = () => request.result.createObjectStore('records');
    request.onerror = () => reject(new Error('无法打开本地记录，可能被系统清理'));
    request.onsuccess = () => resolve(request.result);
  });
}
async function transact(mode, action) {
  const db = await openDb();
  try {
    return await new Promise((resolve, reject) => {
      const tx = db.transaction('records', mode), req = action(tx.objectStore('records'));
      let result;
      req.onsuccess = () => { result = req.result; };
      req.onerror = () => reject(new Error('加密记录操作失败'));
      tx.oncomplete = () => resolve(result);
      tx.onerror = () => reject(new Error('存储事务失败，可能是配额已满'));
      tx.onabort = () => reject(new Error('存储事务已中断'));
    });
  } finally { db.close(); }
}
export async function saveAuthorizedRecord(value, password, authorized) {
  if (authorized !== true) throw new Error('需要明确授权后才能持久化');
  const encrypted = await encryptRecord(value, password);
  await transact('readwrite', store => store.put(encrypted, SLOT));
}
export async function loadAuthorizedRecord(password) {
  const record = await transact('readonly', store => store.get(SLOT));
  if (!record) throw new Error('没有本地已授权记录');
  return decryptRecord(record, password);
}
export async function exportEncryptedBlob() {
  const record = await transact('readonly', store => store.get(SLOT));
  if (!record) throw new Error('没有可导出的记录');
  return JSON.stringify(record, null, 2);
}
export async function removeLocalRecord() { await transact('readwrite', store => store.delete(SLOT)); }
