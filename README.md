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