# -- coding: utf-8 --
import os
import json
import requests

API_KEY = ""   # 填写你的 API Key
SECRET_KEY = ""  # 填写你的 Secret Key
#Api Key和Secret Key 请自行去百度千帆大模型平台注册获取
payload = json.dumps({
    "messages": [
        {
            "role": "user",
            "content": "你好"
        },
        {
            "role": "assistant",
            "content": "你好！我是文心一言，有什么可以帮助你的吗？"
        },
        {
            "role": "user",
            "content": "自我介绍一下"
        },
        {
            "role": "assistant",
            "content": "您好，我是文心一言，英文名是ERNIE Bot。我能够与人对话互动，回答问题，协助创作，高效便捷地帮助人们获取信息、知识和灵感。"
        }
    ],
    "disable_search": False,
    "enable_citation": False,
    "stream": True
})

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

save=""

file_list=os.listdir('.')
if "history_message.json" not in file_list:
    with open("history_message.json","w") as f:
        f.write(payload)
else:
    with open("history_message.json","r") as f:
        payload=f.read()
def ask():
    global payload
    global flag
    global save
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()
    
    headers = {
        'Content-Type': 'application/json'
    }
    questions=str(input("请输入\n"))
    if questions=="quit":
        flag=False
        save=input("是否保存聊天记录？(yes/no)\n")    
        return 0
    temp_payload=json.loads(payload)
    temp_payload["messages"].append(
    {
    "role": "user",
    "content": questions
    }
    )
    payload=json.dumps(temp_payload)
    response = requests.request("POST", url, headers=headers, data=payload,stream=True)
    res_txt=""
    for line in response.iter_lines():
        if line == b'':
            continue
        res=line.decode("utf-8")[5::]
        line=res.encode()
        res_dict=json.loads(line)
        print(res_dict["result"],end="")
        res_txt+=res_dict["result"]
    print("\n")
    #json_object=json.loads(response.text)
    temp_payload=json.loads(payload)
    temp_payload["messages"].append(
    {
    "role": "assistant",
    "content": res_txt
    }
    )
    payload=json.dumps(temp_payload)
flag=True
def main():
    global flag
    global payload
    global save
    history_message=input("是否读取历史消息？(yes/no)\n")
    if history_message=="yes":
        with open("history_message.json","r") as f:
            payload=f.read()
    while flag:
        ask()
    if save == "yes":
        with open("history_message.json","w") as f:
            f.write(payload)
if __name__ == '__main__':
    main()