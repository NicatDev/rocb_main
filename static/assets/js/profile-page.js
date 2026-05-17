(function () {
  function getCsrfToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    if (match) return decodeURIComponent(match[1]);
    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    return input ? input.value : '';
  }

  function trimValue(val) {
    return val == null ? '' : String(val).trim();
  }

  function updateEmptyState(row) {
    const valueEl = row.querySelector('.profile-field-value');
    const emptyEl = row.querySelector('.profile-field-empty');
    if (!valueEl || !emptyEl) return;
    const hasValue = trimValue(valueEl.textContent) !== '';
    valueEl.classList.toggle('is-hidden', !hasValue);
    emptyEl.classList.toggle('is-hidden', hasValue);
  }

  function updateDisplayName() {
    const root = document.getElementById('profilePageRoot');
    if (!root) return;
    const first = trimValue(
      root.querySelector('[data-field="first_name"] .profile-field-value')?.textContent
    );
    const last = trimValue(
      root.querySelector('[data-field="last_name"] .profile-field-value')?.textContent
    );
    const el = document.getElementById('profileDisplayName');
    if (el) {
      el.textContent = [first, last].filter(Boolean).join(' ') || '—';
    }
  }

  function showToast(message, isError) {
    const card = document.querySelector('.profile-details-card');
    if (!card) return;
    const existing = card.querySelector('.profile-toast--flash');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = `profile-toast profile-toast--flash profile-toast--${isError ? 'error' : 'success'}`;
    toast.setAttribute('role', 'alert');
    toast.textContent = message;
    card.insertBefore(toast, card.firstChild);
    setTimeout(() => toast.remove(), 4000);
  }

  function enterEditMode(row) {
    document.querySelectorAll('.profile-field-row.is-editing').forEach((other) => {
      if (other !== row) exitEditMode(other, true);
    });

    const display = row.querySelector('.profile-field-display');
    const edit = row.querySelector('.profile-field-edit');
    const input = row.querySelector('.profile-field-input');
    const valueEl = row.querySelector('.profile-field-value');
    const err = row.querySelector('.profile-field-error');

    if (!display || !edit || !input) return;

    input.value = trimValue(valueEl?.textContent || '');
    display.classList.add('is-hidden');
    edit.classList.remove('is-hidden');
    row.classList.add('is-editing');
    if (err) {
      err.classList.add('is-hidden');
      err.textContent = '';
    }
    input.focus();
  }

  function exitEditMode(row, revert) {
    const display = row.querySelector('.profile-field-display');
    const edit = row.querySelector('.profile-field-edit');
    const input = row.querySelector('.profile-field-input');
    const valueEl = row.querySelector('.profile-field-value');

    if (revert && valueEl && input) {
      input.value = trimValue(valueEl.textContent);
    }

    display?.classList.remove('is-hidden');
    edit?.classList.add('is-hidden');
    row.classList.remove('is-editing');
  }

  async function saveField(row) {
    const root = document.getElementById('profilePageRoot');
    const field = row.dataset.field;
    const input = row.querySelector('.profile-field-input');
    const valueEl = row.querySelector('.profile-field-value');
    const err = row.querySelector('.profile-field-error');
    const saveBtn = row.querySelector('.profile-field-btn--save');

    if (!root || !field || !input) return;

    const url = root.dataset.fieldUrl;
    const value = input.value;

    if (saveBtn) saveBtn.disabled = true;
    if (err) {
      err.classList.add('is-hidden');
      err.textContent = '';
    }

    try {
      const res = await fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({ field, value }),
      });

      let data = {};
      try {
        data = await res.json();
      } catch (e) {
        /* ignore */
      }

      if (!res.ok || !data.success) {
        const msg = data.message || 'Could not save. Please try again.';
        if (err) {
          err.textContent = msg;
          err.classList.remove('is-hidden');
        }
        return;
      }

      if (valueEl) {
        valueEl.textContent = trimValue(data.value);
      }
      input.value = trimValue(data.value);
      updateEmptyState(row);
      exitEditMode(row, false);

      if (field === 'first_name' || field === 'last_name') {
        updateDisplayName();
      }

      showToast('Saved successfully.', false);
    } catch (e) {
      if (err) {
        err.textContent = 'Could not save. Please try again.';
        err.classList.remove('is-hidden');
      }
    } finally {
      if (saveBtn) saveBtn.disabled = false;
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    const root = document.getElementById('profilePageRoot');
    if (!root) return;

    root.querySelectorAll('.profile-field-row[data-editable="true"]').forEach(updateEmptyState);
    updateDisplayName();

    const fileInput = document.getElementById('profile-picture-input');
    if (fileInput) {
      fileInput.addEventListener('change', function () {
        if (this.files && this.files.length) {
          document.getElementById('profile-avatar-upload-form')?.submit();
        }
      });
    }

    root.addEventListener('click', function (evt) {
      const editBtn = evt.target.closest('.profile-field-btn--edit');
      const saveBtn = evt.target.closest('.profile-field-btn--save');
      const cancelBtn = evt.target.closest('.profile-field-btn--cancel');
      const row = evt.target.closest('.profile-field-row[data-editable="true"]');

      if (editBtn && row) {
        evt.preventDefault();
        enterEditMode(row);
        return;
      }
      if (saveBtn && row) {
        evt.preventDefault();
        saveField(row);
        return;
      }
      if (cancelBtn && row) {
        evt.preventDefault();
        exitEditMode(row, true);
      }
    });

    root.addEventListener('keydown', function (evt) {
      const row = evt.target.closest('.profile-field-row.is-editing');
      if (!row) return;
      if (evt.key === 'Enter' && evt.target.classList.contains('profile-field-input')) {
        evt.preventDefault();
        saveField(row);
      }
      if (evt.key === 'Escape') {
        exitEditMode(row, true);
      }
    });
  });
})();
