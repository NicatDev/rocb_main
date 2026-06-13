(function (window, document) {
  'use strict';

  var STORAGE_KEY = 'openai_page_lang';
  var ORIGINAL_ATTR = 'data-openai-original-html';
  var CONTENT_SELECTOR = 'main#primary, main.site-main';
  var API_URL = '/api/translate/';
  var loadingEl = null;

  function getLanguageFromUrl() {
    var path = window.location.pathname;
    if (path === '/ru' || path.indexOf('/ru/') === 0) return 'ru';
    if (path === '/en' || path.indexOf('/en/') === 0) return 'en';
    return null;
  }

  function pathWithLanguagePrefix(langCode) {
    var path = window.location.pathname;
    var bare = path;

    if (bare.indexOf('/ru/') === 0) bare = bare.substring(3) || '/';
    else if (bare.indexOf('/en/') === 0) bare = bare.substring(3) || '/';
    else if (bare === '/ru' || bare === '/en') bare = '/';

    if (langCode === 'ru') return '/ru' + (bare === '/' ? '' : bare);
    if (langCode === 'en') return '/en' + (bare === '/' ? '' : bare);
    return bare === '' ? '/' : bare;
  }

  function getPageSourceLanguage() {
    var urlLang = getLanguageFromUrl();
    if (urlLang) return urlLang;
    var lang = (document.documentElement.getAttribute('lang') || 'en').toLowerCase();
    if (lang.indexOf('ru') === 0) return 'ru';
    return 'en';
  }

  function resolveActiveLanguage() {
    return getLanguageFromUrl() || (localStorage.getItem(STORAGE_KEY) || 'en').toLowerCase();
  }

  function getCsrfToken() {
    var csrfMeta = document.querySelector('meta[name="csrf-token"]');
    if (csrfMeta) return csrfMeta.getAttribute('content');

    var csrfTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (csrfTokenInput) return csrfTokenInput.value;

    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var parts = cookies[i].trim().split('=');
      if (parts[0] === 'csrftoken') return decodeURIComponent(parts[1] || '');
    }
    return null;
  }

  function getContentElements() {
    var nodes = document.querySelectorAll(CONTENT_SELECTOR);
    return nodes.length ? Array.prototype.slice.call(nodes) : [];
  }

  function ensureOriginalHtml(el) {
    if (!el.hasAttribute(ORIGINAL_ATTR)) {
      el.setAttribute(ORIGINAL_ATTR, el.innerHTML);
    }
    return el.getAttribute(ORIGINAL_ATTR);
  }

  function showLoading() {
    if (loadingEl) return;
    loadingEl = document.createElement('div');
    loadingEl.className = 'openai-translate-loading';
    loadingEl.innerHTML =
      '<div class="openai-translate-loading__panel">' +
      '<div class="openai-translate-loading__spinner"></div>' +
      '<p>Translating page…</p></div>';
    document.body.appendChild(loadingEl);
  }

  function hideLoading() {
    if (loadingEl && loadingEl.parentNode) {
      loadingEl.parentNode.removeChild(loadingEl);
    }
    loadingEl = null;
  }

  function updateFlagState(langCode) {
    document.querySelectorAll('.lang-flag-btn, .mobile-lang-flag-btn').forEach(function (btn) {
      var isActive = btn.dataset.lang === langCode;
      btn.classList.toggle('is-active', isActive);
      btn.removeAttribute('style');
    });
  }

  function translateHtml(html, targetLang, sourceLang) {
    var csrf = getCsrfToken();
    var headers = { 'Content-Type': 'application/json' };
    if (csrf) headers['X-CSRFToken'] = csrf;

    return fetch(API_URL, {
      method: 'POST',
      headers: headers,
      credentials: 'same-origin',
      body: JSON.stringify({
        html: html,
        source_language: sourceLang,
        target_language: targetLang,
      }),
    }).then(function (response) {
      return response.json().then(function (data) {
        if (!response.ok) {
          throw new Error(data.detail || 'Translation failed');
        }
        return data.html;
      });
    });
  }

  function restoreOriginal() {
    getContentElements().forEach(function (el) {
      var original = el.getAttribute(ORIGINAL_ATTR);
      if (original != null) {
        el.innerHTML = original;
      }
    });
  }

  function switchLanguage(langCode) {
    langCode = (langCode || 'en').toLowerCase();
    localStorage.setItem(STORAGE_KEY, langCode);

    var nextPath = pathWithLanguagePrefix(langCode);
    if (nextPath !== window.location.pathname) {
      window.location.assign(nextPath + window.location.search + window.location.hash);
      return Promise.resolve();
    }

    updateFlagState(langCode);
    document.documentElement.setAttribute('lang', langCode);

    if (getLanguageFromUrl() === langCode) {
      return Promise.resolve();
    }

    if (langCode === 'en') {
      restoreOriginal();
      return Promise.resolve();
    }

    var sourceLang = getPageSourceLanguage();
    var elements = getContentElements();
    if (!elements.length) {
      return Promise.resolve();
    }

    showLoading();
    var chain = Promise.resolve();

    elements.forEach(function (el) {
      chain = chain.then(function () {
        var original = ensureOriginalHtml(el);
        return translateHtml(original, langCode, sourceLang).then(function (translated) {
          el.innerHTML = translated;
        });
      });
    });

    return chain
      .catch(function (err) {
        console.error('OpenAI translate error:', err);
        window.alert(err.message || 'Could not translate this page.');
      })
      .finally(hideLoading);
  }

  function initFromStorage() {
    var active = resolveActiveLanguage();
    localStorage.setItem(STORAGE_KEY, active);
    updateFlagState(active);
    document.documentElement.setAttribute('lang', active);

    if (getLanguageFromUrl()) {
      return;
    }

    if (active !== 'en') {
      switchLanguage(active);
    }
  }

  window.OpenAITranslate = {
    switchLanguage: switchLanguage,
    restoreOriginal: restoreOriginal,
    init: initFromStorage,
    getLanguageFromUrl: getLanguageFromUrl,
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFromStorage);
  } else {
    initFromStorage();
  }
})(window, document);
