FROM python:3.11-slim

WORKDIR /app

# 필요한 파일 복사
COPY requirements.txt .
COPY main.py .

# 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 포트 설정
EXPOSE 8000

# 컨테이너 실행 명령어
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 