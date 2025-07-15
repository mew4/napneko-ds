from ncatbot.core import BotClient
from utils.NCatBot import handle_request_async
import os
import asyncio

async def NcatBot(bot_id, root_id):
    bot = BotClient()
    bot.add_request_event_handler(handle_request_async)  # 好友请求模块
    api = bot.run_blocking(bt_uin=bot_id, root=root_id)  # bt_uin 为 bot 的 QQ 号（一般填你的小号）, root 为 机器人管理员的 QQ 号（一般填你的大号）
    await api.post_private_msg(root_id, "Hello NcatBot~喵")  # 第一个参数表示发送消息的对象（QQ 号）
    # await api.post_group_msg(test_group, "Hello NcatBot~meow")  # 第一个参数表示发送消息的对象 (群号)z`

    await asyncio.Future()  # 永久挂载，防止程序退出

bot_id = os.getenv('bot_id')
root_id = os.getenv('root_id')
asyncio.run(NcatBot(bot_id, root_id))

