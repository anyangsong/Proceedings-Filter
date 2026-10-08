from bs4 import BeautifulSoup
import requests

urls = [
    "https://lrec-coling-2024.org/list-of-accepted-papers/",
]

output_paths = [
    "./data/COLING-2024.txt",
]


def fetch_and_save_paper_titles(url, output_txt_path):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }

    print(f"正在爬取网页: {url} ...")
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"网页抓取失败: {e}")
        return

    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    titles = []

    # 遍历页面中的所有表格行 <tr>
    rows = soup.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        # 该页面表格结构中：第1列是序号/ID，第2列是作者，第3列是论文题目
        if len(cols) >= 3:
            title = cols[2].get_text(strip=True)
            if title:
                titles.append(title)
        # 兼容只有2列的特殊情况（第1列是ID，第2列是题目）
        elif len(cols) == 2:
            title = cols[1].get_text(strip=True)
            if title:
                titles.append(title)

    # 写入文件，仅保存题目，一行一个
    with open(output_txt_path, "w", encoding="utf-8") as f:
        for title in titles:
            f.write(f"{title}\n")

    print(f"提取完成！共保存 {len(titles)} 个论文题目到 {output_txt_path}")


if __name__ == "__main__":
    for url, output_path in zip(urls, output_paths):
        fetch_and_save_paper_titles(url, output_path)
