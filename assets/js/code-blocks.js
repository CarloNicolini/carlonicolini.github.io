// Prism's standard toolbar, clipboard, and line-number plugins, applied to
// Jekyll/Rouge output as well as ordinary <pre><code> snippets.
if (window.Prism) {
  const icon = (name, paths) => `<svg class="code-icon code-icon-${name}" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">${paths}</svg>`;
  const numbersIcon = icon('numbers', '<path d="M10 6h11M10 12h11M10 18h11M3 4h1v5M3 9h3M3 14a1.5 1.5 0 0 1 3 0c0 1.5-3 2-3 4h3"/>');
  const copyIcon = icon('copy', '<rect x="8" y="8" width="12" height="13" rx="2"/><path d="M16 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3"/>');
  const checkIcon = icon('check', '<path d="m5 12 4 4L19 6"/>');
  const errorIcon = icon('error', '<circle cx="12" cy="12" r="9"/><path d="M12 7v6M12 17h.01"/>');
  const aliases = {plaintext:'none', text:'none', py:'python', sh:'bash', shell:'bash', console:'bash', terminal:'bash', html:'markup', xml:'markup', js:'javascript', dockerfile:'docker', tex:'latex'};
  Prism.plugins.toolbar.registerButton('toggle-line-numbers', env => {
    const pre = env.element.parentElement;
    const button = document.createElement('button');
    button.type = 'button';
    button.innerHTML = numbersIcon;
    function updateLabel() {
      const enabled = pre.classList.contains('line-numbers');
      button.setAttribute('aria-pressed', String(enabled));
      const label = `${enabled ? 'Hide' : 'Show'} line numbers`;
      button.setAttribute('aria-label', label);
      button.title = label;
    }
    button.addEventListener('click', () => {
      pre.classList.toggle('line-numbers');
      Prism.highlightElement(env.element);
      updateLabel();
    });
    updateLabel();
    return button;
  });

  document.querySelectorAll('main pre').forEach(pre => {
    let code = pre.querySelector('code');
    if (!code) {
      code = document.createElement('code');
      code.textContent = pre.textContent;
      pre.replaceChildren(code);
    }
    const languageContainer = code.closest('[class*="language-"]');
    const match = languageContainer?.className.match(/\blanguage-([\w+-]+)/);
    const language = aliases[match?.[1]] || match?.[1] || 'none';
    // Keep the exact source text, replacing server-generated highlighting only.
    code.textContent = code.textContent;
    code.className = `language-${language}`;
    pre.setAttribute('data-toolbar-order', 'show-language,toggle-line-numbers,copy-to-clipboard');
    pre.setAttribute('data-prismjs-copy-timeout', '2000');
    pre.setAttribute('tabindex', '0');
    pre.setAttribute('aria-label', `${language === 'none' ? 'Plain text' : language} code snippet`);
    Prism.highlightElement(code);
    const copy = pre.parentElement.querySelector('.copy-to-clipboard-button');
    if (copy) {
      copy.setAttribute('aria-label', 'Copy code');
      copy.setAttribute('aria-live', 'polite');
      copy.title = 'Copy code';
      copy.insertAdjacentHTML('beforeend', copyIcon + checkIcon + errorIcon);
      new MutationObserver(() => {
        const state = copy.dataset.copyState;
        const label = state === 'copy-success' ? 'Copied!' : state === 'copy-error' ? copy.querySelector('span').textContent : 'Copy code';
        copy.setAttribute('aria-label', label);
        copy.title = label;
      }).observe(copy, {attributes:true, attributeFilter:['data-copy-state']});
    }
  });
}
