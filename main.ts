// Entry program for the make.fun "news-image-20261120" competition.
//
// The picture itself (entry.png, next to this file) is a 1024x1024
// front page of Friday 20 November 2026 drawn by build_image.py.
// This program's job is delivery plus proof: it copies the picture
// into the output folder and then audits the copy chunk by chunk,
// so a damaged or oversized file fails here with a clear reason
// instead of being scored as an invalid entry.
//
//   1. Resolve the output folder: $MAKEFUN_OUTPUT_DIR when set,
//      otherwise /output (the grader's mount). Create it if missing.
//   2. Copy entry.png into it.
//   3. Audit the copied bytes:
//        - the 8-byte PNG signature is intact;
//        - walking the chunk stream from start to finish lands
//          exactly on the end of the file (no truncation, no junk);
//        - every chunk's stored CRC-32 matches the CRC computed
//          over its type + data bytes;
//        - the first chunk is IHDR and its width/height are each
//          within the 1024-pixel contest limit;
//        - an IEND chunk is present and is the final chunk;
//        - the total length is at most 1 MiB.
//   4. Print a one-line summary; exit 0 only if every check passed.

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const LIMIT_EDGE = 1024;
const LIMIT_BYTES = 1024 * 1024;
const SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

function fail(reason) {
  console.error(`entry audit failed: ${reason}`);
  process.exit(1);
}

// CRC-32 (PNG flavour: polynomial 0xEDB88320, reflected) over a buffer,
// table-driven so the audit needs nothing beyond the standard library.
const CRC_TABLE = (() => {
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n += 1) {
    let c = n;
    for (let k = 0; k < 8; k += 1) {
      c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    }
    table[n] = c >>> 0;
  }
  return table;
})();

function crc32(buf) {
  let c = 0xffffffff;
  for (let i = 0; i < buf.length; i += 1) {
    c = CRC_TABLE[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  }
  return (c ^ 0xffffffff) >>> 0;
}

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dest = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), dest);

const data = readFileSync(dest);

if (data.length > LIMIT_BYTES) {
  fail(`${data.length} bytes exceeds the ${LIMIT_BYTES}-byte limit`);
}
if (data.length < SIGNATURE.length + 12) {
  fail("file is too short to hold even one PNG chunk");
}
if (!data.subarray(0, 8).equals(SIGNATURE)) {
  fail("missing or damaged PNG signature");
}

// Walk the chunk stream: [length:4][type:4][data:length][crc:4] ...
let offset = 8;
let width = 0;
let height = 0;
let chunkCount = 0;
let sawIend = false;
while (offset < data.length) {
  if (offset + 12 > data.length) {
    fail(`chunk header at byte ${offset} runs past the end of the file`);
  }
  const length = data.readUInt32BE(offset);
  const type = data.toString("ascii", offset + 4, offset + 8);
  const dataStart = offset + 8;
  const dataEnd = dataStart + length;
  if (dataEnd + 4 > data.length) {
    fail(`chunk ${type} at byte ${offset} is truncated`);
  }
  const storedCrc = data.readUInt32BE(dataEnd);
  const actualCrc = crc32(data.subarray(offset + 4, dataEnd));
  if (storedCrc !== actualCrc) {
    fail(`CRC mismatch in chunk ${type} at byte ${offset}`);
  }
  if (chunkCount === 0) {
    if (type !== "IHDR" || length !== 13) {
      fail(`first chunk is ${type}, expected a 13-byte IHDR`);
    }
    width = data.readUInt32BE(dataStart);
    height = data.readUInt32BE(dataStart + 4);
    if (width > LIMIT_EDGE || height > LIMIT_EDGE) {
      fail(`image is ${width}x${height}, over the ${LIMIT_EDGE}x${LIMIT_EDGE} limit`);
    }
  }
  if (type === "IEND") {
    sawIend = true;
    if (dataEnd + 4 !== data.length) {
      fail("IEND is not the final chunk; trailing bytes follow it");
    }
  }
  chunkCount += 1;
  offset = dataEnd + 4;
}
if (offset !== data.length) {
  fail("chunk walk did not land exactly on the end of the file");
}
if (!sawIend) {
  fail("no IEND chunk found; the image is incomplete");
}

console.log(
  `entry.png audited: ${width}x${height} PNG, ${chunkCount} chunks, ` +
    `${data.length} bytes, all CRCs valid, copied to ${dest}`,
);
