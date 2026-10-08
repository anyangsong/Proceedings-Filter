import requests
from bs4 import BeautifulSoup

urls = [
    "https://2024.eacl.org/program/main-accepted/",
    "https://2024.eacl.org/program/findings-accepted/",
    "https://2026.eacl.org/program/main-accepted/",
    "https://2026.eacl.org/program/findings-accepted/",
]

output_paths = [
    "./data/EACL-2024-main.txt",
    "./data/EACL-2024-findings.txt",
    "./data/EACL-2026-main.txt",
    "./data/EACL-2026-findings.txt",
]


def scrape_eacl_titles(url, output_file):
    # 设置 User-Agent 请求头，模拟浏览器访问
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    print(f"正在爬取页面: {url} ...")

    try:
        # 1. 爬取页面内容
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        response.encoding = "utf-8"
        print("页面爬取成功，开始解析结构...")

        # 2. 使用 BeautifulSoup 解析 HTML 内容
        soup = BeautifulSoup(response.text, "html.parser")

        # 3. 提取论文题目
        # 在 EACL 2024 官方页面中，论文题目置于 <b> 或 <strong> 标签内，或者位于列表项 (<li>) 中
        titles = []

        # 方法一：遍历所有 <b> 和 <strong> 标签提取标题
        for tag in soup.find_all(["b", "strong"]):
            title = tag.get_text(strip=True)
            # 过滤不需要的非标题粗体文字（如导航栏、脚标等）
            if title and len(title) > 5 and not title.lower().startswith("follow"):
                titles.append(title)

        # 如果没有通过 b/strong 匹配到，备用方案：按列表项 <li> 提取
        if not titles:
            for li in soup.find_all("li"):
                text = li.get_text(strip=True)
                if text:
                    titles.append(text)

        # 去重并保持原有顺序
        unique_titles = list(dict.fromkeys(titles))

        # 4. 保存论文题目到本地文件
        with open(output_file, "w", encoding="utf-8") as f:
            for idx, title in enumerate(unique_titles, 1):
                f.write(f"{title}\n")

        print(
            f"分析完成！共提取到 {len(unique_titles)} 篇论文题目，已保存至 '{output_file}'。"
        )

    except requests.RequestException as e:
        print(f"网络请求失败: {e}")
    except Exception as e:
        print(f"解析发生错误: {e}")


if __name__ == "__main__":
    for url, output_path in zip(urls, output_paths):
        scrape_eacl_titles(url, output_path)
