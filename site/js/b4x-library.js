async function loadGzippedJSON(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('HTTP ' + response.status);
        
        if (url.endsWith('.gz')) {
            try {
                const ds = new DecompressionStream('gzip');
                const stream = response.body.pipeThrough(ds);
                return await new Response(stream).json();
            } catch (e) {
                const fallbackUrl = url.replace('.gz', '');
                const resp = await fetch(fallbackUrl);
                return await resp.json();
            }
        }
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

function renderLibraries(libraries, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    if (!libraries || libraries.length === 0) {
        container.innerHTML = '<div style="text-align:center;padding:40px;color:#999;">📭 没有找到匹配的库</div>';
        return;
    }
    
    let html = '';
    libraries.forEach(lib => {
        const tagsHtml = (lib.tags || []).map(t => `<span class="tag tag-${t}">${t}</span>`).join('');
        const link = lib.link || '#';
        const versionHtml = lib.version ? 'v' + lib.version : '';
        const dateHtml = lib.date || '';
        const authorHtml = lib.author ? '@' + lib.author : '';
        
        html += `
            <article class="library-card">
                <div class="card-header">
                    <h5 class="card-title"><a href="${link}" target="_blank" rel="noopener">${lib.name}</a></h5>
                    <div class="card-tags">${tagsHtml}</div>
                </div>
                ${lib.desc ? `<blockquote class="card-desc">${lib.desc}</blockquote>` : ''}
                <div class="card-footer">
                    <span class="card-author">${authorHtml}</span>
                    ${dateHtml ? '· <span class="card-date">' + dateHtml + '</span>' : ''}
                    ${versionHtml ? '· <span class="card-version">' + versionHtml + '</span>' : ''}
                </div>
            </article>
        `;
    });
    container.innerHTML = html;
}

window.B4XLib = {
    loadGzippedJSON: loadGzippedJSON,
    getUrlParams: getUrlParams,
    filterLibraries: filterLibraries,
    renderLibraries: renderLibraries
};