import mysqlPy,asyncio
from models import entity

async def test(loop):
    await mysqlPy.create_pool(loop,user='bm',password='bm!@#123',db='dev')
    u = entity(data='Test1')
    await u.save()


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait([test(loop)]))
loop.run_forever()