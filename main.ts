// Entry point for the news-image-20261124 submission (Node 22, stdlib only).
//
// draw.py has already rendered the front page into entry.png next to this
// file. All this program does is hand that exact file to the grader as
// /output/entry.png, after checking it really is a complete PNG.
//
// Try it outside the grading container with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_HEAD = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
const PNG_TAIL = [0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82];
// The competition gate: at most 1 MiB and 1024 by 1024 pixels.
const MAX_BYTES = 1048576;

function looksLikePng(bytes: Buffer): string | null {
  if (bytes.length < 20) return "file too short to be a PNG";
  if (bytes.length > MAX_BYTES) return "file is over the 1 MiB limit";
  for (let i = 0; i < PNG_HEAD.length; i++) {
    if (bytes[i] !== PNG_HEAD[i]) return "first bytes are not the PNG signature";
  }
  for (let i = 0; i < PNG_TAIL.length; i++) {
    if (bytes[bytes.length - PNG_TAIL.length + i] !== PNG_TAIL[i]) {
      return "missing the IEND trailer: file looks truncated";
    }
  }
  return null;
}

const root = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(root, "entry.png");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const outputPath = join(outputDir, "entry.png");

const bytes = await readFile(sourcePath);
const problem = looksLikePng(bytes);
if (problem) {
  throw new Error(`entry.png failed its sanity check: ${problem}`);
}

await mkdir(outputDir, { recursive: true });
await writeFile(outputPath, bytes);

const written = await readFile(outputPath);
if (written.length !== bytes.length || !written.equals(bytes)) {
  throw new Error("the copy in /output does not match entry.png byte for byte");
}
// Deterministic by construction: the same entry.png bytes go out on
// every run, so the grader's two runs produce identical output.
console.log(`wrote ${outputPath} (${written.length} bytes)`);
