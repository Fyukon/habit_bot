import logging

import aiohttp

logger = logging.getLogger("aiohttp")
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Добавляем вывод в файл
file_handler = logging.FileHandler('dog_api.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


async def get_dog_url():
    async with aiohttp.ClientSession() as session:

        try:
            async with session.get(r"https://dog.ceo/api/breeds/image/random") as response:
                data = await response.json()
                return data['message']
        except Exception as e:
            logger.exception(e)
            return None
