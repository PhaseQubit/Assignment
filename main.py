import httpx
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
# I used PyCharm professional version, so it was a bit easier to code this with the AI code assistant.
app = FastAPI()

GITHUB_CLIENT_ID = "Your client ID"
REDIRECT_URI = "http://localhost:8000/auth/github/callback"
CLIENT_SECRET = "Your client secret"


@app.get("/")
def read_root():
    return {"This app should be working as expected!"}


# I used this video as source: https://www.youtube.com/watch?v=Pm938UxLEwQ&ab_channel=WillEstes
@app.get("/github-login")
async def github_login():
    # Redirect user to GitHub for authorization
    return RedirectResponse(f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}", status_code=302)


@app.get("/auth/github/callback")
async def github_callback(code: str):
    # Exchange code for token
    params = {"client_id": GITHUB_CLIENT_ID, "client_secret": CLIENT_SECRET, "code": code}
    headers = {"Accept": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.post("https://github.com/login/oauth/access_token", params=params, headers=headers)
    response_json = response.json()
    access_token = response_json.get("access_token")

    # Use token to fetch starred repos
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {access_token}"}
        starred_repos_response = await client.get("https://api.github.com/user/starred", headers=headers)
        starred_repos = starred_repos_response.json()

        # Filter out private repos and map to desired structure
        filtered_repos = [
            {
                "name": repo["name"],
                "description": repo["description"],
                "url": repo["html_url"],
                "license": repo["license"]["name"] if repo["license"] else None,
                "topics": repo["topics"]
            }
            for repo in starred_repos if not repo["private"]
        ]

    return JSONResponse(content={
        "number of starred repositories": len(filtered_repos),
        "repositories": filtered_repos
    })
