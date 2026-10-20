/* Public documentation search: browser-local matching, no account or telemetry. */
(() => {
  'use strict';
  if (document.getElementById('ss-docs-search-button')) return;
  const indexUrl = 'https://raw.githubusercontent.com/subscan-explorer/subscan-OpenAPI/main/docs/search-index.json';
  let indexPromise;
  const button = document.createElement('button');
  button.id = 'ss-docs-search-button';
  button.type = 'button';
  button.textContent = 'Search docs';
  button.title = 'Full-text search (Ctrl/Cmd + Shift + K)';
  const dialog = document.createElement('dialog');
  dialog.id = 'ss-docs-search';
  dialog.setAttribute('aria-labelledby', 'ss-docs-search-title');
  dialog.innerHTML = '<div class="ss-docs-search-header"><h2 id="ss-docs-search-title">Search documentation</h2>' +
    '<button type="button" aria-label="Close search">Close</button></div>' +
    '<input type="search" aria-label="Search all documentation" placeholder="Search endpoints, fields, and guides" maxlength="160">' +
    '<p role="status" aria-live="polite"></p><ul aria-label="Search results"></ul>';
  if (typeof dialog.showModal !== 'function') return;
  const input = dialog.querySelector('input');
  const status = dialog.querySelector('[role="status"]');
  const results = dialog.querySelector('ul');

  function loadIndex() {
    if (!indexPromise) {
      indexPromise = fetch(indexUrl, {credentials: 'omit', referrerPolicy: 'no-referrer'})
        .then(response => {
          if (!response.ok) throw new Error('Search index unavailable');
          return response.json();
        })
        .then(data => data.entries.filter(entry => /^\/(?:api|doc|folder)-\d+$/.test(entry.url))
          .map(entry => ({...entry, titleSearch: entry.title.toLowerCase(),
            descriptionSearch: entry.description.toLowerCase(), textSearch: entry.text.toLowerCase()})))
        .catch(error => { indexPromise = undefined; throw error; });
    }
    return indexPromise;
  }

  let version = 0;
  async function search() {
    const current = ++version;
    const query = input.value.trim().toLowerCase();
    results.replaceChildren();
    if (!query) { status.textContent = 'Search API names, parameters, response fields, and guide text.'; return; }
    status.textContent = 'Searching…';
    try {
      const entries = await loadIndex();
      if (current !== version || !dialog.open) return;
      const tokens = query.match(/[\p{L}\p{N}_-]+/gu)?.slice(0, 8) ?? [];
      const matches = tokens.length ? entries.map(entry => {
        let score = 0;
        for (const token of tokens) {
          const value = (entry.titleSearch.includes(token) ? 8 : 0) +
            (entry.descriptionSearch.includes(token) ? 3 : 0) + (entry.textSearch.includes(token) ? 1 : 0);
          if (!value) return null;
          score += value;
        }
        return {entry, score};
      }).filter(Boolean).sort((a, b) => b.score - a.score) : [];
      status.textContent = matches.length ? `${matches.length} results${matches.length > 20 ? ' · showing the first 20' : ''}` : 'No matching documentation found.';
      for (const {entry} of matches.slice(0, 20)) {
        const item = document.createElement('li');
        const link = document.createElement('a');
        link.href = entry.url;
        const title = document.createElement('strong');
        title.textContent = entry.title;
        const category = document.createElement('span');
        category.textContent = ` ${entry.category}`;
        const snippet = document.createElement('p');
        const content = `${entry.description} ${entry.text}`.replace(/\s+/g, ' ');
        const position = Math.max(0, content.toLowerCase().indexOf(tokens[0]) - 60);
        snippet.textContent = (position ? '…' : '') + content.slice(position, position + 200);
        link.append(title, category, snippet);
        item.append(link);
        results.append(item);
      }
    } catch {
      if (current === version) status.textContent = 'Full-text search is temporarily unavailable. You can use the sidebar search.';
    }
  }

  function openSearch() {
    if (!dialog.open) dialog.showModal();
    input.focus();
    search();
  }
  button.addEventListener('click', openSearch);
  dialog.querySelector('button').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => { version++; button.focus(); });
  let timer;
  input.addEventListener('input', () => {
    version++;
    results.replaceChildren();
    clearTimeout(timer);
    timer = setTimeout(search, 120);
  });
  input.addEventListener('keydown', event => {
    if (event.key === 'Enter') results.querySelector('a')?.click();
  });
  document.addEventListener('keydown', event => {
    if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.code === 'KeyK') {
      event.preventDefault();
      openSearch();
    }
  });
  document.body.append(button, dialog);
})();
