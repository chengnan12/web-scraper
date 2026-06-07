---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 52e2ce4f4ddb091dafdc1cda199f5f16_968483e761a311f1832e5254006c9bbf
    ReservedCode1: 2sIPTlvflhpdY0f/I45kXZSZROWvCVsL1P83GFQjVk6Btlcqlq9F3vaxKaK7xjWBztl4Qs/zKFRR8++M859d5RLZmUas3y6yB2YetbqvX9j/o/TUuY3UxdTJJtf9udEBTaYf1C20M8lbP8ylDP5oMhft5LfDpwt+RyLAoDEeOOH2gFR4Ui34MsnVkG4=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 52e2ce4f4ddb091dafdc1cda199f5f16_968483e761a311f1832e5254006c9bbf
    ReservedCode2: 2sIPTlvflhpdY0f/I45kXZSZROWvCVsL1P83GFQjVk6Btlcqlq9F3vaxKaK7xjWBztl4Qs/zKFRR8++M859d5RLZmUas3y6yB2YetbqvX9j/o/TUuY3UxdTJJtf9udEBTaYf1C20M8lbP8ylDP5oMhft5LfDpwt+RyLAoDEeOOH2gFR4Ui34MsnVkG4=
---

# 网页数据采集工具

通用网页数据采集器，支持 CSS 选择器定位、多页自动翻页、导出 CSV。

## 适用场景

- 采集竞品信息（商品价格、评价数据）
- 汇总公开新闻、资讯、公告
- 批量下载表格数据做分析

## 运行环境

- Python 3.7+
- 依赖安装：`pip install requests beautifulsoup4`

## 使用方法

修改脚本底部的示例配置，填入目标网站的 URL 和 CSS 选择器即可运行：

```python
from web_scraper import WebScraper

scraper = WebScraper(delay=2.0)  # 每次请求间隔2秒

data = scraper.scrape_list(
    url="https://example.com/news",
    item_css="div.news-item",        # 每条新闻的容器
    field_map={
        "标题": "h3.title",
        "链接": "a[href]",
        "时间": "span.date",
        "摘要": "p.summary",
    },
    max_pages=5,                     # 最多翻5页
    next_css="a.next-page",          # "下一页"按钮
)

scraper.save_to_csv(data, "采集结果.csv")
```

## 功能特点

- CSS 选择器定位，无需学 XPath
- 支持多页自动翻页
- 自动处理相对链接转绝对链接
- 请求间隔控制，避免被封 IP
- 结果直接导出 CSV，Excel 可打开

