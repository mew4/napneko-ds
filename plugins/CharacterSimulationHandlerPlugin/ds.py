import requests
import json
import yaml

def get_answer(message, Authorization):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": Authorization,
            "Content-Type": "application/json",
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "<YOUR_SITE_NAME>",  # Optional. Site title for rankings on openrouter.ai.
        },
        data=json.dumps({
            "model": "deepseek/deepseek-chat-v3-0324:free",
            "messages": message,
        })
    )

    # for chunks in response.iter_lines():
    #     # 打印返回的每帧内容
    #     # print(chunks)
    #     if (chunks and '[DONE]' not in str(chunks)):
    #         data_org = chunks[6:]
    #
    #         chunk = json.loads(data_org)
    #         text = chunk['choices'][0]['delta']
    #
    #         # 判断最终结果状态并输出
    #         if ('content' in text and '' != text['content']):
    #             content = text["content"]
    #             if (True == isFirstContent):
    #                 isFirstContent = False
    #             print(content, end="")
    #             full_response += content
    print("Response:", response.json()['choices'][0]['message']['content'])
    # print("Usage Stats:", response.json()['usage'])
    return response.json()['choices'][0]['message']['content']

# 管理对话历史，按序编为列表
def getText(text,role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

# 获取对话中的所有角色的content长度
def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

# 判断长度是否超长，当前限制16K tokens
def checklen(text):
    while (getlength(text) > 22000):
        del text[0]
    return text


if __name__ == "__main__":
    with open("./plugins/CharacterSimulationHandlerPlugin/config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        Authorization = config['Authorization']
        f.close()
    while 1:
        History=[]
        question = input("用户:")
        question = checklen(getText(History, "user", question))
        output = get_answer(question, Authorization)
        getText(History, "assistant", output)