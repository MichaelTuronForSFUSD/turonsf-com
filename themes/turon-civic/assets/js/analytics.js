/*
 * analytics.js — Umami event shim for turonsf.com v1.3.0+
 *
 * Wires the 14-event taxonomy specified in docs/Phase1_Analytics_Spec.md.
 *
 * Loading:
 *   {{ $analytics := resources.Get "js/analytics.js" | resources.Minify | resources.Fingerprint }}
 *   <script defer src="{{ $analytics.RelPermalink }}" integrity="{{ $analytics.Data.Integrity }}"></script>
 *
 * The Umami site script must load FIRST (it sets window.umami). This shim
 * uses defer so DOM is ready when it runs; it gracefully degrades to
 * console.log if window.umami is absent (development / preview / Umami offline).
 *
 * Cookieless. No PII. No external requests beyond Umami's own beacon.
 */

(function () {
  'use strict';

  /* ---------------------------------------------------------------------
   * Core track() function — single point of truth for event dispatch.
   * --------------------------------------------------------------------- */
  var seen = new Set();

  function track(eventName, dims) {
    dims = dims || {};
    var lang = document.documentElement.getAttribute('lang') || 'en';
    var viewport = window.innerWidth < 768 ? 'mobile' : 'desktop';
    var fullDims = Object.assign({ language: lang, viewport: viewport }, dims);

    if (window.umami && typeof window.umami.track === 'function') {
      window.umami.track(eventName, fullDims);
    } else if (typeof console !== 'undefined' && console.log) {
      console.log('[umami:offline]', eventName, fullDims);
    }
  }

  /* ---------------------------------------------------------------------
   * Click events on any element carrying data-event="..."
   * Dimensions populated from data-source, data-pillar, data-to attributes.
   * --------------------------------------------------------------------- */
  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-event]');
    if (!el) return;
    var dims = {};
    if (el.dataset.source) dims.source = el.dataset.source;
    if (el.dataset.pillar) dims.pillar = el.dataset.pillar;
    if (el.dataset.to) dims.to_language = el.dataset.to;
    if (el.dataset.from) dims.from_language = el.dataset.from;
    track(el.dataset.event, dims);
  });

  /* ---------------------------------------------------------------------
   * Impression events — IntersectionObserver, fires once per session per event.
   * --------------------------------------------------------------------- */
  function observeImpression(selector, eventName, threshold) {
    threshold = threshold || 0.5;
    var el = document.querySelector(selector);
    if (!el) return;
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting && entry.intersectionRatio >= threshold && !seen.has(eventName)) {
            seen.add(eventName);
            track(eventName, { page: location.pathname });
          }
        });
      },
      { threshold: threshold }
    );
    io.observe(el);
  }

  observeImpression('[data-cta-primary]', 'hero_cta_primary_view', 0.5);
  observeImpression('[data-trust-strip]', 'trust_strip_view', 0.5);

  /* Pending-notice impression — only fires on placeholder pages where the
     notice is rendered. Rebind after language toggle for SPA-like behavior. */
  function bindPendingNoticeObserver() {
    seen.delete('language_pending_notice_view');
    var el = document.querySelector('[data-pending-notice]');
    if (!el) return;
    if (window.getComputedStyle(el).display === 'none') return;
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (
            entry.isIntersecting &&
            entry.intersectionRatio >= 0.3 &&
            !seen.has('language_pending_notice_view')
          ) {
            seen.add('language_pending_notice_view');
            track('language_pending_notice_view', { page: location.pathname });
          }
        });
      },
      { threshold: 0.3 }
    );
    io.observe(el);
  }
  bindPendingNoticeObserver();

  /* ---------------------------------------------------------------------
   * Scroll depth events.
   * --------------------------------------------------------------------- */
  var depth75 = false;
  var depth100 = false;
  function checkScrollDepth() {
    var pct = (window.scrollY + window.innerHeight) / document.documentElement.scrollHeight;
    if (!depth75 && pct >= 0.75) {
      depth75 = true;
      track('scroll_depth_75', { page: location.pathname });
    }
    if (!depth100 && pct >= 0.98) {
      depth100 = true;
      track('scroll_depth_100', { page: location.pathname });
    }
  }
  /* Throttle to once per 250ms to avoid event-stream noise */
  var scrollThrottle = null;
  window.addEventListener(
    'scroll',
    function () {
      if (scrollThrottle) return;
      scrollThrottle = setTimeout(function () {
        scrollThrottle = null;
        checkScrollDepth();
      }, 250);
    },
    { passive: true }
  );

  /* ---------------------------------------------------------------------
   * Language switcher events — open + select.
   * Bound by data-event attributes on the switcher trigger and options;
   * those are added by themes/turon-civic/layouts/partials/language-switcher.html.
   * (Click handler above catches them; no extra wiring needed.)
   * --------------------------------------------------------------------- */

  /* ---------------------------------------------------------------------
   * Brevo newsletter form success callback — the actual conversion event.
   * Brevo fires a custom event on successful submission; we listen and
   * dispatch newsletter_signup_submit with the source dimension from
   * a hidden form field the embed inserts.
   * --------------------------------------------------------------------- */
  window.addEventListener('sib_form_success', function (e) {
    var detail = (e && e.detail) || {};
    var evtName = window.location.pathname.indexOf('volunteer') !== -1 ? 'volunteer_signup_submit' : 'newsletter_signup_submit';
    track(evtName, {
      source: detail.source || 'unknown',
      list_id: detail.list_id || ''
    });
  });

  /* ---------------------------------------------------------------------
   * Expose track() for inline use from partials that need to fire events
   * outside the data-event click pattern (e.g., form-submit handlers).
   * --------------------------------------------------------------------- */
  window.turonAnalytics = { track: track };  /* Copy-link button handler for desktop volunteer share */
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-copy-url]');
    if (!btn) return;
    var url = btn.dataset.copyUrl;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(function () {
        var arrow = btn.querySelector('.btn__arrow');
        btn.childNodes[0].textContent = 'Link copied! ';
        if (arrow) arrow.textContent = '✓';
        setTimeout(function () {
          btn.childNodes[0].textContent = 'Copy volunteer link ';
          if (arrow) arrow.textContent = '→';
        }, 2000);
      });
    }
  });

})();
