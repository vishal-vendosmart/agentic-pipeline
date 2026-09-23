#!/usr/bin/env node
/**
 * Company Brain Batch 1 - distribution step 2.
 *  1. PATCH Post 2 on Zernio (personal LinkedIn) with the revised copy
 *     that names proposal engineering as the proof coworker.
 *  2. Create 6 X posts: personal + WEFAB brand, for each of the 3 posts.
 *
 * Reads: content/company-brain-batch-1-post2-revised.md
 *        content/company-brain-batch-1-x-cuts.md
 * Usage: node scripts/zernio/distribute-company-brain-b1.mjs [--dry]
 */

import fs from 'fs';
import { zernioPost, zernioPatch, zernioGet } from './zernio-api.mjs';

const VISHAL_LI_ACCOUNT_ID = '6a0ee81e520992756d91d5d6';
const X_PERSONAL_ACCOUNT_ID = process.env.ZERNIO_TWITTER_PERSONAL_ACCOUNT_ID || '6a0ee834520992756d91d691';
const X_WEFAB_ACCOUNT_ID = process.env.ZERNIO_TWITTER_WEFAB_ACCOUNT_ID || '6a0f049f520992756d92c57a';

// Zernio id of the already-scheduled Post 2 (personal LinkedIn)
const POST2_ID = '6ab3325f02cc3839b1af7475';

// post number -> date. X personal 13:00 UTC, WEFAB 13:30 UTC (same day as LinkedIn)
const DATE = {
  1: '2026-09-23',
  2: '2026-09-25',
  3: '2026-09-28',
};

const DRY = process.argv.includes('--dry');

function parseBlocks(md) {
  const out = {};
  const parts = md.split(/^##\s*(.+?)\s*$/m);
  for (let i = 1; i < parts.length; i += 2) {
    out[parts[i].trim()] = parts[i + 1].trim();
  }
  return out;
}

const revised = fs.readFileSync('content/company-brain-batch-1-post2-revised.md', 'utf8').trim();
const cuts = parseBlocks(fs.readFileSync('content/company-brain-batch-1-x-cuts.md', 'utf8'));

let ok = 0, fail = 0;

// ---- Step 1: PATCH Post 2 ----
console.log('--- Step 1: PATCH Post 2 (personal LinkedIn) ---');
if (DRY) {
  console.log('[dry] would patch', POST2_ID, '->', revised.length, 'chars');
} else {
  const r = await zernioPatch(`posts/${POST2_ID}`, { content: revised });
  if (!r.ok) {
    console.error('Patch FAILED', r.status, (await r.text()).substring(0, 300));
    fail++;
  } else {
    console.log('Patch OK');
    ok++;
  }
}

// ---- Step 2: create X posts ----
console.log('\n--- Step 2: X posts ---');
const jobs = [];
for (const n of [1, 2, 3]) {
  const d = DATE[n];
  jobs.push({
    name: `Post ${n} X personal`,
    text: cuts[`POST ${n} - X PERSONAL`],
    platform: 'twitter',
    accountId: X_PERSONAL_ACCOUNT_ID,
    scheduledFor: `${d}T13:00:00.000Z`,
  });
  jobs.push({
    name: `Post ${n} WEFAB X`,
    text: cuts[`POST ${n} - WEFAB X`],
    platform: 'twitter',
    accountId: X_WEFAB_ACCOUNT_ID,
    scheduledFor: `${d}T13:30:00.000Z`,
  });
}

for (const j of jobs) {
  if (!j.text) { console.error(`${j.name}: MISSING TEXT`); fail++; continue; }
  if (j.text.length > 280) {
    console.error(`${j.name}: TOO LONG (${j.text.length} chars)`); fail++; continue;
  }
  if (DRY) { console.log(`[dry] ${j.name} | ${j.scheduledFor} | ${j.text.length} chars`); continue; }

  const res = await zernioPost('posts', {
    content: j.text,
    platforms: [{ platform: j.platform, accountId: j.accountId }],
    scheduledFor: j.scheduledFor,
  });
  if (!res.ok) {
    console.error(`${j.name}: FAILED`, (await res.text()).substring(0, 200));
    fail++;
  } else {
    const data = await res.json();
    console.log(`${j.name}: scheduled ${j.scheduledFor} (id: ${data._id || data.id || '?'})`);
    ok++;
  }
  await new Promise(r => setTimeout(r, 700));
}

console.log(`\nOK: ${ok}  FAIL: ${fail}`);
if (fail) process.exit(1);
