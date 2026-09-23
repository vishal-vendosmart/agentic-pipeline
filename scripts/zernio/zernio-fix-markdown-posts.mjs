import { zernioGet, zernioDelete, zernioPost } from './zernio-api.mjs';
import { linkedInAccountId } from './zernio-config.mjs';
import fs from 'fs';
import path from 'path';

/**
 * Fix already-scheduled LinkedIn posts that have markdown syntax.
 * Deletes old posts and re-schedules with clean text.
 */

const topicsDir = 'content/topics';

// Files that had markdown bold syntax (already fixed on disk)
const fixedFiles = [
  'topic02-linkedin-may24.md',
  'topic05-linkedin-may30.md',
  'topic07-linkedin-jun3.md',
  'topic08-linkedin-jun5.md',
  'topic09-linkedin-jun7.md',
  'topic10-linkedin-jun9.md',
  'topic15-linkedin-jun19.md',
  'topic19-linkedin-may29.md',
  'topic21-linkedin-jun2.md'
];

function getScheduledTime(dateStr) {
  const monthMap = { 'may': '05', 'jun': '06' };
  const month = monthMap[dateStr.slice(0, 3)] || '06';
  const day = dateStr.slice(3).padStart(2, '0');
  return `2026-${month}-${day}T02:30:00.000Z`;
}

async function main() {
  console.log('Fetching scheduled posts from Zernio...\n');
  
  // Get all scheduled LinkedIn posts
  const response = await zernioGet('posts?limit=100');
  if (!response.ok) {
    console.error('Failed to fetch posts:', await response.text());
    return;
  }
  
  const data = await response.json();
  const posts = data.posts || [];
  
  const linkedInPosts = posts.filter(p => 
    p.platforms?.some(pl => pl.platform === 'linkedin') &&
    p.status === 'scheduled'
  );
  
  console.log(`Found ${linkedInPosts.length} scheduled LinkedIn posts\n`);
  
  let deleted = 0;
  let recreated = 0;
  let skipped = 0;
  
  for (const post of linkedInPosts) {
    // Check if this post has markdown syntax
    if (!post.content?.includes('**')) {
      skipped++;
      continue;
    }
    
    console.log(`🔧 Fixing post: ${post._id}`);
    console.log(`   Content preview: ${post.content?.substring(0, 80)}...`);
    
    // Extract date from scheduled time
    const scheduledDate = post.scheduledFor?.split('T')[0];
    const month = scheduledDate?.split('-')[1];
    const day = parseInt(scheduledDate?.split('-')[2]);
    
    // Find matching file
    const dateStr = `${month === '05' ? 'may' : 'jun'}${day}`;
    const matchingFile = fixedFiles.find(f => f.includes(dateStr));
    
    if (!matchingFile) {
      console.log(`   ⚠️  No matching file found for ${dateStr}, skipping`);
      skipped++;
      continue;
    }
    
    // Delete old post
    console.log(`   🗑️  Deleting old post...`);
    const delResponse = await zernioDelete(`posts/${post._id}`);
    if (!delResponse.ok) {
      console.error(`   ❌ Failed to delete:`, await delResponse.text());
      continue;
    }
    deleted++;
    
    // Read clean content
    const cleanText = fs.readFileSync(path.join(topicsDir, matchingFile), 'utf8');
    
    // Re-schedule with clean text
    console.log(`   📝 Re-scheduling with clean text...`);
    const newPost = {
      content: cleanText,
      platforms: [{
        platform: 'linkedin',
        accountId: linkedInAccountId
      }],
      scheduledFor: post.scheduledFor
    };
    
    const createResponse = await zernioPost('posts', newPost);
    if (!createResponse.ok) {
      console.error(`   ❌ Failed to recreate:`, await createResponse.text());
      continue;
    }
    recreated++;
    console.log(`   ✅ Fixed!\n`);
    
    // Small delay to avoid rate limiting
    await new Promise(r => setTimeout(r, 500));
  }
  
  console.log(`\n--- Summary ---`);
  console.log(`🗑️  Deleted: ${deleted}`);
  console.log(`📝 Re-created: ${recreated}`);
  console.log(`⏭️  Skipped (no markdown): ${skipped}`);
}

main().catch(console.error);
