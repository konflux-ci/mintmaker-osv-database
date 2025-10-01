import requests
import os
import subprocess

QUAY_API_KEY = os.environ["QUAY_API_KEY"]
QUAY_ROBOT_USERNAME = os.environ["QUAY_ROBOT_USERNAME"]
QUAY_ROBOT_PASSWORD = os.environ["QUAY_ROBOT_PASSWORD"]
KEEP = 24 * 7  # Keep images for a week
LIMIT = 250

repos = ["konflux-ci/mintmaker-osv-database", "redhat-user-workloads/konflux-mintmaker-tenant/mintmaker-osv-database"]
repo_tags_url = lambda repo: f"https://quay.io/api/v1/repository/{repo}/tag"
repo_delete_tag_url = lambda repo, tag: f"docker://quay.io/{repo}:{tag}"

def skopeo_login(registry, username, password):
    try:
        result = subprocess.run(
            [
                "skopeo", "login", registry,
                "--username", username,
                "--password", password
            ],
            check=True,
            text=True,
            capture_output=True
        )
        print("✅ Login successful")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("❌ Login failed")
        print(e.stderr)
    return result.returncode


def skopeo_delete_tag(repo, tag):
    img_url = repo_delete_tag_url(repo, tag)
    try:
        result = subprocess.run(
            ["skopeo", "delete", img_url],
            check=True,
            text=True,
            capture_output=True
        )
        print(f"✅ Deleted tag {tag}")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to delete {tag}")
        print(e.stderr)
    
    return result.returncode

def get_tags_repo(repo):
    pages = 1
    repo_tags = []

    while True:

        url = repo_tags_url(repo)
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
    return repo_tags

def delete_tags(repo, tags):
    deleted = 0
    for tag in tags:
        return_code = skopeo_delete_tag(repo, tag["name"])
        if return_code == 0:
            deleted += 1

    print("For {} Deleted {} stale images".format(repo, deleted))



def main():
    for repo in repos:
        print(f"Fetching stale tags for repo {repo}")
        tags = get_tags_repo(repo)
        skopeo_login("quai.io", QUAY_ROBOT_USERNAME, QUAY_ROBOT_PASSWORD)
        delete_tags(repo, tags[KEEP:])


if __name__ == "__main__":
    main()
