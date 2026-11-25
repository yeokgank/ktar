/* 의미 단위 줄바꿈 보정: 한 줄 끝이나 다음 줄 첫머리에 홀로 떨어지면 어색한 말을
   앞뒤 단어와 줄바꿈 없는 공백(U+00A0)으로 묶는다. CSS(keep-all·text-wrap)로 못 잡는 부분만 다룬다.
   예) "3일 이내", "가능 여부", "입증할 수 있습니다", "및 기관", "All rights reserved" */
(function () {
  var NB = ' ';
  var RULES = [
    // ~할 수 있다/없다
    [/(\S) 수 (있|없)/g, '$1' + NB + '수' + NB + '$2'],
    // 앞 단어에 붙어야 하는 말
    [/ (여부|경우|등|위해|통해|이내|이상|이하|소요|기준|중)(?=[\s.,)·]|$)/g, NB + '$1'],
    // 뒤 단어와 함께 가야 하는 접속어
    [/(^|\s)(및|또는|본) /g, '$1$2' + NB],
    // 괄호 뒤 조사가 다음 줄로 떨어지지 않게: "협회(KACI)의"
    [/\)(?=[가-힣])/g, ')⁠'],
    [/All rights reserved/g, 'All' + NB + 'rights' + NB + 'reserved']
  ];
  var SKIP = { SCRIPT: 1, STYLE: 1, TEXTAREA: 1, OPTION: 1 };

  function tidy(root) {
    if (!root) return;
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        return n.parentNode && SKIP[n.parentNode.nodeName] ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    var node;
    while ((node = walker.nextNode())) {
      var text = node.nodeValue;
      if (!/\S/.test(text)) continue;
      var next = RULES.reduce(function (t, r) { return t.replace(r[0], r[1]); }, text);
      if (next !== text) node.nodeValue = next;
    }
  }

  window.ktarTidyWrap = tidy;
  tidy(document.body);
})();
