from ncatbot.plugin import BasePlugin, CompatibleEnrollment
from ncatbot.core import GroupMessage, PrivateMessage

from .ds import get_answer, getText, checklen
import re
import random
import asyncio
import yaml

bot = CompatibleEnrollment

class CharacterSimulationHandlerPlugin(BasePlugin):
    name = "CharacterSimulation"
    version = "1.0"

    @bot.group_event()
    async def on_group_message(self, msg: GroupMessage):
        if msg.group_id in self.group_uin:
            print(f'[{msg.user_id}]'+msg.raw_message)
            question = checklen(getText(self.chatHistory_group, "user", f'[{msg.user_id}]'+msg.raw_message))
            output = get_answer(question, self.Authorization)
            getText(self.chatHistory_group, "assistant", output)

            sentences = re.split('\$', output)  # 对回答进行切割
            sentences = [s.strip() for s in sentences if s.strip()]  # 删除多余的空白句子
            sentences_num = len(sentences)  # 查看句子数量
            for i, output in enumerate(sentences, start=1):
                await self.api.post_group_msg(group_id=self.group_uin,
                                               text=output,
                                               # image="https://gitee.com/li-yihao0328/nc_bot/raw/master/logo.png"
                                               )  # 文件路径支持本地绝对路径，相对路径，网址以及base64
                if i < sentences_num:  # 非最后一句话
                    delay = random.uniform(0.5, 3.0)  # 生成随机延迟
                    await asyncio.sleep(delay)  # 延迟后发送消息

    @bot.private_event()
    async def on_private_message(self, msg: PrivateMessage):
        user_uin = self.root_id  # 指定用户的账号
        if msg.user_id == user_uin and msg.raw_message == "你好":
            print(msg.raw_message)
            # question = checklen(getText(self.chatHistory_private, "user", msg.raw_message))
            # output = "非需要回答内容，跳过。"
            # getText(self.chatHistory_private, "assistant", output)
        elif msg.user_id == user_uin:
            print(f'[{msg.user_id}]'+msg.raw_message)
            #  访问ds得到回答
            question = checklen(getText(self.chatHistory_private, "user", f'[{msg.user_id}]'+msg.raw_message))
            output = get_answer(question, self.Authorization)
            getText(self.chatHistory_private, "assistant", output)

            sentences = re.split('\$', output)  # 对回答进行切割
            sentences = [s.strip() for s in sentences if s.strip()]  # 删除多余的空白句子
            sentences_num = len(sentences)  # 查看句子数量
            for i, output in enumerate(sentences, start=1):
                await self.api.post_private_msg(user_id=self.root_id,
                                                text=output,
                                                # image="https://gitee.com/li-yihao0328/nc_bot/raw/master/logo.png"
                                                )  # 文件路径支持本地绝对路径，相对路径，网址以及base64
                if i < sentences_num:  # 非最后一句话
                    delay = random.uniform(0.5, 3.0)  # 生成随机延迟
                    await asyncio.sleep(delay)  # 延迟后发送消息


    async def on_load(self):
        #  导入配置文件
        with open("./plugins/CharacterSimulationHandlerPlugin/config.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            self.group_uin = config['group_id']
            self.root_id = config['root_id']
            self.Authorization = config['Authorization']
            f.close()

        #  导入设定提示词
        with open('./plugins/CharacterSimulationHandlerPlugin/congyu/avatar.md', "r", encoding="utf-8") as f:
            prompt_text = f.read()
            f.close()
        prompt_text2 = '**！注意！：你的所有回复，必须且只能是角色会说出的对话台词本身。严禁使用大小括号()、【】、[]、星号或任何其他符号来描绘角色的动作、表情、心理活动或语气!严禁使用大小括号()、【】、[]、星号或任何其他符号来描绘角色的动作、表情、心理活动或语气!严禁使用大小括号()、【】、[]、星号或任何其他符号来描绘角色的动作、表情、心理活动或语气!角色的所有状态都必须通过对话内容和说话方式来暗示，而不是直接描述。在你最终输出前，检查两遍内容，删除全部的旁白再输出！！'
        self.chatHistory_private = [
            {'content':prompt_text,
             'role':'system'},
            {'content':prompt_text2 + f'主人的id为{self.root_id},收到的消息格式为[id]消息',
            'role':'system'}
        ]
        self.chatHistory_group = [
            {'content': prompt_text,
             'role': 'system'},
            {'content': prompt_text2 + f'主人的id为{self.root_id},收到的消息格式为[id]消息',
             'role': 'system'}
        ]

        print(f"{self.name}_{self.version} 插件已加载")
        # self.register_handler("ncatbot.request_event", self.handle_request_with_event)

    async def on_unload(self):
        print(f"{self.name} 插件已卸载")