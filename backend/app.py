from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import difflib
from urllib.parse import urljoin

app = Flask(__name__)
CORS(app)

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
}

BASE_URL = "https://www.scimagojr.com/"

@app.route("/health-check")
def health_check():
    return "OK", 200


@app.route("/rank")
def rank():
    journal = request.args.get("journal", "").strip()
    if not journal:
        return jsonify({"error": "未提供期刊名"})

    try:
        # Step 1: 搜索页面
        search_url = f"{BASE_URL}journalsearch.php?q={requests.utils.quote(journal)}"
        res = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        # Step 2: 匹配最相似期刊链接
        results = soup.select("div.search_results > a")
        if not results:
            return jsonify({"error": "没有搜索到相关期刊"})

        best_score = 0
        best_link = None
        for a in results:
            name_tag = a.find("span", class_="jrnlname")
            name = name_tag.text.strip() if name_tag else a.text.strip()
            score = difflib.SequenceMatcher(None, journal.lower(), name.lower()).ratio()
            if score > best_score:
                best_score = score
                best_link = a

        if not best_link:
            return jsonify({"error": "未匹配到合适期刊"})

        detail_url = urljoin(BASE_URL, best_link["href"])

        # Step 3: 请求详情页并提取数据
        detail_res = requests.get(detail_url, headers=headers)
        detail_soup = BeautifulSoup(detail_res.text, "html.parser")

        def get_text(label):
            h2 = detail_soup.find("h2", text=label)
            if h2:
                p = h2.find_next_sibling("p")
                return p.text.strip() if p else "N/A"
            return "N/A"

        import re
        sjr_h2 = detail_soup.find("h2", string=re.compile(r"SJR\s+\d{4}"))
        sjr = "N/A"
        quartile = "N/A"
        if sjr_h2:
            sjr_p = sjr_h2.find_next_sibling("p")
            if sjr_p:
                sjr = sjr_p.text.strip()
                span = sjr_p.find("span")
                if span:
                    quartile = span.text.strip()

        hindex = get_text("H-Index")
        publisher_tag = detail_soup.find("h2", text="Publisher")
        publisher = publisher_tag.find_next_sibling("p").text.strip() if publisher_tag else "N/A"

        # 获取 subject area 和 category（树形结构）
        subject = []
        try:
            subject_h2 = detail_soup.find("h2", string="Subject Area and Category")
            if subject_h2:
                all_uls = subject_h2.find_all_next("ul", limit=10)  # 只取紧跟的几个 ul
                for ul in all_uls:
                    li = ul.find("li")
                    if not li: continue
                    area_a = li.find("a")
                    if not area_a: continue
                    area = area_a.text.strip()
                    categories = li.select("ul.treecategory li a")
                    if not categories:
                        subject.append(f"{area} / N/A")
                    else:
                        for cat in categories:
                            subject.append(f"{area} / {cat.text.strip()}")
        except Exception as e:
            print("⚠️ 多学科提取失败：", str(e))
            subject = ["N/A"]


        return jsonify({
            "journal": journal,
            "sjr": sjr,
            "quartile": quartile,
            "hindex": hindex,
            "publisher": publisher,
            "subject": subject,
            "sjr_link": detail_url
        })

    except Exception as e:
        return jsonify({"error": f"服务异常：{str(e)}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
