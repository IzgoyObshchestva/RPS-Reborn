import aiohttp
from ..core.config import BOT_API_SECRET, API_V1_URL
from .schemas import ApiResponse

async def get_api(url: str, params: dict = {}) -> ApiResponse | str:
    '''
    Функция нужна для отправки GET запроса к API и в нём мы передаём params и headers.
    '''
    async with aiohttp.ClientSession() as session:
        headers={
            "X-Bot-Secret": BOT_API_SECRET
        }
        try:
            async with session.get(f'{API_V1_URL}{url}', headers=headers, params=params) as response:
                result = await response.json()

                res = ApiResponse.from_api(result, response.status)
                
                return res

        except aiohttp.ClientError as e:
            return str(e)
        

async def post_api(url: str, params: dict = {}, json_data: dict = {}) -> ApiResponse | str:
    '''
    Функция нужна для отправки POST запроса к API и в нём мы передаём params, json и headers.
    '''
    async with aiohttp.ClientSession() as session:
        headers={
            "X-Bot-Secret": BOT_API_SECRET
        }
        try:
            async with session.post(
                f'{API_V1_URL}{url}', 
                headers=headers,
                params=params,
                json=json_data
            ) as response:
                result = await response.json()
                
                res = ApiResponse.from_api(result, response.status)

                return res

        except aiohttp.ClientError as e:
            return str(e)



async def patch_api(url: str, params: dict = {}, json_data: dict = {}) -> ApiResponse | str:
    '''
    Функция нужна для отправки PATCH запроса к API и в нём мы передаём params и headers.
    '''
    async with aiohttp.ClientSession() as session:
        headers={
            "X-Bot-Secret": BOT_API_SECRET
        }
        try:
            async with session.patch(
                f'{API_V1_URL}{url}', 
                headers=headers, 
                params=params,
                json=json_data
            ) as response:
                result = await response.json()
                
                res = ApiResponse.from_api(result, response.status)

                return res

        except aiohttp.ClientError as e:
            return str(e)


async def delete_api(url: str, params: dict = {}) -> ApiResponse | str:
    '''
    Функция нужна для отправки DELETE запроса к API и в нём мы передаём params и headers.
    '''
    async with aiohttp.ClientSession() as session:
        headers={
            "X-Bot-Secret": BOT_API_SECRET
        }
        try:
            async with session.delete(f'{API_V1_URL}{url}', headers=headers, params=params) as response:
                result = await response.json()
                
                res = ApiResponse.from_api(result, response.status)

                return res

        except aiohttp.ClientError as e:
            return str(e)