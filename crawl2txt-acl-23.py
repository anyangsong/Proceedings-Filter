import re
from bs4 import BeautifulSoup
import requests

urls = [
    "https://2023.aclweb.org/program/accepted_main_conference/",
    "https://2023.aclweb.org/program/accepted_findings/",
    "https://2023.aclweb.org/program/accepted_system_demonstration/",
]

output_paths = [
    "./data/ACL-2023-main.txt",
    "./data/ACL-2023-findings.txt",
    "./data/ACL-2023-demos.txt",
]

if __name__ == '__main__':
    # 目标 URL
    for url, output_path in zip(urls, output_paths):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
                " like Gecko) Chrome/115.0.0.0 Safari/537.36"
            )
        }

        # 1. 发起请求并获取 HTML
        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"

        # 2. 解析 HTML
        soup = BeautifulSoup(response.text, "html.parser")

        papers = []

        # 遍历所有包含题目和作者的 <p> 标签
        for p in soup.find_all("p"):
            strong_tag = p.find("strong")
            em_tag = p.find("em")

            if strong_tag and em_tag:
                title = strong_tag.get_text(strip=True)
                authors = em_tag.get_text(strip=True)

                # 清洗换行符和多余空格
                title = re.sub(r"\s+", " ", title)
                authors = re.sub(r"\s+", " ", authors)

                if title:
                    papers.append({"title": title, "authors": authors})

        # 3. 输出提取结果并保存
        print(f"成功提取到 {len(papers)} 篇论文。")

        # 保存为 TXT 文件（每行一篇）
        with open(output_path, "w", encoding="utf-8") as f:
            for item in papers:
                # f.write(f"{item['title']} | Authors: {item['authors']}\n")
                f.write(f"{item['title']}\n")
