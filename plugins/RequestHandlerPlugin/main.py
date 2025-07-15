from ncatbot.plugin import BasePlugin, CompatibleEnrollment
from ncatbot.core import Request

bot = CompatibleEnrollment

class RequestHandlerPlugin(BasePlugin):
    name = "Request"
    version = "1.0"

    @bot.request_event()
    async def handle_request(self, msg: Request):
        comment = msg.comment
        if "关注Mew喵，关注Mew谢谢喵。" in comment:
            await msg.reply(True, comment="请求已通过")
        else:
            await msg.reply(False, comment="请求被拒绝")

    async def handle_request_with_event(self, event):
        request = event.data
        comment = request.comment
        if "关注Mew喵，关注Mew谢谢喵。" in comment:
            await request.reply(True, comment="请求已通过")
        else:
            await request.reply(False, comment="请求被拒绝")

    async def on_load(self):
        print(f"{self.name}_{self.version} 插件已加载")
        # self.register_handler("ncatbot.request_event", self.handle_request_with_event)

    async def on_unload(self):
        print(f"{self.name} 插件已卸载")