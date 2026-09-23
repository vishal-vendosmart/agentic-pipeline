
import { zernioPatch } from './zernio-api.mjs';

const postId = '6a2453a956503cef7e507f60';

const twitterContent = [
  "I used to send RFQs that were puzzles—8 files, 32 drawings, and zero links. My vendors spent afternoons matching BOM lines to drawing sheets. They weren't quoting; they were doing the clerical work I failed to do.",
  "This invisible work is either absorbed into the price or leads to bids based on guesses. Stop sending puzzles. Start sending packages. Book a discovery call here: cal.proqsmart.com/vishal/discovery-call"
];

const linkedinContent = `I used to send RFQs that were puzzles. 8 files, 32 drawings, and zero links between them. I didn't send a request for quote; I sent a riddle.

Vendors don't bill you for the time they spend organizing your mess. That invisible labor is either absorbed into the price (a 'frustration tax') or it leads to a bid based on a guess.

The goal is simple: the buyer manages, and the vendor executes. Stop sending puzzles. Start sending packages.

Book a discovery call here: cal.proqsmart.com/vishal/discovery-call`;

const payload = {
  platforms: [
    {
      platform: 'twitter',
      accountId: '6a0f049f520992756d92c57a',
      platformSpecificData: {
        threadItems: twitterContent.map(text => ({ content: text, mediaItems: [] }))
      }
    },
    {
      platform: 'linkedin',
      accountId: '6a0ee81e520992756d91d5d6',
      customContent: linkedinContent
    }
  ]
};

async function updatePost() {
  try {
    const response = await zernioPatch(`posts/${postId}`, payload);
    if (!response.ok) {
      const err = await response.text();
      console.error(`Failed to update post ${postId}: ${response.status} ${err}`);
      process.exit(1);
    }
    const data = await response.json();
    console.log('Successfully updated post:');
    console.log(JSON.stringify(data, null, 2));
  } catch (err) {
    console.error(`Exception updating post ${postId}: ${err.message}`);
    process.exit(1);
  }
}

updatePost();
