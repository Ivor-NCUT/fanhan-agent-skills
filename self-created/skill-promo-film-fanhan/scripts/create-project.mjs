#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { cpSync, existsSync, mkdirSync, readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { dirname, extname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const args = process.argv.slice(2);
const value = (flag) => {
  const index = args.indexOf(flag);
  return index >= 0 ? args[index + 1] : undefined;
};
const fail = (message) => {
  console.error(message);
  process.exit(1);
};

const skillInput = value('--skill');
const musicInput = value('--music');
const scriptInput = value('--script');
const outputInput = value('--output');
if (!skillInput || !musicInput || !outputInput) {
  fail('Usage: create-project.mjs --skill <SKILL.md|directory> --music <audio> [--script <script.md|txt>] --output <new-directory>');
}

let skillPath = resolve(skillInput);
if (existsSync(skillPath) && statSync(skillPath).isDirectory()) skillPath = join(skillPath, 'SKILL.md');
const musicPath = resolve(musicInput);
const scriptPath = scriptInput ? resolve(scriptInput) : undefined;
const outputPath = resolve(outputInput);
if (!existsSync(skillPath)) fail(`Skill not found: ${skillPath}`);
if (!existsSync(musicPath)) fail(`Music not found: ${musicPath}`);
if (scriptPath && !existsSync(scriptPath)) fail(`Script not found: ${scriptPath}`);
if (existsSync(outputPath) && readdirSync(outputPath).length) fail(`Output directory is not empty: ${outputPath}`);

const allowedAudio = new Set(['.mp3', '.wav', '.m4a', '.aac', '.flac', '.ogg']);
const musicExt = extname(musicPath).toLowerCase();
if (!allowedAudio.has(musicExt)) fail(`Unsupported music type: ${musicExt || '(none)'}`);

const here = dirname(fileURLToPath(import.meta.url));
const template = resolve(here, '../assets/codex-light-template');
mkdirSync(outputPath, { recursive: true });
cpSync(template, outputPath, { recursive: true });
mkdirSync(join(outputPath, 'inputs'), { recursive: true });
mkdirSync(join(outputPath, 'renders'), { recursive: true });
cpSync(skillPath, join(outputPath, 'inputs/source-skill.md'));
if (scriptPath) cpSync(scriptPath, join(outputPath, 'inputs/user-script.md'));

const musicName = `bgm${musicExt}`;
cpSync(musicPath, join(outputPath, 'assets', musicName));
const htmlPath = join(outputPath, 'index.html');
const html = readFileSync(htmlPath, 'utf8').replace('assets/bgm.mp3', `assets/${musicName}`);
writeFileSync(htmlPath, html);

const sha256 = (path) => createHash('sha256').update(readFileSync(path)).digest('hex');
const manifest = {
  schemaVersion: 1,
  inputs: {
    skill: { file: 'inputs/source-skill.md', sha256: sha256(skillPath) },
    music: { file: `assets/${musicName}`, sha256: sha256(musicPath) },
    script: scriptPath
      ? { mode: 'user-provided', file: 'inputs/user-script.md', sha256: sha256(scriptPath) }
      : { mode: 'agent-generated' }
  },
  canvas: { width: 1080, height: 1920, fps: 30 },
  style: 'codex-light-apple-adjacent',
  motionSystem: {
    name: 'motion-web',
    source: 'https://github.com/feitangyuan/motion-web',
    commit: '440316bfbb0f527c8775ff9104189d1b0db99ce9',
    license: 'MIT',
    role: 'physics-choreography-verification'
  },
  scriptMode: scriptPath ? 'user-provided' : 'agent-generated',
  status: 'scaffolded-reference-content-must-be-rewritten'
};
writeFileSync(join(outputPath, 'promo.json'), `${JSON.stringify(manifest, null, 2)}\n`);
console.log(JSON.stringify({ ok: true, output: outputPath, manifest }, null, 2));
