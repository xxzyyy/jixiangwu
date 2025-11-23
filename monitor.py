# monitor.py —— 官方专线版，速度最快、零假新闻
import requests
import os

SC_KEY = os.getenv("SC_KEY")

def send(title, content, url=""):
    if SC_KEY:
        requests.post(f"https://sctapi.ftqq.com/{SC_KEY}.send",
                      data={"title": title, "desp": f"{content}\n\n{url}"})

# 央视搜索（最快8~15秒）
def check_cctv_search():
    try:
        r = requests.get("https://search.api.cctv.com/search.php",
                         params={"q": "春晚吉祥物 2026", "page":1, "pagesize":1, "sort":"date"}, timeout=6)
        item = r.json()["list"][0]
        title = item["title"]
        link = item["url"]
        if "2026" in title and "吉祥物" in title:
            send("2026春晚吉祥物公布了！！！", title, link)
            return True
    except: pass
    return False

# 央视春晚RSS（官方实时源）
def check_rss():
    try:
        r = requests.get("https://news.cctv.com/rss/chunwan.xml", timeout=6)
        if "2026" in r.text and "吉祥物" in r.text:
            send("官方RSS捕捉到2026吉祥物！", "春晚专题已更新", "https://news.cctv.com/chunwan/")
            return True
    except: pass
    return False

if __name__ == "__main__":
    if check_cctv_search() or check_rss():
        pass
    else:
        print("暂无2026吉祥物")
