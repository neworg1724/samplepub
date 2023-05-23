import requests
import pandas as pd

# GitHub credentials
github_token = "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"
github_organization = "neworg1724"

# GitHub API URLs
repositories_url = f"https://api.github.com/orgs/{github_organization}/repos"
teams_url = f"https://api.github.com/orgs/{github_organization}/teams"

# Authenticate with GitHub using a token
github_headers = {"Authorization": f"Bearer {github_token}"}

# Fetch repositories
repositories_response = requests.get(repositories_url, headers=github_headers)
repositories_data = repositories_response.json()

# Fetch teams
teams_response = requests.get(teams_url, headers=github_headers)
teams_data = teams_response.json()

# Prepare data for the repository, team, members, and permissions
data = []
for repo in repositories_data:
    team_response = requests.get(repo["teams_url"], headers=github_headers)
    team_data = team_response.json()
    if team_data:
        team_name = team_data[0]["name"]
        members_url = team_data[0]["members_url"].replace("{/member}", "")
        members_response = requests.get(members_url, headers=github_headers)
        members_data = members_response.json()
        for member in members_data:
            member_login = member["login"]
            permissions_url = f"https://api.github.com/repos/{github_organization}/{repo['name']}/collaborators/{member_login}/permission"
            permissions_response = requests.get(permissions_url, headers=github_headers)
            if permissions_response.status_code == 200:
                permissions_data = permissions_response.json()
                permission = permissions_data.get("permission", "")
            else:
                permission = ""
            data.append({
                "Repository": repo["name"],
                "Team": team_name,
                "Member": member_login,
                "Permission": permission
            })

# Create a pandas DataFrame from the data
df = pd.DataFrame(data)

# Save data to Excel sheet
df.to_excel("fetched.xlsx", index=False)

