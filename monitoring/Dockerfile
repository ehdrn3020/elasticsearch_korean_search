# Java가 설치된 기본 이미지를 사용합니다. Celebro는 Java를 필요로 합니다.
FROM openjdk:11-jre-slim

# 작업 디렉토리를 설정합니다.
WORKDIR /app

# wget을 설치합니다.
RUN apt-get update && apt-get install -y wget

# Celebro tar 파일을 GitHub에서 다운로드합니다.
RUN wget -O celebro-version.tar.gz https://github.com/lmenezes/celebro/releases/download/v0.9.4/celebro-0.9.4.tar.gz

# tar 파일을 추출합니다.
RUN tar -xzf celebro-version.tar.gz

# Celebro가 실행될 포트를 노출합니다.
EXPOSE 9000

# Celebro를 실행하는 명령어를 설정합니다.
CMD ["bin/celebro", "-p", "9000"]