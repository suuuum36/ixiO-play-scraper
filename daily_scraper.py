# daily_scraper.py
from google_play_scraper import Sort, reviews
import pandas as pd
from datetime import datetime, timedelta
import os

# 앱 패키지명
package_name = 'com.lguplus.aicallagent'

# 날짜 설정
today = datetime.now()
today_str = today.strftime('%Y-%m-%d')
midnight = datetime(today.year, today.month, today.day)

# 리뷰 수집
result, _ = reviews(
    package_name,
    lang='ko',
    country='kr',
    sort=Sort.NEWEST,
    count=1000
)

# 필터링: 자정 이후 리뷰만
filtered = []
for r in result:
    r['scraped_date'] = today_str
    r['review_date'] = r['at'].strftime('%Y-%m-%d')
    if r['at'] >= midnight:
        filtered.append(r)

# 저장
if filtered:
    df = pd.DataFrame(filtered)
    filename = f'reviews_{today_str}.csv'
    df[['at', 'review_date', 'userName', 'score', 'content', 'scraped_date']].to_csv(filename, index=False)
    print(f"[SUCCESS] {len(filtered)} reviews saved to {filename}")
else:
    print("[INFO] No new reviews found today.")
