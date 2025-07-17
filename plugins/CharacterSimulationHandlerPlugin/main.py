from ncatbot.plugin import BasePlugin, CompatibleEnrollment
from ncatbot.core import GroupMessage, PrivateMessage

from .ds import get_answer, getText, checklen
from .fuction_calling.send_emojis import send_emojis
from .history_manager import save_history, load_history
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
        user_uin = self.root_id
        user_key = msg.user_id
        group_key = msg.group_id
        message = [item['data']['text'] for item in msg.message if item['type'] == 'text']
        at = [item['data']['qq'] for item in msg.message if item['type'] == 'at']
        if group_key in self.group_uin and len(message) != 0:
            current_group_history = self._get_or_create_history(self.chatHistory_group, str(group_key))  # 获取历史聊天记录
            print(f'[{user_key}]{message[0]}')
            question = checklen(getText(current_group_history, "user", f'[{user_key}]{message[0]}'))
            if msg.message[0]['type'] == 'at' and int(at[0]) == msg.self_id:
                print(question)
                output = get_answer(question, self.plugin_config)
                print(output)
                getText(current_group_history, "assistant", output)

                sentences = re.split('\$', output)  # 对回答进行切割
                sentences = [s.strip() for s in sentences if s.strip()]  # 删除多余的空白句子

                for i, sentence in enumerate(sentences, start=1):
                    is_last_sentence = (i == len(sentences))
                    emotion_match = re.search(r'\[(.*?)\]', sentence)

                    if is_last_sentence and emotion_match:
                        print(f'检测到情绪标签: {sentence}')
                        if random.random() < self.plugin_config['frequency']:
                            print(f'发送对应情绪图片')
                            emotion = emotion_match.group(1)
                            try:
                                await send_emojis(emotion, self.api, group_key, 'group')
                            except Exception as e:
                                print(f"发送表情包时出错: {e}")
                        else:
                            print(f'不发送对应情绪图片')
                        continue

                    await self.api.post_group_msg(group_id=group_key,text=sentence)

                    if i < len(sentences):
                        await asyncio.sleep(random.uniform(1, 3.0))
            save_history(self.history_path, self.chatHistory_private, self.chatHistory_group)  # 更新本地历史记录

    @bot.private_event()
    async def on_private_message(self, msg: PrivateMessage):
        user_uin = self.root_id  # 指定用户的账号
        user_key = msg.user_id
        if user_key == user_uin and msg.raw_message == "你好":
            await self.api.post_private_msg(user_id=self.root_id, text='你好喵')
            print(msg.raw_message)

        elif user_key == user_uin:
            current_private_history = self._get_or_create_history(self.chatHistory_private, str(user_key))  # 获取历史聊天记录
            print(f'[{user_key}]'+msg.raw_message)

            # 1. 如果有旧计时器，先取消
            if user_key in self.private_timers:
                self.private_timers[user_key].cancel()

            # 2. 存入新消息到缓冲区
            if user_key not in self.private_message_buffers:
                self.private_message_buffers[user_key] = []
            self.private_message_buffers[user_key].append(msg.raw_message)

            # 3. 启动新计时器
            loop = asyncio.get_running_loop()
            self.private_timers[user_key] = loop.call_later(
                self.reply_delay,  # 从config加载的延迟时间
                lambda: asyncio.create_task(self._process_and_reply_private(user_key, current_private_history))
            )

    async def _process_and_reply_private(self, user_key, current_private_history):
        print(f"用户 {user_key} 的私聊消息等待时间结束，开始处理...")
        buffered_messages = self.private_message_buffers.pop(user_key, [])
        self.private_timers.pop(user_key, None)
        if not buffered_messages: return

        full_message = "\n".join(buffered_messages)
        print(f"合并后的私聊消息: {full_message}")

        formatted_message = f'[{user_key}]{full_message}'
        question = checklen(getText(current_private_history, "user", formatted_message))
        output = get_answer(question, self.plugin_config)
        getText(current_private_history, "assistant", output)

        # print("AI Raw Output:", output)
        sentences = re.split('\$', output)
        sentences = [s.strip() for s in sentences if s.strip()]

        for i, sentence in enumerate(sentences, start=1):
            is_last_sentence = (i == len(sentences))
            emotion_match = re.search(r'\[(.*?)\]', sentence)

            if is_last_sentence and emotion_match:
                print(f'检测到情绪标签: {sentence}')
                if random.random() < self.plugin_config['frequency']:
                    print(f'发送对应情绪图片')
                    emotion = emotion_match.group(1)
                    try:
                        await send_emojis(emotion, self.api, self.root_id, 'private')
                    except Exception as e:
                        print(f"发送表情包时出错: {e}")
                else:
                    print(f'不发送对应情绪图片')
                continue

            await self.api.post_private_msg(user_id=self.root_id, text=sentence)

            if i < len(sentences):
                await asyncio.sleep(random.uniform(1, 3.0))
        save_history(self.history_path, self.chatHistory_private, self.chatHistory_group)  # 更新本地历史记录

    def _get_or_create_history(self, history_dict, key):
        """
        一个辅助函数，用于获取或创建指定ID的聊天记录列表。
        """
        if key not in history_dict:
            # 如果是新的会话，用系统提示词初始化它
            history_dict[key] = self.system_prompt.copy()
        return history_dict[key]

    async def on_load(self):
        #  导入配置文件
        with open("./plugins/CharacterSimulationHandlerPlugin/config.yaml", "r", encoding="utf-8") as f:
            self.plugin_config = yaml.safe_load(f)
            self.root_id = self.plugin_config['root_id']
            self.group_uin = self.plugin_config['group_id']
            self.reply_delay = self.plugin_config['reply_delay']
            self.history_path = self.plugin_config['history_file_path']
            f.close()

        #  导入设定提示词
        with open('./plugins/CharacterSimulationHandlerPlugin/congyu/avatar.md', "r", encoding="utf-8") as f:
            prompt_text = f.read()
            f.close()
        prompt_text2 = f'**！注意！：收到的消息格式为:[用户id]消息内容，例如[114514]早上好。不同用户id代表不同的人，在一次聊天中会出现多个不同id的人，注意分辨。你的主人的id为且仅为{self.root_id}，其余皆为你主人的“朋友”,你的所有回复，必须且只能是角色会说出的对话台词本身，不能透露任何关于现实的信息，例如id、人设、ai等等。严禁使用大小括号()、【】、[]、星号或任何其他符号来描绘角色的动作、表情、心理活动或语气!严禁使用大小括号()、【】、[]、星号或任何其他符号来描绘角色的动作、表情、心理活动或语气!严禁使用大小括号()、【】、[]、星号或任何其他符号来描绘角色的动作、表情、心理活动或语气!角色的所有状态都必须通过对话内容和说话方式来暗示，而不是直接描述。在你最终输出前，检查两遍内容，删除全部的旁白再输出！！'

        self.system_prompt = [
            {'content': prompt_text, 'role': 'system'},
            {'content': prompt_text2, 'role': 'system'},
        ]

        self.chatHistory_private, self.chatHistory_group = load_history(self.history_path)

        #  私聊状态管理的字典
        self.private_timers = {} # 键是 user_id, 值是 TimerHandle
        self.private_message_buffers = {} # 键是 user_id, 值是消息列表
        self.group_timers = {}
        self.group_message_buffers = {}

        print(f"{self.name}_{self.version} 插件已加载")
        # self.register_handler("ncatbot.request_event", self.handle_request_with_event)



    async def on_unload(self):
        print(f"{self.name} 插件已卸载")