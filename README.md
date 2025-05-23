# elasticsearch_korean_search
### 엘라스틱서치 한글 형태소 검색
<img src="architecture.png" width="600">
<br>

### 프로젝트 구조
```
├── statistics_korean/
│   └── korean_data_index_agg_query
├── single_node/
│   ├── docker-compose.yml
│   ├── README.md
│   ├── elastic_indexs/
│   │   └── index_setting.json
│   ├── generation/
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── collection/
│       └── Dockerfile
├── setting_aws/
│   ├── keypair.pem
│   ├── .env
│   ├── env_example 
│   ├── setup_server.sh
│   └── user_script.sh
└── README.md
```
- statistics_korean : 예제 파일
- single_node : 단일노드로 generation, collection docker 실행
  - generation : 한글 인덱스 생성 FastAPI 서비스
  - collection : Nori가 설치된 ElasticSearch
- setting_aws : AWS 서버 자동화 설정
<br>
<br>

## [ AWS Server Setting ]
- 설치 서버는 AWS EC2  를 사용
- 참조 : https://www.elastic.co/docs/deploy-manage/deploy/self-managed/install-elasticsearch-docker-basic

### .env 파일 생성
- .env는 aws 관련 접속정보가 정의 된 파일
- setting_aws/env_example 참조하여 생성

### keypair.pem 키 생성
- ec2 접속을 위해 keypair.pem 키를 setting_aws 폴더에 생성
- 파일 권한 수정 : sudo chmod 600 setting_aws/keypair.pem
<br>


## [ AWS EC2 실행 ]
```commandline
sh setting_aws/setup_server.sh server_1
```

### SSH 접속
```commandline
ssh -i setting_aws/keypair.pem ec2-user@{server_ip}
```
<br>


## Single Node로 실행
### ElasticSearch 설치
```commandline
# docker compose file 실행
cd elasticsearch_korean_search/single_node
sudo docker-compose up -d

# 삭제
sudo docker-compose down --rmi all --volumes
```
<br>


## Elastic(Collection) 설치확인
```commandline
# Check Elastic Install
sudo docker image ls
sudo docker ps -a

# 로그 확인
sudo docker logs es01

# 메모리 모니터링
sudo docker stats es01

# Check Elasic API
curl http://localhost:9200
curl http://localhost:9200/_cluster/health?pretty
curl http://localhost:9200/_nodes?pretty

# Nori Plugin 확인
sudo docker exec -it es01 bin/elasticsearch-plugin list

# Nori API 실행 에제
curl -X GET "localhost:9200/_analyze" -H 'Content-Type: application/json' -d '
{
  "tokenizer": "nori_tokenizer",
  "text": "동해물과 백두산이"
}'
```
<br>

## Fast API(Generation) 설치확인
```
# 로그 확인
sudo docker logs fapi01

# 해당 컨테이너만 재실행
sudo docker-compose build fapi01 && sudo docker-compose up -d --no-deps --force-recreate fapi01

# 루트 엔드포인트 테스트
curl http://localhost:8000/
{"status":"active","message":"랜덤 데이터 생성 API가 실행 중입니다."}
```
<br>

## Kibana 설치확인
```
# kibana dashboard 확인
http://13.123.123.123:5601/app/dev_tools#/console/shell

# 한글데이터 인덱스 확인
GET /korean_data/_search
```
<br>

## Cerebro 확인
```
https:{$ip}:9000 웹URL에 접속하여,
"http://es01:9200" 입력
```
<img src="cerebro.png" width="700">
<br>

## 검색 집계 예제
### 기본예제
statistics_korean/korean_data_index_agg_query
- 직업별로 많이 분포하는 주소의 시 집계
- 직업별로 많이 분포하는 주요 키워드(캐치프레지즈) 형태소 집계
<br>
<br>

## 참조 
- 토크나이저에 따른 기본 예제 
  - https://esbook.kimjmin.net/06-text-analysis/6.7-stemming/6.7.2-nori
- Nori Docs
  - https://www.elastic.co/docs/reference/elasticsearch/plugins/analysis-nori