#!/bin/bash

STATUS="$1"

if [[ "$STATUS" != "success" && "$STATUS" != "failed" ]]; then
  echo "Usage: $0 success|failed"
  exit 1
fi

mkdir -p .github/logs

LOG_ENTRY=$(jq -n \
  --arg issue_number "$ISSUE_NUMBER" \
  --arg owner_repo "$OWNER_REPO" \
  --arg badge_color "$BADGE_COLOR" \
  --arg badge_label "$BADGE_LABEL" \
  --arg file_name "$FILE_NAME" \
  --arg badge_url "https://raw.githubusercontent.com/$REPO/refs/heads/main/badges/$FILE_NAME" \
  '{issue_number: $issue_number, owner_repo: $owner_repo, badge_color: $badge_color, badge_label: $badge_label, file_name: $file_name, badge_url: $badge_url}')

LOG_FILE=".github/logs/${STATUS}.json"

if [ -f "$LOG_FILE" ]; then
  tmp=$(mktemp)
  jq ". += [$LOG_ENTRY]" "$LOG_FILE" > "$tmp" && mv "$tmp" "$LOG_FILE"
else
  echo "[$LOG_ENTRY]" > "$LOG_FILE"
fi

git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"
git add "$LOG_FILE"
git commit -m "$STATUS entry logged for issues #$ISSUE_NUMBER" || echo "No changes to commit"
git push origin HEAD:"$BRANCH"
