#!/bin/bash
# Usage: ./zernio-publish-now.sh <topic-file>
# Publishes a content file immediately with proper newline handling

if [ -z "$1" ]; then
  echo "Usage: $0 <topic-file>"
  echo "Example: $0 content/topics/topic16-xpersonal-may23.md"
  exit 1
fi

FILE="$1"
if [ ! -f "$FILE" ]; then
  echo "File not found: $FILE"
  exit 1
fi

# Extract platform and account from filename
BASENAME=$(basename "$FILE")
if [[ "$BASENAME" =~ linkedin ]]; then
  PLATFORM="linkedin"
  ACCOUNT="6a0ee81e520992756d91d5d6"
elif [[ "$BASENAME" =~ xpersonal ]]; then
  PLATFORM="twitter"
  ACCOUNT="6a0ee834520992756d91d691"
elif [[ "$BASENAME" =~ xwefab ]]; then
  PLATFORM="twitter"
  ACCOUNT="6a0f049f520992756d92c57a"
else
  echo "Cannot determine platform from filename"
  exit 1
fi

# Read file content with actual newlines
CONTENT=$(cat "$FILE")

# Create JSON payload using jq to properly handle newlines
echo "Publishing $BASENAME to $PLATFORM..."

# Build JSON with jq
echo "$CONTENT" | jq -Rs '{
  content: .,
  platforms: [
    {
      platform: "'$PLATFORM'",
      accountId: "'$ACCOUNT'"
    }
  ]
}' | curl -s -X POST "https://zernio.com/api/v1/posts" \
  -H "Authorization: Bearer $(grep zernioApiKey zernio-config.mjs | sed 's/.*"\(sk_[^"]*\)".*/\1/')" \
  -H "Content-Type: application/json" \
  -d @- | jq -r '.message // .error'
