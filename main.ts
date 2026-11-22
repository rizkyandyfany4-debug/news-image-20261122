// Entry point for news-image-20261122.
// Copies the pre-rendered front page (entry.png, built by render.py)
// into the output directory. Never deletes anything.
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = join(here, "entry.png");

if (!existsSync(src)) {
  console.error("entry.png not found next to main.ts");
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));
const bytes = statSync(join(outDir, "entry.png")).size;
console.log(`entry.png written to ${join(outDir, "entry.png")} (${bytes} bytes)`);
