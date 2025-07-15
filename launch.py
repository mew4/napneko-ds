from ncatbot.core import BotClient
import yaml

bot = BotClient()

if __name__ == "__main__":
    with open("./config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        f.close()
    bot_id = config['bt_uin']
    root_id = config['root']
    bot.run(bt_uin=bot_id, root_id=root_id)