import requests

data = {
    "host": "www.pokemongammaemeraldgame.com",
    "key": "7131a90bb91549d1b7a242c187b40516",
    "keyLocation": "https://pokemongammaemeraldgame.com/7131a90bb91549d1b7a242c187b40516.txt",
    "urlList": [
       "https://pokemongammaemeraldgame.com/stonecraft"

    ]
}


response = requests.post(
    "https://api.indexnow.org/IndexNow",
    json=data,
    headers={"Content-Type": "application/json; charset=utf-8"}
)

print("状态码：", response.status_code)
print("返回内容：", response.text)