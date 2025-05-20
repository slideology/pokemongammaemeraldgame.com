import requests
import xml.etree.ElementTree as ET
import os

SITEMAP_URL = "https://pokemongammaemeraldgame.com/sitemap.xml"  # 替换为你自己的 sitemap 地址
KEY = "1097d5a190b24fcb941eacf89b4911b0"  # 替换为你的 IndexNow key
KEY_LOCATION = "https://pokemongammaemeraldgame.com/你的key.txt"  # 替换为你的 key 文件地址
HOST = "www.pokemongammaemeraldgame.com"  # 替换为你的域名
HISTORY_FILE = "last_sitemap_urls.txt"

def fetch_sitemap_urls():
    resp = requests.get(SITEMAP_URL)
    urls = []
    if resp.status_code == 200:
        root = ET.fromstring(resp.content)
        for url in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
            loc = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
            if loc is not None:
                urls.append(loc.text.strip())
    return urls

def load_last_urls():
    if not os.path.exists(HISTORY_FILE):
        return set()
    with open(HISTORY_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip())

def save_current_urls(urls):
    with open(HISTORY_FILE, "w") as f:
        for url in urls:
            f.write(url + "\n")

def push_to_indexnow(new_urls):
    if not new_urls:
        print("没有新增页面需要推送。")
        return
    data = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": list(new_urls)
    }
    resp = requests.post(
        "https://api.indexnow.org/IndexNow",
        json=data,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )
    print("推送状态码：", resp.status_code)
    print("返回内容：", resp.text)

if __name__ == "__main__":
    current_urls = set(fetch_sitemap_urls())
    last_urls = load_last_urls()
    new_urls = current_urls - last_urls
    push_to_indexnow(new_urls)
    save_current_urls(current_urls)