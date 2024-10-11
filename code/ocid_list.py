import aiohttp
import asyncio
from tqdm.asyncio import tqdm  # tqdm의 비동기 버전
import nest_asyncio
import time

# 코랩과 같은 환경에서 중첩된 asyncio 이벤트 루프를 허용하기 위해 적용
nest_asyncio.apply()

# API URL 및 헤더 설정
url = 'https://open.api.nexon.com/maplestory/v1/id?character_name='
headers = {
    'x-nxopen-api-key': 'API_KEY'
}

# 429 에러 처리 및 OCID 요청 함수
async def fetch_ocid(session, character_name, retries=5, backoff_factor=1.0):
    try:
        async with session.get(url + character_name, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('ocid')
            elif response.status == 429:  # Too Many Requests 처리
                if retries > 0:
                    retry_after = int(response.headers.get('Retry-After', backoff_factor))  # 'Retry-After' 헤더 확인
                    wait_time = backoff_factor * (6 - retries)  # 지수적 백오프 (기본은 1초)
                    print(f"Rate limit exceeded for {character_name}. Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)  # 대기 후 재시도
                    return await fetch_ocid(session, character_name, retries - 1, backoff_factor)
                else:
                    print(f"Failed to fetch {character_name} after multiple retries.")
                    return None
            else:
                return None
    except Exception as e:
        print(f"Exception occurred for {character_name}: {str(e)}")
        return None

# 배치 처리를 통해 여러 캐릭터 정보를 동시에 요청하는 함수
async def fetch_all_ocids(character_list, batch_size=500):
    ocid_list = []  # OCID를 저장할 리스트
    async with aiohttp.ClientSession() as session:
        for i in range(0, len(character_list), batch_size):  # 배치로 처리
            batch = character_list[i:i+batch_size]  # 배치 처리
            tasks = [fetch_ocid(session, character_name) for character_name in batch]
            # 비동기 요청을 동시에 처리하면서 tqdm으로 진행 상황을 표시
            for task in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc=f"Fetching batch {i // batch_size + 1}"):
                ocid = await task
                if ocid:
                    ocid_list.append(ocid)
            # API 요청 제한을 피하기 위해 잠시 대기 (필요에 따라 조절 가능)
            time.sleep(1)
    return ocid_list

# 메인 함수
async def main():
    start_time = time.time()

    # 5만 개의 캐릭터를 500개씩 배치로 요청
    ocid_list = await fetch_all_ocids(character_list, batch_size=500)
    
    # 완료 후 처리 시간 출력
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    
    # OCID 리스트 반환 또는 저장
    return ocid_list

# 비동기 함수 실행
ocid_list = asyncio.run(main())
