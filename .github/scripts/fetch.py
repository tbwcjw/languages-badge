import os
import requests
import re

def main():
    issue_body = os.getenv("ISSUE_BODY", "")
    if not issue_body:
        print("No ISSUE_BODY found")
        exit(1)
    match = re.search(r'([\w.-]+)/([\w.-]+)', issue_body)
    if not match:
        print("No repo pattern 'user/repo' found in issue body")
        exit(1)

    owner, repo = match.group(1), match.group(2)
    print(f"Parsed owner: {owner}, repo: {repo}")

    url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    headers = {
        "User-Agent": "github-actions",
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch languages: {response.status_code} {response.text}")
        exit(1)

    data = response.json()
    languages = " , ".join(list(data.keys())[:3]) if data else "Unknown"

    badge_url = f"https://img.shields.io/badge/languages-{requests.utils.quote(languages)}-blue"
    print(f"Fetching badge from: {badge_url}")

    badge_response = requests.get(badge_url)
    if badge_response.status_code != 200:
        print(f"Failed to fetch badge SVG: {badge_response.status_code}")
        exit(1)

    os.makedirs("badges", exist_ok=True)
    with open(f"badges/{owner}_{repo}.svg", "wb") as f:
        f.write(badge_response.content)

    print(f"Badge saved to badges/{owner}_{repo}.svg")
    exit(0)

if __name__ == "__main__":
    main()