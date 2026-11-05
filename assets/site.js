/* abhijeettoshniwal.com — one small, deferred script. Every feature here is
   progressive: pages are complete without it. */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  function $(s, c) { return (c || d).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); }
  function esc(t) { var e = d.createElement('div'); e.textContent = t == null ? '' : String(t); return e.innerHTML; }

  // Analytics hook. Cloudflare Web Analytics (page views only) is the current
  // setup and has no custom events; if Vercel Web Analytics is enabled later,
  // these named events flow to it. Never send form contents or contact details.
  function track(name, props) { try { if (window.va) window.va('event', { name: name, data: props || {} }); } catch (e) {} }
  $$('[data-track]').forEach(function (el) {
    el.addEventListener('click', function () { track(el.getAttribute('data-track'), { page: location.pathname }); });
  });

  // Theme: the inline <head> script already set data-theme before paint.
  var tt = $('#themeToggle');
  if (tt) {
    var sync = function () {
      var dark = root.getAttribute('data-theme') === 'dark';
      tt.setAttribute('aria-pressed', dark ? 'true' : 'false');
      tt.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
    };
    sync();
    tt.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
      sync();
    });
  }

  // Mobile menu.
  var mb = $('#menuBtn'), nl = $('#navList');
  if (mb && nl) {
    var close = function (focusBtn) { nl.classList.remove('open'); mb.setAttribute('aria-expanded', 'false'); if (focusBtn) mb.focus(); };
    mb.addEventListener('click', function () {
      var open = !nl.classList.contains('open');
      nl.classList.toggle('open', open);
      mb.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) { var f = $('a', nl); if (f) f.focus(); }
    });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nl.classList.contains('open')) close(true); });
    d.addEventListener('click', function (e) { if (nl.classList.contains('open') && !nl.contains(e.target) && e.target !== mb && !mb.contains(e.target)) close(false); });
    window.addEventListener('resize', function () { if (window.innerWidth > 760) close(false); });
  }

  // Signature: one signal, three readings (tabs with arrow-key support).
  var lens = $('.lens');
  if (lens) {
    // Roles are added here so that without JavaScript the four readings simply show as text.
    var tl = $('.lens-tabs', lens); if (tl) tl.setAttribute('role', 'tablist');
    $$('.lens-tabs button', lens).forEach(function (b) { b.setAttribute('role', 'tab'); });
    $$('.lens-note', lens).forEach(function (n) { n.setAttribute('role', 'tabpanel'); n.tabIndex = 0; });
    var tabs = $$('[role="tab"]', lens), panels = $$('[role="tabpanel"]', lens), steps = $$('.chain li', lens);
    var select = function (tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
      });
      panels.forEach(function (p) { p.hidden = p.id !== tab.getAttribute('aria-controls'); });
      var hits = (tab.getAttribute('data-hits') || '').split(',');
      steps.forEach(function (s, i) { s.classList.toggle('hit', hits.indexOf(String(i)) > -1); });
      if (focus) tab.focus();
      track('lens_select', { lens: tab.id });
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t, false); });
      t.addEventListener('keydown', function (e) {
        var k = e.key, n = null;
        if (k === 'ArrowRight' || k === 'ArrowDown') n = tabs[(i + 1) % tabs.length];
        if (k === 'ArrowLeft' || k === 'ArrowUp') n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (k === 'Home') n = tabs[0];
        if (k === 'End') n = tabs[tabs.length - 1];
        if (n) { e.preventDefault(); select(n, true); }
      });
    });
    if (tabs[0]) select(tabs[0], false);
  }

  // LinkedIn figures (updated weekly; HTML holds the fallback).
  var sf = $('#statFollowers'), si = $('#statImpressions');
  if (sf || si) {
    fetch('/api/linkedin-stats').then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (s) {
      if (sf && s.followersLabel) sf.textContent = s.followersLabel;
      if (si && s.impressionsLabel) si.textContent = s.impressionsLabel;
    }).catch(function () {});
  }

  var IST = { timeZone: 'Asia/Kolkata' };
  function fmtDate(ms, withTime) {
    var o = { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'Asia/Kolkata' };
    if (withTime) { o.hour = 'numeric'; o.minute = '2-digit'; }
    return new Date(ms).toLocaleString('en-IN', o) + (withTime ? ' IST' : '');
  }
  function ago(ms) {
    var m = Math.round((Date.now() - ms) / 60000);
    if (m < 60) return m <= 1 ? 'just now' : m + ' min ago';
    var h = Math.round(m / 60); if (h < 24) return h + ' h ago';
    return Math.round(h / 24) + ' d ago';
  }
  function setStatus(el, cls, text) { if (!el) return; el.className = 'status ' + cls; el.textContent = text; }

  // Daily briefing: third-party headlines (api/news.js), one edition per day.
  var bg = $('#briefingGrid');
  if (bg) {
    var bs = $('#briefingStatus'), bm = $('#briefingMeta');
    var fail = function (msg) {
      setStatus(bs, 'err', 'Unavailable');
      bg.innerHTML = '<p class="note">' + esc(msg) + ' My own analysis is listed above and does not depend on this feed.</p>';
    };
    var ctl = window.AbortController ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctl) ctl.abort(); }, 12000);
    fetch('/api/news', ctl ? { signal: ctl.signal } : {}).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (ed) {
      clearTimeout(timer);
      var topics = (ed && ed.topics) || [];
      var any = topics.some(function (t) { return t.items && t.items.length; });
      if (!any) { setStatus(bs, 'stale', 'No headlines'); bg.innerHTML = '<p class="note">This edition has no headlines yet. It refreshes daily at 11:00 AM IST.</p>'; return; }
      if (bm) bm.textContent = (ed.stale ? 'Last available edition: ' : 'Edition of ') + fmtDate(ed.cutoff, true);
      setStatus(bs, ed.stale ? 'stale' : 'ok', ed.stale ? 'Showing an older edition' : 'Up to date');
      bg.innerHTML = topics.map(function (t) {
        var items = (t.items || []).map(function (it) {
          return '<li><a href="' + esc(it.link) + '" rel="noopener noreferrer" target="_blank" data-track="briefing_click">' + esc(it.title) +
            '</a><span class="src">' + esc(it.source || 'Publisher') + ' · published ' + esc(fmtDate(it.published, true)) + '</span></li>';
        }).join('') || '<li class="note">No major headlines in this edition.</li>';
        return '<div class="brief-topic"><h4>' + esc(t.label) + '</h4><ul>' + items + '</ul></div>';
      }).join('');
      $$('[data-track]', bg).forEach(function (a) { a.addEventListener('click', function () { track('briefing_click'); }); });
    }).catch(function () { clearTimeout(timer); fail('The briefing could not load right now.'); });
  }

  // Market snapshot (api/market-indices.js, Yahoo Finance; may be delayed).
  var mt = $('#marketRows');
  if (mt) {
    var ms = $('#marketStatus'), mm = $('#marketMeta');
    var nf = new Intl.NumberFormat('en-IN', { maximumFractionDigits: 2, minimumFractionDigits: 2 });
    fetch('/api/market-indices').then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (j) {
      var rows = (j.indices || []).filter(function (x) { return x.price != null; });
      if (!rows.length) throw 0;
      var anyStale = rows.some(function (x) { return x.cached; });
      var t = rows.map(function (x) { return x.marketTime || 0; }).reduce(function (a, b) { return Math.max(a, b); }, 0);
      mt.innerHTML = rows.map(function (x) {
        var up = (x.change || 0) >= 0, cls = up ? 'up' : 'down', sign = up ? '+' : '';
        var ch = x.change == null ? '—' : sign + nf.format(x.change) + ' (' + sign + (x.changePercent || 0).toFixed(2) + '%)';
        return '<tr><th scope="row">' + esc(x.name) + '</th><td class="num">' + nf.format(x.price) + '</td><td class="num ' + cls + '">' + ch + '</td></tr>';
      }).join('');
      if (mm) mm.textContent = (t ? 'Last price at ' + fmtDate(t, true) : 'Price time not reported') + ' · fetched ' + fmtDate(Date.parse(j.updatedAt) || Date.now(), true);
      setStatus(ms, anyStale ? 'stale' : 'ok', anyStale ? 'Last known values' : 'Delayed quotes');
    }).catch(function () {
      setStatus(ms, 'err', 'Unavailable');
      mt.innerHTML = '<tr><td colspan="3" class="note">Market data could not load right now.</td></tr>';
    });
  }

  // Music: load a video only when asked; never autoplay sound.
  $$('.media button.play').forEach(function (b) {
    b.addEventListener('click', function () {
      var wrap = b.parentNode, src = b.getAttribute('data-src'), poster = b.getAttribute('data-poster');
      var v = d.createElement('video');
      v.controls = true; v.playsInline = true; v.preload = 'metadata'; v.src = src; if (poster) v.poster = poster;
      v.setAttribute('aria-label', b.getAttribute('data-label') || 'Music video');
      wrap.innerHTML = ''; wrap.appendChild(v);
      var p = v.play(); if (p && p.catch) p.catch(function () {});
      v.focus();
      track('music_play', { video: src });
    });
  });

  // UTM capture: remembered for this visit and attached to contact messages.
  try {
    var q = new URLSearchParams(location.search), keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content'], seen = false;
    keys.forEach(function (k) { if (q.get(k)) { sessionStorage.setItem(k, q.get(k).slice(0, 80)); seen = true; } });
    if (!seen && !sessionStorage.getItem('landing_ref') && document.referrer && !document.referrer.includes(location.host)) {
      sessionStorage.setItem('landing_ref', new URL(document.referrer).hostname);
    }
  } catch (e) {}

  // Contact form: validate in place, submit in the background, honest states.
  var form = $('#contactForm');
  if (form) {
    var topic = $('#topic', form), status = $('#formStatus'), btn = $('button[type="submit"]', form);
    try {
      var want = new URLSearchParams(location.search).get('topic');
      if (want && topic && $('option[value="' + want.replace(/[^a-z-]/g, '') + '"]', topic)) topic.value = want;
      var src = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content'].map(function (k) { var v = sessionStorage.getItem(k); return v ? k + '=' + v : ''; }).filter(Boolean).join('&') || sessionStorage.getItem('landing_ref') || 'direct';
      var hs = $('input[name="source"]', form); if (hs) hs.value = src;
    } catch (e) {}
    var check = function (f) {
      var field = f.closest('.field'), err = field && $('.err', field), msg = '';
      if (f.validity.valueMissing) msg = 'Please fill this in.';
      else if (f.validity.typeMismatch) msg = 'Please enter a valid email address.';
      else if (f.validity.tooShort) msg = 'Please write at least ' + f.minLength + ' characters.';
      if (field) field.classList.toggle('invalid', !!msg);
      if (err) { err.textContent = msg; err.hidden = !msg; }
      f.setAttribute('aria-invalid', msg ? 'true' : 'false');
      return !msg;
    };
    $$('input:not([type=hidden]):not(.hp input), textarea, select', form).forEach(function (f) {
      f.addEventListener('blur', function () { if (f.value) check(f); });
      f.addEventListener('input', function () { if (f.getAttribute('aria-invalid') === 'true') check(f); });
    });
    form.setAttribute('novalidate', '');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var fields = $$('[required]', form), first = null;
      fields.forEach(function (f) { if (!check(f) && !first) first = f; });
      if (first) { first.focus(); return; }
      if (!window.fetch) { form.removeAttribute('novalidate'); form.submit(); return; }
      btn.disabled = true; btn.textContent = 'Sending…';
      status.hidden = true;
      var endpoint = form.getAttribute('action').replace('formsubmit.co/', 'formsubmit.co/ajax/');
      fetch(endpoint, { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok || String(j.success) === 'false') throw 0; }); })
        .then(function () {
          track('contact_submit', { topic: topic ? topic.value : '' });
          form.reset();
          status.className = 'form-status ok';
          status.innerHTML = '<strong>Thank you. Your message was sent.</strong> I read every message and reply personally.';
          status.hidden = false; status.focus();
          btn.disabled = false; btn.textContent = 'Send message';
        })
        .catch(function () {
          status.className = 'form-status bad';
          status.innerHTML = '<strong>Your message was not sent.</strong> Please try again, or email <a href="mailto:abhijeettoshniwal14@gmail.com">abhijeettoshniwal14@gmail.com</a>. What you wrote is still in the form.';
          status.hidden = false; status.focus();
          btn.disabled = false; btn.textContent = 'Send message';
        });
    });
  }

  var y = $('#year'); if (y) y.textContent = new Date().getFullYear();
})();
