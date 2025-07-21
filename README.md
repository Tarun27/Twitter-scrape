# Twitter-to-Excel Exporter

Export any public Twitter user's tweets (up to 3,200) to Excel using the **official Twitter API v2** and Python 3.11+.

---

## 🚀 Quick Start

1. **Clone this repository**
    ```bash
    git clone <your-repo-url> twitter-excel
    cd twitter-excel
    ```

2. **Create & activate a Python virtual environment**
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate        # macOS / Linux
    # .\venv\Scripts\activate      # Windows
    ```

3. **Install dependencies**
    ```bash
    pip install tweepy pandas openpyxl
    ```

4. **Get a Twitter Bearer Token**
    - Sign in at [developer.twitter.com](https://developer.twitter.com)
    - Create a Project → App → Keys & Tokens
    - Copy the Bearer Token (OAuth 2.0)

5. **Configure your script**
    - Open `twit.py`
    - Paste your Bearer Token:
      ```python
      BEARER_TOKEN = "YOUR_TOKEN_HERE"
      ```
    - Set the username you want to export:
      ```python
      USERNAME = "twitter_username"
      ```

6. **Run the exporter**
    ```bash
    python twit.py
    ```

7. **Find your exported file**
    - The file will appear as:  
      `USERNAME_tweets_YYYY-MM-DD.xlsx`  
      in the same folder.

---

## 📁 File Layout

| File             | Purpose                                 |
| ---------------- | --------------------------------------- |
| `twit.py`        | Main script                             |
| `requirements.txt`| tweepy, pandas, openpyxl, requests     |
| `README.md`      | This file                               |

---

## 🛠️ Requirements

- Python **3.11+**
- Twitter Bearer Token (free tier is OK)
- Internet connection

---

## 📝 Usage Details

- **Handle to export:**  
  Edit `USERNAME` inside `twit.py`.

- **Rate limits:**  
  Free tier = 300 requests / 15 min (the script will auto-sleep as needed).

- **Max tweets:**  
  Twitter API caps at 3,200 most-recent tweets.

---

## 📊 Output Columns

| Column    | Content                                 |
| --------- | --------------------------------------- |
| Date      | Tweet timestamp (UTC, naïve)            |
| Link      | Full URL to tweet                       |
| Tweet     | Text content                            |
| Likes     | Like count                              |
| Retweets  | Retweet count                           |
| Replies   | Reply count                             |

---

## 🧪 Troubleshooting

| Symptom                       | Fix                                                |
|-------------------------------|----------------------------------------------------|
| Unauthorized                  | Regenerate Bearer Token, ensure read permissions   |
| Rate-limit hit – sleeping…    | Normal; let it finish (≈15 min with free tier)     |
| Excel timezone error          | Script strips timezones – no action needed         |
| ConnectionError               | Script retries; use stable Wi-Fi                   |

---

## 📄 License

MIT – feel free to use, modify, and redistribute.

---

