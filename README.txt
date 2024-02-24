You need to have:
-Python 3.8 or higher
-A GitHub account
-HTTPX and FastAPI installed in your Python environment

step 1:
-Create a GitHub OAuth App
-Navigate to your GitHub settings and create a new OAuth app.
-For "Homepage URL", you can use http://localhost:8000.
-For "Authorization callback URL", enter http://localhost:8000/auth/github/callback.
-Note down the Client ID and Client Secret provided after creation.

Step 2:
-Install dependencies by running pip install fastapi, httpx, uvicorn.
-Open main.py and replace GITHUB_CLIENT_ID and CLIENT_SECRET with your GitHub OAuth app credentials.

Step 3:
-Start the app by runnin in terminal uvicorn main:app --reload or by PyCharm IDE just pressing run after putting FastAPI configuration.
-open web browser and navigate to "http://localhost:8000/github-login"
-After authorizing the application, you will be redirected to a page displaying your starred repositories.
