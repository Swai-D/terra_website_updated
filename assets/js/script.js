// Terra Consulting - site behaviour (navigation, form validation, prefill)
document.addEventListener('DOMContentLoaded', function () {
  var burger = document.getElementById('hamburger');
  var menu = document.getElementById('nav-menu');
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var open = menu.classList.toggle('active');
      burger.classList.toggle('active', open);
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { menu.classList.remove('active'); burger.classList.remove('active'); burger.setAttribute('aria-expanded', 'false'); });
    });
  }
  var y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();

  // Prefill ?service= and ?sector= on the contact form
  var params = new URLSearchParams(location.search);
  ['service', 'sector'].forEach(function (k) {
    var el = document.querySelector('#consultation-form [name="' + k + '"]');
    if (el && params.get(k)) el.value = params.get(k);
  });
  // Server-side error message (?status=error&msg=...)
  var st = document.getElementById('form-status');
  if (st && params.get('status') === 'error') {
    st.textContent = params.get('msg') || 'Sorry, we could not send your message. Please try again or contact us directly.';
    st.hidden = false;
  }

  // Forms POST natively to PHP. JS only validates and records the render time (spam check).
  document.querySelectorAll('form[data-validate]').forEach(function (form) {
    var ts = form.querySelector('input[name="ts"]'); if (ts) ts.value = String(Date.now());
    form.setAttribute('novalidate', 'novalidate');
    form.addEventListener('submit', function (e) {
      var ok = true;
      form.querySelectorAll('.field-error').forEach(function (n) { n.remove(); });
      form.querySelectorAll('[required]').forEach(function (f) {
        f.classList.remove('invalid');
        var bad = f.type === 'checkbox' ? !f.checked : !f.value.trim();
        if (!bad && f.type === 'email') bad = !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.value.trim());
        if (bad) {
          ok = false; f.classList.add('invalid');
          var m = document.createElement('div'); m.className = 'field-error';
          m.textContent = f.type === 'checkbox' ? 'Please tick this box to continue' : f.type === 'email' ? 'Enter a valid email address' : 'This field is required';
          (f.closest('.form-group') || f.closest('label') || f.parentNode).appendChild(m);
        }
      });
      if (!ok) { e.preventDefault(); var first = form.querySelector('.invalid'); if (first) first.focus(); return; }
      var btn = form.querySelector('button[type="submit"]'); if (btn) { btn.disabled = true; btn.textContent = 'Sending...'; }
    });
  });
});
