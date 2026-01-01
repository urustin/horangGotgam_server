from datetime import datetime
import pytz

# 한국 표준시 (KST) 타임존 설정
kst = pytz.timezone('Asia/Seoul')

# 현재 시간을 KST로 변환
current_time_kst = datetime.now(kst)

# 원하는 포맷으로 출력
formatted_time_kst = current_time_kst.strftime("%Y. %m. %d %p %I:%M:%S")
print(formatted_time_kst)
