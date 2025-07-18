import requests
import json
import yaml

def get_answer(message, config):
    authorization = config['Authorization']
    url = config['url']
    model = config['model']
    is_tool = config['is_tool']
    if is_tool:
        tools = config['tools']
        tool_choice = config['tool_choice']

    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json",
        "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>",  # Optional. Site title for rankings on openrouter.ai.
    }
    if is_tool:
        data = json.dumps({
        "model": model,
        "messages": message,
        "tools": tools,
        "tool_choice": tool_choice
        })
    else:
        data = json.dumps({
            "model": model,
            "messages": message,
        })
    proxies={
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
        }

    response = requests.post(
        url=url,
        headers=headers,
        data=data,
        proxies=proxies
    )

    try:
        data = response.json()
    except Exception as e:
        return f"解析 JSON 失败: {e}"

    if "choices" not in data:
        return f"请求返回异常：{data}"

    content = data["choices"][0]["message"]["content"]
    print(data)
    # print("Answer:", content)
    return content

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
        f.close()
    while 1:
        History=[]
        question = input("用户:")
        question = checklen(getText(History, "user", question))
        output = get_answer(question, config)
        getText(History, "assistant", output)