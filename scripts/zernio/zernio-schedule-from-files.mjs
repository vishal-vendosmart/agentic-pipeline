import { linkedInAccountId, twitterPersonalAccountId, twitterWeFabAccountId } from './zernio-config.mjs';
import { zernioPost } from './zernio-api.mjs';
import fs from 'fs';
import path from 'path';

/**
 * Strip markdown syntax for platforms that don't render it (LinkedIn, X).
 * Preserves paragraph breaks and plain text readability.
 */
function stripMarkdown(text) {
  return text
    // Remove bold/italic markdown: **text** or *text* or __text__
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/\*([^*]+)\*/g, '$1')
    .replace(/__([^_]+)__/g, '$1')
    // Remove inline code: `text`
    .replace(/`([^`]+)`/g, '$1')
    // Remove headers: ### Text or ## Text
    .replace(/^#{1,6}\s+/gm, '')
    // Remove horizontal rules
    .replace(/^---$/gm, '')
    // Remove link syntax but keep text: [text](url) → text
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    // Remove image syntax: ![alt](url)
    .replace(/!\[([^\]]*)\]\([^)]+\)/g, '')
    // Clean up multiple blank lines
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

// Read all topic files from content/topics/
const topicsDir = 'content/topics';
const files = fs.readdirSync(topicsDir).sort();

// Group by topic number
const topics = {};
for (const file of files) {
  const match = file.match(/topic(\d+)-(\w+)-(\w+)\.md/);
  if (!match) continue;
  
  const [, num, platform, date] = match;
  if (!topics[num]) topics[num] = { num, date, files: {} };
  topics[num].files[platform] = file;
}

const topicList = Object.values(topics).sort((a, b) => parseInt(a.num) - parseInt(b.num));

console.log(`Found ${topicList.length} topics\n`);

function getScheduledTime(dateStr, platform) {
  const monthMap = { 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12' };
  const month = monthMap[dateStr.slice(0, 3)] || '06';
  const day = dateStr.slice(3).padStart(2, '0');
  
  const hourMap = {
    'linkedin': '02:30',      // 8AM IST = 2:30 UTC
    'xpersonal': '00:30',     // 6AM IST = 12:30 AM UTC  
    'xwefab': '13:30'         // 7PM IST = 1:30 PM UTC
  };
  const time = hourMap[platform] || '02:30';
  
  return `2026-${month}-${day}T${time}:00.000Z`;
}

async function createPost(name, text, platforms, accountId, scheduledAt) {
  const body = {
    content: text,
    platforms: platforms.map(p => ({
      platform: p,
      accountId: accountId
    })),
    scheduledFor: scheduledAt
  };

  const response = await zernioPost('posts', body);

  if (!response.ok) {
    const error = await response.text();
    console.error(`❌ ${name}:`, error.substring(0, 100));
    return false;
  }

  console.log(`✅ ${name}`);
  return true;
}

async function main() {
  console.log(`Scheduling ${topicList.length} topics × 3 platforms = ${topicList.length * 3} posts...\n`);
  
  let success = 0;
  let failed = 0;
  let skipped = 0;
  
  for (const topic of topicList) {
    const dateStr = topic.date;
    
    // Skip past dates
    const postDate = new Date(getScheduledTime(dateStr, 'linkedin'));
    const now = new Date();
    
    if (postDate < now) {
      console.log(`⏭️  Skipping past date: ${dateStr}`);
      skipped += 3;
      continue;
    }
    
    console.log(`\n📅 Topic ${topic.num} (${dateStr})`);
    
    // LinkedIn - strip markdown for clean rendering
    if (topic.files.linkedin) {
      const rawText = fs.readFileSync(path.join(topicsDir, topic.files.linkedin), 'utf8');
      const text = stripMarkdown(rawText);
      const result = await createPost(
        `  LinkedIn ${dateStr}`,
        text,
        ['linkedin'],
        linkedInAccountId,
        getScheduledTime(dateStr, 'linkedin')
      );
      result ? success++ : failed++;
    }
    
    // X Personal - strip markdown
    if (topic.files.xpersonal) {
      const rawText = fs.readFileSync(path.join(topicsDir, topic.files.xpersonal), 'utf8');
      const text = stripMarkdown(rawText);
      const result = await createPost(
        `  X Personal ${dateStr}`,
        text,
        ['twitter'],
        twitterPersonalAccountId,
        getScheduledTime(dateStr, 'xpersonal')
      );
      result ? success++ : failed++;
    }
    
    // X WeFab - strip markdown
    if (topic.files.xwefab) {
      const rawText = fs.readFileSync(path.join(topicsDir, topic.files.xwefab), 'utf8');
      const text = stripMarkdown(rawText);
      const result = await createPost(
        `  X WeFab ${dateStr}`,
        text,
        ['twitter'],
        twitterWeFabAccountId,
        getScheduledTime(dateStr, 'xwefab')
      );
      result ? success++ : failed++;
    }
    
    await new Promise(r => setTimeout(r, 300));
  }
  
  console.log(`\n--- Summary ---`);
  console.log(`✅ Scheduled: ${success}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`⏭️  Skipped (past): ${skipped}`);
}

main().catch(console.error);
