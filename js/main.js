(function () {
  var slides = document.querySelectorAll('.slide');
  var cur = document.getElementById('cur');
  var toggle = document.querySelector('.ctrl__toggle');
  var header = document.getElementById('header');
  var idx = 0, playing = true, timer = null, INTERVAL = 6000;

  function show(n) {
    idx = (n + slides.length) % slides.length;
    slides.forEach(function (s, i) { s.classList.toggle('is-active', i === idx); });
    cur.textContent = idx + 1;
  }
  function start() { stop(); timer = setInterval(function () { show(idx + 1); }, INTERVAL); }
  function stop() { clearInterval(timer); }

  document.querySelector('.ctrl').addEventListener('click', function (e) {
    var act = e.target.getAttribute('data-act');
    if (act === 'prev') show(idx - 1);
    if (act === 'next') show(idx + 1);
    if (act === 'toggle') {
      playing = !playing;
      toggle.innerHTML = playing ? '&#10074;&#10074;' : '&#9654;';
      toggle.setAttribute('aria-label', playing ? '일시정지' : '재생');
      playing ? start() : stop();
    }
  });

  function onScroll() { header.classList.toggle('is-solid', window.scrollY > 60); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  start();
})();
