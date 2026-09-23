import { zernioDelete, listAllPosts } from './zernio-api.mjs';

// Clean slate - delete ALL posts first, then schedule properly

async function deletePost(postId) {
  const response = await zernioDelete(`posts/${postId}`);
  return response.ok;
}

async function cleanAll() {
  console.log("Fetching all posts...");
  const posts = await listAllPosts();
  console.log(`Found ${posts.length} posts to delete`);

  let deleted = 0;
  for (const post of posts) {
    const ok = await deletePost(post._id);
    if (ok) deleted++;
    process.stdout.write(`\rDeleted ${deleted}/${posts.length}`);
  }
  console.log(`\n✅ Cleaned ${deleted} posts`);
}

cleanAll().catch(console.error);
