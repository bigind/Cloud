# 5000 포트로 돌아가는 서비스를 강제종료
fuser -k 5000/tcp

# 플라스크 그린유니콘 서버 시작
gunicorn --bind 0:5000 main:app