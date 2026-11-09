#!/usr/bin/env python3
"""시험 상세 2종(공인시험·일반시험 V&V) 생성기. gen_subpages.py 가 호출한다.
구성: 히어로+핵심정보 패널 → 앵커 탭 → 활용 상황 → 비교표 → 프로세스 → 준비 서류 → 문의.
인증 3종(gen_cert.py)과 같은 골격·CSS(cert.css)를 쓴다."""
import re

import gen_cert
from gen_cert import HEAD, TAIL, who

SWITCH = [("공인시험", "certified"), ("일반시험(V&V)", "vv")]
EXTRA_E = "&amp;"

# 모든 문구·수치는 시안용 샘플 (실제 인정 번호·실적은 확정 후 기재)
STEPS_COMMON = [
    ("견적 확인", "견적문의로 의뢰하시면 시험 가능 여부와 견적을 확인해 안내합니다.", ["KTAR"]),
    ("계약 진행", "견적 확인 후 시험 계약을 체결합니다.", ["의뢰자", "KTAR"]),
    ("시험 접수", "시험 대상(실행 파일 · 접속 정보 · 시료)과 관련 자료를 접수합니다.", ["의뢰자"]),
    ("신청서·절차서 제출", "시험신청서와 시험절차서를 작성해 제출합니다. 양식 정리는 KTAR이 돕습니다.", ["의뢰자", "KTAR"]),
    ("시험 진행", "시험절차서에 따라 시험을 수행하고 중간 결과를 공유합니다.", ["KTAR"]),
]

PAGES = {
    "certified": dict(
        title="공인시험",
        lead="공인된 기준과 절차에 따라 시험하고 제3자 공식 성적서를 발급합니다. 제출처가 요구하는 형식에 맞춰 시험 범위를 설계합니다.",
        h1="공인시험,<br><em>공식 성적서</em>로 결과를 증명합니다",
        desc="공인된 기준과 절차에 따라 시험하고 공식 성적서를 발급합니다.",
        facts=[("대상", "공식 성적서가 필요한 소프트웨어 · 제품 · 서비스"),
               ("기준", "공인 시험 기준과 절차 (적용 규격은 확정 시 정리)"),
               ("인정", "인정 범위와 번호는 확정 후 기재"),
               ("효력", "제3자 공식 성적서 — 제출처 요건에 따라 인정"),
               ("소요", "접수 후 1~3주 (시험 항목별 상이)")],
        gain_title="공식 성적서가 필요한 여섯 가지 상황",
        gain_lead="제3자 성적서가 요구되는 대표 상황입니다. 제출 기한 2개월 전에는 시작하는 것이 안전합니다.",
        gains=[("R&D 과제 결과 평가", "과제 최종 평가에서 정량 목표 달성을 제3자 성적서로 증빙합니다."),
               ("공공·조달 제출", "입찰·납품 단계에서 제품 성능과 기능을 공식 문서로 증명합니다."),
               ("정보시스템 검수", "구축 사업의 최종 검수 조건으로 시험 성적서를 요구하는 경우가 많습니다."),
               ("인증 신청 증빙", "인증 신청 시 시험 결과 자료로 제출할 수 있습니다."),
               ("고객사 제출", "제3자 기관의 공식 결과로 신뢰도를 확보합니다."),
               ("홍보 · 마케팅", "공식 시험 결과를 제품 소개서와 영업 자료에 인용할 수 있습니다.")],
        cmp_label="SCOPE", cmp_title="시험 분야별로 이렇게 진행됩니다",
        cmp_lead="대상과 제출처 요건에 맞춰 분야를 정합니다. 범위를 벗어나는 항목은 일반시험(V&V)으로 함께 진행할 수 있습니다.",
        cmp_head=["분야", "시험 내용", "성적서 활용"], cmp_rec=0,
        cmp_rows=[("기능", "기능 명세와 실제 동작을 대조해 충족 여부를 확인", "과제 평가 · 검수 · 조달 제출"),
                  ("성능", "응답시간 · 처리량 · 동시 사용자 등을 시나리오 기반으로 측정", "정량 목표 증빙 · 입찰 제안"),
                  ("신뢰성", "장시간 구동과 오류 상황에서 안정적으로 동작하는지 확인", "납품 검수 · 인증 신청"),
                  ("데이터", "데이터의 정확성 · 완전성 · 일관성을 기준에 따라 측정", "데이터 거래 · 과제 증빙")],
        cmp_note="※ 분야와 세부 항목은 적용 기준에 따라 확정하며, 표는 구조 확인용 샘플입니다.",
        proc_title="접수 전에 범위를 확정합니다.<br>그래서 성적서가 한 번에 나옵니다.",
        last_step=("성적서 발급", "결과를 검토한 뒤 공식 성적서를 발급합니다.", ["KTAR"]),
        docs_title="기업이 준비할 것",
        docs_lead="제출처가 요구하는 항목이 적힌 자료를 먼저 보내 주세요. 나머지 서류는 KTAR 양식으로 정리합니다.",
        docs_you=[("과제 계획서 · 요건 자료", "정량 목표 부분만 가능"), ("시험 대상", "실행 파일 · 접속 정보 · 시료"),
                  ("제품 사양서 · 기능 설명서", "있는 대로"), ("사업자등록증", "신청서 첨부")],
        docs_me=[("시험 신청서", "KTAR 양식"), ("시험 절차서", "상담 후 작성"), ("공식 시험 성적서", "발급")],
        cta_title="계획서의 시험 항목만 보내주시면<br>영업일 3일 내 가능 여부와 견적을 안내합니다",
        cta_lead="협약서 발췌본이면 충분합니다. 시험 가능 여부, 견적, 성적서 발급 예정일을 항목별로 정리해 드립니다.",
    ),
    "vv": dict(
        title="일반시험(V&V)",
        lead="규격에 없는 항목도 고객이 제시한 방법으로 시험합니다. 개발 단계 어디서든 의뢰할 수 있고, 회신이 빠릅니다.",
        h1="규격에 없는 항목도,<br><em>고객 요구</em>에 맞춰 시험합니다",
        desc="고객 요구에 맞춰 시험 항목과 방법을 설계하고 시험 결과 보고서를 발급합니다.",
        facts=[("대상", "소프트웨어 · ICT 제품 · 데이터 · 정보시스템 전 분야"),
               ("방법", "의뢰자 제시 항목·방법 또는 KTAR이 설계한 시험 절차"),
               ("결과서", "일반 시험성적서 · 시험 결과 보고서"),
               ("회신", "영업일 3일 이내 시험 가능 여부 · 견적 · 발급 예정일"),
               ("소요", "접수 후 1~3주 (항목 수에 따라 조정)")],
        gain_title="일반시험(V&V)이 맞는 여섯 가지 상황",
        gain_lead="공식 규격으로 담기 어려운 항목, 빠른 회신이 필요한 상황에 적합합니다. 공식 성적서가 필수인지 먼저 확인해 드립니다.",
        gains=[("발주처 규격서의 고유 요건", "납품 규격서의 성능·기능 요건을 그대로 항목화해 검수용 결과서를 만듭니다."),
               ("과제 계획서의 특수 지표", "공식 규격에 없는 정량 목표를 의뢰자 제시 방법으로 측정합니다."),
               ("출시 전 자체 검증", "제3자 시각으로 기능·성능을 점검해 결함을 미리 걸러냅니다."),
               ("성능 · 부하 측정", "응답시간 · 처리량 · 동시 사용자 · 자원 사용률을 시나리오로 측정합니다."),
               ("데이터 · AI 결과 검증", "학습 데이터 품질과 모델 출력 정확도를 의뢰자 데이터셋 기준으로 검증합니다."),
               ("공인시험 전 사전 시험", "공인 항목으로 가기 전 합격 가능성을 확인해 재시험 비용을 줄입니다.")],
        cmp_label="COMPARE", cmp_title="공인시험과 일반시험(V&V), 언제 무엇을 택하나",
        cmp_lead="제출처가 공식 성적서를 명시하면 공인시험, 항목 설계의 자유도와 속도가 중요하면 일반시험입니다. 두 가지를 섞어 비용을 줄이기도 합니다.",
        cmp_head=["항목", "일반시험(V&V)", "공인시험"], cmp_rec=1,
        cmp_rows=[("시험 항목", "의뢰자가 제시한 항목 · 방법", "공인 기준의 정형 항목"),
                  ("결과서", "시험 결과 보고서 · 일반 시험성적서", "공식 성적서"),
                  ("효력", "발주처 · 과제 요건에 따라 인정", "제3자 공식 문서로 통용"),
                  ("회신 속도", "영업일 3일 이내", "항목 검토 후 견적"),
                  ("진행 시점", "개발 단계 어디서나", "출시 · 제출 직전"),
                  ("적합한 경우", "검수 · 자체 검증 · 특수 지표 · 사전 시험", "과제 평가 · 조달 · 인증 준비")],
        cmp_note="※ 공식 성적서가 요구되는 평가에는 일반 시험성적서가 인정되지 않을 수 있습니다. 상담 시 요건을 먼저 확인합니다.",
        proc_title="영업일 3일 안에<br>가능 여부부터 알려드립니다",
        last_step=("결과서 발급", "결과를 검토한 뒤 시험 결과 보고서를 발급합니다.", ["KTAR"]),
        docs_title="기업이 준비할 것",
        docs_lead="시험하고 싶은 항목이 적힌 자료면 어떤 형식이든 좋습니다. 규격서, 계획서, 메일 본문도 괜찮습니다.",
        docs_you=[("시험 항목 · 요건 자료", "형식 무관"), ("시험 대상", "실행 파일 · 접속 정보 · 시료"),
                  ("제품 사양서 · 사용자 설명서", "있는 대로"), ("사업자등록증", "신청서 첨부")],
        docs_me=[("시험 신청서", "KTAR 양식"), ("시험 절차서", "항목 · 방법 · 판정 기준"), ("시험 결과 보고서", "발급")],
        cta_title="시험하고 싶은 항목만 적어 보내주시면<br>영업일 3일 내 가능 여부와 견적을 안내합니다",
        cta_lead="규격서나 계획서 일부, 메일 본문으로도 충분합니다. 시험 가능 여부, 견적, 결과서 발급 예정일을 함께 회신합니다.",
    ),
}

ANCHORS = [("gain", "활용 상황"), ("cmp", "비교"), ("proc", "프로세스"), ("docs", "준비 서류"), ("contact", "견적문의")]


def esc(s):
    return s.replace("&", "&amp;")


def head_for(slug):
    d = PAGES[slug]
    head = re.sub(r"<title>.*?</title>", f"<title>{esc(d['title'])} | KTAR 한국시험평가원</title>", HEAD)
    head = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{esc(d["desc"])}">', head)
    head = head.replace('<li><a href="../test/certified.html">', '<li class="is-current"><a href="../test/certified.html">', 1)
    return head.replace('<link rel="stylesheet" href="../css/sub.css">',
                        '<link rel="stylesheet" href="../css/sub.css">\n<link rel="stylesheet" href="../css/cert.css">')


def cmp_table(d):
    heads = ""
    for n, h in enumerate(d["cmp_head"]):
        rec = n == d["cmp_rec"] and n > 0
        heads += f'<th scope="col"{" class=rec" if rec else ""}>{esc(h)}{"<small>권장</small>" if rec else ""}</th>'
    rows = ""
    for r in d["cmp_rows"]:
        cells = f'<th scope="row">{esc(r[0])}</th>'
        for n, c in enumerate(r[1:], 1):
            cells += f'<td class="{"rec" if n == d["cmp_rec"] else ""}">{esc(c)}</td>'
        rows += f"<tr>{cells}</tr>"
    return f'<div class="cmp-wrap"><table class="cmp"><thead><tr>{heads}</tr></thead><tbody>{rows}</tbody></table></div>'


def build(slug, repo):
    d = PAGES[slug]
    t = esc(d["title"])
    facts = "".join(f"<div><dt>{k}</dt><dd>{esc(v)}</dd></div>" for k, v in d["facts"])
    tabs = "".join(f'<a href="#{i}">{n}</a>' for i, n in ANCHORS)
    sw = "".join(f'<a href="{s}.html"' + (' aria-current="page"' if s == slug else "") + f">{esc(n)}</a>" for n, s in SWITCH)
    gains = "".join(f'<li><span class="gain__no">{n:02d}</span><b>{esc(a)}</b><span>{esc(b)}</span></li>'
                    for n, (a, b) in enumerate(d["gains"], 1))
    steps_src = STEPS_COMMON + [d["last_step"]]
    steps = "".join(
        f'<li class="{"k" if len(r) == 1 and r[0] == "KTAR" else ""}"><span class="proc__no">{n}</span><b>{esc(a)}</b><p>{esc(b)}</p>{who(r)}</li>'
        for n, (a, b, r) in enumerate(steps_src, 1))
    you = "".join(f"<li>{esc(a)}<span>{esc(b)}</span></li>" for a, b in d["docs_you"])
    me = "".join(f"<li>{esc(a)}<span>{esc(b)}</span></li>" for a, b in d["docs_me"])

    main = f'''<main class="cp">
  <section class="ph">
    <div class="inner ph__inner">
      <ol class="crumb" aria-label="현재 위치">
        <li><a href="../index.html">홈</a></li>
        <li>시험</li>
        <li aria-current="page">{t}</li>
      </ol>
      <div>
        <p class="eyebrow">TEST</p>
        <h1>{d["h1"].replace("&", "&amp;")}</h1>
        <p class="ph__lead">{esc(d["lead"])}</p>
        <div class="ph__cta">
          <a class="btn btn--fill" href="../index.html#inquiry">{t} 견적문의</a>
          <a class="btn btn--line" href="#proc">발급 프로세스 보기</a>
        </div>
      </div>
      <aside class="fact" aria-label="{t} 핵심 정보">
        <div class="fact__head">{t} 한눈에 보기<small>KTAR</small></div>
        <dl>{facts}</dl>
      </aside>
    </div>
  </section>

  <div class="atab">
    <div class="inner atab__inner">
      <nav aria-label="페이지 내 이동">{tabs}</nav>
      <div class="atab__sw"><span>시험 서비스</span>{sw}</div>
    </div>
  </div>

  <section class="cs" id="gain">
    <div class="inner">
      <div class="kh"><p class="kh__label">USE CASE</p><h2>{esc(d["gain_title"])}</h2><p>{esc(d["gain_lead"])}</p></div>
      <ol class="gain">{gains}</ol>
    </div>
  </section>

  <section class="cs cs--bg" id="cmp">
    <div class="inner">
      <div class="kh"><p class="kh__label">{d["cmp_label"]}</p><h2>{esc(d["cmp_title"])}</h2><p>{esc(d["cmp_lead"])}</p></div>
      {cmp_table(d)}
      <p class="cmp-note">{esc(d["cmp_note"])}</p>
    </div>
  </section>

  <section class="cs" id="proc">
    <div class="inner">
      <div class="kh"><p class="kh__label">PROCESS</p><h2>{d["proc_title"]}</h2></div>
      <div class="proc-ban"><b>진행 방식이 궁금하시면 <em>견적문의</em>로 먼저 남겨 주세요.</b><a href="../index.html#inquiry">견적문의</a></div>
      <ol class="proc">{steps}</ol>
    </div>
  </section>

  <section class="cs cs--bg" id="docs">
    <div class="inner">
      <div class="kh"><p class="kh__label">DOCUMENTS</p><h2>{esc(d["docs_title"])}</h2><p>{esc(d["docs_lead"])}</p></div>
      <div class="docs">
        <div class="docs__col"><h3>기업<small>준비</small></h3><ul>{you}</ul></div>
        <div class="docs__col me"><h3>KTAR<small>대행</small></h3><ul>{me}</ul></div>
      </div>
      <p class="docs-note">서류 양식은 견적문의 후 담당자가 메일로 보내드립니다.</p>
    </div>
  </section>

  <section class="contact" id="contact">
    <div class="inner contact__inner">
      <div>
        <p class="kh__label">CONTACT</p>
        <h2>{d["cta_title"]}</h2>
        <p>{esc(d["cta_lead"])}</p>
      </div>
      <div class="contact__side">
        <div class="contact__tel">대표전화<b>00-0000-0000</b></div>
        <a class="btn btn--fill" href="../index.html#inquiry">{t} 견적문의</a>
      </div>
    </div>
  </section>

  <div class="sample-wrap"><div class="inner"><p class="sample-note">※ 본 페이지의 문구·수치는 시안용 샘플입니다. 실제 내용 확정 후 교체됩니다.</p></div></div>
</main>'''
    path = f"{repo}/test/{slug}.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(head_for(slug) + main + TAIL)
    return path


def build_all(repo):
    for slug in PAGES:
        print("wrote", build(slug, repo))
