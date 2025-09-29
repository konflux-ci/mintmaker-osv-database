import requests
import os

QUAY_API_KEY = os.environ["QUAY_API_KEY"]
KEEP = 24 * 7  # Keep images for a week
LIMIT = 250

repos = ["konflux-ci/mintmaker-osv-database", "redhat-user-workloads/konflux-mintmaker-tenant/mintmaker-osv-database"]
repo_url = lambda repo: f"https://quay.io/api/v1/repository/{repo}/tag"

for repo in repos:
    pages = 1
    repo_tags = []

    while True:
        url = repo_url(repo)
        resp = requests.get(url, 
                            params={"page": pages, 
                                    "limit": LIMIT, 
                                    "onlyActiveTags": "true"},
                                    headers={
                                        "Authorization" : f"Bearer {QUAY_API_KEY}"
                                    })
        resp.raise_for_status()
        tags = resp.json()
        repo_tags.extend(tags.get("tags", []))
        
        if not tags["has_additional"]:
            break
        
        pages += 1
    
    repo_tags.sort(key=lambda t: t["start_ts"], reverse=True)
    
    for tag in repo_tags[KEEP:]:
        del_resp = requests.delete(url + tag["name"], 
                        headers={
                            "Authorization" : f"Bearer {QUAY_API_KEY}"
                            })
        if del_resp.status_code != 200:
            print(f"Somthing went wrong with deleteing{tag["name"]}. Skipping it")

print("For {} Deleted {} stale images".format(len(repo_tags) - KEEP, repo))