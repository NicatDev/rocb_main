(function () {
  function getCsrfToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    if (match) return decodeURIComponent(match[1]);
    const input = document.querySelector('#changePasswordForm [name=csrfmiddlewaretoken]');
    return input ? input.value : '';
  }

  function getModal() {
    return document.getElementById('changePasswordModal');
  }

  function clearErrors(modal) {
    modal.querySelectorAll('.change-password-field__error').forEach((el) => {
      el.textContent = '';
      el.hidden = true;
    });
    modal.querySelectorAll('.change-password-input').forEach((input) => {
      input.classList.remove('is-invalid');
    });
    const formError = modal.querySelector('#changePasswordFormError');
    if (formError) {
      formError.textContent = '';
      formError.hidden = true;
    }
  }

  function setFieldError(modal, fieldName, message) {
    const wrap = modal.querySelector(`.change-password-field[data-field="${fieldName}"]`);
    if (!wrap) return;
    const input = wrap.querySelector('.change-password-input');
    const errorEl = wrap.querySelector('.change-password-field__error');
    if (input) input.classList.add('is-invalid');
    if (errorEl) {
      errorEl.textContent = message;
      errorEl.hidden = false;
    }
  }

  function setFormError(modal, message) {
    const formError = modal.querySelector('#changePasswordFormError');
    if (formError) {
      formError.textContent = message;
      formError.hidden = false;
    }
  }

  function resetPasswordVisibility(modal) {
    modal.querySelectorAll('[data-toggle-password]').forEach((btn) => {
      const inputId = btn.getAttribute('data-toggle-password');
      const input = document.getElementById(inputId);
      if (input) input.type = 'password';
      const icon = btn.querySelector('i');
      if (icon) {
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
      }
      btn.setAttribute('aria-label', modal.dataset.labelShow || 'Show password');
      btn.setAttribute('aria-pressed', 'false');
    });
  }

  function openChangePasswordModal() {
    const modal = getModal();
    if (!modal) return;

    const form = modal.querySelector('#changePasswordForm');
    if (form) form.reset();

    clearErrors(modal);
    resetPasswordVisibility(modal);

    modal.classList.add('is-open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';

    const firstInput = modal.querySelector('#cpOldPassword');
    if (firstInput) {
      window.setTimeout(() => firstInput.focus(), 80);
    }
  }

  function closeChangePasswordModal() {
    const modal = getModal();
    if (!modal) return;

    modal.classList.remove('is-open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';

    const submitBtn = modal.querySelector('#changePasswordSubmit');
    if (submitBtn) submitBtn.disabled = false;
    submitBtn?.classList.remove('is-loading');
  }

  function togglePasswordVisibility(button) {
    const modal = getModal();
    const inputId = button.getAttribute('data-toggle-password');
    const input = document.getElementById(inputId);
    if (!input) return;

    const icon = button.querySelector('i');
    const isHidden = input.type === 'password';
    input.type = isHidden ? 'text' : 'password';

    if (icon) {
      icon.classList.toggle('fa-eye', !isHidden);
      icon.classList.toggle('fa-eye-slash', isHidden);
    }

    const showLabel = modal?.dataset.labelShow || 'Show password';
    const hideLabel = modal?.dataset.labelHide || 'Hide password';
    button.setAttribute('aria-label', isHidden ? hideLabel : showLabel);
    button.setAttribute('aria-pressed', isHidden ? 'true' : 'false');
  }

  async function submitChangePassword(event) {
    event.preventDefault();
    const modal = getModal();
    if (!modal) return;

    const form = modal.querySelector('#changePasswordForm');
    const submitBtn = modal.querySelector('#changePasswordSubmit');
    if (!form || !submitBtn) return;

    clearErrors(modal);

    const formData = new FormData(form);
    submitBtn.disabled = true;
    submitBtn.classList.add('is-loading');

    try {
      const response = await fetch(modal.dataset.url, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCsrfToken(),
        },
        body: formData,
        credentials: 'same-origin',
      });

      let data = {};
      try {
        data = await response.json();
      } catch (parseError) {
        data = {};
      }

      if (response.ok && data.success) {
        closeChangePasswordModal();
        const message = data.message || modal.dataset.msgSuccess || 'Password updated successfully.';
        if (typeof window.showProfileToast === 'function') {
          window.showProfileToast(message, false);
        } else {
          window.alert(message);
        }
        return;
      }

      const errors = data.errors || {};
      Object.keys(errors).forEach((field) => {
        const msgs = errors[field];
        if (msgs && msgs.length) {
          setFieldError(modal, field, msgs[0]);
        }
      });

      const message = data.message || modal.dataset.msgGenericError || 'Could not update password.';
      if (!Object.keys(errors).length) {
        setFormError(modal, message);
      } else if (Object.keys(errors).length > 1) {
        setFormError(modal, message);
      }
    } catch (error) {
      setFormError(modal, modal.dataset.msgGenericError || 'Could not update password.');
    } finally {
      submitBtn.disabled = false;
      submitBtn.classList.remove('is-loading');
    }
  }

  function initChangePasswordModal() {
    if (window.__changePasswordModalInit) return;
    window.__changePasswordModalInit = true;

    const modal = getModal();
    if (!modal) return;

    modal.querySelectorAll('[data-close-change-password]').forEach((el) => {
      el.addEventListener('click', closeChangePasswordModal);
    });

    modal.querySelectorAll('[data-toggle-password]').forEach((btn) => {
      btn.addEventListener('click', () => togglePasswordVisibility(btn));
    });

    const form = modal.querySelector('#changePasswordForm');
    if (form) {
      form.addEventListener('submit', submitChangePassword);
    }

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && modal.classList.contains('is-open')) {
        closeChangePasswordModal();
      }
    });

    document.querySelectorAll('[data-open-change-password]').forEach((trigger) => {
      trigger.addEventListener('click', (event) => {
        event.preventDefault();
        openChangePasswordModal();
      });
    });

    const params = new URLSearchParams(window.location.search);
    if (params.get('change_password') === '1') {
      openChangePasswordModal();
      params.delete('change_password');
      const newQuery = params.toString();
      const newUrl = window.location.pathname + (newQuery ? `?${newQuery}` : '') + window.location.hash;
      window.history.replaceState({}, '', newUrl);
    }
  }

  window.openChangePasswordModal = openChangePasswordModal;
  window.closeChangePasswordModal = closeChangePasswordModal;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initChangePasswordModal);
  } else {
    initChangePasswordModal();
  }
})();
