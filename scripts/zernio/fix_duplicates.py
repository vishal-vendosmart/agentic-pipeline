import requests
import os
from datetime import datetime, timedelta

# Config
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

def is_weekday(date):
    return date.weekday() < 5

def get_next_weekday(date):
    date += timedelta(days=1)
    while not is_weekday(date):
        date += timedelta(days=1)
    return date

def fix_schedule():
    # 1. Fetch all scheduled posts
    all_posts = []
    page = 1
    while True:
        url = f"{BASE_URL}/posts?status=scheduled&accountId={ACCOUNT_ID}&page={page}&limit=100"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"Error fetching page {page}: {resp.status_code}")
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

    print(f"Total posts found: {len(all_posts)}")
    
    # Sort posts by current scheduled time
    all_posts.sort(key=lambda x: x.get('scheduledFor', ''))

    # Track which dates are occupied
    occupied_dates = set()
    updated_count = 0

    for post in all_posts:
        post_id = post["_id"]
        current_sf = post.get("scheduledFor", "")
        if not current_sf:
            continue
        
        # Convert to date object
        current_date = datetime.strptime(current_sf, "%Y-%m-%dT%H:%M:%S.%fZ").date()
        date_str = current_date.strftime("%Y-%m-%d")

        # If date is already occupied, move to next weekday
        while date_str in occupied_dates:
            current_date = get_next_weekday(datetime.combine(current_date, datetime.min.time()))
            date_str = current_date.strftime("%Y-%m-%d")

        occupied_dates.add(date_str)
        
        # New scheduled time: 13:00 UTC (6:30 PM IST)
        new_sf = f"{date_str}T13:00:00.000Z"
        
        if current_sf != new_sf:
            put_url = f"{BASE_URL}/posts/{post_id}"
            payload = {"scheduledFor": new_sf}
            put_resp = requests.put(put_url, headers=headers, json=payload)
            if put_resp.status_code == 200:
                print(f"Moved {post_id[-6:]}: {current_sf} -> {new_sf}")
                updated_count += 1
            else:
                print(f"Failed to update {post_id[-6:]}: {put_resp.status_code}")
        else:
            print(f"Post {post_id[-6:]} already correct: {new_sf}")

    print(f"\nSuccessfully updated {updated_count} posts.")
    
    # Final verification report
    print("\n--- Final Verified Schedule ---")
    # Re-fetch all to be sure
    final_posts = []
    page = 1
    while True:
        url = f"{BASE_URL}/posts?status=scheduled&accountId={ACCOUNT_ID}&page={page}&limit=100"
        resp = requests.get(url, headers=headers)
        data = resp.json()
        posts = data.get("posts", [])
        if not posts: break
        final_posts.extend(posts)
        pagination = data.get("pagination", {})
        if page >= pagination.get("pages", 1): break
        page += 1
    
    final_posts.sort(key=lambda x: x.get('scheduledFor', ''))
    for p in final_posts:
        print(f"{p.get('scheduledFor')} | {p['_id'][-6:]}")

if __name__ == "__main__":
    fix_schedule()
