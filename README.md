# elasticsearch_korean_search
### 엘라스틱서치 한글 형태소 검색

## [ AWS Server Setting ]
- 설치 서버는 AWS EC2  를 사용
- 참조 : https://www.elastic.co/docs/deploy-manage/deploy/self-managed/install-elasticsearch-docker-basic
### .env 파일 생성
- .env는 aws 관련 접속정보가 정의 된 파일
- setting_aws/env_example 참조하여 생성

### keypair.pem 키 생성
- ec2 접속을 위해 keypair.pem 키를 setting_aws 폴더에 생성
- 파일 권한 수정 : sudo chmod 600 setting_aws/keypair.pem


## [ Single Mode 설치 ]
```commandline
sh setting_aws/setup_server.sh server_1
```

### SSH 접속
```commandline
ssh -i setting_aws/keypair.pem ec2-user@{server_ip}
```

### ElasticSearch 설치
```commandline
# Image Download
sudo docker pull docker.elastic.co/elasticsearch/elasticsearch:8.17.4

# Create a new docker network
sudo docker network create elastic

# Cheak network
sudo docker network ls

# Run Container ( 보안 비활성화 )
sudo docker run --name es01 --net elastic -p 9200:9200 -it -m 1GB \
  -e "discovery.type=single-node" \
  -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
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
sudo docker run --name kib01 --net elastic -p 5601:5601 -it \
  -e "ELASTICSEARCH_HOSTS=http://es01:9200" \
  -e "xpack.security.enabled=false" \
  docker.elastic.co/kibana/kibana:8.17.4
```