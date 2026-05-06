# AI教育行业动态追踪助手

## 项目背景

在AI教育公司工作期间，需要持续关注行业动态，原有方式是人工浏览多个资讯网站，效率低且容易遗漏重要信息。本工具通过自动抓取RSS订阅源，结合大模型分析，每次运行即可获得一份结构化的行业动态报告。

## 解决的问题

- 人工浏览多个网站耗时：整合多个RSS源，一键获取
- 信息量大难以筛选：关键词过滤，只保留AI教育相关内容
- 原始信息缺乏分析：接入DeepSeek API，自动生成趋势判断和行业启示

## 功能介绍

- **RSS自动抓取**：支持多个订阅源，按关键词过滤相关文章
- **AI智能分析**：调用DeepSeek API生成核心动态、趋势判断、从业建议
- **双格式导出**：原始文章保存为Excel，AI报告保存为txt

## 技术栈

- Python 3.x
- feedparser（RSS解析）
- openai SDK（DeepSeek API调用）
- pandas（数据整理与导出）

## 使用方法

### 安装依赖
```bash
pip install feedparser openai pandas openpyxl
```

### 配置API Key
打开 `news_tracker.py`，填入你的DeepSeek API Key：
```python
DEEPSEEK_API_KEY = "你的Key"
```

### 运行
```bash
python news_tracker.py
```

### 输出结果

运行后在 `news_reports/` 目录生成：
- `行业动态_日期.xlsx`：原始文章列表
- `AI分析报告_日期.txt`：AI生成的结构化报告

## 项目意义

将原本需要30-60分钟的人工信息收集工作，缩短至2分钟内自动完成，同时通过AI分析提炼出可操作的行业洞察。
