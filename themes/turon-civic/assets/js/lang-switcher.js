(function () {
  var toggle = document.querySelector('[data-lang-switcher-toggle]');
  if (!toggle) return;
  var menu = document.getElementById('lang-switcher-menu');
  if (!menu) return;
  var links = menu.querySelectorAll('.lang-switcher__link');

  function trackOpen() {
    if (window.turonAnalytics && typeof window.turonAnalytics.track === 'function') {
      window.turonAnalytics.track('language_switcher_open', { source: 'header' });
    }
  }

  function setOpen(open) {
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) {
      menu.removeAttribute('hidden');
    } else {
      menu.setAttribute('hidden', '');
    }
  }

  toggle.addEventListener('click', function () {
    var isOpen = toggle.getAttribute('aria-expanded') === 'true';
    setOpen(!isOpen);
    if (!isOpen && links.length) {
      trackOpen();
      links[0].focus();
    }
  });

  toggle.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowDown' || e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      if (toggle.getAttribute('aria-expanded') !== 'true') {
        trackOpen();
      }
      setOpen(true);
      if (links.length) links[0].focus();
    }
  });

  links.forEach(function (link, idx) {
    link.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        var next = links[idx + 1] || links[0];
        next.focus();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        var prev = links[idx - 1] || links[links.length - 1];
        prev.focus();
      } else if (e.key === 'Escape') {
        e.preventDefault();
        setOpen(false);
        toggle.focus();
      } else if (e.key === 'Home') {
        e.preventDefault();
        links[0].focus();
      } else if (e.key === 'End') {
        e.preventDefault();
        links[links.length - 1].focus();
      }
    });
  });

  document.addEventListener('click', function (e) {
    if (!toggle.parentNode.contains(e.target)) {
      setOpen(false);
    }
  });
})();
