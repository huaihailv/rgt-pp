(() => {
  const tabs = [...document.querySelectorAll('.benchmark-tabs [role="tab"]')];
  const panels = tabs.map(tab => document.getElementById(tab.getAttribute('aria-controls')));
  function select(index, focus = false, updateHash = false) {
    tabs.forEach((tab, i) => {
      tab.setAttribute('aria-selected', String(i === index));
      tab.tabIndex = i === index ? 0 : -1;
      panels[i].hidden = i !== index;
      if (i !== index) panels[i].querySelectorAll('video').forEach(video => video.pause());
    });
    if (focus) tabs[index].focus();
    if (updateHash) history.replaceState(null, '', `#${panels[index].id}`);
  }
  tabs.forEach((tab, index) => {
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
  function fromHash() {
    const index = panels.findIndex(panel => `#${panel.id}` === location.hash);
    if (index >= 0) select(index);
  }
  window.addEventListener('hashchange', fromHash);
  fromHash();
})();
