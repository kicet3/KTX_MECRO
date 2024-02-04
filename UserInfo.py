# 전화번호 로그인만 가능합니다.
user = {
    "middlePhoneNumber": "1234", # 전화번호 중간자리
    "lastPhoneNumber": "5678", # 전화번호 끝자리
    "startStation": "나주", # 출발역
    "destinationStation": "용산", # 도착역
    "password": "password", # 비밀번호
    "findStartTime":"12", # 조회 시작 시간
    "wantDate": "2024-02-11", # 원하는 날짜
    #현재는 분단위는 지원하지 않습니다. 다만 추후 분 단위 지원을 위해 :00분은 붙여주세요.
    "wantStartTime": "13:00", # 원하는 시간 범위 시작 
    "wantEndTime": "18:00", # 원하는 시간 범위 끝 
}

## 디스코드에 알림을 보내기 위한 정보 입니다. 해당 정보가 없으면 실행되지 않습니다.
discordInfo = {
    "applicationId":"applicationId",  # 디스코드 봇의 applicationId
    "token":"discordToken", # 디스코드 봇의 토큰
    "channelId": "discordTokenId", # 디스코드 채널의 아이디 (알림을 받고 싶은 서버의 채널의 아이디를 넣어주면 됩니다.)
}