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

  function onScroll() { header.classList.toggle('is-stuck', window.scrollY > 60); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  setPlaying(playing);

  // 견적 문의 폼: 필수 항목 검사 + 접수 전송.
  // 접수 저장·담당자 전달 엔드포인트는 form[data-endpoint] 로 지정한다(미지정 시 전송하지 않음).
  var form = document.getElementById('inquiryForm');

  // 문의 내용 작성 양식: 문의 분야를 고르면 입력란에 양식 텍스트를 넣는다(참고용, 항목별 필수 아님).
  // 고객이 내용을 작성한 뒤 분야를 바꾸면 작성 내용을 그대로 둔다.
  var GUIDES = {
    certified: ['1. 정부 R&D 과제명 :', '2. 시험 대상 제품 및 기술 :', '3. 과제 종료일 :', '4. 정량적 목표항목 및 목표치 :',
      '5. 시험 장비 보유 여부 (교정 여부 포함) :', '6. 성적서 발급 희망일 :', '7. 기타 문의사항 :'],
    vv: ['1. 정부 R&D 과제명 :', '2. 시험 대상 제품 및 기술 :', '3. 과제 종료일 :', '4. 시험 희망 항목 및 목표치 :',
      '5. 시험 장비 보유 여부 (교정 여부 포함) :', '6. 성적서 발급 희망일 :', '7. 기타 문의사항 :'],
    kc: ['1. 제품명 및 모델명 :', '2. 제품 용도 및 주요 사양 :', '3. 국내 제조 / 해외 수입 여부 :',
      '4. 기존 시험성적서 및 인증서 보유 여부 :', '5. 인증 완료 희망일 :', '6. 기타 문의사항 :'],
    etc: ['1. 문의 분야 :', '2. 제품 및 기술 정보 :', '3. 희망 진행 일정 :', '4. 세부 문의사항 :']
  };
  var typeSel = document.getElementById('inquiryType');
  var msgBox = document.getElementById('inquiryMessage');
  if (typeSel && msgBox) {
    var templates = Object.keys(GUIDES).map(function (k) { return GUIDES[k].join('\n'); });
    // 비어 있거나 양식을 손대지 않은 상태일 때만 교체한다(작성한 내용은 덮어쓰지 않음).
    var isUntouched = function () {
      var v = msgBox.value.trim();
      return v === '' || templates.indexOf(v) !== -1;
    };
    var fillGuide = function () {
      if (!isUntouched()) return;
      var opt = typeSel.options[typeSel.selectedIndex];
      if (!opt || !opt.value) { msgBox.value = ''; return; }
      msgBox.value = GUIDES[opt.getAttribute('data-guide') || 'etc'].join('\n');
    };
    msgBox.placeholder = '문의 분야를 선택하시면 작성 양식이 자동으로 입력됩니다.';
    typeSel.addEventListener('change', fillGuide);
    fillGuide();
  }

  // 약관 동의: 각 항목은 독립 선택(기본 미선택). '전체 동의'는 선택 항목까지 포함하며,
  // 체크하면 선택 동의 내용을 먼저 확인할 수 있도록 선택 영역을 펼친다. 필수 2개만 동의해도 접수 가능.
  var agreeAll = document.querySelector('[data-agree-all]');
  var agrees = document.querySelectorAll('[data-agree]');
  var optAgrees = document.querySelectorAll('[data-agree-opt]');
  var optToggle = document.querySelector('.agree__toggle');
  var optBody = document.getElementById('agreeOpt');
  var optCount = document.querySelector('[data-agree-count]');
  var optLabel = document.querySelector('[data-agree-toggle-label]');
  var setOptOpen = function (open) {
    if (!optToggle || !optBody) return;
    optBody.hidden = !open;
    optToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (optLabel) optLabel.textContent = open ? '접기' : '펼치기';
  };
  var syncAgrees = function () {
    if (agreeAll) agreeAll.checked = Array.prototype.every.call(agrees, function (c) { return c.checked; });
    if (optCount) {
      var n = Array.prototype.filter.call(optAgrees, function (c) { return c.checked; }).length;
      optCount.textContent = '(' + n + '/' + optAgrees.length + ')';
    }
  };
  if (agreeAll) {
    agreeAll.addEventListener('change', function () {
      agrees.forEach(function (c) { c.checked = agreeAll.checked; });
      if (agreeAll.checked) setOptOpen(true);
      syncAgrees();
    });
    agrees.forEach(function (c) { c.addEventListener('change', syncAgrees); });
  }
  if (optToggle) {
    optToggle.addEventListener('click', function () { setOptOpen(optBody.hidden); });
  }
  if (form) form.addEventListener('reset', function () { setTimeout(syncAgrees, 0); });

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
