document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("#lang-en-button, #lang-ru-button, #lang-en-button2, #lang-ru-button2").forEach(btn => {
    btn.addEventListener("click", function () {
      const langCode = this.dataset.lang;
      switchLanguage(langCode);
    });
  });
});

function switchLanguage(langCode) {
  // OpenAI DOM translation (primary language switcher)
  if (window.OpenAITranslate && typeof window.OpenAITranslate.switchLanguage === "function") {
    window.OpenAITranslate.switchLanguage(langCode);
    return;
  }

  // Legacy Django i18n redirect — kept for reference, disabled in favour of OpenAI:
  // switchLanguageDjango(langCode);
}

/*
function switchLanguageDjango(langCode) {
    let csrfValue = getCsrfToken();
    if (!csrfValue) {
      console.warn("CSRF token not found, using simple redirect");
      redirectWithLanguage(langCode);
      return;
    }
    const newPath = calculateNewPath(langCode);
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
*/

 function getCsrfToken() {
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    if (csrfMeta) {
      return csrfMeta.getAttribute("content");
    }
    const csrfTokenInput = document.querySelector(
      'input[name="csrfmiddlewaretoken"]'
    );
    if (csrfTokenInput) {
      return csrfTokenInput.value;
    }
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      const [name, value] = cookie.trim().split("=");
      if (name === "csrftoken") {
        return value;
      }
    }
    if (window.django && window.django.csrf) {
      return window.django.csrf.getCookie("csrftoken");
    }
    return null;
  }

   function calculateNewPath(langCode) {
    const currentPath = window.location.pathname;
    let newPath = currentPath;
    if (currentPath.startsWith("/ru/")) {
      newPath = currentPath.substring(3);
    } else if (currentPath.startsWith("/en/")) {
      newPath = currentPath.substring(3);
    } else if (currentPath === "/ru" || currentPath === "/en") {
      newPath = "/";
    }
    if (langCode === "ru") {
      newPath = `/ru${newPath === "/" ? "" : newPath}`;
    } else if (langCode === "en") {
      newPath = `/en${newPath === "/" ? "" : newPath}`;
    } else {
      newPath = newPath === "" ? "/" : newPath;
    }
    return newPath;
  }
