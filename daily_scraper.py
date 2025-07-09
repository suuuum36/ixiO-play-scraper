from google_play_scraper import Sort, reviews
import pandas as pd
from datetime import datetime

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

# 저장 파일 이름
filename = f'reviews_{today_str}.csv'

# 저장
if filtered:
    df = pd.DataFrame(filtered)
    df[['at', 'review_date', 'userName', 'score', 'content', 'scraped_date']].to_csv(filename, index=False)
    print(f"[SUCCESS] 신규 리뷰 {len(filtered)}건 저장 완료: {filename}")
else:
    # 신규 리뷰 없을 때 메시지 저장
    df = pd.DataFrame([{
        'at': '',
        'review_date': today_str,
        'userName': '',
        'score': '',
        'content': '오늘 신규 리뷰가 없어요',
        'scraped_date': today_str
    }])
    df.to_csv(filename, index=False)
    print(f"[INFO] 신규 리뷰 없음. 메시지 저장됨: {filename}")
