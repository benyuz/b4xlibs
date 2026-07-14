# B4X 资料库导航

聚合B4X官方与社区维护的库资源，提供一站式检索与浏览服务。

## 数据源
- **官方库**：Erel维护的Google Sheets
- **社区库**：B4XGoods（walt61维护）

## 技术架构
- **数据抓取**：PHP脚本（GitHub Actions定时触发）
- **数据存储**：JSON + GZIP压缩
- **前端展示**：纯静态HTML + CSS + JavaScript
- **托管平台**：GitHub Pages

## 本地开发
```bash
cd site
python3 -m http.server 8000
# 访问 http://localhost:8000
```

## 部署
1. 推送代码到GitHub仓库
2. 在 Settings → Pages 中设置发布源为 `main` 分支的 `/site` 文件夹
3. 手动触发Actions工作流生成数据

## 目录结构
```
├── .github/workflows/   # GitHub Actions
├── fetch/               # PHP抓取脚本
├── site/                # 网站根目录
│   ├── css/             # 样式
│   ├── js/              # 前端JS
│   ├── data/            # JSON数据（由PHP生成）
│   └── *.html
└── README.md
```

## 许可证
MIT