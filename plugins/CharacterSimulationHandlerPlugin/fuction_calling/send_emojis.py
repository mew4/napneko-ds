from ncatbot.plugin import CompatibleEnrollment
import os, random

# bot = CompatibleEnrollment

async def send_emojis(emotion, bot, id, private_or_group):
    folder = f"./plugins/CharacterSimulationHandlerPlugin/congyu/emojis/{emotion}"  # 获取表情包路径
    files = os.listdir(folder)
    images = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]  # 筛选图片文件
    selected_image = random.choice(images)  # 随机挑选一张表情包
    full_path = os.path.join(folder, selected_image)
    if private_or_group == 'private':
        await bot.post_private_msg(user_id=id, image=full_path)
    elif private_or_group == 'group':
        await bot.post_group_msg(group_id=id, image=full_path)
    else:
        print(f"参数private_or_group设置错误，参数类型应为string，值只能为'private'或'group',而非{private_or_group}")