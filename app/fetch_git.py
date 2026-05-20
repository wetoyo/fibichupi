import requests
from datetime import datetime, timedelta, timezone
TOKEN = "tolkien"

def get_commits(user: str, since=None):
    if since is None:
        since = datetime.now(timezone.utc) - timedelta(days=90)
    url = f"https://api.github.com/users/{user}/events"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    total = 0
    last_date = ""
    page = 1

    while True:
        res = requests.get(f"{url}?page={page}&per_page=100", headers=headers)
        if res.status_code != 200:
            break

        events = res.json()
        if not events:
            break

        for e in events:
            created_at = e.get("created_at")
            if created_at:
                created_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                if since and created_date < since:
                    return total, last_date

            if e.get("type") == "PushEvent":
                if not last_date:
                    last_date = created_at

                pl = e.get("payload", {})
                commits = pl.get("commits")
                if commits is not None:
                    total += len(commits)
                else:
                    total += 1

        if len(events) < 100:
            # github gives 100 at a time, so if less than 100 we quit w tech?
            break

        page += 1

    return total, last_date

if __name__ == "__main__":
    c, d = get_commits("wetoyo")
    print(c)
