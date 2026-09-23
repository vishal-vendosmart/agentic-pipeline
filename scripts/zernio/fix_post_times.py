import requests
import os
import re

# Config
API_KEY = "sk_7570371f0bcc4041920101b9230a9f3fa4f1cfde3476a8bed71dec971c01 la la" # Wait, the key in my previous exec output was truncated. I should read it properly from the file.
# I'll read it from the file in the script.
EOF_MARKER = "___END_OF_FILE___"

def get_key():
    with open('/opt/marketing-stack/dev/workspace/.env.joint', 'r') as f:
        for line in f:
            if line.startswith('ZERNIO_API_KEY='):
                return line.strip().split('=')[1]
    return None

API_KEY = get_key()
BASE_URL = "https://zernio.com/api/v1"
ACCOUNT_ID = "6a0ee81e520992756d91d5d6"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def update_posts():
    # 1. Fetch ALL scheduled posts for this account (handle pagination)
    all_posts = []
    page = 1
    while True:
        url = f"{BASE_URL}/posts?status=scheduled&accountId={ACCOUNT_ID}&page={page}&limit=100"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"Error fetching posts page {page}: {resp.status_code} - {resp.text}")
            break
        data = resp.json()
        posts = data.get("posts", [])
        if not posts:
            break
        all_posts.extend(posts)
        pagination = data.get("pagination", {})
        if page >= pagination.get("pages", 1):
            break
        page += 1
    
    print(f"Found {len(all_posts)} scheduled posts across all pages.")

    updated_count = 0
    for post in all_posts:
        post_id = post["_id"]
        current_time = post.get("scheduledFor")
        
        if not current_time:
            continue

        # current_time is like "2026-08-19T08:00:00.000Z"
        # Target is 13:00:00.000Z (6:30 PM IST)
        date_part = current_time.split("T")[0]
        new_time = f"{date_part}T13:00:00.000Z"
        
        if current_time == new_time:
            print(f"Post {post_id} already set to 13:00 UTC. Skipping.")
            continue

        # 2. PUT the post (Zernio uses PUT, not PATCH)
        put_url = f"{BASE_URL}/posts/{post_id}"
        payload = {
            "scheduledFor": new_time
        }
        
        put_resp = requests.put(put_url, headers=headers, json=payload)
        if put_resp.status_code == 200:
            print(f"Updated post {post_id}: {current_time} -> {new_time}")
            updated_count += 1
        else:
            print(f"Failed to update post {post_id}: {put_resp.status_code} - {put_resp.text}")

    print(f"Successfully updated {updated_count} posts to 6:30 PM IST.")

if __name__ == "__main__":
    update_posts()
