import { createHash } from 'node:crypto';
import { lstat, mkdir, mkdtemp, readFile, realpath, rename, rm, writeFile } from 'node:fs/promises';
import { dirname, join, posix } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
export const PUBLIC_MODULES = [
  'app', 'core', 'decision', 'decision-contract', 'decision-intake', 'decision-plan', 'platform-contract.generated',
  'information', 'timing', 'timing-investigation',
  'scoring', 'scoring-objectives', 'scoring-regret', 'scoring-shared', 'scoring-weights',
  'ui-input', 'ui-output', 'vault',
];
const publicFiles = [
  'index.html', 'styles.css', 'manifest.webmanifest',
  'assets/icon.svg', 'assets/apple-touch-icon.png', 'assets/icon-192.png', 'assets/icon-512.png',
  ...PUBLIC_MODULES.map(name => `src/${name}.mjs`),
];
const mediaTypes = {
  html: 'text/html', css: 'text/css', webmanifest: 'application/manifest+json',
  png: 'image/png', svg: 'image/svg+xml', mjs: 'text/javascript',
};

async function publicInput(path) {
  const absolute = join(root, path);
  if (!(await lstat(absolute)).isFile() || !(await lstat(dirname(absolute))).isDirectory()) {
    throw new Error(`Public release input must be a regular file: ${path}`);
  }
  return readFile(absolute);
}

export async function build() {
  const sources = new Map();
  for (const path of publicFiles) sources.set(path, await publicInput(path));

  // The app uses literal native-module imports, including multi-line named imports.
  const imports = /(?:^\s*(?:import|export)(?:[ \t]+[^;'"`]+?\s+from)?[ \t]+|\bimport\(\s*)['"]([^'"]+)['"]/gm;
  for (const [path, bytes] of sources) {
    if (!path.endsWith('.mjs')) continue;
    for (const [, specifier] of bytes.toString().matchAll(imports)) {
      if (!/^\.\.?\//.test(specifier) || !sources.has(posix.join(posix.dirname(path), specifier))) {
        throw new Error(`Module ${path} refers to a file absent from the public release: ${specifier}`);
      }
    }
  }

  const worker = await publicInput('sw.js');
  const builder = await readFile(new URL(import.meta.url));
  const revision = sha256(JSON.stringify([
    ...Array.from(sources, ([path, bytes]) => [path, sha256(bytes)]),
    ['sw.js', sha256(worker)], ['scripts/build.mjs', sha256(builder)],
  ]));
  const releasePath = `releases/${revision}/`;
  const manifest = JSON.parse(sources.get('manifest.webmanifest'));
  for (const key of ['scope', 'start_url']) manifest[key] = '../../';
  for (const { src } of manifest.icons) {
    if (!src.startsWith('./') || !sources.has(src.slice(2))) {
      throw new Error(`Install icon is missing from the public release: ${src}`);
    }
  }
  sources.set('manifest.webmanifest', Buffer.from(`${JSON.stringify(manifest, null, 2)}\n`));

  const shell = sources.get('index.html').toString().replace(/\b(href|src)=(['"])\.\/([a-zA-Z0-9_./-]+)\2/gi,
    (_match, attribute, quote, path) => {
      if (!sources.has(path) || path === 'index.html') {
        throw new Error(`HTML refers to a file absent from the public release: ${path}`);
      }
      return `${attribute}=${quote}./${releasePath}${path}${quote}`;
    });
  const outputs = new Map([['index.html', Buffer.from(shell)]]);
  for (const [path, bytes] of sources) {
    if (path !== 'index.html') outputs.set(`${releasePath}${path}`, bytes);
  }
  const files = Array.from(outputs, ([path, bytes]) => ({
    path, contentType: mediaTypes[path.split('.').at(-1)], bytes: bytes.length, sha256: sha256(bytes),
  }));
  const releaseManifest = `${JSON.stringify({ schema: 1, revision, files }, null, 2)}\n`;
  const release = sha256(releaseManifest);
  outputs.set('release-manifest.json', releaseManifest);
  const publicPaths = publicFiles.filter(path => path !== 'index.html');
  outputs.set('sw.js', worker.toString().replace('__MOBILE_RELEASE_SHA256__', release)
    .replace('__MOBILE_PUBLIC_PATHS__', JSON.stringify(publicPaths)));

  const destination = join(root, 'dist');
  const staging = await mkdtemp(join(root, '.dist-'));
  try {
    for (const [path, bytes] of outputs) {
      const target = join(staging, path);
      await mkdir(dirname(target), { recursive: true });
      await writeFile(target, bytes);
    }
    await rm(destination, { recursive: true, force: true });
    await rename(staging, destination);
  } finally {
    await rm(staging, { recursive: true, force: true });
  }
  return { destination, files, outputs, release };
}

const entry = process.argv[1] && await realpath(process.argv[1]).catch(() => undefined);
if (fileURLToPath(import.meta.url) === entry) {
  const { destination, release } = await build();
  console.log(`Built public release ${release} in ${destination}`);
}
