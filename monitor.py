# monitor.py  —— 2026春晚吉祥物监控
import requests
import os
from datetime import datetime

SC_KEY = os.getenv("SC_KEY")
PUSHPLUS_TOKEN = os.getenv("PUSHPLUS_TOKEN")
WECOM_WEBHOOK = os.getenv("WECOM_WEBHOOK")

HASH_FILE = "/tmp/mascot_hash.txt"
seen = set()
if os.path.exists(HASH_FILE):
    with open(HASH_FILE) as f:
        seen = set(f.read().splitlines())

def send(title, content, url=""):
    desp = f"{content}\n\n[点我查看]({url})" if url else content
    if SC_KEY:
        requests.post(f"https://sctapi.ftqq.com/{SC_KEY}.send", data={"title": title, "desp": desp})
    if PUSHPLUS_TOKEN:
        requests.post("http://www.pushplus.plus/send", json={"token": PUSHPLUS_TOKEN, "title": title, "content": content, "template": "markdown"})
    if WECOM_WEBHOOK:
        requests.post(WECOM_WEBHOOK, json={"msgtype": "markdown", "markdown": {"content": f"**{title}**\n\n{content}"}})

def check():
    try:
        r = requests.get("https://search.api.cctv.com/search.php", params={
            "q": "春晚吉祥物", "page": 1, "pagesize": 3, "sort": "date"
        }, timeout=8)
        if r.status_code == 200:
            item = r.json()["list"][0]
            title = item["title"]
            date = item["date"][:10]
            link = item["url"]
            text = title + (item.get("summary",""))
            h = str(hash(text + date))
            if h not in seen and any(k in text for k in ["2026","吉祥物","公布","亮相"]):
                msg = f"标题：{title}\n时间：{date}\n链接：{link}"
                send("2026春晚吉祥物公布了！！！", msg, link)
                seen.add(h)
                with open(HASH_FILE, "a") as f:
                    f.write(h + "\n")
    except: pass

    try:
        r = requests.get("https://weibo.com/ajax/side/hotSearch", timeout=8)
        if r.status_code == 200:
            for item in r.json()["data"]["hotgov"].get("list", []):
                word = item["word"].replace("#","").strip()
                if "春晚吉祥物" in word:
                    send("微博热搜爆炸！", word, f"https://s.weibo.com/weibo?q={word}")
    except: pass

if __name__ == "__main__":
    check()
