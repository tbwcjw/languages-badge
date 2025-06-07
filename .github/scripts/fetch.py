import os
import requests
import re

def main():
    owner_repo = os.getenv("OWNER_REPO", "")
    badge_color = os.getenv("BADGE_COLOR", "blue")
    badge_label = os.getenv("BADGE_LABEL", "Languages")

    match = re.search(r'([\w.-]+)/([\w.-]+)', owner_repo)
    if not match:
        raise ValueError("No repo pattern 'user/repo' found in issue body")

    owner, repo = match.group(1), match.group(2)
    print(f"Parsed owner: {owner}, repo: {repo}")

    url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    headers = {
        "User-Agent": "github-actions",
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch languages: {response.status_code} {response.text}")

    data = response.json()
    languages = ", ".join(list(data.keys())[:3]) if data else "Unknown"

    badge_url = f"https://img.shields.io/badge/{badge_label}-{requests.utils.quote(languages)}-{badge_color}"
    print(f"Fetching badge from: {badge_url}")

    badge_response = requests.get(badge_url)
    if badge_response.status_code != 200:
        raise ValueError(f"Failed to fetch badge SVG: {badge_response.status_code}")

    os.makedirs("badges", exist_ok=True)
    with open(f"badges/{badge_label}_{owner}_{repo}_{badge_color}.svg", "wb") as f:
        f.write(badge_response.content)

    print(f"Badge saved to badges/{badge_label}_{owner}_{repo}_{badge_color}.svg")
    exit(0)

if __name__ == "__main__":
    main()