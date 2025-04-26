from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from faker import Faker
import datetime
from typing import Dict, Any, Optional
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="랜덤 데이터 생성 API")

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

# 데이터 저장소
last_generated_data: Dict[str, Any] = {
    "timestamp": None,
    "data": None
}

async def generate_data_periodically() -> None:
    """10초마다 새로운 데이터를 생성하는 백그라운드 태스크"""
    while True:
        data: Dict[str, Any] = {
            "name": fake.name(),
            "address": fake.address(),
            "job": fake.job(),
            "company": fake.company(),
            "catch_phrase": fake.catch_phrase(),
            "generated_at": datetime.datetime.now().isoformat()
        }
        
        last_generated_data["timestamp"] = datetime.datetime.now()
        last_generated_data["data"] = data
        
        logger.info(f"새 데이터 생성: {data['name']}")
        await asyncio.sleep(10)  # 10초 간격으로 실행

@app.on_event("startup")
async def startup_event() -> None:
    """앱 시작 시 백그라운드 태스크 시작"""
    asyncio.create_task(generate_data_periodically())
    logger.info("랜덤 데이터 생성 서비스가 시작되었습니다.")

@app.get("/")
async def root() -> Dict[str, str]:
    """서비스 상태 확인 엔드포인트"""
    return {"status": "active", "message": "랜덤 데이터 생성 API가 실행 중입니다."}

@app.get("/data")
async def get_data() -> Dict[str, Any]:
    """가장 최근에 생성된 데이터를 반환"""
    if last_generated_data["data"] is None:
        # 첫 요청 시 즉시 데이터 생성
        data: Dict[str, Any] = {
            "name": fake.name(),
            "address": fake.address(),
            "job": fake.job(),
            "company": fake.company(),
            "catch_phrase": fake.catch_phrase(),
            "generated_at": datetime.datetime.now().isoformat()
        }
        
        last_generated_data["timestamp"] = datetime.datetime.now()
        last_generated_data["data"] = data
    
    # 시간 계산 개선 - 음수 값 방지
    next_update = 0
    if last_generated_data["timestamp"]:
        current_time = datetime.datetime.now()
        time_diff = (current_time - last_generated_data["timestamp"]).total_seconds()
        next_update = max(0, 10 - int(time_diff))
    
    return {
        "data": last_generated_data["data"],
        "next_update_in_seconds": next_update
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 