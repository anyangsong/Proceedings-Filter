import requests
from bs4 import BeautifulSoup

urls = [
    "https://2023.emnlp.org/program/accepted_main_conference/",
    "https://2023.emnlp.org/program/accepted_findings/",
    "https://2023.emnlp.org/program/demo/",
    "https://2024.emnlp.org/program/accepted_main_conference/",
    "https://2024.emnlp.org/program/accepted_findings/",
    "https://2024.emnlp.org/program/demo/",
]

output_paths = [
    "./data/EMNLP-2023-main.txt",
    "./data/EMNLP-2023-findings.txt",
    "./data/EMNLP-2023-demos.txt",
    "./data/EMNLP-2024-main.txt",
    "./data/EMNLP-2024-findings.txt",
    "./data/EMNLP-2024-demos.txt",
]

if __name__ == '__main__':
    # 1. 目标 URL
    for url, output_path in zip(urls, output_paths):
        # 设置 Request Headers，模拟浏览器访问，防止被网站拦截
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }

        print("正在爬取网页数据...")
        response = requests.get(url, headers=headers)

        # 确保请求成功
        if response.status_code == 200:
            response.encoding = 'utf-8'
            html_content = response.text

            # 2. 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(html_content, "html.parser")

            # 3. 提取所有论文题目
            # EMNLP 2023 接收论文页面中，题目通常位于 <p> 标签内的 <strong> 标签中
            titles = []
            p_tags = soup.find_all("p")

            for p in p_tags:
                strong_tag = p.find("strong")
                if strong_tag:
                    title_text = strong_tag.get_text().strip()
                    if title_text:
                        titles.append(title_text)

            # 4. 保存提取的题目到本地 txt 文件
            with open(output_path, "w", encoding="utf-8") as f:
                for title in titles:
                    f.write(title + "\n")

            print(f"成功爬取并提取了 {len(titles)} 篇论文题目，已保存至 '{output_path}'。")

        else:
            print(f"请求失败，HTTP 状态码: {response.status_code}")
