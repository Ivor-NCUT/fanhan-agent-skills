#!/usr/bin/env node
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { existsSync, mkdtempSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const root = mkdtempSync(join(tmpdir(), 'skill-promo-film-'));
const skill = join(root, 'SKILL.md');
const music = join(root, 'music.wav');
const script = join(root, 'script.md');
writeFileSync(skill, '---\nname: demo\ndescription: demo\n---\n');
writeFileSync(music, 'RIFF');
writeFileSync(script, '# 用户剧本\n');

const run = (name, extra = []) => {
  const output = join(root, name);
  execFileSync(process.execPath, [new URL('./create-project.mjs', import.meta.url).pathname, '--skill', skill, '--music', music, ...extra, '--output', output]);
  return JSON.parse(readFileSync(join(output, 'promo.json'), 'utf8'));
};

assert.equal(run('without-script').scriptMode, 'agent-generated');
const supplied = run('with-script', ['--script', script]);
assert.equal(supplied.scriptMode, 'user-provided');
assert.equal(supplied.inputs.script.file, 'inputs/user-script.md');
assert.equal(supplied.motionSystem.commit, '440316bfbb0f527c8775ff9104189d1b0db99ce9');
assert.ok(existsSync(new URL('../vendor/motion-web/LICENSE', import.meta.url)));

const occupied = join(root, 'occupied');
mkdirSync(occupied);
writeFileSync(join(occupied, 'keep.txt'), 'keep');
assert.throws(() => execFileSync(process.execPath, [new URL('./create-project.mjs', import.meta.url).pathname, '--skill', skill, '--music', music, '--output', occupied], { stdio: 'pipe' }));
console.log('create-project: ok');
