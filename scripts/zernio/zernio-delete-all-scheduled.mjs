import { zernioGet, zernioDelete } from './zernio-api.mjs';

// Delete ALL scheduled posts
async function deleteAllScheduled() {
  const response = await zernioGet('posts?limit=100');

  if (!response.ok) {
    console.error('Failed to fetch posts:', await response.text());
    return;
  }

  const data = await response.json();
  const posts = data.posts || [];

  let deleted = 0;
  let skipped = 0;

  for (const post of posts) {
    const status = post.status;
    const id = post._id;

    if (status === 'published') {
      skipped++;
      continue;
    }

    const delResponse = await zernioDelete(`posts/${id}`);

    if (delResponse.ok) {
      console.log(`✅ Deleted ${id} (${status})`);
      deleted++;
    } else {
      console.error(`❌ Failed to delete ${id}`);
    }
  }

  console.log(`\nDeleted: ${deleted} | Skipped (published): ${skipped}`);
}

deleteAllScheduled().catch(console.error);
