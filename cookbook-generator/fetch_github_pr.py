import requests
import os
# Replace with the username and repository name you want to scrape
owner = "langchain-ai"
repo = "langchain"

# GitHub API endpoint for pull requests
url = f"https://api.github.com/repos/{owner}/{repo}/pulls"

# Headers (optional: add your GitHub token if you face rate limits)
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": os.environ.get("GITHUB_TOKEN")
    
}

# Parameters to get all PRs (state can be 'all', 'open', 'closed')
params = {
    "state": "closed",
    "per_page": 100  # GitHub API limits the results to 100 per page
}

# Function to fetch all PRs
def fetch_prs(url, params, headers):
    prs = []
    idx=0
    while url and idx<10:
        idx+=1
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        prs.extend(response.json())
        # Check for pagination
        url = response.links.get("next", {}).get("url", None)
        params = {}
        print(url)
        
    return prs

# Function to get comments for a PR
def fetch_comments(pr_url, headers):
    comments_url = f"{pr_url}/comments"
    response = requests.get(comments_url, headers=headers)
    response.raise_for_status()
    return response.json()

# Fetch all PRs
prs = fetch_prs(url, params, headers)

# Iterate over PRs and print titles and comments
for pr in prs:
    print(f"PR Title: {pr['title']}")
    print(f"PR URL: {pr['html_url']}")
    print("Comments:")
    comments = fetch_comments(pr["url"], headers)
    for comment in comments:
        print(f"  - {comment['user']['login']}: {comment['body']}")
    print("\n" + "="*50 + "\n")
    

