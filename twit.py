#!/usr/bin/env python3
"""
Export all available tweets for a user to Excel (max 3 200 tweets).
Free-tier API friendly – auto-resumes after rate-limit window.
"""
import tweepy, pandas as pd, datetime, time, requests
from tweepy.errors import TooManyRequests   

# -----------------------------------------------------------
# CONFIGURE THESE TWO VALUES
# -----------------------------------------------------------
BEARER_TOKEN = "BEARER_TOKEN"   # <<<<<<  paste your Bearer Token
USERNAME     = "username"              # <<<<<<  target handle (no @)
# -----------------------------------------------------------

client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=False)

# --- helper: retry with exponential back-off -----------------
def robust_request(func, *args, **kwargs):
    delay = 1
    while True:
        try:
            return func(*args, **kwargs)
        except TooManyRequests as e:
            reset = int(e.response.headers.get("x-rate-limit-reset", 0))
            sleep_for = max(reset - int(time.time()) + 5, 900)
            print(f"⏱️  Rate-limit hit – sleeping {sleep_for}s …")
            time.sleep(sleep_for)
        except (tweepy.TweepyException, requests.exceptions.ConnectionError) as e:
            # catches 5xx / dropped connections
            print(f"⚠️  {e.__class__.__name__} – retry in {delay}s …")
            time.sleep(delay)
            delay = min(delay * 2, 60)
        except Exception:
            raise

# --- resolve username → user-id -----------------------------
user_info = robust_request(client.get_user, username=USERNAME)
user_id   = user_info.data.id

# --- page through tweets ------------------------------------
tweets, pagination_token = [], None
while True:
    page = robust_request(
        client.get_users_tweets,
        id=user_id,
        max_results=100,
        pagination_token=pagination_token,
        tweet_fields=["created_at", "public_metrics", "text"]
    )
    if not page.data:
        break
    tweets.extend(page.data)
    pagination_token = page.meta.get("next_token")
    print(f"📥  Downloaded {len(tweets):,} tweets …")
    if not pagination_token:
        break

# --- build DataFrame ----------------------------------------
df = pd.DataFrame([
    {
        "Date":     pd.to_datetime(t.created_at).strftime("%Y-%m-%d %H:%M:%S"),
        "Link":     f"https://twitter.com/{USERNAME}/status/{t.id}",
        "Type":     "Retweet" if t.text.startswith("RT @") else "Tweet",
        "Tweet":    t.text,
        "Likes":    t.public_metrics["like_count"],
        "Retweets": t.public_metrics["retweet_count"],
        "Replies":  t.public_metrics["reply_count"]
    }
    for t in tweets
])

file_name = f"{USERNAME}_tweets_{datetime.date.today()}.xlsx"
df.to_excel(file_name, index=False)
print(f"💾  Saved {len(df):,} tweets → {file_name}")