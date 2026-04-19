function normalizePath(pathname) {
  if (!pathname || pathname === '') {
    return '/';
  }

  if (pathname.length > 1 && pathname.endsWith('/')) {
    return pathname.slice(0, -1);
  }

  return pathname;
}

function getTabTarget(label) {
  if (label === 'BoxLite') {
    return '/';
  }

  if (label === 'BoxRun') {
    return '/boxrun';
  }

  return null;
}

function isActiveTab(target, pathname) {
  if (target === '/') {
    return pathname === '/';
  }

  return pathname === target || pathname.startsWith(target + '/');
}

function applyTabState(link, active) {
  link.dataset.active = active ? 'true' : 'false';

  link.classList.toggle('text-gray-800', active);
  link.classList.toggle('dark:text-gray-200', active);
  link.classList.toggle('[text-shadow:-0.2px_0_0_currentColor,0.2px_0_0_currentColor]', active);

  link.classList.toggle('text-gray-600', !active);
  link.classList.toggle('dark:text-gray-400', !active);

  const underline = link.querySelector('div.absolute');
  if (!underline) {
    return;
  }

  underline.classList.toggle('bg-primary', active);
  underline.classList.toggle('dark:bg-primary-light', active);
  underline.classList.toggle('group-hover:bg-gray-200', !active);
  underline.classList.toggle('dark:group-hover:bg-gray-700', !active);
}

function syncTopNavTabs() {
  const pathname = normalizePath(window.location.pathname);
  const tabLinks = document.querySelectorAll('a.nav-tabs-item');

  tabLinks.forEach((link) => {
    const label = (link.textContent || '').trim();
    const target = getTabTarget(label);

    if (!target) {
      return;
    }

    link.setAttribute('href', target);
    applyTabState(link, isActiveTab(target, pathname));

    if (link.dataset.codexNavFixed === 'true') {
      return;
    }

    link.dataset.codexNavFixed = 'true';
    link.addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      tabLinks.forEach((tabLink) => {
        const tabLabel = (tabLink.textContent || '').trim();
        const tabTarget = getTabTarget(tabLabel);
        if (!tabTarget) {
          return;
        }
        applyTabState(tabLink, normalizePath(tabTarget) === normalizePath(target));
      });

      if (normalizePath(window.location.pathname) !== normalizePath(target)) {
        window.location.assign(target);
        return;
      }

      syncTopNavTabs();
    });
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', syncTopNavTabs);
} else {
  syncTopNavTabs();
}

window.addEventListener('popstate', syncTopNavTabs);
window.addEventListener('pageshow', syncTopNavTabs);
window.addEventListener('load', syncTopNavTabs);
document.addEventListener('visibilitychange', () => {
  if (!document.hidden) {
    syncTopNavTabs();
  }
});

const observer = new MutationObserver(() => {
  syncTopNavTabs();
});

observer.observe(document.documentElement, {
  childList: true,
  subtree: true,
});

let syncAttempts = 0;
const syncTimer = window.setInterval(() => {
  syncTopNavTabs();
  syncAttempts += 1;
  if (syncAttempts >= 20) {
    window.clearInterval(syncTimer);
  }
}, 250);
