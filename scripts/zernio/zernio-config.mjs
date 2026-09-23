import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: join(__dirname, '.env') });

const zernioApiKey = process.env.ZERNIO_API_KEY || '';
const zernioBaseUrl = process.env.ZERNIO_BASE_URL || 'https://zernio.com/api/v1/';
const linkedInAccountId = process.env.ZERNIO_LINKEDIN_ACCOUNT_ID || '';
const twitterPersonalAccountId = process.env.ZERNIO_TWITTER_PERSONAL_ACCOUNT_ID || '';
const twitterWeFabAccountId = process.env.ZERNIO_TWITTER_WEFAB_ACCOUNT_ID || '';

if (!zernioApiKey || !linkedInAccountId) {
  console.error('[zernio-config.mjs] WARNING: Missing Zernio secrets in ~/.openclaw/workspace/.env');
  console.error('[zernio-config.mjs] Required: ZERNIO_API_KEY, ZERNIO_LINKEDIN_ACCOUNT_ID');
}

export { zernioApiKey, zernioBaseUrl, linkedInAccountId, twitterPersonalAccountId, twitterWeFabAccountId };

// Backward compat for old scripts that do: import Config from './zernio-config.mjs'
export default {
  zernioApiKey,
  zernioBaseUrl,
  linkedInAccountId,
  twitterPersonalAccountId,
  twitterWeFabAccountId,
};
