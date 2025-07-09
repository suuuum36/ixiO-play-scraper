from google_play_scraper import Sort, reviews
import pandas as pd
from datetime import datetime
import os
import requests

# ✅ 슬랙 메시지 전송 함수
def send_slack_message(message):
    webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    if not webhook_url:
        print("[WARNING] SLACK_WEBHOOK_URL 환경변수가 없습니다. 슬랙 전송 생략")
        return

    res = requests.post(webhook_url, json={"text": message})
    if res.status_code == 200:
        print("[SLACK] 슬랙 메시지 전송 성공")
    else:
        print(f"[SLACK] 전송 실패: {res.status_code} - {res.text}")

# ✅ 날짜 설정
today = datetime.now()
today_str = today.strftime('%Y-%m-%d')
midnight = datetime(today.year, today.month, today.day)

# ✅ 앱 패키지명
package_name = 'com.lguplus.aicallagent'

# ✅ 리뷰 수집
result, _ = reviews(
    package_name,
    lang='ko',
    country='kr',
    sort=Sort.NEWEST,
    count=1000
)

# ✅ 리뷰 데이터 전처리
for r in result:
    r['scraped_date'] = today_str
    r['review_date'] = r['at'].strftime('%Y-%m-%d')

# ✅ 오늘 날짜 신규 리뷰 필터링
new_reviews = [r for r in result if r['at'] >= midnight]

# ✅ 신규 리뷰 블록 생성
if new_reviews:
    new_df = pd.DataFrame(new_reviews)
    new_df = new_df[['review_date', 'userName', 'score', 'content', 'scraped_date']]
    new_df.insert(0, 'status', '✅ 새로운 리뷰')

    # 슬랙 메시지 전송: 미리보기 3개
    preview = '\n'.join([
        f"{i+1}. ⭐{r['score']} | {r['content'][:50].strip()}…" for i, r in enumerate(new_reviews[:3])
    ])
    message = f"✅ *{today_str}* 새로운 리뷰 {len(new_reviews)}건 수집됨!\n\n{preview}"
    send_slack_message(message)
else:
    new_df = pd.DataFrame([{
        'status': '❌ 새로운 리뷰가 없어요',
        'review_date': '',
        'userName': '',
        'score': '',
        'content': '',
        'scraped_date': today_str
    }])
    send_slack_message(f"❌ *{today_str}* - 새로운 리뷰가 없어요.")

# ✅ 전체 리뷰 블록 생성
all_df = pd.DataFrame(result)
all_df = all_df[['review_date', 'userName', 'score', 'content', 'scraped_date']]
all_df.insert(0, 'status', '📦 전체 리뷰')

# ✅ 최종 결합
final_df = pd.concat([new_df, all_df], ignore_index=True)

# ✅ CSV 저장
filename = f'reviews_{today_str}.csv'
final_df.to_csv(filename, index=False)
print(f"[INFO] 리뷰 CSV 저장 완료: {filename}")
