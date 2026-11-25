import { once } from 'node:events';
import { readFile } from 'node:fs/promises';
import { createServer as httpServer } from 'node:http';
import { createServer as httpsServer } from 'node:https';
import { isIP } from 'node:net';
import { parseArgs } from 'node:util';
import { build } from './build.mjs';

const { values } = parseArgs({ options: {
  host: { type: 'string', default: '127.0.0.1' }, port: { type: 'string', default: '8766' },
  'base-path': { type: 'string', default: '/' }, cert: { type: 'string' }, key: { type: 'string' },
} });
const { host, port, 'base-path': basePath, cert, key } = values;
if (!/^\d+$/.test(port) || Number(port) > 65535 || !/^(?:\/[a-zA-Z0-9_-]+)*\/$/.test(basePath)
  || Boolean(cert) !== Boolean(key)) {
  throw new Error('Use --port 0–65535, a slash-terminated --base-path and both --cert and --key for HTTPS.');
}

const { files, outputs } = await build();
const types = new Map(files.map(file => [file.path, file.contentType]));
types.set('sw.js', 'text/javascript');
types.set('release-manifest.json', 'application/json');

function serve(request, response) {
  const rawPath = request.url;
  const path = rawPath === basePath ? 'index.html'
    : rawPath.startsWith(basePath) ? rawPath.slice(basePath.length) : '';
  if (!['GET', 'HEAD'].includes(request.method)) {
    response.writeHead(405, { Allow: 'GET, HEAD' }).end();
    return;
  }
  const type = types.get(path);
  if (!type) {
    response.writeHead(404, { 'Cache-Control': 'no-store' }).end();
    return;
  }
  const body = outputs.get(path);
  const contentType = /^(text\/|application\/)/.test(type) ? `${type}; charset=utf-8` : type;
  response.writeHead(200, {
    'Cache-Control': 'no-store', 'Content-Type': contentType,
    'Content-Length': Buffer.byteLength(body), 'X-Content-Type-Options': 'nosniff',
  }).end(request.method === 'HEAD' ? undefined : body);
}

const server = cert ? httpsServer({ cert: await readFile(cert), key: await readFile(key) }, serve) : httpServer(serve);
server.listen(Number(port), host);
await once(server, 'listening');
const urlHost = isIP(host) === 6 ? `[${host}]` : host;
console.log(`Preview ${cert ? 'https' : 'http'}://${urlHost}:${server.address().port}${basePath}`);
