import requests

data = {
    "host": "www.pokemongammaemeraldgame.com",
    "key": "7131a90bb91549d1b7a242c187b40516",
    "keyLocation": "https://pokemongammaemeraldgame.com/7131a90bb91549d1b7a242c187b40516.txt",
    "urlList": [
       "https://pokemongammaemeraldgame.com/tung-tung-sahur-obby-challenge",
  "https://pokemongammaemeraldgame.com/terradome",
  "https://pokemongammaemeraldgame.com/wacky-flip",
  "https://pokemongammaemeraldgame.com/dreamy-room",
  "https://pokemongammaemeraldgame.com/game",
  "https://pokemongammaemeraldgame.com/italian-brainrot-2048",
  "https://pokemongammaemeraldgame.com/",
  "https://pokemongammaemeraldgame.com/contact",
  "https://pokemongammaemeraldgame.com/lemon-clicker",
  "https://pokemongammaemeraldgame.com/italian-brainrot-playground",
  "https://pokemongammaemeraldgame.com/italian-brainrot-clicker-2",
  "https://pokemongammaemeraldgame.com/speed-stars",
  "https://pokemongammaemeraldgame.com/multi-theme-clicker-game",
  "https://pokemongammaemeraldgame.com/tung-sahur-clicker",
  "https://pokemongammaemeraldgame.com/about",
  "https://pokemongammaemeraldgame.com/merge-fellas",
  "https://pokemongammaemeraldgame.com/poor-bunny",
  "https://pokemongammaemeraldgame.com/white-horizon",
  "https://pokemongammaemeraldgame.com/merge-fellas-brainrot",
  "https://pokemongammaemeraldgame.com/privacy-policy",
  "https://pokemongammaemeraldgame.com/crazy-mouse-battle",
  "https://pokemongammaemeraldgame.com/bombardino-crocodilo-clicker",
  "https://pokemongammaemeraldgame.com/terms-of-service",
  "https://pokemongammaemeraldgame.com/faq",
  "https://pokemongammaemeraldgame.com/drive-beyond-horizons"

    ]
}


response = requests.post(
    "https://api.indexnow.org/IndexNow",
    json=data,
    headers={"Content-Type": "application/json; charset=utf-8"}
)

print("状态码：", response.status_code)
print("返回内容：", response.text)