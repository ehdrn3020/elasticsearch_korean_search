from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from faker import Faker
import datetime
from typing import Dict, Any, Optional
import logging
from elasticsearch import AsyncElasticsearch
import json
import os
import re  # 정규표현식 모듈 추가

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="한글 데이터 생성 API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 한국어 faker 인스턴스 생성
fake = Faker('ko_KR')

# Elasticsearch 클라이언트
es_client = None
ES_INDEX_NAME = "korean_data"

# Elasticsearch 인덱스 설정 - 외부 JSON 파일에서 로드
def load_index_settings() -> Dict[str, Any]:
    """외부 JSON 파일에서 인덱스 설정을 로드하는 함수"""
    # Docker 컨테이너 내부 경로를 직접 지정
    settings_path = '/app/elastic_indexs/index_setting.json'
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"인덱스 설정 파일 로드 중 오류 발생: {str(e)}")
        raise

# 인덱스 설정 로드
INDEX_SETTINGS = load_index_settings()

# 주소에서 시/도와 구/군까지 추출하는 함수
def extract_address_district(address: str) -> str:
    """
    주소에서 시/도와 구/군까지 추출하는 함수
    예: '서울특별시 강남구 삼성동 123-45' -> '서울특별시 강남구'
    """
    # 시/도 + 구/군 패턴 매칭
    pattern = r'^([가-힣]+(?:특별시|광역시|특별자치시|특별자치도|도))\s+([가-힣]+(?:시|군|구))'
    match = re.search(pattern, address)
    
    if match:
        # 시/도와 구/군 모두 매칭된 경우
        return f"{match.group(1)} {match.group(2)}"
    else:
        # 시/도만 매칭 시도
        pattern_city = r'^([가-힣]+(?:특별시|광역시|특별자치시|특별자치도|도))'
        match_city = re.search(pattern_city, address)
        if match_city:
            return match_city.group(1)
        else:
            return "기타"  # 매칭되지 않는 경우

async def setup_elasticsearch() -> None:
    """Elasticsearch 연결 및 인덱스 설정"""
    global es_client
    # Elasticsearch 클라이언트 초기화 - Docker Compose에서 설정한 서비스명 사용
    es_client = AsyncElasticsearch(hosts=["http://es01:9200"])
    # 인덱스 존재 여부 확인
    if not await es_client.indices.exists(index=ES_INDEX_NAME):
        # 인덱스 생성 및 매핑 설정
        logger.info(f"인덱스 '{ES_INDEX_NAME}' 생성 중...")
        await es_client.indices.create(index=ES_INDEX_NAME, body=INDEX_SETTINGS)
        logger.info(f"인덱스 '{ES_INDEX_NAME}' 생성 완료")
    else:
        logger.info(f"인덱스 '{ES_INDEX_NAME}'가 이미 존재합니다")

async def generate_data_periodically() -> None:
    """10초마다 새로운 데이터를 생성하고 Elasticsearch에 저장하는 백그라운드 태스크"""
    while True:
        current_time = datetime.datetime.now()
        
        # 주소 생성
        address = fake.address()        
        address_district = extract_address_district(address)
        
        data: Dict[str, Any] = {
            "name": fake.name(),
            "address": address,
            "address_district": address_district,  # 추출된 시/도와 구/군 정보 저장
            "job": fake.job(),
            "company": fake.company(),
            "catch_phrase": fake.catch_phrase(),
            "generated_at": current_time.isoformat(),
            "timestamp": current_time
        }
   
        # Elasticsearch에 데이터 저장
        if es_client:
            try:
                response = await es_client.index(
                    index=ES_INDEX_NAME,
                    document=data,
                    refresh=True  # 즉시 검색 가능하도록 설정
                )
                doc_id = response.get("_id")
                logger.info(f"ES에 데이터 저장 완료: ID={doc_id}, 이름={data['name']}")
            except Exception as e:
                logger.error(f"ES 저장 중 오류 발생: {str(e)}")
        
        logger.info(f"새 데이터 생성: {data['name']}")
        await asyncio.sleep(10)  # 10초 간격으로 실행

@app.on_event("startup")
async def startup_event() -> None:
    """앱 시작 시 Elasticsearch 설정 및 백그라운드 태스크 시작"""
    try:
        await setup_elasticsearch()
        asyncio.create_task(generate_data_periodically())
        logger.info("랜덤 데이터 생성 서비스가 시작되었습니다.")
    except Exception as e:
        logger.error(f"시작 중 오류 발생: {str(e)}")

@app.on_event("shutdown")
async def shutdown_event() -> None:
    """앱 종료 시 Elasticsearch 연결 종료"""
    if es_client:
        await es_client.close()
        logger.info("Elasticsearch 연결 종료")

@app.get("/")
async def root() -> Dict[str, str]:
    """서비스 상태 확인 엔드포인트"""
    return {"status": "active", "message": "한글 데이터 생성 API가 실행 중입니다."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 