
import { zernioGet } from './zernio-api.mjs';

async function getPost(postId) {
  try {
    const response = await zernioGet(`posts/${postId}`);
    if (!response.ok) {
      console.error(`Error fetching post ${postId}: ${response.status} ${await response.text()}`);
      return null;
    }
    const data = await response.json();
    return data;
  } catch (err) {
    console.error(`Exception fetching post ${postId}: ${err.message}`);
    return null;
  }
}

const postId = '6a2453a956503cef7e507f60';
const post = await getPost(postId);
console.log(JSON.stringify(post, null, 2));
