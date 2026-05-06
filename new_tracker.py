"""
AI教育行业动态追踪助手
功能：自动抓取RSS新闻 → DeepSeek摘要分析 → 生成行业报告
作者：刘珍汝
"""

import feedparser
import requests
from openai import OpenAI
from datetime import datetime
import pandas as pd
import os

# ── 配置 ──
DEEPSEEK_API_KEY = "请将你的Deepseek API输入在此"
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

# ── RSS订阅源（AI教育/科技相关）──
RSS_FEEDS = {
    "36氪-AI": "https://36kr.com/feed",
    "机器之心": "https://www.jiqizhixin.com/rss",
    "少数派":   "https://sspai.com/feed",
}

# ── 关键词过滤（只保留相关文章）──
KEYWORDS = ["AI", "人工智能", "大模型", "教育", "LLM", "GPT", "智能体", "教培"]


# ==================== 1. 抓取RSS ====================

def fetch_rss(feeds: dict, max_per_feed: int = 5) -> list:
    """抓取所有RSS源，返回文章列表"""
    articles = []
    for source, url in feeds.items():
        try:
            feed = feedparser.parse(url)
            count = 0
            for entry in feed.entries:
                if count >= max_per_feed:
                    break
                title   = entry.get('title', '')
                summary = entry.get('summary', '')[:300]
                link    = entry.get('link', '')
                # 关键词过滤
                if any(kw in title or kw in summary for kw in KEYWORDS):
                    articles.append({
                        "来源":   source,
                        "标题":   title,
                        "摘要":   summary,
                        "链接":   link,
                        "抓取时间": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    count += 1
            print(f"✅ {source}：获取 {count} 条相关文章")
        except Exception as e:
            print(f"⚠️  {source} 抓取失败：{e}")
    return articles


# ==================== 2. AI分析 ====================

def analyze_articles(articles: list) -> str:
    """将文章列表传给DeepSeek，生成行业分析报告"""
    if not articles:
        return "未找到相关文章，请检查网络或RSS源。"

    # 整理文章内容给模型
    content = ""
    for i, a in enumerate(articles, 1):
        content += f"{i}. 【{a['来源']}】{a['标题']}\n   {a['摘要']}\n\n"

    prompt = f"""
以下是今日AI教育行业的最新资讯，请帮我生成一份简洁的行业动态报告。

{content}

请按以下结构输出报告：
1. 今日核心动态（3条最重要的信息，每条1-2句话）
2. 行业趋势判断（基于以上信息，简要分析1-2个值得关注的趋势）
3. 对AI教育从业者的启示（1-2条实用建议）

语言简洁专业，总字数控制在400字以内。
"""

    print("\n🤖 正在调用DeepSeek生成分析报告...")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一名专注AI教育行业的资深分析师。"},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800
    )
    return response.choices[0].message.content


# ==================== 3. 导出报告 ====================

def export_report(articles: list, analysis: str, output_dir: str = "news_reports"):
    """导出原始文章列表和AI分析报告"""
    os.makedirs(output_dir, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d_%H%M")

    # 导出Excel（原始文章）
    if articles:
        df = pd.DataFrame(articles)
        excel_path = os.path.join(output_dir, f"行业动态_{today}.xlsx")
        df.to_excel(excel_path, index=False)
        print(f"✅ 原始文章已保存：{excel_path}")

    # 导出AI分析报告（txt）
    report_path = os.path.join(output_dir, f"AI分析报告_{today}.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"AI教育行业动态报告\n")
        f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("=" * 50 + "\n\n")
        f.write(analysis)
    print(f"✅ 分析报告已保存：{report_path}")

    return report_path


# ==================== 4. 主程序 ====================

def main():
    print("=" * 50)
    print("   AI教育行业动态追踪助手 v1.0")
    print("=" * 50)

    # Step1: 抓取RSS
    print("\n📡 正在抓取RSS订阅源...")
    articles = fetch_rss(RSS_FEEDS, max_per_feed=5)
    print(f"\n共获取 {len(articles)} 条相关文章")

    if not articles:
        print("❌ 未获取到任何文章，请检查网络连接或RSS源地址")
        return

    # Step2: AI分析
    analysis = analyze_articles(articles)

    # Step3: 打印报告
    print("\n" + "=" * 50)
    print("📋 今日AI教育行业动态报告")
    print("=" * 50)
    print(analysis)

    # Step4: 导出
    export_report(articles, analysis)

    print("\n🎉 完成！报告保存在 news_reports/ 文件夹")
    print("=" * 50)


if __name__ == "__main__":
    main()