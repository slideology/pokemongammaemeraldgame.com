import requests

data = {
    "host": "www.pokemongammaemeraldgame.com",
    "key": "1097d5a190b24fcb941eacf89b4911b0",
    "keyLocation": "https://pokemongammaemeraldgame.com/1097d5a190b24fcb941eacf89b4911b0.txt",
    "urlList": [
        "https://pokemongammaemeraldgame.com/terradome"
    ]
}

response = requests.post(
    "https://api.indexnow.org/IndexNow",
    json=data,
    headers={"Content-Type": "application/json; charset=utf-8"}
)

print("状态码：", response.status_code)
print("返回内容：", response.text)