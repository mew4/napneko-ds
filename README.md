# 基于大模型和 NcatBot 框架的 QQ 角色扮演聊天机器人

本项目基于 [NcatBot](https://github.com/liyihao1110/ncatbot)，这是 [NapCat](https://github.com/NapNeko/NapCatQQ) 的 Python SDK（开发者套件），使用 noebot11 协议。  
当前示例中使用的大模型 API 为 DeepSeekV3，所用 prompt 基于小黑盒大佬 [@KoishiY](https://www.xiaoheihe.cn/app/user/profile/21866880) 提供的丛雨设定，并在此基础上做了微调。

---

## ✨ 已实现功能

1. 角色扮演聊天  
2. 根据情绪发送对应表情包  
3. 群聊中识别不同用户  
4. 聊天记录本地存档  
5. 自动通过指定的好友申请

---

## 🚀 使用指南

> **Python 版本：3.10**

### 一、安装 NapNeko

- [NapNeko 文档](https://napneko.github.io/)  
- [NapNeko 下载链接](https://github.com/NapNeko/NapCatQQ/releases/)

### 二、安装 NcatBot

- [NcatBot 文档与安装指南](https://docs.ncatbot.xyz/guide/onestepi/)

### 三、安装依赖环境

进入项目根目录，执行：

```bash
pip install -r requirements.txt
```
若下载过慢，可自行使用镜像源下载。

### 四、复制插件文件

下载本仓库中的 `plugins` 文件夹及 `launch.py` 文件，并复制到你的项目根目录下。

### 五、配置文件

将 `plugins/CharacterSimulationHandlerPlugin` 中的 `config.example.yaml` 重命名为 `config.yaml`，并按要求填写账号及 API 参数。

### 六、运行

执行：

```bash
python launch.py
```

## 📌 其他说明

1. 大模型 API 请自行在相应大模型官网购买，或参考 [代理平台](https://www.bilibili.com/video/BV1S6KezyEMn) 免费申请试用。  
2. 好友申请功能：请修改 `plugins/RequestHandlerPlugin/main.py` 中的 `“关注Mew喵，关注Mew谢谢喵。”` 字段，如申请人的备注中包含该关键词，则会自动通过好友申请。  
3. 群聊中对不同用户的识别，目前是通过在发送给大模型的消息前附加用户 ID（如 `[114514] 吃了吗`）实现，若大模型的上下文逻辑较弱，可能存在误判。  
4. 大模型生成的对话不可控，**本项目仅供学习与参考使用**，对于大模型产生的任何输出内容，作者概不负责。

---

欢迎 PR 与建议，祝使用愉快！✨


