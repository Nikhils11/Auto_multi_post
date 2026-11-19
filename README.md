# Auto Multi Post

Auto Multi Post is a FastAPI service that publishes one message to Bluesky, Mastodon, DEV Community, GitHub Gist, and a Telegram channel.

> **Caution:** A request to the posting endpoint attempts to publish the message to every configured platform. Use test accounts or test content until you are ready to publish publicly.

## Requirements

- Python 3.13 or later
- [uv](https://docs.astral.sh/uv/) for dependency and environment management
- Credentials and account details for the platforms you want to use

## Setup

From the project directory, create the virtual environment and install the locked dependencies:

```shell
uv sync
```

Copy the sample environment file to the location read by the application:

**Windows PowerShell**

```powershell
Copy-Item app\.env.example app\.env
```

**macOS / Linux**

```shell
cp app/.env.example app/.env
```

Edit `app/.env` and replace the example values with your own credentials and account details. Keep this file private; it contains secrets and is excluded from Git. The application requires all listed settings, even if you do not plan to post to a particular platform.

## Run the API

Start the development server from the project directory:

```shell
uv run uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Open `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

## Publish a message

Send a `POST` request to `/posting` with a JSON body containing a `message` of at most 200 characters. For example:

```shell
curl -X POST http://127.0.0.1:8000/posting \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"Hello from Auto Multi Post!\"}"
```

The response includes an overall success value and a result for each platform, including its status and, when available, the published URL or an error.

## Environment settings

The sample file is [`app/.env.example`](app/.env.example). It lists the settings required by the service:

| Setting | Purpose |
| --- | --- |
| `BLUESKY_USERNAME` | Bluesky account handle or identifier |
| `BLUESKY_PASSWORD` | Bluesky password or app password |
| `BLUESKY_DID` | Bluesky repository DID |
| `BLUESKY_SESSION_URL` | Bluesky session creation endpoint |
| `BLUESKY_POST_URL` | Bluesky record creation endpoint |
| `MASTODON_USERNAME` | Mastodon account name used when constructing the post URL |
| `MASTODON_ACCESS_TOKEN` | Mastodon access token |
| `MASTODON_POST_URL` | Status creation endpoint for your Mastodon instance |
| `DEVTO_USERNAME` | DEV Community username |
| `DEVTO_API_KEY` | DEV Community API key |
| `DEVTO_POST_URL` | DEV Community article creation endpoint |
| `GIST_PAT_TOKEN` | GitHub personal access token with permission to create Gists |
| `GIST_POST_URL` | GitHub Gist creation endpoint |
| `TELEGRAM_API_TOKEN` | Telegram bot token |
| `TELEGRAM_BASE_URL` | Telegram Bot API base URL |
| `TELEGRAM_CHANNEL_URL` | Public channel URL prefix used to construct post links |
| `TELEGRAM_CHANNEL_ID` | Telegram channel ID or username the bot will post to |

Use the endpoint URLs and account-specific values appropriate for your accounts and instances. The values in the sample are examples, not working credentials.
