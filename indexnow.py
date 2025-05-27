import requests

data = {
    "host": "www.pokemongammaemeraldgame.com",
    "key": "7131a90bb91549d1b7a242c187b40516",
    "keyLocation": "https://pokemongammaemeraldgame.com/7131a90bb91549d1b7a242c187b40516.txt",
    "urlList": [
        "https://pokemongammaemeraldgame.com/terradome",
        "https://pokemongammaemeraldgame.com/white-horizon",
        "https://pokemongammaemeraldgame.com/bombardino-crocodilo-clicker",
        "https://pokemongammaemeraldgame.com/tung-tung-sahur-obby-challenge",
        "https://pokemongammaemeraldgame.com/tung-sahur-clicker",
        "https://pokemongammaemeraldgame.com/stimulation-clicker",
        "https://pokemongammaemeraldgame.com/unchill-guy-clicker",
        "https://pokemongammaemeraldgame.com/the-ultimate-clicker-squad"

    ]
}


response = requests.post(
    "https://api.indexnow.org/IndexNow",
    json=data,
    headers={"Content-Type": "application/json; charset=utf-8"}
)

print("状态码：", response.status_code)
print("返回内容：", response.text)