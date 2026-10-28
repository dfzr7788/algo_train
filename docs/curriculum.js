(() => {
  'use strict';
  const search = document.querySelector('#search');
  const difficulty = document.querySelector('#difficulty');
  const rows = [...document.querySelectorAll('tr[data-search]')];
  const sections = [...document.querySelectorAll('.week')];
  function filter() {
    const query = search.value.trim().toLocaleLowerCase();
    let count = 0;
    rows.forEach(row => {
      row.hidden = !(row.dataset.search.toLocaleLowerCase().includes(query) &&
        (!difficulty.value || row.dataset.color === difficulty.value));
      if (!row.hidden) count++;
    });
    sections.forEach(section => {
      section.hidden = ![...section.querySelectorAll('tr[data-search]')].some(row => !row.hidden);
    });
    document.querySelector('#result-count').textContent = `显示 ${count} / ${rows.length} 道题`;
    document.querySelector('#empty').hidden = count !== 0;
  }
  function reset() {
    search.value = '';
    difficulty.value = '';
    filter();
  }
  search.addEventListener('input', filter);
  difficulty.addEventListener('change', filter);
  document.querySelector('#reset').addEventListener('click', reset);
  document.querySelectorAll('.week-nav a').forEach(link => link.addEventListener('click', reset));
  window.addEventListener('hashchange', () => {
    if (/^#week-[0-8]$/.test(location.hash)) {
      reset();
      document.querySelector(location.hash)?.scrollIntoView();
    }
  });
  document.querySelector('.filters').hidden = false;
  filter();
})();
