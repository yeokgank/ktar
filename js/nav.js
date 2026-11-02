(function () {
  var btn = document.querySelector('[data-nav-toggle]');
  if (!btn) return;

  function setOpen(open) {
    document.body.classList.toggle('nav-open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  btn.addEventListener('click', function () {
    setOpen(!document.body.classList.contains('nav-open'));
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') setOpen(false);
  });

  document.querySelectorAll('#gnb a').forEach(function (a) {
    a.addEventListener('click', function () { setOpen(false); });
  });
})();
