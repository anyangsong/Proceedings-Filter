import requests
from bs4 import BeautifulSoup

urls = [
    "https://proceedings.neurips.cc/paper_files/paper/2023",
    "https://proceedings.iclr.cc/paper_files/paper/2024",
    "https://proceedings.neurips.cc/paper_files/paper/2024",
    "https://proceedings.iclr.cc/paper_files/paper/2025",
    "https://proceedings.neurips.cc/paper_files/paper/2025/vol38-main-conference",
    "https://proceedings.iclr.cc/paper_files/paper/2026",
]

output_paths = [
    "./data/NIPS-2023.txt",
    "./data/ICLR-2024.txt",
    "./data/NIPS-2024.txt",
    "./data/ICLR-2025.txt",
    "./data/NIPS-2025.txt",
    "./data/ICLR-2026.txt",
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}


if __name__ == '__main__':
    for url, output_path in zip(urls, output_paths):
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            paper_links = soup.select('ul.paper-list li div.paper-content a')

            titles = [link.get_text(strip=True) for link in paper_links]

            with open(output_path, 'w', encoding='utf-8') as f:
                for title in titles:
                    f.write(f"{title}\n")

            print(f"爬取成功，共获取 {len(titles)} 篇论文题目。")
        else:
            print(f"请求失败，状态码: {response.status_code}")
