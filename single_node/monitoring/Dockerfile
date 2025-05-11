# Java가 설치된 기본 이미지를 사용합니다. Cerebro는 Java를 필요로 합니다.
FROM openjdk:11-jre-slim

# 작업 디렉토리를 설정합니다.
WORKDIR /app

# wget과 unzip을 설치합니다.
RUN apt-get update && apt-get install -y wget unzip

# Cerebro zip 파일을 GitHub에서 다운로드합니다.
RUN wget https://github.com/lmenezes/cerebro/releases/download/v0.9.4/cerebro-0.9.4.zip

# zip 파일을 추출합니다.
RUN unzip cerebro-0.9.4.zip

# 심볼릭 링크를 생성합니다.
RUN ln -s cerebro-0.9.4 cerebro

# Cerebro가 실행될 포트를 노출합니다.
EXPOSE 9000

# Cerebro를 실행하는 명령어를 설정합니다.
CMD ["cerebro/bin/cerebro", "-Dhttp.port=9000"]