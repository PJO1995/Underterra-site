/* Underterra — shared site behaviour (2026 redesign) */
(function () {
  'use strict';

  /* ── Mobile menu ───────────────────────────────────────── */
  var toggle = document.querySelector('[data-ut-menu-toggle]');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('ut-menu-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('ut-menu-open')) toggle.click();
    });
  }

  /* ── Hero background video (loads after the page, skipped for reduced motion / data saver) ── */
  var hv = document.querySelector('.ut-hero-video');
  if (hv) {
    var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    var save = navigator.connection && navigator.connection.saveData;
    if (!reduce && !save) {
      hv.src = (window.innerWidth <= 900 ? hv.getAttribute('data-src-mobile') : hv.getAttribute('data-src'));
      var p = hv.play(); if (p && p.catch) p.catch(function () {});
    }
  }

  /* ── Live category counts + sold check (home page) ─────── */
  var countEls = document.querySelectorAll('[data-ut-count]');
  var featured = document.querySelectorAll('[data-ut-featured]');
  if (countEls.length || featured.length) {
    Promise.all([
      fetch('/inventory', { credentials: 'same-origin' }).then(function (r) { return r.text(); }),
      fetch('/sold.json', { cache: 'no-store' }).then(function (r) { return r.ok ? r.json() : []; }).catch(function () { return []; })
    ]).then(function (res) {
      var doc = new DOMParser().parseFromString(res[0], 'text/html');
      var sold = res[1];
      var soldIds = Array.isArray(sold) ? sold : (sold && (sold.sold || sold.ids)) || [];
      var counts = { all: 0 };
      doc.querySelectorAll('.machine-card').forEach(function (c) {
        var id = c.getAttribute('data-machine-id');
        if (soldIds.indexOf(id) !== -1 || c.classList.contains('sold')) return;
        var t = c.getAttribute('data-type') || 'other';
        counts[t] = (counts[t] || 0) + 1;
        counts.all++;
      });
      countEls.forEach(function (el) {
        var k = el.getAttribute('data-ut-count');
        if (counts[k] != null) el.textContent = counts[k];
      });
      featured.forEach(function (el) {
        if (soldIds.indexOf(el.getAttribute('data-ut-featured')) !== -1) el.style.display = 'none';
      });
    }).catch(function () { /* keep static numbers */ });
  }

  /* ── Live prices for featured cards (prices.json) ──────── */
  var priceEls = document.querySelectorAll('[data-ut-price-id]');
  if (priceEls.length) {
    fetch('/prices.json?_=' + Date.now()).then(function (r) { return r.json(); }).then(function (d) {
      var map = {};
      (d.prices || []).forEach(function (p) { map[p.id] = p.listPrice; });
      priceEls.forEach(function (el) {
        var p = map[el.getAttribute('data-ut-price-id')];
        if (p) el.textContent = '$' + Number(p).toLocaleString('en-US');
      });
    }).catch(function () {});
  }

  /* ── Contact form (contact page) ───────────────────────── */
  var form = document.getElementById('ut-quote-form');
  if (form) {
    var params = new URLSearchParams(location.search);
    var machine = params.get('machine');
    var category = params.get('category');
    if (category) {
      var sel = form.querySelector('[name=equipment]');
      for (var i = 0; i < sel.options.length; i++) if (sel.options[i].value === category) sel.selectedIndex = i;
    }
    if (machine) {
      form.querySelector('[name=message]').value = 'I am interested in the ' + machine + '. Please send me more information and pricing.';
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = form.querySelector('button[type=submit]');
      var box = document.getElementById('ut-form-status');
      var label = btn.textContent;
      btn.textContent = 'Sending…';
      btn.disabled = true;
      box.style.display = 'none';
      var v = function (n) { var f = form.querySelector('[name=' + n + ']'); return f ? f.value.trim() : ''; };
      var dest = v('destination');
      var msg = v('message');
      if (dest) msg = msg + (msg ? '\n\n' : '') + 'Delivery to: ' + dest;
      fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ firstName: v('firstName'), lastName: v('lastName'), email: v('email'), phone: v('phone'), equipment: v('equipment'), message: msg })
      }).then(function (r) { return r.json(); }).then(function (d) {
        if (!d.success) throw new Error(d.error || 'error');
        box.textContent = '✓ Thank you! We’ll get back to you within 24 hours.';
        box.style.display = 'block';
        form.reset();
        btn.style.display = 'none';
      }).catch(function () {
        box.textContent = '✗ Something went wrong. Please email us at ap@underterradelrio.com or call sales (830) 422-5062 or the office (830) 488-5594.';
        box.style.display = 'block';
        btn.textContent = label;
        btn.disabled = false;
      });
    });
  }
})();
