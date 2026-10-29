/* Shared client-side behaviour for every page (theme toggle, nav dropdowns,
   priority nav, mobile drawer, language switcher, back-to-top, article tables,
   KaTeX, tool-form reset, copy-result buttons). Built to public/site.min.js
   by generate.py and loaded with `defer` from all three templates. Each
   function is a no-op on pages without its markup. */
(function () {
  function initThemeToggle() {
    var btn = document.getElementById('themeToggleBtn');
    if (!btn) return;
    btn.setAttribute('aria-pressed', document.documentElement.classList.contains('dark'));
    btn.addEventListener('click', function () {
      var isDark = document.documentElement.classList.toggle('dark');
      document.documentElement.style.colorScheme = isDark ? 'dark' : 'light';
      try { localStorage.setItem('theme', isDark ? 'dark' : 'light'); } catch (e) {}
      btn.setAttribute('aria-pressed', String(isDark));
    });
  }
  function initCategoryDropdowns() {
    var buttons = document.querySelectorAll('.cat-menu-btn');
    function closeAll(except) {
      buttons.forEach(function (b) {
        if (b === except) return;
        b.setAttribute('aria-expanded', 'false');
        var menu = document.getElementById(b.getAttribute('aria-controls'));
        if (menu) menu.hidden = true;
      });
    }
    function positionMenu(b, menu) {
      var rect = b.getBoundingClientRect();
      menu.style.top = (rect.bottom + 8) + 'px';
      menu.style.left = Math.max(8, Math.min(rect.left, window.innerWidth - menu.offsetWidth - 8)) + 'px';
    }
    buttons.forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.stopPropagation();
        var expanded = b.getAttribute('aria-expanded') === 'true';
        closeAll();
        var menu = document.getElementById(b.getAttribute('aria-controls'));
        if (!expanded && menu) {
          menu.hidden = false;
          positionMenu(b, menu);
          b.setAttribute('aria-expanded', 'true');
        }
      });
    });
    document.addEventListener('click', function () { closeAll(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeAll(); });
    window.addEventListener('scroll', function () { closeAll(); }, { passive: true });
    return closeAll;
  }
  function initPriorityNav(closeAll) {
    var strip = document.querySelector('.category-strip');
    var moreItem = document.getElementById('moreMenuItem');
    if (!strip || !moreItem) return;
    var items = Array.prototype.slice.call(strip.querySelectorAll('.cat-menu-item[data-cat-key]'));
    var sections = document.querySelectorAll('.more-menu-section');
    function layout() {
      items.forEach(function (item) { item.hidden = false; });
      sections.forEach(function (s) { s.hidden = true; });
      moreItem.hidden = false;

      var available = strip.clientWidth;
      var gap = parseFloat(getComputedStyle(strip).columnGap) || 0;
      var fixedWidth = 0;
      Array.prototype.forEach.call(strip.children, function (el) {
        if (el !== moreItem && items.indexOf(el) === -1) {
          fixedWidth += el.getBoundingClientRect().width + gap;
        }
      });
      var moreWidth = moreItem.getBoundingClientRect().width + gap;
      var itemWidths = items.map(function (it) { return it.getBoundingClientRect().width + gap; });
      var total = itemWidths.reduce(function (a, b) { return a + b; }, fixedWidth);

      if (total <= available) {
        moreItem.hidden = true;
        return;
      }

      var used = fixedWidth;
      var visibleCount = 0;
      for (var i = 0; i < itemWidths.length; i++) {
        if (used + itemWidths[i] + moreWidth > available) break;
        used += itemWidths[i];
        visibleCount++;
      }

      items.forEach(function (item, idx) {
        if (idx >= visibleCount) {
          item.hidden = true;
          var section = document.querySelector('.more-menu-section[data-cat-key="' + item.getAttribute('data-cat-key') + '"]');
          if (section) section.hidden = false;
        }
      });
    }
    var resizeTimer;
    window.addEventListener('resize', function () {
      closeAll();
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(layout, 100);
    });
    layout();
    window.addEventListener('load', layout);
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(layout);
    }
  }
  function initMobileDrawer() {
    var hamburger = document.getElementById('navHamburgerBtn');
    var drawer = document.getElementById('navDrawer');
    var backdrop = document.getElementById('navDrawerBackdrop');
    var closeBtn = document.getElementById('navDrawerClose');
    if (!hamburger || !drawer || !backdrop) return;
    var sectionButtons = drawer.querySelectorAll('.drawer-section-btn');
    function isOpen() { return !drawer.hidden && drawer.classList.contains('translate-x-0'); }
    function openDrawer() {
      drawer.hidden = false;
      backdrop.hidden = false;
      setTimeout(function () {
        drawer.classList.remove('translate-x-full');
        drawer.classList.add('translate-x-0');
        backdrop.classList.remove('opacity-0');
        backdrop.classList.add('opacity-100');
      }, 10);
      hamburger.setAttribute('aria-expanded', 'true');
      document.body.classList.add('overflow-hidden');
    }
    function closeDrawer(returnFocus) {
      drawer.classList.remove('translate-x-0');
      drawer.classList.add('translate-x-full');
      backdrop.classList.remove('opacity-100');
      backdrop.classList.add('opacity-0');
      hamburger.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('overflow-hidden');
      if (returnFocus) hamburger.focus();
      setTimeout(function () {
        if (!isOpen()) { drawer.hidden = true; backdrop.hidden = true; }
      }, 220);
    }
    hamburger.addEventListener('click', function () { isOpen() ? closeDrawer(false) : openDrawer(); });
    closeBtn.addEventListener('click', function () { closeDrawer(true); });
    backdrop.addEventListener('click', function () { closeDrawer(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && isOpen()) closeDrawer(true); });
    sectionButtons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var expanded = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', expanded ? 'false' : 'true');
        var panel = document.getElementById(btn.getAttribute('aria-controls'));
        if (panel) panel.hidden = expanded;
      });
    });
    var mq = window.matchMedia('(min-width:769px)');
    var mqHandler = function (e) { if (e.matches && isOpen()) closeDrawer(false); };
    if (mq.addEventListener) mq.addEventListener('change', mqHandler);
    else mq.addListener(mqHandler);
  }
  (function () {
    var wrap = document.getElementById('backToTopWrap');
    var btn = document.getElementById('backToTop');
    if (!wrap || !btn) return;
    var shown = false;
    function update() {
      var show = window.pageYOffset > 600;
      if (show !== shown) { shown = show; wrap.hidden = !show; }
    }
    window.addEventListener('scroll', update, { passive: true });
    update();
    btn.addEventListener('click', function () {
      var calm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: 0, behavior: calm ? 'auto' : 'smooth' });
      var main = document.getElementById('main-content');
      if (main) { main.setAttribute('tabindex', '-1'); main.focus({ preventScroll: true }); }
    });
  })();
  document.addEventListener('click', function (e) {
    var d = document.getElementById('langSwitch');
    if (d && d.open && !d.contains(e.target)) d.open = false;
  });
  document.addEventListener('keydown', function (e) {
    var d = document.getElementById('langSwitch');
    if (e.key === 'Escape' && d && d.open) { d.open = false; d.querySelector('summary').focus(); }
  });
  function wrapTables() {
    document.querySelectorAll('.article table').forEach(function (table) {
      if (table.closest('.table-scroll')) return;
      var wrap = document.createElement('div');
      wrap.className = 'table-scroll overflow-x-auto';
      table.parentNode.insertBefore(wrap, table);
      wrap.appendChild(table);
    });
  }
  function initToolForm() {
    var form = document.querySelector('.tool-section form');
    if (!form) return;
    form.addEventListener('submit', function (e) { e.preventDefault(); });
    var resetBtn = form.querySelector('.reset-btn');
    if (!resetBtn) return;
    resetBtn.addEventListener('click', function () {
      form.reset();
      // form.reset() clears input/textarea values but fires no 'input'
      // event, so each field's own oninput="calculate()" (or, on the
      // tabbed home-page tool, calcBasic()/calcChange()/calcReverse())
      // never re-runs. Dispatching 'input' on every field re-invokes
      // whichever handler is already wired to it, which is also what
      // resets that tool's own <output>s/formula line back to their
      // empty state -- no per-tool JS needed here.
      form.querySelectorAll('input, textarea, select').forEach(function (field) {
        field.dispatchEvent(new Event('input', { bubbles: true }));
      });
      var firstField = form.querySelector('input, textarea');
      if (firstField) firstField.focus();
    });
  }
  function renderMath() {
    // content_html's formulas use $$...$$ (display) and \(...\) (inline) —
    // never single-$ delimiters, since the site is full of literal dollar
    // amounts ($5,000 etc.) that would otherwise be misparsed as math.
    if (typeof renderMathInElement === 'undefined') return;
    document.querySelectorAll('.article').forEach(function (el) {
      renderMathInElement(el, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '\\(', right: '\\)', display: false }
        ],
        throwOnError: false
      });
    });
  }
  function initCopyButtons() {
    // Localised button text comes from the page itself (data attributes on <main>).
    var main = document.getElementById('main-content');
    var labels = { copy: main ? main.dataset.copyLabel : '', copied: main ? main.dataset.copiedLabel : '' };
    // Wraps each primary result <output> (one per calculator section, tagged
    // by the shared .calc-result-row.primary/.calc-results markup every
    // tool's fields_html already uses) with a small copy-to-clipboard button,
    // injected once here rather than authored per-tool so every calculator
    // -- present and future -- gets it for free.
    document.querySelectorAll('.calc-result-row.primary').forEach(function (row) {
      var output = row.querySelector('output.value');
      if (!output || output.dataset.copyWired) return;
      output.dataset.copyWired = 'true';
      var wrap = document.createElement('span');
      wrap.className = 'inline-flex items-center gap-2';
      output.parentNode.insertBefore(wrap, output);
      wrap.appendChild(output);
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'copy-btn flex h-7 w-7 flex-none items-center justify-center rounded-lg border border-border bg-surface text-text-muted transition-colors hover:border-accent hover:text-accent';
      btn.setAttribute('aria-label', labels.copy);
      btn.setAttribute('title', labels.copy);
      btn.innerHTML =
        '<svg class="copy-icon h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>' +
        '<svg class="check-icon h-4 w-4 text-accent" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" hidden><path d="M20 6 9 17l-5-5"/></svg>';
      wrap.appendChild(btn);
      var copyIcon = btn.querySelector('.copy-icon');
      var checkIcon = btn.querySelector('.check-icon');
      var revertTimer;
      btn.addEventListener('click', function () {
        var text = output.textContent.trim();
        if (!text || text === '–') return;
        var showCopied = function () {
          copyIcon.hidden = true;
          checkIcon.hidden = false;
          btn.setAttribute('title', labels.copied);
          clearTimeout(revertTimer);
          revertTimer = setTimeout(function () {
            copyIcon.hidden = false;
            checkIcon.hidden = true;
            btn.setAttribute('title', labels.copy);
          }, 1500);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(showCopied, function () {});
        } else {
          var ta = document.createElement('textarea');
          ta.value = text;
          ta.style.position = 'fixed';
          ta.style.opacity = '0';
          document.body.appendChild(ta);
          ta.select();
          try { document.execCommand('copy'); showCopied(); } catch (e) {}
          document.body.removeChild(ta);
        }
      });
    });
  }
  document.addEventListener('DOMContentLoaded', function () {
    initThemeToggle();
    var closeAll = initCategoryDropdowns();
    initPriorityNav(closeAll);
    initMobileDrawer();
    wrapTables();
    initToolForm();
    initCopyButtons();
    renderMath();
  });
})();
