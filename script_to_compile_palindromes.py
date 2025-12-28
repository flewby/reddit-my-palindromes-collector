import praw
import json
from datetime import datetime

# Configure these
CLIENT_ID = "my_client_id"
CLIENT_SECRET = "my_client_secret"
USERNAME = "my_username"
PASSWORD = "my_password"
USER_AGENT = f"script:scraper:v1.0 (by u/{USERNAME})"


SUBREDDIT_NAME = "palindromes"
YEAR = 2025  # Year to filter

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    username=USERNAME,
    password=PASSWORD
)

def scrape_posts_and_comments(subreddit_name, year):
    data = {"posts": [], "comments": []}
    user = reddit.redditor(USERNAME)
    
    print(f"Scraping posts from r/{subreddit_name} in {year}...")
    
    # Get posts
    for post in user.submissions.new(limit=None):
        post_date = datetime.fromtimestamp(post.created_utc)
        if post_date.year == year and post.subreddit.display_name.lower() == subreddit_name.lower():
            data["posts"].append({
                "title": post.title,
                "text": post.selftext,
                "url": f"https://reddit.com{post.permalink}",
                "score": post.score,
                "created_utc": post.created_utc,
                "date": post_date.strftime("%Y-%m-%d %H:%M:%S")
            })
    
    print(f"Found {len(data['posts'])} posts")
    print(f"Scraping comments from r/{subreddit_name} in {year}...")
    
    # Get comments
    for comment in user.comments.new(limit=None):
        comment_date = datetime.fromtimestamp(comment.created_utc)
        if comment_date.year == year and comment.subreddit.display_name.lower() == subreddit_name.lower():
            data["comments"].append({
                "text": comment.body,
                "post_title": comment.submission.title,
                "url": f"https://reddit.com{comment.permalink}",
                "score": comment.score,
                "created_utc": comment.created_utc,
                "date": comment_date.strftime("%Y-%m-%d %H:%M:%S")
            })
    
    print(f"Found {len(data['comments'])} comments")
    
    # Save to file
    filename = f"reddit-my-palindromes_{year}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nData saved to {filename}")
    return data

# Run the scraper
if __name__ == "__main__":
    scrape_posts_and_comments(SUBREDDIT_NAME, YEAR)
