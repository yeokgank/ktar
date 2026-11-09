#!/usr/bin/env python3
"""KTAR 서브페이지 생성기 (공공기관 톤). 사용: python3 gen2.py <repo 경로>"""
import os, re, sys

SP = os.path.dirname(os.path.abspath(__file__))
REPO = sys.argv[1]
HEAD = open(f"{SP}/tpl_head.html", encoding="utf-8").read()
TAIL = open(f"{SP}/tpl_tail.html", encoding="utf-8").read()

GROUPS = {
    "about": ("KTAR 소개", "KTAR 소개", [("기관 소개", "intro"), ("오시는 길", "location")]),
    "test": ("시험", "시험", [("공인시험", "certified"), ("일반시험(V&V)", "vv")]),
    "cert": ("인증", "인증", [("GS인증", "gs"), ("KC인증", "kc"), ("클라우드서비스확인제", "cloud")]),
}
GNB_FIRST = {"about": "../about/intro.html", "test": "../test/certified.html", "cert": "../cert/gs.html"}


def esc(s):
    return s.replace("&", "&amp;")


def sec(title, body):
    return f'      <section class="sec">\n        <h3>{title}</h3>\n        {body}\n      </section>\n'


def text(*ps):
    return '<div class="text">' + "".join(f"<p>{p}</p>" for p in ps) + "</div>"


def bul(items):
    return '<ul class="bul">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def tbl(heads, rows, th_first=True, centers=()):
    thead = "<thead><tr>" + "".join(f'<th scope="col">{h}</th>' for h in heads) + "</tr></thead>" if heads else ""
    body = ""
    for r in rows:
        cells = ""
        for n, c in enumerate(r):
            if n == 0 and th_first:
                cells += f'<th scope="row">{c}</th>'
            else:
                cells += f'<td class="c">{c}</td>' if n in centers else f"<td>{c}</td>"
        body += f"<tr>{cells}</tr>"
    return f'<div class="tbl-wrap"><table class="tbl">{thead}<tbody>{body}</tbody></table></div>'


def flow(steps):
    lis = "".join(f"<li><small>STEP {n:02d}</small><b>{t}</b><span>{d}</span></li>" for n, (t, d) in enumerate(steps, 1))
    return f'<ol class="flow">{lis}</ol>'


def note(items, title="유의사항"):
    return f'<div class="note"><b>{title}</b>{bul(items)}</div>'


ASK = '''      <section class="sec">
        <div class="ask">
          <div><b>견적 문의</b><span>대상과 범위를 확인한 뒤 비용과 일정을 안내해 드립니다.</span></div>
          <a href="../index.html#inquiry">견적 문의하기</a>
        </div>
      </section>
'''

DOCS_COMMON = [
    ("신청서", "소정 양식에 따라 작성합니다.", "필수"),
    ("사업자등록증 사본", "법인·개인 사업자 공통입니다.", "필수"),
    ("대상 설명서", "제품·서비스 개요와 사양을 적습니다.", "필수"),
    ("시료 또는 설치본", "시험·평가가 가능한 상태로 준비합니다.", "필수"),
    ("담당자 연락처", "진행 상황 안내에 사용합니다.", "필수"),
]

PAGES = {}

# ── 시험 ─────────────────────────────────────────────
PAGES["test/certified"] = dict(
    title="공인시험", lead="공인된 기준과 절차에 따라 시험하고 공식 성적서를 발급합니다.",
    body=
    sec("서비스 개요", text("공인된 시험 기준과 절차에 따라 대상 제품·서비스를 시험하고, 그 결과를 공식 성적서로 발급합니다.",
                          "시험 항목과 범위는 대상 사양을 확인한 뒤 견적 단계에서 확정합니다."))
    + sec("성적서 활용", bul(["<b>공공·조달 제출</b> — 입찰, 납품 등 공공 목적의 증빙 자료", "<b>고객사 제출</b> — 제3자 기관의 공식 결과로 신뢰도 확보", "<b>인증 신청 증빙</b> — 인증 신청 시 시험 결과 자료로 제출"]))
    + sec("접수 및 발급 절차", tbl(["단계", "처리 내용", "비고"], [
        ("1. 상담·견적 문의", "대상과 시험 범위를 확인합니다.", "온라인 접수"),
        ("2. 신청서 접수", "신청서와 제출 서류를 접수합니다.", ""),
        ("3. 계약·시료 접수", "일정과 비용을 확정하고 시료를 접수합니다.", ""),
        ("4. 시험 수행", "합의된 기준에 따라 시험을 수행합니다.", ""),
        ("5. 성적서 발급", "결과를 검토한 뒤 성적서를 발급합니다.", "")]))
    + sec("제출 서류", tbl(["서류", "내용", "구분"], DOCS_COMMON, centers=(2,)))
    + sec("유의사항", note(["시험 범위와 소요 기간은 대상에 따라 달라지며 견적 시 안내합니다.", "시료가 시험 가능한 상태가 아니면 접수 후 일정이 조정될 수 있습니다."]))
    + ASK)

PAGES["test/vv"] = dict(
    title="일반시험(V&V)", lead="개발 단계에서 요구사항 충족 여부를 검증하고 개선점을 확인합니다.",
    body=
    sec("서비스 개요", text("개발 중이거나 출시를 앞둔 제품·서비스가 요구사항을 충족하는지 검증하고, 품질 개선에 필요한 시험 결과 보고서를 제공합니다.",
                          "공식 성적서가 아닌 고객 요구에 맞춘 시험이므로, 개발 단계 어디서든 의뢰할 수 있습니다."))
    + sec("공인시험과의 차이", tbl(["구분", "공인시험", "일반시험(V&V)"], [
        ("목적", "공식 성적서 발급", "개발 품질 검증·개선"),
        ("결과서", "공인 성적서", "시험 결과 보고서"),
        ("시험 범위", "공인 기준에 따른 정형 항목", "고객 요구에 맞춰 협의"),
        ("진행 시점", "출시·제출 직전", "개발 단계 어디서나"),
        ("소요 기간", "협의", "협의")]))
    + sec("진행 절차", flow([("상담·견적", "목적과 범위 확인"), ("요구사항 확정", "검증 항목·기준 합의"), ("시험 수행", "합의된 항목 수행"), ("결과 분석", "결함·개선점 정리"), ("보고서 발급", "시험 결과 보고서")]))
    + sec("제출 서류", tbl(["서류", "내용", "구분"], [
        ("신청서", "소정 양식에 따라 작성합니다.", "필수"),
        ("시험 요구사항", "검증하려는 항목과 기준을 적습니다.", "필수"),
        ("대상 설명서", "제품·서비스 개요와 사양을 적습니다.", "필수"),
        ("시료 또는 설치본", "시험이 가능한 상태로 준비합니다.", "필수"),
        ("담당자 연락처", "진행 상황 안내에 사용합니다.", "필수")], centers=(2,)))
    + ASK)

# ── 인증 ─────────────────────────────────────────────
PAGES["cert/gs"] = dict(
    title="GS인증", lead="소프트웨어 제품의 품질을 제3자가 평가해 인증합니다.",
    body=
    sec("제도 개요", text("소프트웨어 제품이 정해진 품질 기준을 충족하는지 심사와 시험으로 확인하고, 기준을 충족하면 인증서를 발급합니다.",
                        "거래처와 발주처에 제출할 수 있는 객관적인 품질 증빙으로 활용할 수 있습니다."))
    + sec("인증 절차", flow([("상담·견적", "대상과 범위 확인"), ("신청서 접수", "신청서·서류 제출"), ("심사·시험", "기준에 따라 평가"), ("결과 검토", "보완 사항 확인"), ("인증서 발급", "인증서 발급")]))
    + sec("평가 관점", tbl(["관점", "확인 내용"], [
        ("기능성", "요구된 기능이 정확하고 완전하게 제공되는지 확인합니다."),
        ("신뢰성", "정해진 조건에서 안정적으로 동작하는지 확인합니다."),
        ("사용성", "사용자가 이해하고 쉽게 쓸 수 있는지 확인합니다."),
        ("효율성", "자원 사용과 처리 성능이 적정한지 확인합니다."),
        ("유지보수성", "변경과 수정이 용이한 구조인지 확인합니다."),
        ("이식성", "다른 환경으로 옮겨 사용할 수 있는지 확인합니다.")]))
    + sec("제출 서류", tbl(["서류", "내용", "구분"], DOCS_COMMON, centers=(2,)))
    + sec("유의사항", note(["인증 대상 여부와 세부 기준은 상담 시 안내합니다.", "심사 중 보완 요청이 있으면 반영 후 재확인합니다.", "인증 이후 제품이 변경되면 추가 확인이 필요할 수 있습니다."]))
    + ASK)

PAGES["cert/kc"] = dict(
    title="KC인증", lead="제품의 안전성을 확인해 판매·유통 요건을 충족하도록 지원합니다.",
    body=
    sec("제도 개요", text("인증 대상 제품이 판매·유통에 필요한 안전 요건을 충족하는지 확인합니다. 제품의 위험도에 따라 인증 유형이 나뉩니다.",
                        "시험부터 인증서 발급까지 단계별 일정 관리를 지원합니다."))
    + sec("인증 유형", tbl(["유형", "대상", "확인 방식", "비고"], [
        ("안전인증", "안전 위해 우려가 큰 제품", "제품 시험 + 공장 심사", "세부 기준은 담당자 확인"),
        ("안전확인", "안전 위해 우려가 비교적 낮은 제품", "제품 시험", "세부 기준은 담당자 확인"),
        ("공급자적합성확인", "위험도가 낮은 제품", "공급자 자체 확인", "세부 기준은 담당자 확인")]))
    + sec("진행 절차", tbl(["단계", "처리 내용"], [
        ("1. 대상 확인", "제품 정보를 확인해 해당 인증 유형을 안내합니다."),
        ("2. 신청 접수", "신청서와 제출 서류를 접수합니다."),
        ("3. 제품 시험", "유형에 따라 제품 시험을 수행합니다."),
        ("4. 공장 심사", "해당 유형에 한해 심사를 진행합니다."),
        ("5. 결과 검토", "보완 사항을 확인하고 반영합니다."),
        ("6. 인증서 발급", "요건 충족 시 인증서를 발급합니다.")]))
    + sec("제출 서류", tbl(["서류", "내용", "구분"], DOCS_COMMON, centers=(2,)))
    + sec("유의사항", note(["제품 종류에 따라 대상 유형과 필요 서류가 달라질 수 있습니다.", "공장 심사 필요 여부는 인증 유형에 따라 상담 시 안내합니다."]))
    + ASK)

PAGES["cert/cloud"] = dict(
    title="클라우드서비스확인제", lead="클라우드 서비스가 요구 기준을 갖췄는지 확인하고 확인서를 발급합니다.",
    body=
    sec("제도 개요", text("클라우드 서비스가 요구되는 품질·보안 기준을 갖췄는지 확인하고, 그 결과를 확인서로 발급합니다.",
                        "도입을 검토하는 기관이 개별로 확인해야 하는 항목을 줄이는 데 도움이 됩니다."))
    + sec("확인 절차", flow([("상담·견적", "대상과 범위 확인"), ("신청서 접수", "신청서·서류 제출"), ("확인 수행", "기준에 따라 확인"), ("확인서 발급", "결과 확인서 발급")]))
    + sec("확인 영역", tbl(["영역", "확인 내용"], [
        ("서비스 품질", "서비스 수준과 안정적인 제공 체계를 확인합니다."),
        ("정보보호", "데이터 보호와 접근 통제 체계를 확인합니다."),
        ("운영 관리", "장애 대응과 변경 관리 절차를 확인합니다."),
        ("고객 지원", "이용자 문의와 지원 체계를 확인합니다.")]))
    + sec("제출 서류", tbl(["서류", "내용", "구분"], [
        ("신청서", "소정 양식에 따라 작성합니다.", "필수"),
        ("사업자등록증 사본", "법인·개인 사업자 공통입니다.", "필수"),
        ("서비스 설명서", "서비스 구성과 제공 범위를 적습니다.", "필수"),
        ("운영 현황 자료", "운영·보안 현황을 확인할 수 있는 자료입니다.", "해당 시"),
        ("담당자 연락처", "진행 상황 안내에 사용합니다.", "필수")], centers=(2,)))
    + sec("유의사항", note(["대상 서비스 범위와 세부 기준은 상담 시 안내합니다.", "필요 자료는 서비스 형태에 따라 달라질 수 있습니다."]))
    + ASK)

# ── 소개 ─────────────────────────────────────────────
PAGES["about/intro"] = dict(
    title="기관 소개", lead="객관적인 기준으로 시험·평가하고 인증하는 전문 기관입니다.",
    body=
    sec("인사말", '<div class="greet"><div class="photo" role="img" aria-label="대표 사진 자리">사진 영역</div><div class="text">'
        "<strong>정확한 결과, 투명한 절차로 신뢰받는 평가를 하겠습니다.</strong>"
        "<p>KTAR 한국시험평가원 홈페이지를 찾아 주신 여러분을 환영합니다.</p>"
        "<p>우리는 전문성과 공정성을 바탕으로 시험·인증 서비스를 제공하며, 고객의 제품과 서비스가 시장에서 신뢰받을 수 있도록 정확한 결과와 신속한 대응으로 함께하겠습니다.</p>"
        '<p class="sign">한국시험평가원 원장<b>홍 길 동</b></p></div></div>')
    + sec("미션과 비전", tbl(None, [
        ("미션", "객관적인 시험·평가로 제품과 서비스의 신뢰를 높입니다."),
        ("비전", "고객이 가장 먼저 찾는 신뢰받는 시험·인증 기관"),
        ("핵심 가치", "전문성 · 공정성 · 신속성")]))
    + sec("주요 사업", tbl(["구분", "내용", "바로가기"], [
        ("시험", "공인시험, 일반시험(V&amp;V)", '<a href="../test/certified.html">공인시험 보기</a>'),
        ("인증", "GS인증, KC인증, 클라우드서비스확인제", '<a href="../cert/gs.html">GS인증 보기</a>'),
        ("고객지원", "견적 문의 접수 및 상담", '<a href="../index.html#inquiry">견적 문의</a>')], centers=(2,)))
    + sec("연혁", tbl(["연도", "주요 내용"], [
        ("2026", "홈페이지 개편 및 온라인 견적 문의 개설"),
        ("2024", "인증 서비스 확대 운영"),
        ("2022", "일반시험(V&amp;V) 서비스 시작"),
        ("2020", "공인시험 서비스 개시"),
        ("2018", "한국시험평가원 설립")]))
    + sec("조직 및 업무", tbl(["부서", "담당 업무"], [
        ("시험팀", "공인시험, 일반시험(V&amp;V) 수행"),
        ("인증팀", "GS인증, KC인증, 클라우드서비스확인제 운영"),
        ("품질관리팀", "시험·인증 절차의 공정성과 품질 관리"),
        ("경영지원팀", "고객지원, 총무")])))

PAGES["about/location"] = dict(
    title="오시는 길", lead="KTAR 한국시험평가원을 찾아오시는 방법을 안내합니다.",
    body=
    sec("위치", '<div class="map" role="img" aria-label="위치 안내 지도(시안)"><div class="map__pin"><svg><use href="#i-map"/></svg><span>KTAR 한국시험평가원</span></div><span class="map__note">※ 지도 영역 (실제 지도 연동 예정)</span></div>')
    + sec("연락처", tbl(None, [
        ("주소", "사업장 주소 입력"),
        ("대표전화", "00-0000-0000"),
        ("팩스", "00-0000-0000"),
        ("이메일", "info@example.com"),
        ("근무시간", "평일 09:00 – 18:00 (주말·공휴일 휴무)")]))
    + sec("교통 안내", tbl(None, [
        ("지하철", "○호선 ○○역 ○번 출구 도보 ○분"),
        ("버스", "○○번, ○○번 ○○정류장 하차"),
        ("주차", "방문 차량 주차 가능 (사전 문의)")]))
    + sec("방문 안내", note(["방문 전 담당자에게 일시와 목적을 알려 주시면 원활히 안내해 드립니다.", "시료를 직접 가져오시는 경우 접수 방법을 먼저 문의해 주세요."], title="안내")))


def build(key, g_key, page_no):
    d = PAGES[key]
    gname, lnb_title, items = GROUPS[g_key]
    cur = key.split("/")[1]
    head = HEAD
    head = re.sub(r"<title>.*?</title>", f"<title>{esc(d['title'])} | KTAR 한국시험평가원</title>", head)
    head = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{d["lead"]}">', head)
    first = GNB_FIRST[g_key]
    head = head.replace(f'<li><a href="{first}">', f'<li class="is-current"><a href="{first}">', 1)
    lnb = "".join(
        f'<li><a href="../{g_key}/{slug}.html"' + (' aria-current="page"' if slug == cur else "") + f">{esc(name)}</a></li>"
        for name, slug in items)
    main = f'''<main>
  <section class="sub-hero">
    <div class="inner sub-hero__inner">
      <h1>{esc(d['title'])}</h1>
      <p class="sub-hero__lead">{d['lead']}</p>
    </div>
  </section>
  <div class="crumbbar">
    <div class="inner">
      <ol class="crumb" aria-label="현재 위치">
        <li><a href="../index.html">홈</a></li>
        <li>{esc(gname)}</li>
        <li aria-current="page">{esc(d['title'])}</li>
      </ol>
    </div>
  </div>
  <div class="inner sub-wrap">
    <aside class="lnb" aria-label="{esc(gname)} 메뉴">
      <h2>{esc(lnb_title)}</h2>
      <ul>{lnb}</ul>
    </aside>
    <div class="doc">
{d['body']}      <p class="sample-note">※ 본 페이지의 문구·수치는 시안용 샘플입니다. 실제 내용 확정 후 교체됩니다.</p>
    </div>
  </div>
</main>'''
    path = f"{REPO}/{key}.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + main + TAIL)
    return path


import gen_cert  # 인증 3종은 별도 템플릿(히어로+앵커 탭 구조)
import gen_test  # 시험 2종도 같은 골격 (+사례 블록)
for g, (_, _, items) in GROUPS.items():
    for _, slug in items:
        if g in ("cert", "test"):
            continue
        print("wrote", build(f"{g}/{slug}", g, 0))
gen_cert.build_all(REPO)
gen_test.build_all(REPO)
