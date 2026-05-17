(function () {
  function getCsrfToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : '';
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text == null ? '' : String(text);
    return div.innerHTML;
  }

  function countryJsonUrl(id) {
    const tpl = document.getElementById('countryApiConfig')?.dataset.jsonUrlTemplate;
    if (!tpl) return `/region/country/${id}/json/`;
    return tpl.replace('0', String(id));
  }

  function countryEditUrl(id) {
    const tpl = document.getElementById('countryApiConfig')?.dataset.editUrlTemplate;
    if (!tpl) return `/region/country/${id}/edit/`;
    return tpl.replace('0', String(id));
  }

  function renderViewModal(data) {
    const body = document.getElementById('countryViewModalBody');
    const title = document.getElementById('countryViewModalLabel');
    const editBtn = document.getElementById('countryViewEditBtn');
    if (!body || !title) return;

    title.textContent = data.title || '';
    let html = '<div class="country-view-header">';
    if (data.flag_url) {
      html += `<img class="country-view-flag" src="${escapeHtml(data.flag_url)}" alt="" width="80" height="60">`;
    } else if (data.code) {
      html += `<span class="flag">${escapeHtml(data.code)}</span>`;
    }
    html += '</div>';

    if (data.description) {
      html += `<div class="country-view-block"><h6>Description</h6><p>${escapeHtml(data.description).replace(/\n/g, '<br>')}</p></div>`;
    }
    if (data.href) {
      html += `<div class="country-view-block"><h6>Website</h6><p><a href="${escapeHtml(data.href)}" target="_blank" rel="noopener noreferrer">${escapeHtml(data.href)}</a></p></div>`;
    }
    if (data.additional_information && data.additional_information.length) {
      html += '<div class="country-view-block"><h6>Additional information</h6><dl class="country-info-dl">';
      data.additional_information.forEach((row) => {
        html += `<dt>${escapeHtml(row.key)}</dt><dd>${escapeHtml(row.value).replace(/\n/g, '<br>')}</dd>`;
      });
      html += '</dl></div>';
    }
    if (!data.description && !(data.additional_information || []).length && !data.href) {
      html += '<p class="text-muted">No additional information yet.</p>';
    }
    body.innerHTML = html;

    if (editBtn) {
      if (data.can_edit) {
        editBtn.classList.remove('d-none');
        editBtn.dataset.countryId = data.id;
      } else {
        editBtn.classList.add('d-none');
        delete editBtn.dataset.countryId;
      }
    }
  }

  async function openViewModal(countryId) {
    const modalEl = document.getElementById('countryViewModal');
    if (!modalEl || !window.bootstrap) return;
    const body = document.getElementById('countryViewModalBody');
    if (body) body.innerHTML = '<div class="text-center py-4 text-muted">Loading...</div>';
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    modal.show();
    try {
      const res = await fetch(countryJsonUrl(countryId), { credentials: 'same-origin' });
      if (!res.ok) throw new Error('Failed to load');
      const data = await res.json();
      renderViewModal(data);
    } catch (e) {
      if (body) body.innerHTML = '<div class="alert alert-danger">Could not load country details.</div>';
    }
  }

  async function openEditModal(countryId) {
    const modalEl = document.getElementById('countryEditModal');
    if (!modalEl || !window.bootstrap) return;
    const body = document.getElementById('countryEditModalBody');
    if (body) body.innerHTML = '<div class="text-center py-4 text-muted">Loading...</div>';
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    modal.show();
    try {
      const res = await fetch(countryEditUrl(countryId), { credentials: 'same-origin' });
      if (!res.ok) throw new Error('Forbidden');
      body.innerHTML = await res.text();
      bindEditForm(countryId);
    } catch (e) {
      if (body) body.innerHTML = '<div class="alert alert-danger">Could not load edit form.</div>';
    }
  }

  function bindEditForm(countryId) {
    const form = document.getElementById('countryOwnerEditForm');
    if (!form) return;
    form.addEventListener('submit', async (evt) => {
      evt.preventDefault();
      const errBox = document.getElementById('countryEditFormErrors');
      if (errBox) {
        errBox.classList.add('d-none');
        errBox.textContent = '';
      }
      const fd = new FormData(form);
      try {
        const res = await fetch(countryEditUrl(countryId), {
          method: 'POST',
          body: fd,
          credentials: 'same-origin',
          headers: { 'X-CSRFToken': getCsrfToken() },
        });
        const data = await res.json();
        if (!res.ok || !data.success) {
          const msg = data.errors ? JSON.stringify(data.errors) : 'Save failed';
          if (errBox) {
            errBox.textContent = msg;
            errBox.classList.remove('d-none');
          }
          return;
        }
        const editModal = bootstrap.Modal.getInstance(document.getElementById('countryEditModal'));
        if (editModal) editModal.hide();
        await openViewModal(countryId);
      } catch (e) {
        if (errBox) {
          errBox.textContent = 'Save failed.';
          errBox.classList.remove('d-none');
        }
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    const grid = document.getElementById('memberCountryGrid');
    if (!grid) return;

    grid.addEventListener('click', function (evt) {
      const editBtn = evt.target.closest('.country-btn-edit');
      if (editBtn) {
        evt.preventDefault();
        evt.stopPropagation();
        openEditModal(editBtn.dataset.countryId);
        return;
      }
      const viewBtn = evt.target.closest('.country-btn-view');
      if (viewBtn) {
        evt.preventDefault();
        evt.stopPropagation();
        openViewModal(viewBtn.dataset.countryId);
        return;
      }
      const card = evt.target.closest('.country-card');
      if (card && card.dataset.countryId) {
        openViewModal(card.dataset.countryId);
      }
    });

    grid.addEventListener('keydown', function (evt) {
      if (evt.key !== 'Enter' && evt.key !== ' ') return;
      const card = evt.target.closest('.country-card');
      if (!card || !card.dataset.countryId) return;
      evt.preventDefault();
      openViewModal(card.dataset.countryId);
    });

    const viewEditBtn = document.getElementById('countryViewEditBtn');
    if (viewEditBtn) {
      viewEditBtn.addEventListener('click', function () {
        const id = viewEditBtn.dataset.countryId;
        if (!id) return;
        const viewModal = bootstrap.Modal.getInstance(document.getElementById('countryViewModal'));
        if (viewModal) viewModal.hide();
        openEditModal(id);
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
