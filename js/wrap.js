/* 의미 단위 줄바꿈 보정. CSS(keep-all·text-wrap)는 단어가 쪼개지는 것만 막으므로,
   어디서 줄을 바꿀지는 여기서 정한다.
   1) 함께 읽어야 하는 어절은 줄바꿈 없는 공백(U+00A0)으로 묶는다.
      예) "희망 인증등급", "필수 제출사항", "원활한 인증", "입증할 수 있습니다", "3일 이내"
   2) 한 문단에 문장이 둘 이상이면 문장마다 inline-block 으로 감싼다.
      다음 문장이 남은 자리에 통째로 들어가지 않으면 새 줄에서 시작한다.
      예) "…차이가 있습니다. 원활한 인증 / 획득을" → "…차이가 있습니다. / 원활한 인증 획득을…"
   약관 본문(.legal)은 긴 줄글이라 2)를 적용하지 않는다. */
(function () {
  var NB = '\u00A0';
  // 꾸밈말 묶음은 약한 묶음(WEAK)·느슨한 묶음(LOOSE_MARK)으로 표시했다가, 덩어리가 MAX_CHUNK 자를 넘으면 푼다.
  // 연달아 묶여 한 덩어리가 너무 길어지면 앞줄에 큰 빈칸이 생기기 때문이다.
  var WEAK = '\uE000';
  var LOOSE_MARK = '\uE001';
  var MAX_CHUNK = 16;
  // 뒤 명사를 꾸미는 말(이 단어 다음에서는 줄을 바꾸지 않는다)
  var MODIFIERS = '필수|희망|주요|관련|기존|신규|해당|별도|각종|최종|공식|정부|국내|해외|사전|추가|개별|공인|국가|지정|협력|전문|맞춤|정량적|정성적|체계적인|객관적인|공식적인|다양한|원활한|필요한|정확한';
  // 연결이 느슨한 꾸밈말(긴 덩어리를 풀 때 가장 먼저 푼다)
  var LOOSE = '대한|위한|통한|관한|따른|의한';
  // 관형형 어미(~하는/~되는/~된 …)로 끝나는 어절
  var ADNOMINAL = '[가-힣]+(?:하는|되는|있는|없는|받는|하던|한|된|할|될)';
  // 띄어 쓰지만 한 낱말처럼 읽히는 이 사이트의 복합명사
  var COMPOUNDS = ['견적 안내', '시험항목 검토', '검토 지원', '일정 조율', '결과서 발급', '성적서 발급', '인증서 발급',
    '사전 준비', '신청 접수', '결함 보완', '기술 검토', '평가 방식', '점수 기준', '진행 관리', '변경사항 검토',
    '업무 협의', '제품 관련', '심의 결과', '심사 대응', '시험평가 결과', '제품 정보', '인증 목적', '판로 확대', '시험 일정', '연계 서비스'];
  var RULES = [
    [new RegExp('(' + COMPOUNDS.join('|') + ')', 'g'), function (m) { return m.replace(/ /g, NB); }],
    // ~할 수 있다/없다
    [/(\S) 수 (있|없)/g, '$1' + NB + '수' + NB + '$2'],
    // 앞 단어에 붙어야 하는 말
    [/ (여부|경우|등|위해|통해|이내|이상|이하|소요|기준|중)(?=[\s.,)·을를이가은는의에와과도로으]|$)/g, NB + '$1'],
    // 접속어는 앞 단어 끝에 붙인다: "인증 목적 및 / 희망 인증등급"
    [/ (및|또는|그리고)(?=\s)/g, NB + '$1'],
    // "본 약관"처럼 뒤 단어와 함께 가야 하는 말
    [/(^|\s)(본) /g, '$1$2' + NB],
    // "기준에 대한", "기관에 따라"처럼 조사와 뒤따르는 말은 한 덩어리
    [/(에|와|과|에게) (대한|대해|따라|따른|관한|관해|의한|의해|비해|맞춰|맞게|걸쳐|앞서)(?=[\s.,]|$)/g, '$1' + NB + '$2'],
    // 꾸미는 말 + 꾸밈 받는 말
    // 앞 공백을 소비하지 않아야(?<=) "대한 체계적인 사전점검"처럼 연달아 오는 꾸밈말도 모두 묶인다.
    [new RegExp('(?<=^|[\\s(\\u00A0' + WEAK + LOOSE_MARK + '])(' + LOOSE + ') (?=[가-힣A-Za-z0-9])', 'g'), '$1' + LOOSE_MARK],
    [new RegExp('(?<=^|[\\s(\\u00A0' + WEAK + LOOSE_MARK + '])(' + MODIFIERS + ') (?=[가-힣A-Za-z0-9])', 'g'), '$1' + WEAK],
    [new RegExp('(?<=^|[\\s(\\u00A0' + WEAK + LOOSE_MARK + '])(' + ADNOMINAL + ') (?=[가-힣A-Za-z0-9])', 'g'), '$1' + WEAK],
    // "클라우드서비스의 적합성", "시험기관과의 협업"
    [new RegExp('([^\\s\\u00A0' + WEAK + LOOSE_MARK + ']+의) (?=[가-힣A-Za-z0-9])', 'g'), '$1' + LOOSE_MARK],
    // 괄호 뒤 조사가 다음 줄로 떨어지지 않게: "협회(KACI)의"
    [/\)(?=[가-힣])/g, ')\u2060'],
    [/All rights reserved/g, 'All' + NB + 'rights' + NB + 'reserved']
  ];
  var SKIP = { SCRIPT: 1, STYLE: 1, TEXTAREA: 1, OPTION: 1, TITLE: 1 };
  // 문장 끝(마침표 등) 뒤 공백. "1. 항목" 같은 번호는 앞이 숫자라 제외한다.
  var SENTENCE_END = /([^\d\s][.!?])\s+(?=\S)/g;

  // 덩어리가 MAX_CHUNK 자를 넘으면 느슨한 연결('~의', '~에 대한')부터, 없으면 약한 연결을 뒤에서부터 푼다.
  // 예) "명시된◇정량적◇목표의◆달성·여부를"(18자) → "명시된 정량적 목표의 / 달성 여부를"
  //     "기능에·대한◆체계적인◇사전점검이"(17자) → "기능에 대한 / 체계적인 사전점검이"
  function limitChunk(chunk) {
    if (chunk.length <= MAX_CHUNK) return chunk.split(WEAK).join(NB).split(LOOSE_MARK).join(NB);
    var at = chunk.lastIndexOf(LOOSE_MARK);
    if (at === -1) at = chunk.lastIndexOf(WEAK);
    if (at === -1) return chunk;
    return limitChunk(chunk.slice(0, at)) + ' ' + limitChunk(chunk.slice(at + 1));
  }

  function bindWords(text) {
    var bound = RULES.reduce(function (t, r) { return t.replace(r[0], r[1]); }, text);
    if (bound.indexOf(WEAK) === -1 && bound.indexOf(LOOSE_MARK) === -1) return bound;
    return bound.split(' ').map(limitChunk).join(' ');
  }

  function splitSentences(node) {
    var parent = node.parentNode;
    if (parent.closest('.legal, .wrap-sen')) return;
    var parts = node.nodeValue.replace(SENTENCE_END, '$1\n').split('\n');
    if (parts.length < 2) return;
    var frag = document.createDocumentFragment();
    parts.forEach(function (p, i) {
      if (i > 0) frag.appendChild(document.createTextNode(' '));
      var span = document.createElement('span');
      span.className = 'wrap-sen';
      span.textContent = p;
      frag.appendChild(span);
    });
    parent.replaceChild(frag, node);
  }

  function tidy(root) {
    if (!root) return;
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        return n.parentNode && SKIP[n.parentNode.nodeName] ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    var nodes = [];
    var node;
    while ((node = walker.nextNode())) {
      if (/\S/.test(node.nodeValue)) nodes.push(node);
    }
    nodes.forEach(function (n) {
      var next = bindWords(n.nodeValue);
      if (next !== n.nodeValue) n.nodeValue = next;
      splitSentences(n);
    });
  }

  // 제목·표 머리칸은 마지막 어절이 홀로 한 줄을 차지하지 않도록 끝의 두 어절을 묶는다.
  // 예) "신청 준비부터 심사 대응까지 / 지원합니다" → "신청 준비부터 / 심사 대응까지 지원합니다"
  // 제목은 항상, 표 칸·강조문 같은 짧은 문구(SHORT_MAX자 이하)는 길이를 보고 적용한다.
  var HEADINGS = 'h1, h2, h3, h4';
  var SHORT = 'th, td, dt, dd, b, strong, li, label';
  var SHORT_MAX = 30;
  function bindHeadingEnd(root) {
    var sel = HEADINGS + ', ' + SHORT;
    var list = root.matches && root.matches(sel) ? [root] : root.querySelectorAll(sel);
    Array.prototype.forEach.call(list, function (h) {
      if (h.closest('.legal')) return;
      if (!h.matches(HEADINGS) && h.textContent.trim().length > SHORT_MAX) return;
      var walker = document.createTreeWalker(h, NodeFilter.SHOW_TEXT);
      var last = null, n;
      while ((n = walker.nextNode())) { if (/\S/.test(n.nodeValue)) last = n; }
      if (!last || !/ \S+\s*$/.test(last.nodeValue)) return;
      // "<em>시험 결과</em>로 입증합니다"처럼 앞 요소에 붙은 글자까지 묶이면 덩어리가 길어지므로 건너뛴다.
      var head = last.nodeValue.replace(/ \S+\s*$/, '');
      if (last.previousSibling && /^\S+$/.test(head)) return;
      last.nodeValue = last.nodeValue.replace(/ (\S{1,6})(\s*)$/, NB + '$1$2');
    });
  }

  window.ktarTidyWrap = function (root) { tidy(root); if (root) bindHeadingEnd(root); };
  window.ktarTidyWrap(document.body);
})();
