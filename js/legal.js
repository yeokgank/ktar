/* 약관 모달: a[data-legal] 을 누르면 링크한 문서(legal/*.html)의 article.legal 을 <dialog> 로 띄운다.
   불러오기에 실패하면 링크 그대로 페이지 이동한다(스크립트 없는 환경과 같은 동작). */
(function () {
  var links = document.querySelectorAll('a[data-legal]');
  if (!links.length || typeof HTMLDialogElement !== 'function') return;

  var cache = {};
  var dialog = document.createElement('dialog');
  dialog.className = 'legal-modal';
  dialog.innerHTML =
    '<div class="legal-modal__bar"><button type="button" class="legal-modal__close" aria-label="닫기">&times;</button></div>' +
    '<div class="legal-modal__body"></div>' +
    '<div class="legal-modal__foot"><button type="button" class="legal-modal__ok">확인</button></div>';
  document.body.appendChild(dialog);
  var body = dialog.querySelector('.legal-modal__body');

  function close() { dialog.close(); }
  dialog.querySelector('.legal-modal__close').addEventListener('click', close);
  dialog.querySelector('.legal-modal__ok').addEventListener('click', close);
  // 바깥(배경) 클릭 시 닫기
  dialog.addEventListener('click', function (e) { if (e.target === dialog) close(); });
  dialog.addEventListener('close', function () { document.documentElement.classList.remove('is-modal-open'); });

  function load(url) {
    if (cache[url]) return Promise.resolve(cache[url]);
    return fetch(url, { credentials: 'same-origin' })
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.text();
      })
      .then(function (html) {
        var doc = new DOMParser().parseFromString(html, 'text/html');
        var article = doc.querySelector('article.legal');
        if (!article) throw new Error('article.legal 없음');
        cache[url] = article;
        return article;
      });
  }

  function open(article) {
    body.replaceChildren(document.importNode(article, true));
    var title = body.querySelector('h1');
    if (title && title.id) dialog.setAttribute('aria-labelledby', title.id);
    document.documentElement.classList.add('is-modal-open');
    dialog.showModal();
    body.scrollTop = 0;
  }

  links.forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      load(a.href).then(open).catch(function () { window.location.href = a.href; });
    });
  });
})();
