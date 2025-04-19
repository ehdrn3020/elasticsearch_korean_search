#!/bin/bash
# 필요 패키지 설치
sudo yum install -y yum-utils
sudo sudo yum update -y
# Docker 설치
sudo yum install -y docker
# Docker 서비스 시작 및 부팅 시 자동 시작 설정
sudo systemctl start docker
sudo systemctl enable docker
# git 설치
sudo yum install -y git

cd /home/ec2-user 
# git project clone
sudo -u ec2-user git clone https://github.com/ehdrn3020/elasticsearch_korean_search.git
# Docker 볼륨 마운트 디렉토리 생성
mkdir -p _data
