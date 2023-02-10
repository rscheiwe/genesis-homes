import bcrypt
import http3

import aiohttp


async def call_api(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return data
            # do something with data


# async def call_api(url: str):
#     client = http3.AsyncClient()
#     r = await client.get(url)
#     return r.json()
#

def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def verify_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password, hashed_password)


# def run_seed_data():
#     with db_context() as session:
#
#         db_property = models.Property(title="HI", description="HELLO")
#         session.add(db_property)
#         session.commit()
#         session.refresh(db_property)
#
#     return db_property
