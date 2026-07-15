# B4X Resource Navigator

A comprehensive navigation platform for B4X libraries, aggregating official and community-maintained resources for one-stop browsing.

**🌐 Website:** [https://benyuz.github.io/b4xlibs/](https://benyuz.github.io/b4xlibs/)

---

## Features

- **📚 Official Index**: Browse B4X library index curated by Erel
- **🧩 Community Collection**: Explore resources maintained by community enthusiasts
- **🏆 Contributor Ranking**: See top contributors and their library counts
- **🔍 Search & Filter**: Search libraries by name, description, or author; filter by platform (B4A/B4I/B4J/B4R)
- **📅 Daily Updates**: Data is automatically fetched and updated daily via GitHub Actions
- **🌍 Bilingual Support**: Chinese/English interface with language auto-detection
- **📱 Responsive Design**: Optimized for desktop and mobile devices

---

## Data Sources

- **Official Index**: Scraped from [B4X Google Sheets](https://www.b4x.com/android/forum/pages/results/?query=b4x+library)
- **Community Collection**: Scraped from community forum posts

---

## Project Structure

```
b4xlibs/
├── docs/                    # GitHub Pages site
│   ├── index.html          # Home page (statistics, ranking, links)
│   ├── official.html       # Official libraries listing
│   ├── community.html      # Community libraries listing
│   ├── css/style.css       # Stylesheet
│   ├── js/
│   │   ├── b4x-library.js  # Core library rendering logic
│   │   └── locale.js       # Bilingual translation config
│   └── data/               # JSON data files (auto-generated)
├── fetch/                  # PHP fetch scripts
│   ├── fetch_official.php  # Fetch official libraries
│   ├── fetch_community.php # Fetch community libraries
│   └── generate_stats.php  # Generate statistics
└── .github/workflows/
    └── fetch-data.yml      # Daily data fetch workflow
```

---

## Contributing

Contributions are welcome! Here are some ways you can help:

1. **Add New Libraries**: Submit PR with new library links
2. **Fix Bugs**: Report or fix issues with the website
3. **Improve Design**: Suggest UI/UX improvements
4. **Translate**: Help improve translations

---

## License

MIT License

---

---

## 中文说明

一个全面的 B4X 库导航平台，聚合官方和社区维护的资源，提供一站式浏览体验。

**🌐 网站:** [https://benyuz.github.io/b4xlibs/](https://benyuz.github.io/b4xlibs/)

---

## 功能特性

- **📚 官方索引**: 浏览由 Erel 整理维护的 B4X 库索引
- **🧩 社区集合**: 探索由社区爱好者维护的资源集合
- **🏆 贡献者排行榜**: 查看顶级贡献者及其库数量
- **🔍 搜索与筛选**: 按名称、描述或作者搜索；按平台筛选（B4A/B4I/B4J/B4R）
- **📅 每日更新**: 数据通过 GitHub Actions 自动获取和更新
- **🌍 双语支持**: 中英文界面，自动检测语言
- **📱 响应式设计**: 适配桌面和移动设备

---

## 数据来源

- **官方索引**: 从 [B4X Google Sheets](https://www.b4x.com/android/forum/pages/results/?query=b4x+library) 抓取
- **社区集合**: 从社区论坛帖子抓取

---

## 项目结构

```
b4xlibs/
├── docs/                    # GitHub Pages 站点
│   ├── index.html          # 首页（统计、排行榜、链接）
│   ├── official.html       # 官方库列表
│   ├── community.html      # 社区库列表
│   ├── css/style.css       # 样式文件
│   ├── js/
│   │   ├── b4x-library.js  # 核心渲染逻辑
│   │   └── locale.js       # 双语翻译配置
│   └── data/               # JSON 数据文件（自动生成）
├── fetch/                  # PHP 抓取脚本
│   ├── fetch_official.php  # 抓取官方库
│   ├── fetch_community.php # 抓取社区库
│   └── generate_stats.php  # 生成统计数据
└── .github/workflows/
    └── fetch-data.yml      # 每日数据抓取工作流
```

---

## 贡献

欢迎贡献！您可以通过以下方式帮助我们：

1. **添加新库**: 提交 PR 添加新的库链接
2. **修复问题**: 报告或修复网站问题
3. **改进设计**: 建议 UI/UX 改进
4. **翻译**: 帮助改进翻译

---

## 许可证

MIT License
