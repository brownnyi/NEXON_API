import aiohttp
import asyncio
import nest_asyncio

# 이미 실행 중인 이벤트 루프에 다시 진입할 수 있도록 설정
nest_asyncio.apply()

headers = {
    'x-nxopen-api-key': 'API_KEY'
}
# 개발단계 API키로는 너무 많은 요청과 제한량이 적어 계속 에러를 발생시킴
url = 'https://open.api.nexon.com/maplestory/v1/ranking/union?date=2024-09-25&world_name=%EC%8A%A4%EC%B9%B4%EB%8B%88%EC%95%84&page='

character_list = []

async def fetch_page(session, page):
    async with session.get(url + str(page), headers=headers) as response:
        return await response.json()

async def get_character_names():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, i) for i in range(1, 2031)]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            for j in response.get('ranking', []):
                character_list.append(j['character_name'])

# 비동기 함수 실행
await get_character_names()
