<<<<<<< HEAD
import orm,asyncio
from models import User,Blog,Comment

async def test(loop):
    await orm.create_pool(loop,user='root',password='123456',db='awesome')
    u = User(name='Test1',email='test1@example.com',passwd='1234567890',image='about:blank')
    await u.save()


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait([test(loop)]))
=======
import orm,asyncio
from models import User,Blog,Comment

async def test(loop):
    await orm.create_pool(loop,user='root',password='123456',db='awesome')
    u = User(name='Test1',email='test1@example.com',passwd='1234567890',image='about:blank')
    await u.save()


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait([test(loop)]))
>>>>>>> 79d6a477cdaf6ace01063f6a4412dd7d8bb10d22
loop.run_forever()