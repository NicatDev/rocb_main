(function (window, document) {
  'use strict';

  var STORAGE_KEY = 'openai_page_lang';
  var ORIGINAL_ATTR = 'data-openai-original-html';
  var ORIGINAL_LANG_ATTR = 'data-openai-original-lang';
  var CONTENT_SELECTOR = 'main#primary, main.site-main';
  var API_URL = '/api/translate/';
  var CLIENT_CHUNK_SIZE = 3500;
  var loadingEl = null;

  function splitHtmlChunks(html, maxLen) {
    maxLen = maxLen || CLIENT_CHUNK_SIZE;
    if (!html || html.length <= maxLen) return [html];
    var chunks = [];
    var start = 0;
    while (start < html.length) {
      var end = Math.min(start + maxLen, html.length);
      if (end < html.length) {
        var splitAt = html.lastIndexOf('</', start, end);
        if (splitAt > start + maxLen / 3) {
          end = splitAt + html.slice(splitAt).indexOf('>') + 1;
        }
      }
      chunks.push(html.slice(start, end));
      start = end;
    }
    return chunks;
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

  function detectPageLanguage() {
    var lang = (document.documentElement.getAttribute('lang') || 'en').toLowerCase();
    if (lang.indexOf('ru') === 0) return 'ru';
    return 'en';
  }

  function ensureOriginalHtml(el) {
    if (!el.hasAttribute(ORIGINAL_ATTR)) {
      el.setAttribute(ORIGINAL_ATTR, el.innerHTML);
      el.setAttribute(ORIGINAL_LANG_ATTR, detectPageLanguage());
    }
    return el.getAttribute(ORIGINAL_ATTR);
  }

  function getOriginalSourceLang(el) {
    return el.getAttribute(ORIGINAL_LANG_ATTR) || 'en';
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

  function translateHtmlRequest(html, targetLang, sourceLang) {
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

  function translateHtmlInChunks(html, targetLang, sourceLang) {
    var chunks = splitHtmlChunks(html);
    if (chunks.length === 1) {
      return translateHtmlRequest(html, targetLang, sourceLang);
    }
    var chain = Promise.resolve([]);
    chunks.forEach(function (chunk) {
      chain = chain.then(function (parts) {
        return translateHtmlRequest(chunk, targetLang, sourceLang).then(function (translated) {
          parts.push(translated);
          return parts;
        });
      });
    });
    return chain.then(function (parts) {
      return parts.join('');
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
    document.documentElement.setAttribute('lang', 'en');
    updateFlagState('en');
  }

  function switchLanguage(langCode) {
    langCode = (langCode || 'en').toLowerCase();
    localStorage.setItem(STORAGE_KEY, langCode);
    updateFlagState(langCode);
    document.documentElement.setAttribute('lang', langCode);

    if (langCode === 'en') {
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
        var sourceLang = getOriginalSourceLang(el);
        return translateHtmlInChunks(original, langCode, sourceLang).then(function (translated) {
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
    var saved = (localStorage.getItem(STORAGE_KEY) || 'en').toLowerCase();
    updateFlagState(saved);
    document.documentElement.setAttribute('lang', saved);

    if (saved !== 'en') {
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
