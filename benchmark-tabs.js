(() => {
  const selectors = new Map();
  document.querySelectorAll('[data-tabs]').forEach(list => {
    const tabs = [...list.querySelectorAll('[role="tab"]')];
    const panels = tabs.map(tab => document.getElementById(tab.getAttribute('aria-controls')));
    const select = (index, focus = false, updateHash = false) => {
      tabs.forEach((tab, i) => {
        tab.setAttribute('aria-selected', String(i === index));
        tab.tabIndex = i === index ? 0 : -1;
        panels[i].hidden = i !== index;
        if (i !== index) panels[i].querySelectorAll('video').forEach(video => video.pause());
      });
      if (focus) tabs[index].focus({preventScroll: true});
      const tabRect = tabs[index].getBoundingClientRect(), listRect = list.getBoundingClientRect();
      if (tabRect.left < listRect.left) list.scrollLeft -= listRect.left - tabRect.left;
      if (tabRect.right > listRect.right) list.scrollLeft += tabRect.right - listRect.right;
      if (updateHash) history.replaceState(null, '', `#${panels[index].id}`);
    };
    tabs.forEach((tab, index) => {
      selectors.set(panels[index].id, () => select(index));
      tab.addEventListener('click', () => select(index, false, true));
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        else if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = tabs.length - 1;
        else return;
        event.preventDefault();
        select(next, true, true);
      });
    });
  });
  const selectCase = (select, updateHash = false) => {
    const panel = select.closest('.subset-panel');
    panel.querySelectorAll('[data-variant-case]').forEach(item => item.hidden = item.id !== select.value);
    if (updateHash) history.replaceState(null, '', `#${select.value}`);
  };
  document.querySelectorAll('[data-case-select]').forEach(select => {
    select.addEventListener('change', () => selectCase(select, true));
  });
  function fromHash() {
    const target = document.getElementById(location.hash.slice(1));
    if (!target || !target.closest('#explore')) return;
    const ancestors = [];
    for (let el = target; el; el = el.parentElement) if (selectors.has(el.id)) ancestors.unshift(el.id);
    ancestors.forEach(id => selectors.get(id)());
    if (target.matches('[data-variant-case]')) {
      const select = target.closest('.subset-panel').querySelector('[data-case-select]');
      select.value = target.id;
      selectCase(select);
    }
  }
  window.addEventListener('hashchange', fromHash);
  fromHash();
})();
