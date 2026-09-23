#!/usr/bin/env node
/**
 * Schedule Company Brain Batch 1 posts to Zernio (Vishal personal LinkedIn).
 *
 * Reads content/topics/company-brain-batch-1-linkedin.md, sections "## POST n".
 * Strategic slot: 13:00 UTC = 6:30 PM IST (India evening + US East Coast morning).
 *
 * Usage: node scripts/zernio/schedule-company-brain-b1.mjs 1
 *        (one or more post numbers; defaults to post 1)
 */

import fs from 'fs';
import { zernioPost } from './zernio-api.mjs';

const VISHAL_LI_ACCOUNT_ID = '6a0ee81e520992756d91d5d6';
const SLOT_UTC = '13:00:00.000Z'; // 6:30 PM IST

// post number -> date
const DATE = {
  1: '2026-09-23',
  2: '2026-09-25',
  3: '2026-09-28',
};

function parsePosts(md) {
  const out = {};
  const parts = md.split(/^##\s*POST\s*(\d+)\s*$/im);
  for (let i = 1; i < parts.length; i += 2) {
    const n = parseInt(parts[i], 10);
    out[n] = parts[i + 1].trim();
  }
  return out;
}

function stripMd(t) {
  return t
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/\*([^*]+)\*/g, '$1')
    .replace(/`([^`]+)`/g, '$1')
    .replace(/^#{1,6}\s+/gm, '')
    .replace(/^---$/gm, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

const file = 'content/topics/company-brain-batch-1-linkedin.md';
const posts = parsePosts(fs.readFileSync(file, 'utf8'));
const wanted = process.argv.slice(2).map(Number);
const nums = wanted.length ? wanted : [1];

let ok = 0, fail = 0;
for (const n of nums) {
  if (!posts[n]) { console.error(`Post ${n}: not found in file`); fail++; continue; }
  if (!DATE[n]) { console.error(`Post ${n}: no date mapped`); fail++; continue; }
  const scheduledFor = `${DATE[n]}T${SLOT_UTC}`;
  const res = await zernioPost('posts', {
    content: stripMd(posts[n]),
    platforms: [{ platform: 'linkedin', accountId: VISHAL_LI_ACCOUNT_ID }],
    scheduledFor,
  });
  if (!res.ok) {
    console.error(`Post ${n}: FAILED`, (await res.text()).substring(0, 300));
    fail++;
  } else {
    const data = await res.json();
    console.log(`Post ${n}: scheduled ${scheduledFor} (id: ${data._id || data.id || '?'})`);
    ok++;
  }
  await new Promise(r => setTimeout(r, 600));
}
console.log(`\nScheduled: ${ok}  Failed: ${fail}`);
if (fail) process.exit(1);
