function fixTopNavTabs() {
  const tabLinks = document.querySelectorAll('a.nav-tabs-item');

  tabLinks.forEach((link) => {
    const label = (link.textContent || '').trim();
    let target = null;

    if (label === 'BoxLite') {
      target = '/';
    } else if (label === 'BoxRun') {
      target = '/boxrun';
    }

    if (!target) {
      return;
    }

    link.setAttribute('href', target);

    if (link.dataset.codexNavFixed === 'true') {
      return;
    }

    link.dataset.codexNavFixed = 'true';
    link.addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      window.location.assign(target);
    });
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', fixTopNavTabs);
} else {
  fixTopNavTabs();
}

const observer = new MutationObserver(() => {
  fixTopNavTabs();
});

observer.observe(document.documentElement, {
  childList: true,
  subtree: true,
});
