# 基于大模型和NcatBot框架的qq角色扮演聊天机器人
[NcatBot](https://github.com/liyihao1110/ncatbot)是[NapCat](https://github.com/NapNeko/NapCatQQ)的Python SDK(开发者套件)，基于noebot11协议。本库中测试使用的大模型api为DeepSeekV3，使用的prompt基于小黑盒大佬[@KoishiY](https://www.xiaoheihe.cn/app/user/profile/21866880)提供的丛雨设定，并在此基础上做了微调。

目前已实现的功能：  
1.角色扮演聊天。  
2.发送对应情绪的表情包。  
3.群聊中对不同用户的识别。  
4.聊天记录本地存档。  
5.自动通过指定的好友请求。  

## 使用指南（本仓库所使用的python版本为3.10）
### 一、安装NapNeko
NapNeko文档(https://napneko.github.io/)  
NapNeko下载链接(https://github.com/NapNeko/NapCatQQ/releases/)

### 二、安装NcatBot
NcatBot文档以及安装方式(https://docs.ncatbot.xyz/guide/onestepi/)

### 三、安装依赖环境
进入你项目的根目录，执行  
pip install -r requirements.txt

### 四、复制插件
下载本仓库中的plugins文件夹以及launch.py文件，复制到你项目的根目录中。

### 五、修改config文件
将plugins.CharacterSimulationHandlerPlugin中的config.example.yaml文件修改为config.yaml，并按要求填写里面的参数（账号设置和api设置）。

### 六、运行
运行launch.py

## 其他说明
1.大模型api请自行上相应大模型官网购买或去其他[代理平台](https://www.bilibili.com/video/BV1S6KezyEMn/?spm_id_from=333.1391.0.0&vd_source=87ba1a1eb5e612f2b0e413f1519ae66a)白嫖。  
2.好友申请功能请修改.plugins/RequestHandlerPlugin/main.py中的“关注Mew喵，关注Mew谢谢喵。”字段，如果申请人的备注中含有该关键词，则好友申请自动通过。  
3.目前同个群聊识别不同用户是通过发给大模型的消息前附上id实现，如[114514]吃了吗，这种方式可能对大模型的逻辑判别能力有一定要求。  
4.大模型的输出内容不可控，本仓库仅作为学习、参考使用，大模型的所有言论本仓库概不负责。

