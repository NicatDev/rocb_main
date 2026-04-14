document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("#lang-en-button, #lang-ru-button, #lang-en-button2, #lang-ru-button2").forEach(btn => {
    btn.addEventListener("click", function () {
      const langCode = this.dataset.lang;
      switchLanguage(langCode);
    });
  });
});

function switchLanguage(langCode) { 

    // Get CSRF token
    let csrfValue = getCsrfToken();

    if (!csrfValue) {
      console.warn("CSRF token not found, using simple redirect");
      redirectWithLanguage(langCode);
      return;
    }

    // Calculate new path
    const newPath = calculateNewPath(langCode);

    // Create and submit form
    const form = document.createElement("form");
    form.method = "POST";
    form.action = "/i18n/setlang/";
    form.style.display = "none";

    const csrfInput = document.createElement("input");
    csrfInput.type = "hidden";
    csrfInput.name = "csrfmiddlewaretoken";
    csrfInput.value = csrfValue;
    form.appendChild(csrfInput);

    const langInput = document.createElement("input");
    langInput.type = "hidden";
    langInput.name = "language";
    langInput.value = langCode;
    form.appendChild(langInput);

    const nextInput = document.createElement("input");
    nextInput.type = "hidden";
    nextInput.name = "next";
    nextInput.value = newPath;
    form.appendChild(nextInput);

    document.body.appendChild(form);

    form.submit();
  } 
// Dropdown-based language switcher removed in favor of two inline flags.

 function getCsrfToken() {
    // Try meta tag first
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    if (csrfMeta) {
      return csrfMeta.getAttribute("content");
    }

    // Try hidden input
    const csrfTokenInput = document.querySelector(
      'input[name="csrfmiddlewaretoken"]'
    );
    if (csrfTokenInput) {
      return csrfTokenInput.value;
    }

    // Try cookie
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      const [name, value] = cookie.trim().split("=");
      if (name === "csrftoken") {
        return value;
      }
    }

    // Try Django's built-in function if available
    if (window.django && window.django.csrf) {
      return window.django.csrf.getCookie("csrftoken");
    }

    return null;
  }

   function calculateNewPath(langCode) {
    const currentPath = window.location.pathname;
    let newPath = currentPath;

    // Remove existing language prefix
    if (currentPath.startsWith("/ru/")) {
      newPath = currentPath.substring(3);
    } else if (currentPath.startsWith("/en/")) {
      newPath = currentPath.substring(3);
    } else if (currentPath === "/ru" || currentPath === "/en") {
      newPath = "/";
    }

    // Add new language prefix
    if (langCode === "ru") {
      newPath = `/ru${newPath === "/" ? "" : newPath}`;
    } else if (langCode === "en") {
      newPath = `/en${newPath === "/" ? "" : newPath}`;
    } else {
      // Default language (probably English)
      newPath = newPath === "" ? "/" : newPath;
    }

    return newPath;
  }