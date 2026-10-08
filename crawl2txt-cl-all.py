import requests
from bs4 import BeautifulSoup

urls = [
    "https://2024.naacl.org/program/accepted_papers/",
    "https://2024.naacl.org/program/accepted_papers_demo/",
    "https://2024.aclweb.org/program/main_conference_papers/",
    "https://2024.aclweb.org/program/finding_papers/",
    "https://2024.aclweb.org/program/demo_papers/",
    "https://coling2025.org/program/main_conference_papers/",
    "https://coling2025.org/program/system_demonstration_papers/",
    "https://2025.naacl.org/program/accepted_papers/",
    "https://2025.aclweb.org/program/main_papers/",
    "https://2025.aclweb.org/program/find_papers/",
    "https://2025.aclweb.org/program/demo_papers/",
    "https://2025.emnlp.org/program/main_papers/",
    "https://2025.emnlp.org/program/find_papers/",
    "https://2025.emnlp.org/program/demo_papers/",
    "https://2026.aclweb.org/program/accepted_papers/",
    "https://2026.aclweb.org/program/findings/",
    "https://2026.aclweb.org/program/demo/",
]

output_paths = [
    "./data/NAACL-2024.txt",
    "./data/NAACL-2024-demos.txt",
    "./data/ACL-2024-main.txt",
    "./data/ACL-2024-findings.txt",
    "./data/ACL-2024-demos.txt",
    "./data/COLING-2025.txt",
    "./data/COLING-2025-demos.txt",
    "./data/NAACL-2025.txt",
    "./data/ACL-2025-main.txt",
    "./data/ACL-2025-findings.txt",
    "./data/ACL-2025-demos.txt",
    "./data/EMNLP-2025-main.txt",
    "./data/EMNLP-2025-findings.txt",
    "./data/EMNLP-2025-demos.txt",
    "./data/ACL-2026-main.txt",
    "./data/ACL-2026-findings.txt",
    "./data/ACL-2026-demos.txt",
]


def scrape_and_extract_titles(url, output_path):
    # 设置请求头（User-Agent），防止被网站拦截
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        # 1. 自动请求网页内容
        print(f"正在抓取页面: {url} ...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # 检查 HTTP 响应状态码
        response.encoding = 'utf-8'

        # 2. 解析 HTML 页面内容
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = []

        # 3. 提取论文题目：页面结构中论文题目位于 <li> 列表项内的 <strong> 标签中
        list_items = soup.find_all('li')
        for li in list_items:
            strong_tag = li.find('strong')
            if strong_tag:
                title = strong_tag.get_text(strip=True)
                if title:
                    titles.append(title)

        # 4. 保存提取出的论文题目到 TXT 文件（一行一个）
        with open(output_path, 'w', encoding='utf-8') as f:
            for title in titles:
                f.write(title + '\n')

        print(f"解析成功！共提取到 {len(titles)} 篇论文题目，已保存至文件：{output_path}")

    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


# ==================== 执行脚本 ====================
if __name__ == '__main__':
    for url, output_path in zip(urls, output_paths):
        scrape_and_extract_titles(url, output_path)
