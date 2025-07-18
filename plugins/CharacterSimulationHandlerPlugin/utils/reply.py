import asyncio
import random

def reply(self, group_key, msg):
    # 1. 回复触发器
    should_reply = False
    trigger_reason = ""

    # 2. 初始化或更新群聊活动状态
    if group_key not in self.group_activity:
        self.group_activity[group_key] = {'message_count': 0, 'last_bot_reply_time': 0}
    self.group_activity[group_key]['message_count'] += 1

    # 3. 提取消息文本和是否@了自己
    message_text = "".join(item['data']['text'] for item in msg.message if item['type'] == 'text').strip()
    is_at_me = any(int(item['data']['qq']) == msg.self_id for item in msg.message if item['type'] == 'at')
    if not message_text:  # 如果消息为空，则直接忽略
        return should_reply

    # --- 条件一：被明确 @ ---
    if is_at_me:
        should_reply = True
        trigger_reason = "被明确 @"

    # --- 条件二：关键词触发 (如果没有被@) ---
    elif self.keywords and any(keyword in message_text for keyword in self.keywords):
        should_reply = True
        trigger_reason = f"检测到关键词: {next((k for k in self.keywords if k in message_text), '')}"

    # --- 条件三：概率性主动搭话 (如果前两者都未满足) ---
    elif self.proactive_config.get('enable_interjection', False):
        activity = self.group_activity[group_key]
        config = self.proactive_config

        # 检查是否满足所有条件
        is_threshold_met = activity['message_count'] >= config.get('message_threshold', 15)
        is_cooldown_over = (asyncio.get_running_loop().time() - activity['last_bot_reply_time']) >= config.get(
            'cooldown_seconds', 1800)

        if is_threshold_met and is_cooldown_over:
            if random.random() < config.get('interjection_probability', 0.15):
                should_reply = True
                trigger_reason = "概率性主动搭话"
                # 因为是主动搭话，所以重置消息计数器
                self.group_activity[group_key]['message_count'] = 0
    if should_reply:
        print(f"决定在群 {group_key} 中回复，原因: {trigger_reason}")
        self.group_activity[group_key]['last_bot_reply_time'] = asyncio.get_running_loop().time()
    return should_reply