import time
import requests
from bs4 import BeautifulSoup

s_prefix = "https://ojs.aaai.org/index.php/AAAI/issue/view/"

starts = [
    576,  # 24
    624,  # 25
    683,  # 26
]

lens = [
    18,  # 24
    25,  # 25
    25,  # 26
]

output_paths = [
    "./data/AAAI-2024.txt",
    "./data/AAAI-2025.txt",
    "./data/AAAI-2026.txt",
]


def fetch_titles_from_url(url, session):
    """
    爬取单个分卷页面并提取论文题目列表（不带序号）
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = session.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取论文标题的选择器
        title_elements = soup.select('.obj_article_summary .title a, .article-summary .title a, h3.title a')
        if not title_elements:
            title_elements = soup.find_all('h3', class_='title')

        titles = []
        for elem in title_elements:
            title_text = elem.get_text(strip=True)
            if title_text:
                titles.append(title_text)

        return titles

    except Exception as e:
        print(f"  [ERROR] 抓取失败 ({url}): {e}")
        return []


if __name__ == '__main__':
    # 使用 requests.Session 提升网络请求效率
    session = requests.Session()

    for start_id, length, output_path in zip(starts, lens, output_paths):
        output_filename = output_path
        # print(f"\n==================== 开始爬取 {year} 年 (AAAI-{year[-2:]}) 论文题目 ====================")

        all_titles_for_year = []

        # 遍历当前年份下的所有 Issue ID
        for issue_id in range(start_id, start_id + length):
            url = f"{s_prefix}{issue_id}"
            print(f"正在爬取 Issue ID {issue_id}: {url}")

            titles = fetch_titles_from_url(url, session)
            print(f"  -> 成功提取 {len(titles)} 篇论文")

            all_titles_for_year.extend(titles)

            # 适当休眠 0.5 秒，避免请求频率过快
            # time.sleep(0.5)

        # 将该年份所有分卷的论文题目统一保存到 txt 文件（不带序号）
        if all_titles_for_year:
            with open(output_filename, 'w', encoding='utf-8') as f:
                for title in all_titles_for_year:
                    f.write(title + '\n')
            # print(f"\n>>> {year} 年汇总完成！共计 {len(all_titles_for_year)} 篇论文，已保存至: {output_filename}")
            print(f"\n>>> 共计 {len(all_titles_for_year)} 篇论文，已保存至: {output_filename}")
        else:
            print(f"\n>>> 年未抓取到任何论文。")
