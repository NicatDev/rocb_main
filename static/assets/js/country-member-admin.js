(function () {
  const MODAL_IDS = ['countryViewModal', 'countryEditModal'];

  function cleanupModalArtifacts() {
    document.body.classList.remove('modal-open');
    document.body.style.removeProperty('overflow');
    document.body.style.removeProperty('padding-right');
    document.querySelectorAll('.modal-backdrop').forEach((b) => b.remove());
    document.querySelector('.body-overlay')?.classList.remove('opened');
  }

  function getCsrfToken() {
    const fromCookie = document.cookie.match(/csrftoken=([^;]+)/);
    if (fromCookie) {
      return decodeURIComponent(fromCookie[1]);
    }
    const input = document.querySelector('#countryOwnerEditForm input[name="csrfmiddlewaretoken"]');
    return input ? input.value : '';
  }

  function escapeHtml(text) {
    const el = document.createElement('div');
    el.textContent = text == null ? '' : String(text);
    return el.innerHTML;
  }

  function resolveUrl(el, kind) {
    if (!el) return null;
    if (kind === 'json') {
      return el.dataset.jsonUrl || el.closest('.country-card')?.dataset.jsonUrl;
    }
    return el.dataset.editUrl || el.closest('.country-card')?.dataset.editUrl;
  }

  function initCountryModals() {
    MODAL_IDS.forEach((id) => {
      const el = document.getElementById(id);
      if (!el) return;
      if (el.parentElement !== document.body) {
        document.body.appendChild(el);
      }

      el.addEventListener('show.bs.modal', () => {
        document.querySelector('.body-overlay')?.classList.remove('opened');
      });

      el.addEventListener('shown.bs.modal', () => {
        document.querySelector('.modal-backdrop')?.classList.add('country-modal-backdrop');
      });

      el.addEventListener('hidden.bs.modal', cleanupModalArtifacts);
    });
  }

  function getModalInstance(modalEl) {
    if (!modalEl || !window.bootstrap) return null;
    return bootstrap.Modal.getOrCreateInstance(modalEl, {
      backdrop: true,
      keyboard: true,
      focus: true,
    });
  }

  function getModalI18n() {
    const el = document.getElementById('countryModalI18n');
    return {
      description: el?.dataset.labelDescription || 'Description',
      website: el?.dataset.labelWebsite || 'Website',
      entries: el?.dataset.labelEntries || 'Additional entries',
      label: el?.dataset.labelLabel || 'Label',
      information: el?.dataset.labelInformation || 'Information',
      empty: el?.dataset.empty || 'No information available yet.',
    };
  }

  function renderViewModal(data) {
    const body = document.getElementById('countryViewModalBody');
    const title = document.getElementById('countryViewModalLabel');
    const subtitle = document.getElementById('countryViewModalSubtitle');
    const editBtn = document.getElementById('countryViewEditBtn');
    if (!body || !title) return;

    const i18n = getModalI18n();

    title.textContent = data.title || '';
    if (subtitle) {
      subtitle.textContent = data.code ? String(data.code).toUpperCase() : '';
    }

    let html = '<div class="country-view-layout"><header class="country-view-hero">';
    if (data.flag_url) {
      html += `<img class="country-view-flag" src="${escapeHtml(data.flag_url)}" alt="">`;
    } else if (data.code) {
      html += `<span class="country-view-flag-fallback">${escapeHtml(data.code)}</span>`;
    }
    if (data.title) {
      html += `<h3 class="country-view-hero-title">${escapeHtml(data.title)}</h3>`;
    }
    html += '</header>';

    let hasContent = false;

    if (data.description) {
      hasContent = true;
      html += `<article class="country-view-card"><span class="country-view-card-label">${escapeHtml(i18n.description)}</span><div class="country-view-card-body">${escapeHtml(data.description).replace(/\n/g, '<br>')}</div></article>`;
    }
    if (data.href) {
      hasContent = true;
      html += `<a class="country-view-card country-view-card--link" href="${escapeHtml(data.href)}" target="_blank" rel="noopener noreferrer"><span class="country-view-card-label">${escapeHtml(i18n.website)}</span><span class="country-view-link-text">${escapeHtml(data.href)}</span><i class="fa-regular fa-arrow-up-right-from-square country-view-link-icon" aria-hidden="true"></i></a>`;
    }
    const entries = (data.additional_information || []).filter((row) => row.key || row.value);
    if (entries.length) {
      hasContent = true;
      html += '<section class="country-view-entries-section"><div class="country-view-entries">';
      entries.forEach((row, index) => {
        html += `<article class="country-view-entry" style="--entry-delay:${index * 40}ms"><div class="country-view-entry-head"><span class="country-view-entry-index">${index + 1}</span><span class="country-view-entry-label-title">${escapeHtml(i18n.label)}</span></div><p class="country-view-entry-label-text">${escapeHtml(row.key)}</p><span class="country-view-entry-info-title">${escapeHtml(i18n.information)}</span><p class="country-view-entry-info-text">${escapeHtml(row.value).replace(/\n/g, '<br>')}</p></article>`;
      });
      html += '</div></section>';
    }

    if (!hasContent) {
      html += `<p class="country-view-empty">${escapeHtml(i18n.empty)}</p>`;
    }

    html += '</div>';
    body.innerHTML = html;

    if (editBtn) {
      if (data.can_edit) {
        editBtn.classList.remove('d-none');
        editBtn.dataset.countryId = data.id;
        if (data.edit_url) {
          editBtn.dataset.editUrl = data.edit_url;
        }
      } else {
        editBtn.classList.add('d-none');
        delete editBtn.dataset.countryId;
        delete editBtn.dataset.editUrl;
      }
    }
  }

  async function openViewModal(countryId, sourceEl) {
    const modalEl = document.getElementById('countryViewModal');
    const modal = getModalInstance(modalEl);
    if (!modal) return;

    const url = resolveUrl(sourceEl, 'json');
    if (!url) return;

    const body = document.getElementById('countryViewModalBody');
    if (body) {
      body.innerHTML = '<div class="country-modal-loading">Loading…</div>';
    }
    modal.show();

    try {
      const res = await fetch(url, { credentials: 'same-origin' });
      if (!res.ok) throw new Error('Failed');
      const data = await res.json();
      const editUrl = resolveUrl(sourceEl, 'edit');
      if (editUrl) {
        data.edit_url = editUrl;
      }
      renderViewModal(data);
    } catch (e) {
      if (body) {
        body.innerHTML = '<p class="country-view-empty">Could not load country details. Please try again.</p>';
      }
    }
  }

  function editErrorMessage(res, data) {
    if (res.status === 403 && data?.error === 'not_owner') {
      return data.message || 'You are not the owner of this country. Ask an admin to set you as Owner in Django admin.';
    }
    if (res.status === 401 || res.status === 403) {
      return 'Please log in with the account that owns this country.';
    }
    return 'Could not open the edit form. Please try again.';
  }

  async function openEditModal(countryId, sourceEl) {
    const modalEl = document.getElementById('countryEditModal');
    const modal = getModalInstance(modalEl);
    if (!modal) return;

    const url = resolveUrl(sourceEl, 'edit');
    if (!url) return;

    const body = document.getElementById('countryEditModalBody');
    if (body) {
      body.innerHTML = '<div class="country-modal-loading">Loading…</div>';
    }
    modal.show();

    try {
      const res = await fetch(url, { credentials: 'same-origin' });
      const contentType = res.headers.get('content-type') || '';

      if (res.redirected || contentType.includes('text/html') && !contentType.includes('countryOwnerEditForm') && res.url && res.url.includes('login')) {
        if (body) {
          body.innerHTML = '<p class="country-view-empty">Please <a href="/login/">log in</a> to edit this country.</p>';
        }
        return;
      }

      if (!res.ok) {
        let data = {};
        try {
          data = await res.json();
        } catch (err) {
          /* ignore */
        }
        if (body) {
          body.innerHTML = `<p class="country-view-empty">${escapeHtml(editErrorMessage(res, data))}</p>`;
        }
        return;
      }

      const html = await res.text();
      if (!html.includes('countryOwnerEditForm')) {
        if (body) {
          body.innerHTML = '<p class="country-view-empty">Unexpected response. Please refresh and log in again.</p>';
        }
        return;
      }

      body.innerHTML = html;
      bindEditForm(countryId, url);
      applyCountryEditLang(document.getElementById('countryOwnerEditForm'), 'en');
      setEditModalSubtitle(countryId);
    } catch (e) {
      if (body) {
        body.innerHTML = '<p class="country-view-empty">Could not load edit form.</p>';
      }
    }
  }

  function setEditModalSubtitle(countryId) {
    const subtitle = document.getElementById('countryEditModalSubtitle');
    if (!subtitle) return;
    const defaultText = subtitle.dataset.defaultSubtitle || subtitle.textContent;
    const card = document.querySelector(`.country-card[data-country-id="${countryId}"]`);
    const name = card?.querySelector('.country-name')?.textContent?.trim();
    subtitle.textContent = name || defaultText;
  }

  function applyCountryEditLang(form, lang) {
    if (!form) return;
    const active = lang === 'ru' ? 'ru' : 'en';
    form.dataset.activeLang = active;
    form.classList.remove('is-country-lang-en', 'is-country-lang-ru');
    form.classList.add(active === 'ru' ? 'is-country-lang-ru' : 'is-country-lang-en');

    form.querySelectorAll('.country-edit-tab[data-edit-lang]').forEach((tab) => {
      const on = tab.dataset.editLang === active;
      tab.classList.toggle('is-active', on);
      tab.setAttribute('aria-selected', on ? 'true' : 'false');
    });

    form.querySelectorAll('.country-field--en').forEach((el) => {
      el.hidden = active !== 'en';
    });
    form.querySelectorAll('.country-field--ru').forEach((el) => {
      el.hidden = active !== 'ru';
    });
  }

  function initEditModalLanguageDelegation() {
    const modal = document.getElementById('countryEditModal');
    if (!modal || modal.dataset.langTabsReady) return;
    modal.dataset.langTabsReady = '1';

    modal.addEventListener('click', (evt) => {
      const tab = evt.target.closest('.country-edit-tab[data-edit-lang]');
      if (!tab) return;
      const form = document.getElementById('countryOwnerEditForm');
      if (!form || !form.contains(tab)) return;
      evt.preventDefault();
      evt.stopPropagation();
      applyCountryEditLang(form, tab.dataset.editLang);
    });
  }

  function bindEditForm(countryId, editUrl) {
    const form = document.getElementById('countryOwnerEditForm');
    if (!form) return;

    const handler = async (evt) => {
      evt.preventDefault();
      const errBox = document.getElementById('countryEditFormErrors');
      if (errBox) {
        errBox.classList.add('d-none');
        errBox.textContent = '';
      }
      const fd = new FormData(form);
      const token = getCsrfToken();
      const headers = {};
      if (token) {
        headers['X-CSRFToken'] = token;
      }
      try {
        const res = await fetch(editUrl, {
          method: 'POST',
          body: fd,
          credentials: 'same-origin',
          headers,
        });
        let data = {};
        try {
          data = await res.json();
        } catch (err) {
          /* non-json */
        }
        if (!res.ok || !data.success) {
          const msg =
            data?.message ||
            (data?.errors ? 'Please check the form fields.' : editErrorMessage(res, data));
          if (errBox) {
            errBox.textContent = msg;
            errBox.classList.remove('d-none');
          }
          return;
        }
        const editModal = bootstrap.Modal.getInstance(document.getElementById('countryEditModal'));
        if (editModal) editModal.hide();
        const card = document.querySelector(`.country-card[data-country-id="${countryId}"]`);
        setTimeout(() => openViewModal(countryId, card), 300);
      } catch (e) {
        if (errBox) {
          errBox.textContent = 'Save failed. Please try again.';
          errBox.classList.remove('d-none');
        }
      }
    };

    if (form._countrySubmitHandler) {
      form.removeEventListener('submit', form._countrySubmitHandler);
    }
    form._countrySubmitHandler = handler;
    form.addEventListener('submit', handler);
  }

  document.addEventListener('DOMContentLoaded', function () {
    cleanupModalArtifacts();
    initCountryModals();
    initEditModalLanguageDelegation();

    const grid = document.getElementById('memberCountryGrid');
    if (!grid) return;

    grid.addEventListener('click', function (evt) {
      const editBtn = evt.target.closest('.country-btn-edit');
      if (editBtn) {
        evt.preventDefault();
        evt.stopPropagation();
        openEditModal(editBtn.dataset.countryId, editBtn);
        return;
      }

      const card = evt.target.closest('.country-card');
      if (card && card.dataset.countryId) {
        openViewModal(card.dataset.countryId, card);
      }
    });

    grid.addEventListener('keydown', function (evt) {
      if (evt.key !== 'Enter' && evt.key !== ' ') return;
      const card = evt.target.closest('.country-card');
      if (!card || !card.dataset.countryId) return;
      evt.preventDefault();
      openViewModal(card.dataset.countryId, card);
    });

    const viewEditBtn = document.getElementById('countryViewEditBtn');
    if (viewEditBtn) {
      viewEditBtn.addEventListener('click', function () {
        const id = viewEditBtn.dataset.countryId;
        if (!id) return;
        const viewModal = bootstrap.Modal.getInstance(document.getElementById('countryViewModal'));
        if (viewModal) viewModal.hide();
        setTimeout(() => openEditModal(id, viewEditBtn), 300);
      });
    }

    const searchInput = document.getElementById('countrySearchInput');
    if (searchInput) {
      searchInput.addEventListener('keyup', function (event) {
        const term = event.target.value.toLowerCase();
        document.querySelectorAll('#memberCountryGrid .country-card').forEach(function (card) {
          const name = card.querySelector('.country-name');
          const text = name ? name.textContent.toLowerCase() : '';
          card.style.display = text.includes(term) ? '' : 'none';
        });
      });
    }
  });
})();
