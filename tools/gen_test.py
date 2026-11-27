#!/usr/bin/env python3
"""시험 상세 2종(공인시험·일반시험 V&V) 생성기. gen_subpages.py 가 호출한다.
구성: 히어로+핵심정보 패널 → 앵커 탭 → 활용 상황 → 비교표 → 프로세스 → 준비 서류 → 문의.
인증 3종(gen_cert.py)과 같은 골격·CSS(cert.css)를 쓴다."""
import re

import gen_cert
from gen_cert import HEAD, TAIL

SWITCH = [("공인시험", "certified"), ("일반시험(V&V)", "vv")]
EXTRA_E = "&amp;"

PAGES = {
    "certified": dict(
        title="공인시험",
        # Figma 11-25 #89 히어로
        lead="정부 R&D 과제의 정량적 목표부터 제품 및 소프트웨어의 기술적 성능까지, "
             "시험 목적에 적합한 평가 기준을 검토하고 성적서 발급까지 체계적으로 관리합니다.",
        h1="공인시험,<br><em>객관적인 시험 결과</em>로<br>기술의 신뢰성을 입증합니다",
        facts=[("대상", "정부 R&D 과제, 제품·소프트웨어 및 서비스"),
               ("시험분야", "기능적합성, 성능, 신뢰성, 데이터 품질 등"),
               ("시험기준", "시험기관의 KOLAS 인정범위 내 시험규격 및 절차"),
               ("결과문서", "KOLAS 공인시험성적서"),
               ("견적안내", "문의 접수 후 3영업일 이내 안내"),
               ("소요기간", "시험항목, 측정 조건 및 시험기관 일정에 따라 상이")],
        # #90 탭
        tabs=[("gain", "활용 목적"), ("cmp", "평가항목"), ("proc", "진행 절차"), ("docs", "준비자료"), ("contact", "견적 문의")],
        # #69
        gain_title="시험성적서의 주요 활용 목적",
        gain_lead="시험성적서는 제품 및 기술의 시험 결과를 객관적인 자료로 제시하는 데 활용됩니다. "
                  "기업은 연구개발, 품질관리, 사업화 등 다양한 목적에 따라 시험성적서를 활용할 수 있습니다.",
        gains=[("정부 R&D 과제 성과 입증", "정량적 목표 달성 여부, 연구개발 성과보고서 및 중간·최종평가 증빙자료"),
               ("제품 품질 및 성능 관리", "제품의 품질 수준 확인, 성능 개선 전후 비교 및 내부 품질관리 자료"),
               ("공공조달 및 입찰 참여", "공공기관의 입찰 참가 요건, 제안서 평가 및 조달 관련 기술 증빙자료"),
               ("납품 및 검수 대응", "계약상 요구 사양의 충족 여부, 납품 제품 및 구축 시스템의 검수 증빙자료"),
               ("기술 홍보 및 사업화", "제품 소개서, 기술제안서, 투자유치 및 영업 활동을 위한 객관적인 성능자료"),
               ("해외시장 진출", "해외 거래처 및 발주기관의 기술 요구사항 대응과 수출 관련 시험 증빙자료")],
        gain_note="※ 시험성적서의 활용 및 인정 여부는 관련 제도, 계약 조건 및 제출기관의 요구사항에 따라 달라질 수 있습니다.",
        # #70
        cmp_title="주요 시험평가 분야 및 평가항목",
        cmp_lead="제품 및 소프트웨어의 기능, 성능, 신뢰성, 데이터 품질 등 다양한 기술적 특성을 평가합니다. "
                 "제품의 특성과 요구 성능에 따라 적합한 시험항목 및 평가 기준을 검토합니다.",
        cmp_head=["평가 분야", "시험 내용", "주요 평가항목"], cmp_rec=0,
        cmp_rows=[("기능적합성", "요구 기능의 구현 여부 및 정상 작동 여부 평가", "기능 구현율, 기능 정확성, 정상 작동 여부"),
                  ("성능", "요구 성능 및 정량적 성능지표 측정", "응답시간, 처리속도, 처리량, 자원 사용량"),
                  ("신뢰성", "지속적인 작동 및 장애 발생 조건에서의 신뢰성 평가", "작동 성공률, 오류 발생률, 장애 복구시간"),
                  ("데이터 품질", "데이터의 품질특성 및 요구 기준 충족 여부 평가", "정확성, 완전성, 일관성, 현재성")],
        cmp_note="※ 세부 시험항목 및 적용 규격은 제품 특성과 요구사항에 따라 달라지며, "
                 "공인시험 가능 여부는 해당 시험기관의 KOLAS 인정범위를 기준으로 확인합니다.",
        # #71
        proc_title="시험 상담부터 공인시험성적서 발급까지,<br>체계적으로 진행합니다",
        proc_lead="시험 목적에 따른 기술 검토부터 시험방법 협의, 일정 관리 및 성적서 전달까지 단계별로 진행합니다.",
        proc_ban="시험항목과 목표 기준을 남겨주시면 시험 가능 여부 및 견적을 안내드립니다.",
        steps=[("시험 상담 및 견적 안내", "시험 대상과 요구사항을 확인하고 시험 가능 여부, 예상 비용 및 일정을 안내합니다."),
               ("시험 계약", "시험 범위, 비용 및 계약 조건을 확정하고 계약 절차를 진행합니다."),
               ("시험자료 접수", "시험에 필요한 제품, 실행파일, 데이터셋 및 관련 기술자료를 접수합니다."),
               ("시험신청서 및 절차서 준비", "시험기관의 제출 기준에 따라 필요서류를 준비하고 세부 시험방법과 평가 기준을 협의합니다."),
               ("시험평가 수행", "협력 공인시험기관에서 시험을 수행하며, KTAR는 진행 일정 및 관련 사항을 관리합니다."),
               ("공인시험성적서 발급", "공인시험기관에서 시험 결과를 검토하여 성적서를 발급하면 KTAR는 최종 성적서를 전달합니다.")],
        proc_note="※ 세부 진행 절차 및 소요기간은 시험항목과 시험기관의 일정에 따라 달라질 수 있습니다.",
        # #72 (카드는 우측 그대로 — 답글)
        docs_title="공인시험 진행 시 준비자료",
        docs_leads=["시험 대상과 평가항목을 확인할 수 있는 자료를 준비해 주시면 보다 정확한 시험 검토 및 견적 안내가 가능합니다.",
                    "최초 문의 시에는 보유 중인 자료만 전달해 주셔도 되며, 추가 제출서류는 시험 진행 단계에 따라 안내드립니다."],
        docs_you=[("시험항목 및 목표 기준", "연구개발계획서, 정량적 목표항목, 요구 성능 등"),
                  ("시험 대상", "제품, 시료, 실행파일, 접속 정보, 데이터셋 등"),
                  ("제품 사양서 및 기능 설명서", "제품 사양, 주요 기능, 작동 조건 및 기술적 특성"),
                  ("사업자등록증", "계약 및 시험 신청 단계에서 제출"),
                  ("시험신청서", "시험기관별 지정 양식에 따라 별도 안내")],
    ),
    "vv": dict(
        title="일반시험(V&V)",
        # #87 히어로
        lead="정부 R&D 과제의 정량적 목표부터 제품·서비스의 기능 및 성능까지, "
             "요구사항에 적합한 시험방법과 평가 기준을 검토하고 시험 진행 전반을 관리합니다.",
        h1="일반시험,<br><em>검증 목적에 맞는 시험평가</em>를<br>체계적으로 진행합니다",
        cta1="일반시험 견적문의",
        facts=[("대상", "정부 R&D 과제, 제품·서비스 및 특수 시험항목"),
               ("목적", "정량적 목표 달성 여부 및 기능·성능 검증"),
               ("시험기준", "표준 시험규격 또는 협의된 시험방법"),
               ("결과문서", "일반시험성적서 또는 시험결과보고서"),
               ("견적안내", "문의 접수 후 3영업일 이내 안내"),
               ("소요기간", "시험항목, 측정 조건 및 시험기관 일정에 따라 상이")],
        # #88
        tabs=[("gain", "필요 상황"), ("cmp", "시험유형 비교"), ("proc", "진행 절차"), ("docs", "준비자료"), ("contact", "견적 문의")],
        # #63 제목·설명(설명은 #63 본문 채택 — 사용자 확정) + #64 카드
        gain_title="일반시험이 필요한 주요 상황",
        gain_lead="공인시험 적용이 어렵거나 별도의 시험방법 협의가 필요한 경우, 검증 목적과 요구사항에 따라 일반시험을 활용할 수 있습니다.",
        gains=[("R&D 목표 달성을 입증해야 할 때", "정부 R&D 과제계획서상 정량적 목표, 성능지표 및 연구개발 결과의 평가자료 확보"),
               ("개발 기술을 검증해야 할 때", "시제품의 기능 구현, 설계 적합성 및 신규 기술의 성능 검증"),
               ("제품 품질을 관리해야 할 때", "양산 제품의 품질 편차, 반복 작동 성능 및 내구성 확인"),
               ("납품·검수를 앞두고 있을 때", "발주처 요구 사양, 계약상 성능 기준 및 검수용 시험자료 확보"),
               ("제품 경쟁력을 입증해야 할 때", "기존 제품 또는 경쟁 제품과의 비교시험 및 영업·홍보용 객관적 자료 확보"),
               ("인증 취득을 준비하고 있을 때", "인증시험 전 예상 부적합 항목 파악 및 제품 보완을 위한 사전시험")],
        gain_note="※ 일반시험성적서의 인정 여부는 해당 사업의 평가 기준, 계약 조건 및 제출처의 요구사항에 따라 달라질 수 있습니다.",
        # #65 (공인시험 열 강조는 cmp--split)
        cmp_title="공인시험과 일반시험, 제출 목적에 맞게 선택하세요",
        cmp_lead="시험 목적, 적용 시험규격 및 성적서 제출 요건에 따라 적합한 시험 형태를 선택할 수 있습니다.",
        cmp_head=["구분", "일반시험", "공인시험"], cmp_rec=0, cmp_cls="cmp--split",
        cmp_rows=[("시험 기준", "표준 시험규격 또는 협의된 시험방법", "시험기관의 KOLAS 인정범위(ISO/IEC) 내 규격절차"),
                  ("시험 수행", "해당 시험 수행이 가능한 시험기관", "해당 시험항목에 대한 인정범위를 보유한 KOLAS 공인시험기관"),
                  ("결과 문서", "일반시험성적서 또는 시험결과보고서", "KOLAS 공인시험성적서"),
                  ("주요 활용", "R&D 성과 검증, 품질관리, 납품·검수 등", "공인시험성적서 제출이 요구되는 과제평가, 조달, 인증 등"),
                  ("소요기간", "시험일로부터 약 2주", "시험일로부터 약 4주"),
                  ("시험 비용", "시험항목 및 측정 조건에 따라 산정", "적용 규격 및 시험 범위에 따라 산정")],
        cmp_note="※ 시험성적서의 인정 여부는 과제 관리기관, 발주처 등 제출처의 요구사항에 따라 달라질 수 있습니다.<br>"
                 "※ 소요기간 및 비용은 시험항목, 시험환경 및 시험기관의 일정에 따라 달라질 수 있습니다.",
        # #66
        proc_title="시험 상담부터 시험성적서 발급까지,<br>체계적으로 진행합니다",
        proc_ban="시험항목과 목표 기준을 남겨주시면 시험 가능 여부 및 견적을 안내드립니다.",
        steps=[("견적 문의", "시험 대상, 정량적 목표항목, 요구 성능 및 희망 일정을 확인합니다."),
               ("시험 검토·견적", "협력 시험기관과 시험 가능 여부, 시험방법, 비용 및 일정을 검토하여 견적을 안내합니다."),
               ("시험 접수", "시험신청서, 기술자료 및 시험에 필요한 시료를 접수합니다."),
               ("시험방법 및 절차 협의", "시험항목, 측정 조건, 시험방법 및 판정 기준을 구체화하고 세부 시험절차를 협의합니다."),
               ("시험 수행", "협력 시험기관에서 시험을 수행하며, KTAR는 진행 일정 및 관련 사항을 관리합니다."),
               ("성적서·보고서 발급", "시험 수행기관에서 시험 결과를 검토하여 성적서 또는 보고서를 발급하면 KTAR는 최종 결과 문서를 전달합니다.")],
        proc_note="※ 세부 진행 절차 및 소요기간은 시험항목과 시험기관의 일정에 따라 달라질 수 있습니다.",
        # #67 (카드는 우측 그대로 — 답글)
        docs_title="일반시험 문의 시 준비자료",
        docs_leads=["최초 문의 시에는 현재 보유 중인 자료만으로도 시험 검토가 가능합니다. 추가로 필요한 자료는 담당자를 통해 안내드립니다."],
        docs_note="보안이 필요한 기술자료는 담당자와 협의 후 별도로 전달해 주세요.",
        docs_you=[("시험항목 및 목표 기준", "정량적 목표항목, 목표 수치 등"),
                  ("시험 대상 제품·서비스 정보", "제품 소개자료, 기본 사양 등"),
                  ("시험방법 및 측정 조건", "적용 시험규격, 측정방법 등 보유 자료"),
                  ("시료 및 시험환경 정보", "시료 사양, 소프트웨어 실행환경 등")],
        cta_btn="일반시험 견적문의",
    ),
}


def esc(s):
    return s.replace("&", "&amp;")


def head_for(slug):
    d = PAGES[slug]
    head = re.sub(r"<title>.*?</title>", f"<title>{esc(d['title'])} | KTAR 한국시험평가원</title>", HEAD)
    head = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{esc(d.get("desc") or d["lead"])}">', head)
    head = head.replace('<li><a href="../test/certified.html">', '<li class="is-current"><a href="../test/certified.html">', 1)
    return head.replace('<link rel="stylesheet" href="../css/sub.css?v=20261127a">',
                        '<link rel="stylesheet" href="../css/sub.css?v=20261127a">\n<link rel="stylesheet" href="../css/cert.css?v=20261127a">')


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
    cls = f' {d["cmp_cls"]}' if d.get("cmp_cls") else ""
    return f'<div class="cmp-wrap"><table class="cmp{cls}"><thead><tr>{heads}</tr></thead><tbody>{rows}</tbody></table></div>'


def build(slug, repo):
    d = PAGES[slug]
    t = esc(d["title"])
    lead_html = f'<p class="ph__lead">{esc(d["lead"])}</p>' if d["lead"] else ""
    facts ="".join(f"<div><dt>{k}</dt><dd>{esc(v)}</dd></div>" for k, v in d["facts"])
    tabs = gen_cert.tabs_html(d["tabs"])
    sw = "".join(f'<a href="{s}.html"' + (' aria-current="page"' if s == slug else "") + f">{esc(n)}</a>" for n, s in SWITCH)
    gains = "".join(f'<li><span class="gain__no">{n:02d}</span><b>{esc(a)}</b><span>{esc(b)}</span></li>'
                    for n, (a, b) in enumerate(d["gains"], 1))
    gain_note = f'<p class="cmp-note">{esc(d["gain_note"])}</p>' if d.get("gain_note") else ""
    steps_src = d["steps"]
    proc_lead = f'<p>{esc(d["proc_lead"])}</p>' if d.get("proc_lead") else ""
    docs_note = esc(d["docs_note"]) if d.get("docs_note") else None
    steps = gen_cert.steps_html([tuple(esc(x) for x in st) for st in steps_src])
    docs = gen_cert.docs_html(esc(d["docs_title"]), [esc(x) for x in d["docs_leads"]],
                              [(esc(a), esc(b)) for a, b in d["docs_you"]], docs_note)
    cta1 = esc(d.get("cta1", f"{d['title']} 견적문의"))
    cta_btn = esc(d.get("cta_btn", f"{d['title']} 견적문의"))
    proc_ban = esc(d["proc_ban"])
    proc_note = gen_cert.note_html(esc(d["proc_note"])) if d.get("proc_note") else ""

    main = f'''<main class="cp">
  <section class="ph ph--{slug}">
    <div class="inner ph__inner">
      <ol class="crumb" aria-label="현재 위치">
        <li><a href="../index.html">홈</a></li>
        <li>시험</li>
        <li aria-current="page">{t}</li>
      </ol>
      <div>
        <h1>{d["h1"].replace("&", "&amp;")}</h1>
        {lead_html}
        <div class="ph__cta">
          <a class="btn btn--fill" href="../index.html#inquiry">{cta1}</a>
          <a class="btn btn--line" href="#proc">{gen_cert.CTA2}</a>
        </div>
      </div>
      <aside class="fact fact--glass" aria-label="{t} 핵심 정보">
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
      <div class="kh"><h2>{esc(d["gain_title"])}</h2><p>{esc(d["gain_lead"])}</p></div>
      <ol class="gain">{gains}</ol>
      {gain_note}
    </div>
  </section>

  <section class="cs cs--bg" id="cmp">
    <div class="inner">
      <div class="kh"><h2>{esc(d["cmp_title"])}</h2><p>{esc(d["cmp_lead"])}</p></div>
      {cmp_table(d)}
      <p class="cmp-note">{esc(d["cmp_note"])}</p>
    </div>
  </section>

  <section class="cs" id="proc">
    <div class="inner">
      <div class="kh"><h2>{d["proc_title"]}</h2>{proc_lead}</div>
      <div class="proc-ban"><b>{proc_ban}</b><a href="../index.html#inquiry">견적문의</a></div>
      {steps}
      {proc_note}
    </div>
  </section>

  {docs}

  {gen_cert.contact_html(cta_btn)}

</main>'''
    path = f"{repo}/test/{slug}.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(head_for(slug) + main + TAIL)
    return path


def build_all(repo):
    for slug in PAGES:
        print("wrote", build(slug, repo))
