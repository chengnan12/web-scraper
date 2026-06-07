#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网页数据采集工具
功能：从指定网页批量采集结构化数据，支持多页翻页
适用场景：竞品信息采集、公开数据汇总、内容监控
作者：接单作品
"""

import time
import csv
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class WebScraper:
    """通用网页数据采集器"""

    def __init__(self, delay=1.0, timeout=10):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/125.0.0.0 Safari/537.36"
        })
        self.delay = delay
        self.timeout = timeout

    def fetch_page(self, url):
        """请求单个页面"""
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
        return BeautifulSoup(resp.text, "html.parser")

    def scrape_list(self, url, item_css, field_map, max_pages=1, next_css=None):
        """
        采集列表数据
        :param url: 起始页面 URL
        :param item_css: 每条数据的 CSS 选择器
        :param field_map: 字段映射 {"字段名": "CSS选择器"}，支持 'text'/'href'/'src'
        :param max_pages: 最大翻页数
        :param next_css: "下一页"按钮的 CSS 选择器
        :return: 采集结果列表
        """
        results = []
        current_url = url

        for page in range(1, max_pages + 1):
            print(f"正在采集第 {page} 页...")
            soup = self.fetch_page(current_url)
            items = soup.select(item_css)

            if not items:
                print("  未找到数据，采集结束")
                break

            for item in items:
                record = {}
                for field_name, css in field_map.items():
                    el = item.select_one(css)
                    if el:
                        if css.endswith("[href]") or field_name.endswith("_url") or field_name.endswith("_link"):
                            record[field_name] = urljoin(current_url, el.get("href", ""))
                        elif css.endswith("[src]") or field_name.endswith("_img"):
                            record[field_name] = urljoin(current_url, el.get("src", ""))
                        else:
                            record[field_name] = el.get_text(strip=True)
                    else:
                        record[field_name] = ""
                results.append(record)

            print(f"  采集到 {len(results)} 条数据")

            # 翻页
            if next_css and page < max_pages:
                next_btn = soup.select_one(next_css)
                if next_btn and next_btn.get("href"):
                    current_url = urljoin(current_url, next_btn["href"])
                else:
                    print("  无下一页，采集结束")
                    break

            time.sleep(self.delay)

        return results

    def save_to_csv(self, data, output_path):
        """保存为 CSV 文件"""
        if not data:
            print("无数据可保存")
            return
        with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"已保存 {len(data)} 条数据至: {output_path}")


# 使用示例（注释掉，实际使用时根据需要取消注释并修改）
"""
if __name__ == "__main__":
    scraper = WebScraper(delay=2.0)

    # 示例：采集新闻列表
    data = scraper.scrape_list(
        url="https://example.com/news",
        item_css="div.news-item",
        field_map={
            "标题": "h3.title",
            "链接": "a[href]",
            "时间": "span.date",
            "摘要": "p.summary",
        },
        max_pages=5,
        next_css="a.next-page",
    )

    scraper.save_to_csv(data, "采集结果.csv")
"""
