#!/usr/bin/env node
/**
 * Schedule Vishal personal LinkedIn pain-first posts to Zernio.
 *
 * Reads a drafts markdown file with sections like:
 *   ## Post 1
 *   Pillar: A
 *   Date: Mon Jul 20
 *   Workflow: ...
 *   Close Shape: ...
 *   Writer Note: ...
 *
 *   <body text until next ## Post or end of file>
 *
 * Creates one scheduled Zernio post per section, targeting
 * the Vishal personal LinkedIn account (6a0ee81e520992756d91d5d6).
 *
 * Cadence: Mon/Wed/Fri at 8:00 AM IST (02:30 UTC).
 * Usage: node scripts/zernio/schedule-vishal-li-pain.mjs <drafts-file>
 */

import { zernioPost, zernioGet } from './zernio-api.mjs';
import fs from 'fs';

const VISHAL_LI_ACCOUNT_ID = '6a0ee81e520992756d91d5d6';

const DATE_TO_ISO = {
  'Mon Jul 20': '2026-07-20T02:30:00.000Z',
  'Wed Jul 22': '2026-07-22T02:30:00.000Z',
  'Fri Jul 24': '2026-07-24T02:30:00.000Z',
  'Mon Jul 27': '2026-07-27T02:30:00.000Z',
  'Wed Jul 29': '2026-07-29T02:30:00.000Z',
  'Fri Jul 31': '2026-07-31T02:30:00.000Z',
  'Mon Aug 3':  '2026-08-03T02:30:00.000Z',
  'Wed Aug 5':  '2026-08-05T02:30:00.000Z',
  'Fri Aug 7':  '2026-08-07T02:30:00.000Z',
  'Mon Aug 10': '2026-08-10T02:30:00.000Z',
  'Wed Aug 12': '2026-08-12T02:30:00.000Z',
  'Fri Aug 14': '2026-08-14T02:30:00.000Z',
};

function stripMarkdown(text) {
  return text
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/\*([^*]+)\*/g, '$1')
    .replace(/__([^_]+)__/g, '$1')
    .replace(/`([^`]+)`/g, '$1')
    .replace(/^#{1,6}\s+/gm, '')
    .replace(/^---$/gm, '')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/!\[([^\]]*)\]\([^)]+\)/g, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function parseDrafts(content) {
  const posts = [];
  const lines = content.split('\n');
  let current = null;
  let body = [];

  for (const line of lines) {
    const headerMatch = line.match(/^##\s+Post\s+(\d+)/i);
    if (headerMatch) {
      if (current) {
        current.body = body.join('\n').trim();
        posts.push(current);
      }
      current = { num: parseInt(headerMatch[1], 10), meta: {}, body: '' };
      body = [];
      continue;
    }
    if (!current) continue;

    const metaMatch = line.match(/^(Pillar|Date|Workflow|Close Shape|Writer Note):\s*(.+)$/);
    if (metaMatch) {
      const key = metaMatch[1].toLowerCase().replace(/\s+/g, '_');
      current.meta[key] = metaMatch[2].trim();
      continue;
    }

    if (line.trim() === '---') {
      // separator — keep in body? no, skip
      continue;
    }

    body.push(line);
  }

  if (current) {
    current.body = body.join('\n').trim();
    posts.push(current);
  }

  return posts;
}

async function scheduleOne(post) {
  const dateStr = post.meta.date;
  const scheduledFor = DATE_TO_ISO[dateStr];

  if (!scheduledFor) {
    console.error(`❌ Post ${post.num}: unknown date "${dateStr}"`);
    return { ok: false, post: post.num };
  }

  const cleanBody = stripMarkdown(post.body);

  const response = await zernioPost('posts', {
    content: cleanBody,
    platforms: [{ platform: 'linkedin', accountId: VISHAL_LI_ACCOUNT_ID }],
    scheduledFor,
  });

  if (!response.ok) {
    const err = await response.text();
    console.error(`❌ Post ${post.num} (${dateStr}):`, err.substring(0, 200));
    return { ok: false, post: post.num, error: err };
  }

  const data = await response.json();
  console.log(`✅ Post ${post.num} (${dateStr}) → ${scheduledFor} (id: ${data._id || data.id || '?'})`);
  return { ok: true, post: post.num, id: data._id || data.id };
}

async function main() {
  const file = process.argv[2];
  if (!file) {
    console.error('Usage: node schedule-vishal-li-pain.mjs <drafts-file>');
    process.exit(1);
  }

  const content = fs.readFileSync(file, 'utf8');
  const posts = parseDrafts(content);
  console.log(`Parsed ${posts.length} posts from ${file}\n`);

  let success = 0;
  let failed = 0;

  for (const post of posts) {
    const result = await scheduleOne(post);
    if (result.ok) success++;
    else failed++;
    // small delay between API calls
    await new Promise(r => setTimeout(r, 500));
  }

  console.log(`\n--- Summary ---`);
  console.log(`✅ Scheduled: ${success}`);
  console.log(`❌ Failed: ${failed}`);

  if (failed > 0) process.exit(1);
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
