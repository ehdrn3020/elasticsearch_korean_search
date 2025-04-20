#!/bin/bash

# 필요 패키지 설치
sudo yum install -y yum-utils
sudo sudo yum update -y

# Docker 설치
sudo yum install -y docker
# Docker Compose 설치
sudo curl -L https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-x86_64 \
  -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
# Docker 서비스 시작 및 부팅 시 자동 시작 설정
sudo systemctl start docker
sudo systemctl enable docker

# git 설치
sudo yum install -y git
# git project clone
cd /home/ec2-user 
sudo -u ec2-user git clone https://github.com/ehdrn3020/elasticsearch_korean_search.git

# Docker 볼륨 마운트 디렉토리 생성
cd elasticsearch_korean_search/single_node
mkdir -p esdata
sudo chown -R 1000:1000 esdata