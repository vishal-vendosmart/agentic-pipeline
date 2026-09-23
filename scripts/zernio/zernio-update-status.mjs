import { zernioGet, zernioPatch } from './zernio-api.mjs';

async function updateDraftsToScheduled() {
  const response = await zernioGet('posts?limit=100');

  if (!response.ok) {
    console.error('Failed to fetch posts:', await response.text());
    return;
  }

  const data = await response.json();
  const posts = data.posts || [];

  let updated = 0;
  let skipped = 0;

  for (const post of posts) {
    if (post.status !== 'draft') {
      skipped++;
      continue;
    }

    const patchResponse = await zernioPatch(`posts/${post._id}`, {
      status: 'scheduled',
      publishNow: false
    });

    if (patchResponse.ok) {
      const platform = post.platforms?.[0]?.platform || 'unknown';
      console.log(`✅ ${platform} | ${post.scheduledFor?.slice(0, 10)}`);
      updated++;
    } else {
      console.error(`❌ Failed to update ${post._id}`);
    }
  }

  console.log(`\nUpdated: ${updated} | Skipped: ${skipped}`);
}

updateDraftsToScheduled().catch(console.error);
