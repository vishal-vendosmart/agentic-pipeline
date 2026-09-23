import { zernioApiKey, zernioBaseUrl } from './zernio-config.mjs';

const DEFAULT_TIMEOUT = 15000; // 15 seconds
const MAX_RETRIES = 2;
const RETRY_DELAY = 1000;

/**
 * Fetch with timeout, retries, and auth headers for Zernio API.
 * Prevents hangs when Zernio is slow or unresponsive.
 */
export async function zernioFetch(endpoint, options = {}) {
  const url = `${zernioBaseUrl}${endpoint}`;
  const timeout = options.timeout || DEFAULT_TIMEOUT;
  const retries = options.retries ?? MAX_RETRIES;

  const fetchOptions = {
    ...options,
    headers: {
      'Authorization': `Bearer ${zernioApiKey}`,
      ...(options.headers || {})
    }
  };
  delete fetchOptions.timeout;
  delete fetchOptions.retries;

  let lastError;
  for (let attempt = 0; attempt <= retries; attempt++) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(url, {
        ...fetchOptions,
        signal: controller.signal
      });
      clearTimeout(timer);
      return response;
    } catch (err) {
      clearTimeout(timer);
      lastError = err;

      if (err.name === 'AbortError') {
        const msg = `Zernio API timeout (${timeout}ms) on attempt ${attempt + 1}: ${endpoint}`;
        console.error(msg);
        if (attempt < retries) {
          console.log(`  Retrying in ${RETRY_DELAY}ms...`);
          await new Promise(r => setTimeout(r, RETRY_DELAY));
          continue;
        }
        throw new Error(msg);
      }

      // Non-timeout error — retry once
      if (attempt < retries) {
        console.error(`  Zernio API error (attempt ${attempt + 1}): ${err.message}. Retrying...`);
        await new Promise(r => setTimeout(r, RETRY_DELAY));
        continue;
      }
      throw err;
    }
  }
  throw lastError;
}

/**
 * GET with timeout
 */
export async function zernioGet(endpoint, options = {}) {
  return zernioFetch(endpoint, { method: 'GET', ...options });
}

/**
 * POST with timeout
 */
export async function zernioPost(endpoint, body, options = {}) {
  return zernioFetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
    ...options
  });
}

/**
 * PATCH with timeout
 */
export async function zernioPatch(endpoint, body, options = {}) {
  return zernioFetch(endpoint, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
    ...options
  });
}

/**
 * DELETE with timeout
 */
export async function zernioDelete(endpoint, options = {}) {
  return zernioFetch(endpoint, { method: 'DELETE', ...options });
}

/**
 * List all posts with automatic pagination.
 * Safe from hangs because each page fetch has a timeout.
 */
export async function listAllPosts(limit = 100) {
  const allPosts = [];
  let skip = 0;
  while (true) {
    const response = await zernioGet(`posts?limit=${limit}&skip=${skip}`);
    if (!response.ok) {
      const err = await response.text();
      throw new Error(`Failed to list posts: ${err.substring(0, 200)}`);
    }
    const data = await response.json();
    const posts = data.posts || [];
    if (posts.length === 0) break;
    allPosts.push(...posts);
    skip += limit;
    if (posts.length < limit) break;
  }
  return allPosts;
}
