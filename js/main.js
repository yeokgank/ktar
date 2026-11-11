(function () {
  var slides = document.querySelectorAll('.slide');
  var cur = document.getElementById('cur');
  var toggle = document.querySelector('.ctrl__toggle');
  var video = document.querySelector('.hero__video');
  var header = document.getElementById('header');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var idx = 0, playing = !reduce, timer = null, INTERVAL = 6000;

  function show(n) {
    idx = (n + slides.length) % slides.length;
    slides.forEach(function (s, i) { s.classList.toggle('is-active', i === idx); });
    cur.textContent = idx + 1;
  }
  function start() { stop(); timer = setInterval(function () { show(idx + 1); }, INTERVAL); }
  function stop() { clearInterval(timer); }
  function setPlaying(on) {
    playing = on;
    toggle.innerHTML = on ? '&#10074;&#10074;' : '&#9654;';
    toggle.setAttribute('aria-label', on ? '일시정지' : '재생');
    if (on) { start(); if (video) video.play().catch(function () {}); }
    else { stop(); if (video) video.pause(); }
  }

  document.querySelector('.ctrl').addEventListener('click', function (e) {
    var act = e.target.getAttribute('data-act');
    if (act === 'prev') show(idx - 1);
    if (act === 'next') show(idx + 1);
    if (act === 'toggle') setPlaying(!playing);
  });

  // 빠른 서비스 탭
  var tabs = document.querySelectorAll('.qs__tabs button');
  var panels = document.querySelectorAll('.qs__panel');
  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      var n = t.getAttribute('data-tab');
      tabs.forEach(function (b) { b.setAttribute('aria-selected', b === t ? 'true' : 'false'); });
      panels.forEach(function (p) { p.classList.toggle('is-active', p.getAttribute('data-panel') === n); });
    });
  });

  function onScroll() { header.classList.toggle('is-stuck', window.scrollY > 60); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  setPlaying(playing);
})();
