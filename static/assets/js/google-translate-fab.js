/**
 * ROCB floating Google Translate — shared logic (rocb_main).
 */
(function (global) {
  var GT_LANGS =
    'en,ru,az,fr,de,es,it,tr,uk,pl,ro,ka,kk,uz,tg,hy,be,bs,sq,mk,sr,hr,bg,lt,lv,et,fi,sv,no,da,nl,cs,sk,sl,hu,el,he,pt,mt,is,me,md,ky';
  var GT_LANG_LABELS = {
    en: 'English',
    ru: 'Русский',
    az: 'Azərbaycan',
    fr: 'Français',
    de: 'Deutsch',
    es: 'Español',
    it: 'Italiano',
    tr: 'Türkçe',
    uk: 'Українська',
    pl: 'Polski',
    ro: 'Română',
    ka: 'ქართული',
    kk: 'Қазақ',
    uz: 'Oʻzbek',
    tg: 'Тоҷикӣ',
    hy: 'Հայերեն',
    be: 'Беларуская',
    bs: 'Bosanski',
    sq: 'Shqip',
    mk: 'Македонски',
    sr: 'Српски',
    hr: 'Hrvatski',
    bg: 'Български',
    lt: 'Lietuvių',
    lv: 'Latviešu',
    et: 'Eesti',
    fi: 'Suomi',
    sv: 'Svenska',
    no: 'Norsk',
    da: 'Dansk',
    nl: 'Nederlands',
    cs: 'Čeština',
    sk: 'Slovenčina',
    sl: 'Slovenščina',
    hu: 'Magyar',
    el: 'Ελληνικά',
    he: 'עברית',
    pt: 'Português',
    mt: 'Malti',
    is: 'Íslenska',
    me: 'Crnogorski',
    md: 'Moldovenească',
    ky: 'Кыргызча',
  };

  function getPageLangCode() {
    var html = document.documentElement.lang || 'en';
    return html.split('-')[0].toLowerCase();
  }

  function writeGoogTransCookie(value) {
    var host = window.location.hostname;
    var base = 'googtrans=' + value + ';path=/';
    document.cookie = base;
    document.cookie = base + ';domain=' + host;
    var root = host.replace(/^www\./, '');
    if (root.indexOf('.') !== -1) {
      document.cookie = base + ';domain=.' + root;
    }
  }

  function clearGoogTransCookie() {
    var exp = 'Thu, 01 Jan 1970 00:00:00 GMT';
    var host = window.location.hostname;
    var clear = 'googtrans=;path=/;expires=' + exp;
    document.cookie = clear;
    document.cookie = clear + ';domain=' + host;
    var root = host.replace(/^www\./, '');
    if (root.indexOf('.') !== -1) {
      document.cookie = clear + ';domain=.' + root;
    }
  }

  function getGtCombo() {
    return document.querySelector('#google_translate_element .goog-te-combo');
  }

  function triggerComboChange(combo, lang) {
    if (!combo) return false;
    var matched = false;
    for (var i = 0; i < combo.options.length; i++) {
      var opt = combo.options[i];
      if (opt.value === lang || opt.value === '|' + lang || opt.value.slice(-lang.length) === lang) {
        combo.selectedIndex = i;
        matched = true;
        break;
      }
    }
    if (!matched) combo.value = lang;
    combo.dispatchEvent(new Event('change', { bubbles: true }));
    if (typeof combo.onchange === 'function') combo.onchange();
    return true;
  }

  function translatePageTo(targetLang) {
    if (!targetLang) return;
    var pageLang = getPageLangCode();
    if (targetLang === pageLang) {
      clearGoogTransCookie();
      window.location.reload();
      return;
    }
    writeGoogTransCookie('/' + pageLang + '/' + targetLang);
    var combo = getGtCombo();
    if (combo) triggerComboChange(combo, targetLang);
    window.location.reload();
  }

  function populateLangSelect() {
    var sel = document.getElementById('rocbGtLangSelect');
    if (!sel || sel.getAttribute('data-populated') === '1') return;
    sel.setAttribute('data-populated', '1');
    GT_LANGS.split(',').forEach(function (code) {
      var opt = document.createElement('option');
      opt.value = code;
      opt.textContent = GT_LANG_LABELS[code] || code;
      sel.appendChild(opt);
    });
  }

  function wireLangSelect() {
    var sel = document.getElementById('rocbGtLangSelect');
    if (!sel || sel.getAttribute('data-wired') === '1') return;
    sel.setAttribute('data-wired', '1');
    sel.addEventListener('change', function () {
      if (!sel.value) return;
      translatePageTo(sel.value);
    });
  }

  function initGoogleTranslate() {
    if (!window.google || !window.google.translate) return;
    var mount = document.getElementById('google_translate_element');
    if (!mount) return;
    if (window.__rocbGtInited && mount.querySelector('.goog-te-combo')) return;
    window.__rocbGtInited = true;
    var pageLang = getPageLangCode();
    new window.google.translate.TranslateElement(
      {
        pageLanguage: pageLang,
        includedLanguages: GT_LANGS,
        autoDisplay: false,
        layout: window.google.translate.TranslateElement.InlineLayout.SIMPLE,
      },
      'google_translate_element'
    );
    [0, 300, 1000].forEach(function (ms) {
      setTimeout(global.rocbGtHideTopChrome, ms);
    });
  }

  function loadGtScript() {
    window.googleTranslateElementInit = initGoogleTranslate;
    if (document.getElementById('rocb-google-translate-script')) {
      initGoogleTranslate();
      global.rocbGtHideTopChrome();
      return;
    }
    var s = document.createElement('script');
    s.id = 'rocb-google-translate-script';
    s.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    s.async = true;
    document.body.appendChild(s);
  }

  function isInsideGtFab(el) {
    var fab = document.getElementById('rocbGtFab');
    return fab && fab.contains(el);
  }

  function isGtBannerIframe(el) {
    if (!el || el.tagName !== 'IFRAME') return false;
    if (el.classList.contains('goog-te-banner-frame')) return true;
    if (el.className && String(el.className).indexOf('VIpgJd-') !== -1) return true;
    if (el.id && String(el.id).indexOf('container') !== -1) return true;
    if (el.classList.contains('skiptranslate') && el.getAttribute('src') === '#') return true;
    return false;
  }

  function isGtTopChrome(el) {
    if (!el || isInsideGtFab(el)) return false;
    if (el.tagName === 'IFRAME') return isGtBannerIframe(el);
    if (el.tagName === 'DIV' && el.classList.contains('skiptranslate') && el.parentElement === document.body) {
      return !!el.querySelector(
        'iframe.goog-te-banner-frame, iframe[class*="VIpgJd-"], iframe[id*="container"], iframe.skiptranslate[src="#"]'
      );
    }
    return false;
  }

  function applyGtChromeHide(el) {
    el.style.setProperty('display', 'none', 'important');
    el.style.setProperty('visibility', 'hidden', 'important');
    el.style.setProperty('height', '0', 'important');
    el.style.setProperty('width', '0', 'important');
    el.style.setProperty('overflow', 'hidden', 'important');
  }

  function hideGtTopChrome() {
    document.querySelectorAll('body > div.skiptranslate, body > iframe.skiptranslate, iframe').forEach(function (el) {
      if (!isGtTopChrome(el)) return;
      applyGtChromeHide(el);
    });
    document.body.style.setProperty('top', '0', 'important');
    document.body.style.setProperty('margin-top', '0', 'important');
  }

  function watchGtTopChrome() {
    hideGtTopChrome();
    if (window.__rocbGtChromeObserver) return;
    window.__rocbGtChromeObserver = new MutationObserver(hideGtTopChrome);
    window.__rocbGtChromeObserver.observe(document.body, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ['style', 'class'],
    });
  }

  function setupFab() {
    var btn = document.getElementById('rocbGtToggle');
    var panel = document.getElementById('rocbGtPanel');
    var fab = document.getElementById('rocbGtFab');
    if (!btn || !panel) return;

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = !fab.classList.contains('is-open');
      fab.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      panel.setAttribute('aria-hidden', open ? 'false' : 'true');
      if (open) {
        populateLangSelect();
        wireLangSelect();
        loadGtScript();
        setTimeout(function () {
          var sel = document.getElementById('rocbGtLangSelect');
          if (sel) sel.focus();
        }, 150);
      }
    });

    document.addEventListener('click', function (e) {
      if (!fab.classList.contains('is-open')) return;
      if (fab.contains(e.target)) return;
      fab.classList.remove('is-open');
      btn.setAttribute('aria-expanded', 'false');
      panel.setAttribute('aria-hidden', 'true');
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && fab.classList.contains('is-open')) {
        fab.classList.remove('is-open');
        btn.setAttribute('aria-expanded', 'false');
        panel.setAttribute('aria-hidden', 'true');
      }
    });
  }

  function boot() {
    populateLangSelect();
    wireLangSelect();
    setupFab();
    watchGtTopChrome();
    loadGtScript();
  }

  global.rocbGtHideTopChrome = hideGtTopChrome;
  global.rocbGtBoot = boot;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})(window);
