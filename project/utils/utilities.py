import bcrypt
import aiohttp


async def call_api(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return data


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def verify_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password, hashed_password)

