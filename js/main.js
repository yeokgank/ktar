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

  // 견적 문의 폼: 필수 항목 검사 + 접수 전송.
  // 접수 저장·담당자 전달 엔드포인트는 form[data-endpoint] 로 지정한다(미지정 시 전송하지 않음).
  var form = document.getElementById('inquiryForm');
  if (form) {
    var msg = form.querySelector('.form__msg');
    var MSG_REQUIRED = '필수 항목을 입력해 주세요.';
    var MSG_DONE = '문의가 접수되었습니다. 담당자가 확인 후 연락드리겠습니다.';
    var MSG_FAIL = '접수 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.';
    var say = function (text, isError) {
      msg.textContent = text;
      msg.hidden = false;
      msg.classList.toggle('is-error', !!isError);
    };
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) {
        say(MSG_REQUIRED, true);
        var bad = form.querySelector(':invalid');
        if (bad) bad.focus();
        return;
      }
      var endpoint = form.getAttribute('data-endpoint');
      if (!endpoint) return;
      var btn = form.querySelector('.submit');
      btn.disabled = true;
      fetch(endpoint, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (res) {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          form.reset();
          say(MSG_DONE, false);
        })
        .catch(function () { say(MSG_FAIL, true); })
        .then(function () { btn.disabled = false; });
    });
  }
})();
