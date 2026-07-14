async function loadJSON(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return await response.json();
    } catch (error) {
        console.error('加载数据失败:', error);
        return null;
    }
}

function getUrlParams() {
    const params = new URLSearchParams(window.location.search);
    const result = {};
    for (const [key, value] of params) {
        result[key] = value;
    }
    return result;
}

function parseDate(dateStr) {
    if (!dateStr) return new Date(0);
    const parts = dateStr.match(/(\d{4})[-.\/](\d{1,2})[-.\/](\d{1,2})/);
    if (parts) {
        return new Date(parseInt(parts[1]), parseInt(parts[2]) - 1, parseInt(parts[3]));
    }
    return new Date(dateStr) || new Date(0);
}

function sortByDate(libraries, order = 'desc') {
    return [...libraries].sort((a, b) => {
        const dateA = parseDate(a.date);
        const dateB = parseDate(b.date);
        return order === 'desc' ? dateB - dateA : dateA - dateB;
    });
}

function filterLibraries(libraries, filters) {
    return libraries.filter(lib => {
        if (filters.keyword) {
            const kw = filters.keyword.toLowerCase();
            const matchName = lib.name && lib.name.toLowerCase().includes(kw);
            const matchDesc = lib.desc && lib.desc.toLowerCase().includes(kw);
            const matchAuthor = lib.author && lib.author.toLowerCase().includes(kw);
            if (!matchName && !matchDesc && !matchAuthor) return false;
        }
        if (filters.platform && filters.platform !== 'ALL') {
            if (!lib.tags || !lib.tags.includes(filters.platform)) return false;
        }
        return true;
    });
}

function paginate(libraries, page, pageSize) {
    const start = (page - 1) * pageSize;
    const end = start + pageSize;
    return {
        data: libraries.slice(start, end),
        total: libraries.length,
        page: page,
        pageSize: pageSize,
        totalPages: Math.ceil(libraries.length / pageSize)
    };
}

function renderLibraries(libraries, containerId, locale) {
    const t = locale?.filter || {};
    const container = document.getElementById(containerId);
    if (!container) return;
    if (!libraries || libraries.length === 0) {
        container.innerHTML = '<div style="text-align:center;padding:40px;color:#999;">' + (t.noMatch || '📭 没有找到匹配的库') + '</div>';
        return;
    }
    
    let html = '';
    libraries.forEach(lib => {
        const tagsHtml = (lib.tags || []).map(t => `<span class="tag tag-${t}">${t}</span>`).join('');
        const link = lib.link || '#';
        const versionHtml = lib.version ? 'v' + lib.version : '';
        const dateHtml = lib.date || '';
        const authorHtml = lib.author ? `<a href="?keyword=${encodeURIComponent(lib.author)}" class="card-author-link">@${lib.author}</a>` : '';
        
        html += `
            <article class="library-card">
                <div class="card-header">
                    <h5 class="card-title"><a href="${link}" target="_blank" rel="noopener">${lib.name}</a></h5>
                    <div class="card-tags">${tagsHtml}</div>
                </div>
                ${lib.desc ? `<blockquote class="card-desc">${lib.desc}</blockquote>` : ''}
                <div class="card-footer">
                    ${authorHtml}
                    ${dateHtml ? '· <span class="card-date">' + dateHtml + '</span>' : ''}
                    ${versionHtml ? '· <span class="card-version">' + versionHtml + '</span>' : ''}
                </div>
            </article>
        `;
    });
    container.innerHTML = html;
}

function renderPagination(pagination, containerId, onPageChange, locale) {
    const t = locale?.pagination || {};
    const container = document.getElementById(containerId);
    if (!container) return;
    if (pagination.totalPages <= 1) {
        container.innerHTML = '';
        return;
    }
    
    const { page, totalPages } = pagination;
    let html = `<div class="pagination">`;
    
    html += `<button class="page-btn ${page <= 1 ? 'disabled' : ''}" onclick="(${onPageChange})(${page - 1})">${t.prev || '‹'}</button>`;
    
    const start = Math.max(1, page - 2);
    const end = Math.min(totalPages, page + 2);
    
    if (start > 1) {
        html += `<button class="page-btn" onclick="(${onPageChange})(1)">1</button>`;
        if (start > 2) html += `<span class="page-ellipsis">...</span>`;
    }
    
    for (let i = start; i <= end; i++) {
        html += `<button class="page-btn ${i === page ? 'active' : ''}" onclick="(${onPageChange})(${i})">${i}</button>`;
    }
    
    if (end < totalPages) {
        if (end < totalPages - 1) html += `<span class="page-ellipsis">...</span>`;
        html += `<button class="page-btn" onclick="(${onPageChange})(${totalPages})">${totalPages}</button>`;
    }
    
    html += `<button class="page-btn ${page >= totalPages ? 'disabled' : ''}" onclick="(${onPageChange})(${page + 1})">${t.next || '›'}</button>`;
    const info = (t.info || '第 {page} / {total} 页，共 {count} 条')
        .replace('{page}', page).replace('{total}', totalPages).replace('{count}', pagination.total);
    html += `<span class="page-info">${info}</span>`;
    html += `</div>`;
    
    container.innerHTML = html;
}

window.B4XLib = {
    loadJSON: loadJSON,
    getUrlParams: getUrlParams,
    parseDate: parseDate,
    sortByDate: sortByDate,
    filterLibraries: filterLibraries,
    paginate: paginate,
    renderLibraries: renderLibraries,
    renderPagination: renderPagination
};
