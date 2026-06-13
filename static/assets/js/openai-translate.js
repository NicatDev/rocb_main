(function (window, document) {
  'use strict';

  var STORAGE_KEY = 'openai_page_lang';
  var ORIGINAL_ATTR = 'data-openai-original-html';
  var SOURCE_LANG = 'en';
  var CONTENT_SELECTOR = 'main#primary, main.site-main';
  var API_URL = '/api/translate/';
  var loadingEl = null;

  function getSourceLanguage() {
    var lang = (document.documentElement.getAttribute('lang') || SOURCE_LANG).toLowerCase();
    return lang.indexOf('ru') === 0 ? 'ru' : 'en';
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
    document.querySelectorAll('.lang-flag-btn').forEach(function (btn) {
      var active = btn.dataset.lang === langCode;
      btn.style.opacity = active ? '1' : '0.55';
      btn.style.outline = active ? '2px solid #12579e' : 'none';
    });
  }

  function translateHtml(html, targetLang) {
    var csrf = getCsrfToken();
    var headers = { 'Content-Type': 'application/json' };
    if (csrf) headers['X-CSRFToken'] = csrf;

    return fetch(API_URL, {
      method: 'POST',
      headers: headers,
      credentials: 'same-origin',
      body: JSON.stringify({
        html: html,
        source_language: getSourceLanguage(),
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
    localStorage.setItem(STORAGE_KEY, 'en');
    updateFlagState('en');
    document.documentElement.setAttribute('lang', 'en');
  }

  function switchLanguage(langCode) {
    langCode = (langCode || 'en').toLowerCase();
    localStorage.setItem(STORAGE_KEY, langCode);
    document.documentElement.setAttribute('lang', langCode);

    if (langCode === 'en' || langCode === getSourceLanguage()) {
      restoreOriginal();
      return Promise.resolve();
    }

    var elements = getContentElements();
    if (!elements.length) {
      return Promise.resolve();
    }

    showLoading();
    var chain = Promise.resolve();

    elements.forEach(function (el) {
      chain = chain.then(function () {
        var original = ensureOriginalHtml(el);
        return translateHtml(original, langCode).then(function (translated) {
          el.innerHTML = translated;
        });
      });
    });

    return chain
      .then(function () {
        updateFlagState(langCode);
      })
      .catch(function (err) {
        console.error('OpenAI translate error:', err);
        window.alert(err.message || 'Could not translate this page.');
      })
      .finally(hideLoading);
  }

  function initFromStorage() {
    var saved = (localStorage.getItem(STORAGE_KEY) || 'en').toLowerCase();
    updateFlagState(saved);
    if (saved !== 'en' && saved !== getSourceLanguage()) {
      switchLanguage(saved);
    }
  }

  window.OpenAITranslate = {
    switchLanguage: switchLanguage,
    restoreOriginal: restoreOriginal,
    init: initFromStorage,
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFromStorage);
  } else {
    initFromStorage();
  }
})(window, document);
