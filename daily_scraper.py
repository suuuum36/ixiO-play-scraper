from google_play_scraper import Sort, reviews
import pandas as pd
from datetime import datetime
import os

# 날짜 설정
today = datetime.now()
today_str = today.strftime('%Y-%m-%d')
midnight = datetime(today.year, today.month, today.day)

# 앱 패키지명
package_name = 'com.lguplus.aicallagent'

# Google Play에서 리뷰 수집 (최대 1000개)
result, _ = reviews(
    package_name,
    lang='ko',
    country='kr',
    sort=Sort.NEWEST,
    count=1000
)

# 전체 리뷰 전처리
for r in result:
    r['scraped_date'] = today_str
    r['review_date'] = r['at'].strftime('%Y-%m-%d')

# 오늘 날짜만 필터링
new_reviews = [r for r in result if r['at'] >= midnight]

# ✅ 신규 리뷰 블록 만들기
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

# ✅ 전체 리뷰 DataFrame 생성
all_df = pd.DataFrame(result)
all_df = all_df[['review_date', 'userName', 'score', 'content', 'scraped_date']]
all_df.insert(0, 'status', '📦 전체 리뷰')

# ✅ 최종 결합: 상단에 신규 리뷰, 하단에 전체 리뷰
final_df = pd.concat([new_df, all_df], ignore_index=True)

# 저장
filename = f'reviews_{today_str}.csv'
final_df.to_csv(filename, index=False)
print(f"[INFO] 리뷰 CSV 저장 완료: {filename}")
