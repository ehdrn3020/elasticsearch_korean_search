## [ Single Mode 수동 설치 ]

### ElasticSearch 설치
```commandline
# Image Download
sudo docker pull docker.elastic.co/elasticsearch/elasticsearch:8.17.4

# Create a new docker network
sudo docker network create elastic

# Cheak network
sudo docker network ls

# Run Container ( 보안 비활성화 )
sudo docker run --name es01 --net elastic -p 9200:9200 -d -m 2GB \
  -e "discovery.type=single-node" \
  -e "ES_JAVA_OPTS=-Xms1g -Xmx1g" \
  -e "node.name=es01" \
  -e "cluster.name=elastic-cluster" \
  -e "xpack.security.enabled=false" \
  -e "xpack.security.enrollment.enabled=false" \
  -e "xpack.security.http.ssl.enabled=false" \
  docker.elastic.co/elasticsearch/elasticsearch:8.17.4

# 로그 확인
sudo docker logs es01

# 메모리 모니터링
docker stats es01
```

### Elastic 설치확인
```commandline
# Check Elastic Install
sudo docker image ls
sudo docker ps

# Check Elasic API
curl http://localhost:9200
curl http://localhost:9200/_cluster/health?pretty
curl http://localhost:9200/_nodes?pretty
```

### Kibana 설치
```
# Image Download
sudo docker pull docker.elastic.co/kibana/kibana:8.17.4

# Run Container
sudo docker run --name kib01 --net elastic -p 5601:5601 -d \
  -e "ELASTICSEARCH_HOSTS=http://es01:9200" \
  -e "xpack.security.enabled=false" \
  docker.elastic.co/kibana/kibana:8.17.4
```

### FastAPI 애플리케이션 설치
```
# FastAPI 애플리케이션 디렉토리로 이동
cd generation

# FastAPI 컨테이너 실행 (ElasticSearch와 같은 네트워크에 연결)
sudo docker run --name fapi01 --net elastic -p 8000:8000 -d \
  -e "TZ=Asia/Seoul" \
  -e "ELASTICSEARCH_HOST=http://es01:9200" \
  fapi01

# 로그 확인
sudo docker logs fapi01

# API 동작 확인
curl http://localhost:8000/
curl http://localhost:8000/status
```
<br>

## [ 한글 형태소 분석기 설치 ]
### Nori Plugin 설치
```
# 컨테이너 접속
sudo docker exec -it es01 /bin/bash

# 플러그인 설치
bin/elasticsearch-plugin install analysis-nori
exit

# 컨테이너 재시작
sudo docker restart es01

# 설치 확인
sudo docker exec -it es01 bin/elasticsearch-plugin list

# 예제로 확인
curl -X GET "localhost:9200/_analyze" -H 'Content-Type: application/json' -d '
{
  "tokenizer": "nori_tokenizer",
  "text": "동해물과 백두산이"
}'
```