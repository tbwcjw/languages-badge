#!/bin/bash

OWNER_REPO=$(echo "$ISSUE_BODY" | awk '/^### Repository/{getline; getline; print}' | xargs)

BADGE_LABEL=$(echo "$ISSUE_BODY" | awk '/^### Label/{getline; getline; print}' | xargs)
if [ "$BADGE_LABEL" = "_No response_" ] || [ -z "$BADGE_LABEL" ]; then
  BADGE_LABEL="Languages"
fi

ENCODED_BADGE_LABEL=$(echo "$BADGE_LABEL" | sed 's/ /%20/g')

COLORS=("purple" "blue" "cyan" "green" "yellow" "orange" "red")
ALL_LABELS=($(echo "$LABELS" | jq -r '.[].name'))

COLOR="blue"  # default color
for label in "${ALL_LABELS[@]}"; do
  for c in "${COLORS[@]}"; do
    if [[ "$label" == "$c" ]]; then
      COLOR="$c"
      break 2
    fi
  done
done

FILE_NAME=$(echo "${ENCODED_BADGE_LABEL}_${OWNER_REPO}_${COLOR}" | tr / _).svg

echo "OWNER_REPO=$OWNER_REPO" >> "$GITHUB_OUTPUT"
echo "BADGE_LABEL=$BADGE_LABEL" >> "$GITHUB_OUTPUT"
echo "BADGE_COLOR=$COLOR" >> "$GITHUB_OUTPUT"
echo "FILE_NAME=$FILE_NAME" >> "$GITHUB_OUTPUT"