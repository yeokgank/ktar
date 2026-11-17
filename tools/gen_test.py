#!/usr/bin/env python3
"""시험 상세 2종(공인시험·일반시험 V&V) 생성기. gen_subpages.py 가 호출한다.
구성: 히어로+핵심정보 패널 → 앵커 탭 → 활용 상황 → 비교표 → 프로세스 → 준비 서류 → 문의.
인증 3종(gen_cert.py)과 같은 골격·CSS(cert.css)를 쓴다."""
import re

import gen_cert
from gen_cert import HEAD, TAIL

DOCS_NOTE = "서류 양식은 견적문의 후 담당자가 메일로 보내드립니다."
SAMPLE_NOTE = ('<div class="sample-wrap"><div class="inner"><p class="sample-note">'
               "※ 본 페이지의 문구·수치는 시안용 샘플입니다. 실제 내용 확정 후 교체됩니다.</p></div></div>\n")


def who(roles):
    """KTAR 이 맡는 역할(KTAR, KTAR 지원 등)은 강조 칩으로 표시."""
    return '<div class="who">' + "".join(
        f'<i class="{"me" if r.startswith("KTAR") else ""}">{r}</i>' for r in roles) + "</div>"

SWITCH = [("공인시험", "certified"), ("일반시험(V&V)", "vv")]
EXTRA_E = "&amp;"

PAGES = {
    "certified": dict(
        title="공인시험",
        lead="KTAR은 기업의 연구개발 성과 및 제품의 기술적 성능을 객관적으로 검증할 수 있도록 시험평가 서비스를 지원합니다.<br>"
             "시험 항목 검토부터 적합한 시험기관 연계, 시험 일정 협의 및 성적서 발급까지 체계적인 진행 서비스를 제공합니다.",
        h1="기술의 가치를<br><em>객관적인 시험 결과</em>로 입증합니다",
        desc="KTAR은 시험 항목 검토부터 시험기관 연계, 일정 협의, 성적서 발급까지 시험평가 진행을 지원합니다.",
        facts=[("시험 대상", "소프트웨어, 제품, 서비스 및 정부 R&D 과제 결과물"),
               ("시험 분야", "기능, 성능, 신뢰성, 데이터 품질 등"),
               ("진행 방식", "시험 항목 검토 및 전문 시험기관 연계"),
               ("성적서", "시험 유형과 기관의 인정 범위에 따라 공인 또는 일반시험성적서 발급 지원"),
               ("소요기간", "시험 항목 및 시험기관 일정에 따라 별도 안내")],
        gain_title="시험성적서가 활용되는 주요 분야",
        gain_lead="시험성적서는 연구개발 성과 검증부터 제품의 기술적 신뢰성 확보까지 다양한 목적으로 활용됩니다. "
                  "제출처의 요구사항에 따라 적합한 시험 유형과 평가 항목을 검토할 수 있습니다.",
        gains=[("정부 R&D 과제 성과 검증", "연구개발계획서에 명시된 정량적 목표의 달성 여부를 시험평가 결과로 확인하여 과제 평가에 필요한 객관적인 증빙자료를 확보합니다."),
               ("제품 품질 및 기술 성능 입증", "제품 및 소프트웨어의 기능, 성능, 데이터 품질 등을 시험하여 기술적 완성도와 품질 수준을 객관적인 결과로 제시할 수 있습니다."),
               ("공공조달 및 입찰 평가", "공공기관 입찰 및 조달 과정에서 요구하는 성능과 기능에 관한 시험 결과를 제출자료로 활용할 수 있습니다."),
               ("정보시스템 구축 및 검수", "정보시스템 구축 완료 후 요구된 기능과 성능의 충족 여부를 확인하고, 시험 결과를 최종 검수 및 납품 자료로 활용합니다."),
               ("기술 홍보 및 사업화", "객관적인 시험평가 결과를 제품 소개서, 기술제안서 및 영업자료 등에 활용하여 제품의 기술적 신뢰도를 높일 수 있습니다."),
               ("해외시장 진출", "해외 거래처 또는 발주기관이 요구하는 시험자료를 준비하고, 필요한 경우 국제 상호인정 체계가 적용되는 공인시험 진행을 지원합니다.")],
        gain_note="※ 시험성적서의 활용 및 인정 여부는 제출기관별 요구조건에 따라 달라질 수 있습니다.",
        cmp_label="SCOPE", cmp_title="시험 목적에 맞는 평가 분야를 안내합니다",
        cmp_lead="KTAR은 기업의 시험 목적과 평가 항목을 검토하여 적합한 시험기관을 연계합니다. "
                 "공인시험이 필요한 경우 협력 시험기관의 인정 범위를 확인하여 진행하며, "
                 "그 외 항목은 일반시험(V&V) 가능 여부를 별도로 검토합니다.",
        cmp_head=["분야", "시험 내용", "주요 활용"], cmp_rec=0,
        cmp_rows=[("기능", "소프트웨어의 요구 기능과 실제 동작을 비교하여 기능 충족 여부 평가", "정부과제 성과 검증, 제품 검수"),
                  ("성능", "응답시간, 처리량, 처리속도 등 정량적 성능 지표 측정", "R&D 정량 목표 입증, 입찰자료"),
                  ("신뢰성", "반복 작동, 장시간 운영 및 오류 발생 조건에서의 안정성 평가", "제품 품질 검증, 납품 검수"),
                  ("데이터 품질", "데이터의 정확성, 완전성, 일관성 및 현재성 등 품질 특성 평가", "AI·데이터 관련 과제, 데이터 품질 검증")],
        cmp_note="시험 가능 항목 및 적용 규격은 시험 목적과 의뢰 조건에 따라 검토되며, "
                 "공인시험 여부는 해당 시험기관의 KOLAS 인정 범위를 기준으로 확인합니다.<br>"
                 "※ 본 표는 KTAR의 지원 가능 분야에 대한 안내이며, KTAR 자체의 KOLAS 인정 범위를 의미하지 않습니다.",
        proc_title="시험 상담부터 성적서 발급까지<br>체계적으로 지원합니다",
        proc_lead="KTAR은 시험 의뢰 과정에서 필요한 실무 절차를 지원하고, 협력 시험기관과의 원활한 업무 진행을 돕습니다.",
        steps=[("시험 상담 및 견적 검토", "시험 대상 및 요구사항을 확인하고 시험 가능 여부와 예상 비용을 검토하여 안내합니다.", ["KTAR"]),
               ("시험 계약", "시험 범위와 견적을 확정한 후 계약 절차를 진행합니다.", ["의뢰자", "계약 당사자"]),
               ("시험자료 접수", "시험에 필요한 제품, 실행파일, 데이터셋 및 관련 기술자료를 접수합니다.", ["의뢰자", "KTAR 지원"]),
               ("시험신청서 및 절차서 준비", "시험기관의 제출 기준에 따라 필요한 서류와 시험절차서 작성을 지원합니다.",
                ["KTAR", "의뢰자", "협력 시험기관"]),
               ("시험평가 수행", "확정된 시험절차에 따라 전문 시험기관에서 시험평가를 실시하며, KTAR은 진행 일정과 관련 협의를 지원합니다.",
                ["협력 시험기관", "KTAR 진행 지원"]),
               ("시험성적서 발급", "시험기관에서 시험 결과를 검토하고 해당 기관 명의로 성적서를 발급합니다. KTAR은 발급 일정 확인 및 전달 절차를 지원합니다.",
                ["협력 시험기관", "KTAR 발급 지원"])],
        docs_title="시험평가 진행 시 필요한 준비자료",
        docs_lead="시험 대상과 정량적 평가 항목을 확인할 수 있는 자료를 준비해 주시면 시험 가능 여부 및 진행 절차 검토에 도움이 됩니다.",
        docs_desc=True,
        docs_you=[("연구개발계획서", "정량적 목표 및 시험평가 관련 내용"),
                  ("시험 대상", "실행파일, 접속 정보, 시료, 데이터셋 등"),
                  ("제품 사양서 및 기능 설명서", "시험 대상의 주요 기능과 기술적 특성 확인"),
                  ("사업자등록증", "계약 및 시험 신청 시 필요"),
                  ("시험신청서", "시험기관별 양식에 따라 별도 안내")],
        docs_note="시험에 필요한 서류는 평가 항목 및 시험기관에 따라 달라질 수 있으며, 상담 후 담당자가 상세하게 안내드립니다.",
        cta_title="시험평가가 필요하신가요?<br>KTAR이 함께 검토하겠습니다",
        cta_lead=["기업의 시험 목적과 평가 항목을 확인하여 적합한 시험기관 및 진행 방법을 안내해 드립니다. "
                  "기업명, 담당자 연락처 및 문의사항을 남겨주시면 담당자가 확인 후 연락드립니다.",
                  "견적 검토에 필요한 자료는 별도로 안내하며, 접수 후 영업일 기준 3일 이내 견적 안내를 목표로 합니다."],
        cta_note="※ 시험기관의 추가 검토가 필요한 경우 회신 일정이 조정될 수 있습니다.",
        sample=False,
    ),
    "vv": dict(
        title="일반시험(V&V)",
        lead="정부 R&D 과제의 정량적 목표와 기업별 검증 요구사항을 검토하고, 적합한 협력 시험기관과 연계해 시험 진행 및 성적서 발급 절차를 지원합니다.",
        h1="정해진 규격 외 시험항목도,<br><em>목적에 맞는 시험평가</em>를 지원합니다",
        cta1="일반시험 견적문의", cta2="시험 진행 절차 보기",
        facts=[("대상", "정부 R&D 과제, 제품·서비스 성능 검증, 특수 시험항목"),
               ("방법", "의뢰자 제시 항목과 시험방법을 바탕으로 협력 시험기관과 검토"),
               ("결과서", "시험 수행기관 명의의 일반 시험성적서 또는 시험 결과 보고서"),
               ("회신", "문의 접수 후 영업일 기준 3일 이내 견적 안내 목표 (추가 검토 시 별도 안내)"),
               ("소요", "시험항목·시험 조건·기관 일정에 따라 개별 협의")],
        gain_title="일반시험이 필요한 여섯 가지 상황",
        gain_lead="공인시험 규격만으로 평가하기 어려운 항목부터 정부 R&D 과제의 정량지표까지, 검증 목적과 제출 요건을 먼저 확인합니다.",
        gains=[("R&D 정량적 목표 검증", "과제계획서에 명시된 성능지표와 측정방법을 검토하여 시험기관 연계를 지원합니다."),
               ("특수 성능지표 평가", "정해진 시험규격이 없거나 별도 시험방법 협의가 필요한 항목을 검토합니다."),
               ("개발 성과 확인", "시제품 또는 개발 기술의 기능·성능 검증을 위한 시험 진행을 지원합니다."),
               ("납품·검수 요건 대응", "발주처 및 납품처가 요구하는 시험항목과 결과 문서의 적합성을 검토합니다."),
               ("제품·서비스 성능 확인", "제품의 사용조건과 검증 목적에 맞춰 시험항목 및 측정 조건을 협의합니다."),
               ("공인시험 전 사전 확인", "공인시험 접수 전 내부 또는 외부 시험을 통한 성능 확인 필요성을 검토합니다.")],
        cmp_label="COMPARE", cmp_title="공인시험과 일반시험, 제출 목적에 맞게 선택하세요",
        cmp_lead="공인성적서 제출이 필요한지, 협의된 시험방법을 활용할 수 있는지에 따라 적합한 시험 형태가 달라집니다.",
        cmp_head=["항목", "일반시험(V&V)", "공인시험"], cmp_rec=0,
        cmp_rows=[("시험 기준", "의뢰자 제시 항목 및 협의된 시험방법", "시험기관 인정범위 내 규격·절차"),
                  ("시험 수행", "해당 시험 수행기관", "해당 공인시험기관"),
                  ("결과 문서", "일반 시험성적서 또는 결과 보고서", "해당 공인시험기관 명의의 공인성적서"),
                  ("활용", "과제평가·검수·자체 검증 등", "공인성적서 제출이 요구되는 평가·검증"),
                  ("소요기간", "시험항목 및 기관 일정에 따라 협의", "시험항목 및 기관 일정에 따라 협의"),
                  ("비용", "시험 범위·조건별 개별 견적", "시험 범위·조건별 개별 견적")],
        cmp_note="※ 결과 문서의 제출 가능 여부는 발주처·과제 관리기관 등 제출처의 요구 조건을 우선 확인해야 합니다.",
        proc_title="시험 검토부터<br>성적서 발급 절차까지 지원합니다",
        proc_ban="시험항목과 목표 기준을 남겨주시면 협력 시험기관과 시험 가능 여부 및 견적을 검토합니다.",
        steps=[("견적 문의", "시험 대상, 정량적 목표항목 및 희망 일정을 확인합니다.", ["의뢰자", "KTAR"]),
               ("시험 검토·견적", "협력 시험기관과 시험방법, 비용 및 일정을 협의합니다.", ["KTAR", "협력 시험기관"]),
               ("시험 접수", "시험 대상과 필요한 기술자료 및 시료를 확인해 시험 접수를 지원합니다.", ["의뢰자", "KTAR"]),
               ("신청서·절차서 준비", "시험항목, 시험방법 및 판정 기준을 정리해 신청서 준비를 지원합니다.", ["KTAR", "협력 시험기관"]),
               ("시험 수행", "협력 시험기관이 시험을 수행합니다. KTAR은 진행 일정 및 의사소통을 지원합니다.", ["협력 시험기관", "KTAR"]),
               ("결과서 발급", "시험 수행기관이 결과를 검토해 해당 기관 명의의 성적서 또는 보고서를 발급합니다. KTAR은 전달을 지원합니다.",
                ["협력 시험기관", "KTAR"])],
        docs_title="기업이 준비할 것",
        docs_lead="최초 문의 단계에서는 성능지표 자료 원본을 업로드하지 않아도 됩니다. 필요한 기술자료는 담당자와 별도로 협의하여 전달받습니다.",
        docs_you=[("시험하고 싶은 항목·목표지표", "문서 또는 텍스트"), ("시험 대상 제품·서비스 정보", "기본 사양"),
                  ("시험 조건 및 측정 방법", "보유 자료"), ("시료·실행환경 정보", "시험 유형에 따라 필요")],
        docs_me=[("시험 가능 여부 검토 지원", "협력기관 협의"), ("견적·일정 조율", "개별 안내"),
                 ("신청서·절차서 준비 지원", "시험항목별"), ("시험 진행 현황 관리", "협력기관 수행"),
                 ("성적서 발급 절차 지원", "수행기관 명의")],
        docs_note="보안이 필요한 기술자료는 담당자 안내 후 별도 전달해 주세요.",
        cta_title="시험항목을 남겨주시면<br>3영업일 이내 견적 안내를 진행합니다",
        cta_lead="회사명, 담당자 연락처 및 문의 내용을 먼저 남겨주세요. 시험 가능 여부 검토에 추가 자료가 필요한 경우 담당자가 별도로 안내드립니다.",
        cta_note="KTAR은 시험기관 연계 및 진행을 지원하며, 실제 시험 수행과 성적서 발급은 해당 시험기관이 담당합니다.",
        cta_btn="일반시험 견적문의",
        sample=False,
    ),
}

ANCHORS = [("gain", "활용 상황"), ("cmp", "비교"), ("proc", "프로세스"), ("docs", "준비 서류"), ("contact", "견적문의")]


def esc(s):
    return s.replace("&", "&amp;")


def head_for(slug):
    d = PAGES[slug]
    head = re.sub(r"<title>.*?</title>", f"<title>{esc(d['title'])} | KTAR 한국시험평가원</title>", HEAD)
    head = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{esc(d.get("desc") or d["lead"])}">', head)
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
    lead_html = f'<p class="ph__lead">{esc(d["lead"])}</p>' if d["lead"] else ""
    facts ="".join(f"<div><dt>{k}</dt><dd>{esc(v)}</dd></div>" for k, v in d["facts"])
    tabs = "".join(f'<a href="#{i}">{n}</a>' for i, n in ANCHORS)
    sw = "".join(f'<a href="{s}.html"' + (' aria-current="page"' if s == slug else "") + f">{esc(n)}</a>" for n, s in SWITCH)
    gains = "".join(f'<li><span class="gain__no">{n:02d}</span><b>{esc(a)}</b><span>{esc(b)}</span></li>'
                    for n, (a, b) in enumerate(d["gains"], 1))
    gain_note = f'<p class="cmp-note">{esc(d["gain_note"])}</p>' if d.get("gain_note") else ""
    steps_src = d["steps"]
    proc_lead = f'<p>{esc(d["proc_lead"])}</p>' if d.get("proc_lead") else ""
    leads = d["cta_lead"] if isinstance(d["cta_lead"], list) else [d["cta_lead"]]
    cta_lead = "".join(f"<p>{esc(x)}</p>" for x in leads)
    if d.get("cta_note"):
        cta_lead += f'<p class="contact__note">{esc(d["cta_note"])}</p>'
    docs_cls = "docs__col docs__col--desc" if d.get("docs_desc") else "docs__col"
    docs_note = esc(d.get("docs_note", DOCS_NOTE))
    sample = SAMPLE_NOTE if d.get("sample", True) else ""
    steps = "".join(
        f'<li class="{"k" if len(r) == 1 and r[0] == "KTAR" else ""}"><span class="proc__no">{n}</span><b>{esc(a)}</b><p>{esc(b)}</p>{who(r)}</li>'
        for n, (a, b, r) in enumerate(steps_src, 1))
    you = "".join(f"<li>{esc(a)}<span>{esc(b)}</span></li>" for a, b in d["docs_you"])
    docs_me = d.get("docs_me")
    if docs_me:
        me = "".join(f"<li>{esc(a)}<span>{esc(b)}</span></li>" for a, b in docs_me)
        docs_html = (f'<div class="docs">\n        <div class="{docs_cls}"><h3>기업<small>준비</small></h3><ul>{you}</ul></div>\n'
                     f'        <div class="docs__col me"><h3>KTAR<small>지원</small></h3><ul>{me}</ul></div>\n      </div>')
    else:
        docs_html = (f'<div class="docs docs--one">\n        <div class="{docs_cls}"><h3>기업<small>준비</small></h3><ul>{you}</ul></div>\n      </div>')
    cta1 = esc(d.get("cta1", f"{d['title']} 견적문의"))
    cta2 = esc(d.get("cta2", "발급 프로세스 보기"))
    cta_btn = esc(d.get("cta_btn", f"{d['title']} 견적문의"))
    proc_ban = esc(d["proc_ban"]) if d.get("proc_ban") else "진행 방식이 궁금하시면 <em>견적문의</em>로 먼저 남겨 주세요."

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
        {lead_html}
        <div class="ph__cta">
          <a class="btn btn--fill" href="../index.html#inquiry">{cta1}</a>
          <a class="btn btn--line" href="#proc">{cta2}</a>
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
      <div class="kh"><p class="kh__label">USE CASE</p><h2>{esc(d["gain_title"])}</h2><p>{esc(d["gain_lead"])}</p></div>
      <ol class="gain">{gains}</ol>
      {gain_note}
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
      <div class="kh"><p class="kh__label">PROCESS</p><h2>{d["proc_title"]}</h2>{proc_lead}</div>
      <div class="proc-ban"><b>{proc_ban}</b><a href="../index.html#inquiry">견적문의</a></div>
      <ol class="proc">{steps}</ol>
    </div>
  </section>

  <section class="cs cs--bg" id="docs">
    <div class="inner">
      <div class="kh"><p class="kh__label">DOCUMENTS</p><h2>{esc(d["docs_title"])}</h2><p>{esc(d["docs_lead"])}</p></div>
      {docs_html}
      <p class="docs-note">{docs_note}</p>
    </div>
  </section>

  <section class="contact" id="contact">
    <div class="inner contact__inner">
      <div>
        <p class="kh__label">CONTACT</p>
        <h2>{d["cta_title"]}</h2>
        {cta_lead}
      </div>
      <div class="contact__side">
        <a class="btn btn--fill" href="../index.html#inquiry">{cta_btn}</a>
      </div>
    </div>
  </section>

{sample}</main>'''
    path = f"{repo}/test/{slug}.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(head_for(slug) + main + TAIL)
    return path


def build_all(repo):
    for slug in PAGES:
        print("wrote", build(slug, repo))
