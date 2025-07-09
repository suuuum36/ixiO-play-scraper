from google_play_scraper import Sort, reviews
import pandas as pd
from datetime import datetime
import os

# 앱 패키지명
package_name = 'com.lguplus.aicallagent'

# 날짜 설정
today = datetime.now()
today_str = today.strftime('%Y-%m-%d')
midnight = datetime(today.year, today.month, today.day)

# 수집
result, _ = reviews(
    package_name,
    lang='ko',
    country='kr',
    sort=Sort.NEWEST,
    count=1000
)

# 신규 리뷰 필터링
new_reviews = []
for r in result:
    r['scraped_date'] = today_str
    r['review_date'] = r['at'].strftime('%Y-%m-%d')
    if r['at'] >= midnight:
        new_reviews.append(r)

# 신규 리뷰 DataFrame
if new_reviews:
    new_df = pd.DataFrame(new_reviews)
    new_df = new_df[['review_date', 'userName', 'score', 'content', 'scraped_date']]
    new_df.insert(0, 'status', '✅ 새로운 리뷰')
else:
    new_df = pd.DataFrame([{
        'status': '❌ 새로운 리뷰가 없어요',
        'review_date': '',
        'userName': '',
        'score': '',
        'content': '',
        'scraped_date': today_str
    }])

# 기존 누적 리뷰 불러오기
filename = f'reviews_{today_str}.csv'
if os.path.exists(filename):
    existing_df = pd.read_csv(filename)
else:
    existing_df = pd.DataFrame(columns=['status', 'review_date', 'userName', 'score', 'content', 'scraped_date'])

# 새로운 리뷰를 맨 위에, 기존 리뷰 아래에 붙이기
final_df = pd.concat([new_df, existing_df], ignore_index=True)

# 저장
final_df.to_csv(filename, index=False)
print(f"[INFO] 전체 리뷰 데이터 저장 완료: {filename}")
