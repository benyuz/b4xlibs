const locales = {
    'zh-CN': {
        header: {
            title: 'B4X 资源导航',
            subtitle: '聚合官方与社区维护的 B4X 库资源，一站式检索与浏览',
            pageTitle: 'B4X 资源导航'
        },
        nav: {
            home: '🏠 首页',
            official: '📚 官方库',
            community: '🧩 社区库'
        },
        stats: {
            total: '总库数',
            official: '官方库',
            community: '社区库',
            authors: '作者数',
            update: '数据最后更新：'
        },
        ranking: {
            title: '🏆 贡献者排行榜',
            loading: '加载中...',
            noData: '暂无数据',
            count: '个库'
        },
        entry: {
            officialTitle: '📚 官方库',
            officialDesc: '由 Erel 维护的权威 B4X 库列表',
            communityTitle: '🧩 社区资源',
            communityDesc: '由社区爱好者维护的资源列表',
            viewAll: '→ 浏览全部'
        },
        links: {
            title: '🔗 官方资源',
            b4x: 'B4X 官网',
            b4a: 'B4A (Android)',
            b4i: 'B4I (iOS)',
            b4j: 'B4J (JavaFX)',
            b4r: 'B4R (IoT)',
            forum: 'B4X 论坛'
        },
        filter: {
            placeholder: '🔍 搜索库名、描述或作者...',
            all: '全部',
            b4a: 'B4A',
            b4i: 'B4I',
            b4j: 'B4J',
            b4r: 'B4R'
        },
        pagination: {
            prev: '‹',
            next: '›',
            info: '第 {page} / {total} 页，共 {count} 条'
        },
        empty: {
            noData: '暂无数据',
            noMatch: '📭 没有找到匹配的库',
            loading: '⏳ 加载数据中...',
            failed: '加载失败'
        },
        footer: {
            credit: '♥ B4X 由 Erel 创建 · 数据每日自动更新',
            update: '🔄 更新时间：',
            github: 'GitHub 仓库'
        },
        language: {
            zh: '中文',
            en: 'English'
        }
    },
    'en': {
        header: {
            title: 'B4X Resource Navigator',
            subtitle: 'Aggregate official and community B4X library resources for one-stop browsing',
            pageTitle: 'B4X Resource Navigator'
        },
        nav: {
            home: '🏠 Home',
            official: '📚 Official Libs',
            community: '🧩 Community Libs'
        },
        stats: {
            total: 'Total Libraries',
            official: 'Official',
            community: 'Community',
            authors: 'Authors',
            update: 'Last Updated: '
        },
        ranking: {
            title: '🏆 Contributor Ranking',
            loading: 'Loading...',
            noData: 'No data',
            count: ' libs'
        },
        entry: {
            officialTitle: '📚 Official Libraries',
            officialDesc: 'Authoritative B4X libraries maintained by Erel',
            communityTitle: '🧩 Community Resources',
            communityDesc: 'Resources maintained by community enthusiasts',
            viewAll: '→ View All'
        },
        links: {
            title: '🔗 Official Resources',
            b4x: 'B4X Official Site',
            b4a: 'B4A (Android)',
            b4i: 'B4I (iOS)',
            b4j: 'B4J (JavaFX)',
            b4r: 'B4R (IoT)',
            forum: 'B4X Forum'
        },
        filter: {
            placeholder: '🔍 Search by name, description or author...',
            all: 'All',
            b4a: 'B4A',
            b4i: 'B4I',
            b4j: 'B4J',
            b4r: 'B4R'
        },
        pagination: {
            prev: '‹',
            next: '›',
            info: 'Page {page} / {total}, {count} items'
        },
        empty: {
            noData: 'No data',
            noMatch: '📭 No matching libraries found',
            loading: '⏳ Loading data...',
            failed: 'Load failed'
        },
        footer: {
            credit: '♥ B4X created by Erel · Data updated daily',
            update: '🔄 Last Updated: ',
            github: 'GitHub Repository'
        },
        language: {
            zh: '中文',
            en: 'English'
        }
    }
};

function getLocale(lang) {
    return locales[lang] || locales['zh-CN'];
}

function detectLanguage() {
    const stored = localStorage.getItem('b4x-lang');
    if (stored && locales[stored]) return stored;
    const navLang = navigator.language || navigator.userLanguage;
    if (navLang && navLang.startsWith('zh')) return 'zh-CN';
    return 'en';
}

function setLanguage(lang) {
    if (locales[lang]) {
        localStorage.setItem('b4x-lang', lang);
        window.location.reload();
    }
}

window.Locale = {
    locales: locales,
    getLocale: getLocale,
    detectLanguage: detectLanguage,
    setLanguage: setLanguage
};
