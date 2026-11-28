import test from 'node:test';
import assert from 'node:assert/strict';
import { encryptRecord, decryptRecord, saveAuthorizedRecord } from '../src/vault.mjs';
test('only ciphertext is contained in export envelope', async()=>{
  const value={question:'私密的离线选择测试',model:{x:8}};
  const blob=await encryptRecord(value,'a long and private passphrase');
  assert.ok(!JSON.stringify(blob).includes(value.question));
  assert.deepEqual(await decryptRecord(blob,'a long and private passphrase'),value);
});
test('wrong password and ciphertext corruption must fail closed',async()=>{
  const blob=await encryptRecord({sensitive:'secret'},'a long and private passphrase');
  await assert.rejects(decryptRecord(blob,'wrong long password'));
  blob.ciphertext=blob.ciphertext.slice(0,-4)+'AAAA';
  await assert.rejects(decryptRecord(blob,'a long and private passphrase'));
});
test('unapproved persistence is always blocked before IndexedDB',async()=>{
  await assert.rejects(saveAuthorizedRecord({question:'test'},'a long and private passphrase',false),/授权/);
});
test('short passphrases are refused',async()=>{
  await assert.rejects(encryptRecord({x:1},'guess'),/12/);
});
