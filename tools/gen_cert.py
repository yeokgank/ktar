#!/usr/bin/env python3
"""인증 상세 3종(GS·KC·클라우드) 생성기. gen_subpages.py 가 호출한다.
구성: 히어로+핵심정보 패널 → 앵커 탭 → 이점 → 비교표 → 프로세스 → 준비 서류 → 문의."""
import os, re

SP = os.path.dirname(os.path.abspath(__file__))
HEAD = open(f"{SP}/tpl_head.html", encoding="utf-8").read()
TAIL = open(f"{SP}/tpl_tail.html", encoding="utf-8").read()

SWITCH = [("GS인증", "gs"), ("KC인증", "kc"), ("클라우드서비스확인제", "cloud")]
ROLE_ME = "KTAR"

# 모든 문구·수치는 시안용 샘플
PAGES = {
    "gs": dict(
        title="GS인증",
        lead="소프트웨어 제품의 품질을 제3자가 평가해 인증합니다. 접수 전 점검으로 한 번에 통과하는 길을 설계합니다.",
        h1="GS인증,<br><em>첫 심사</em>에서 끝내는 방법",
        desc="소프트웨어 제품의 품질을 제3자가 평가해 인증합니다.",
        facts=[("대상", "개발이 완료된 소프트웨어 (패키지 · 임베디드 · 웹/모바일 서비스)"),
               ("목적", "국제표준 기준으로 SW 품질을 평가하고 인증서를 부여"),
               ("근거", "소프트웨어 진흥 관련 법령 및 품질인증 운영 지침 (확정 시 정리)"),
               ("인증기관", "지정 인증기관 (상담 시 안내)"),
               ("처리기간", "접수일로부터 최소 30일 이상"),
               ("유효기간", "제품 변경 시 재인증 필요")],
        gain_title="GS인증으로 얻는 여섯 가지",
        gain_lead="품질 개선, 마케팅, 제도적 혜택 세 측면입니다. 공공 납품이 목적이라면 사실상 필수 조건입니다.",
        gains=[("조달 등록 경로 확보", "인증 제품은 공공 조달 등록 경로가 열려 납품 절차가 단순해집니다."),
               ("우선구매 대상 지정", "공공기관 우선구매 대상 제품으로 지정될 수 있습니다."),
               ("공공 정보화사업 우선 도입", "구축·운영 사업에서 우선 도입 대상으로 검토됩니다."),
               ("기술성 평가 우선 반영", "상용 SW 구매 시 제품 신뢰도 항목으로 반영됩니다."),
               ("제3자 인증으로 품질 개선", "단기간에 결함을 찾아 고쳐 비용과 시간을 줄입니다."),
               ("하도급·분리발주 가점", "관련 요건에 해당하면 평가 시 가점을 받을 수 있습니다.")],
        cmp_label="GRADE", cmp_title="1등급과 2등급, 무엇이 다른가",
        cmp_lead="공공 조달이 목적이라면 1등급이 기본입니다. KTAR은 접수 전 점검으로 대부분의 제품을 1등급으로 진행합니다.",
        cmp_head=["항목", "1등급", "2등급"], cmp_rec=1,
        cmp_rows=[("시험 범위", "기능 · 성능 · 사용성 · 신뢰성 · 보안성 · 유지보수성 · 이식성 전 항목", "기능 중심, 일부 항목 축소"),
                  ("결함 허용", "치명·주요 결함 0건, 경미 결함도 수정 후 재확인", "주요 결함 일부 허용"),
                  ("공공 조달", "종합쇼핑몰 등록 · 우선구매 대상", "등록 가능, 우선구매 제외"),
                  ("KTAR 사전 점검", "기능 명세 대조 · 결함 예비 진단 · 매뉴얼 정비 · 시험 환경 구성", "기능 명세 대조 · 매뉴얼 정비"),
                  ("적합한 경우", "공공 납품 · 우선구매 · 과제 증빙", "민간 벤더 등록 · 출시 전 점검")],
        cmp_note="※ 등급별 세부 기준은 인증기관 고시에 따르며, 표는 구조 확인용 샘플입니다.",
        proc_title="접수 전에 결함을 잡습니다.<br>그래서 재시험이 없습니다.",
        steps=[("견적 확인", "견적문의로 의뢰하시면 대상과 유형을 확인하고 견적을 안내합니다.", ["KTAR"]),
               ("계약 진행", "견적 확인 후 인증 진행 계약을 체결합니다.", ["의뢰자", "KTAR"]),
               ("인증 접수", "인증기관에 인증을 접수합니다. 접수 서류는 KTAR이 준비합니다.", ["KTAR", "인증기관"]),
               ("필요 자료 제출", "실행 파일 · 기능 목록 · 사용자 매뉴얼 · 설치 환경 정보를 제출합니다. 양식 정리는 KTAR이 합니다.", ["의뢰자", "KTAR"]),
               ("인증 진행", "인증기관이 시험·심사를 진행합니다. 보완 요청 대응은 KTAR이 합니다.", ["인증기관"]),
               ("인증서 발급", "인증기관이 인증서를 발급합니다. 발급 후 등록·표시 절차를 안내합니다.", ["인증기관", "KTAR"])],
        docs_title="기업이 준비할 것",
        docs_lead="서류 때문에 접수가 늦어지는 경우가 많습니다. 기업은 원본 자료만 주시면 나머지는 KTAR이 인증기관 양식으로 정리합니다.",
        docs_you=[("제품 실행 파일 또는 접속 정보", "시험용"), ("기능 목록 (화면·메뉴 단위)", "엑셀 가능"),
                  ("사용자 매뉴얼 초안", "있는 대로"), ("설치 · 운영 환경 정보", "OS, DB, 브라우저"),
                  ("사업자등록증 · 제품 소개서", "신청서 첨부")],
        docs_me=[("인증 신청서", "기관 양식"), ("제품 설명서", "기관 양식"),
                 ("테스트 케이스 · 기능 명세 대조표", "사전 점검 시 작성"), ("사용자 · 설치 매뉴얼 정비본", "접수 전 정비"),
                 ("사전 결함 점검 보고서", "접수 전 전달")],
        cta_title="기능 목록만 보내주시면<br>영업일 2일 내 등급과 견적을 안내합니다",
        cta_lead="화면·메뉴 단위 기능 목록이면 충분합니다. 없으면 제품 소개서로도 1차 판단이 가능합니다.",
    ),
    "kc": dict(
        title="KC인증",
        lead="전기·전자·통신 제품의 안전 요건을 확인해 국내 판매·유통을 지원합니다. 유형 판별부터 마크 표시까지 함께합니다.",
        h1="KC인증,<br><em>대상 판별</em>부터 마크 표시까지",
        desc="제품의 안전성을 확인해 판매·유통 요건을 충족하도록 지원합니다.",
        facts=[("대상", "전기·전자 제품, 무선·유선 통신 기능이 있는 ICT 기기"),
               ("목적", "화재·감전 등 위험으로 인한 사고 방지 — 인증받은 제품만 판매 허용"),
               ("제도", "전기용품 안전인증 · 안전확인 · 공급자적합성확인 / 방송통신기자재 적합성평가"),
               ("인증기관", "지정 시험·인증기관 (상담 시 안내)"),
               ("처리기간", "유형과 시험 범위에 따라 상이 (견적 시 안내)"),
               ("유효기간", "제품 변경 시 변경신고 또는 재인증")],
        gain_title="KC마크 없이는 팔 수 없는 여섯 가지 상황",
        gain_lead="국내 유통·판매를 위해 법으로 정한 요건입니다. 미인증 판매는 과태료와 회수 대상이 될 수 있습니다.",
        gains=[("국내 판매 가능", "인증받은 제품만 판매할 수 있는 강제 인증입니다. 판매 페이지에 인증번호 표기가 요구됩니다."),
               ("안전성 확보", "기본적인 안전성이 확인된 제품이라는 증표가 됩니다."),
               ("공공기관 구매 요건", "공공기관 구매 품목에서 KC 인증은 기본 요건입니다."),
               ("해외 제품 수입·유통", "해외 인증이 있어도 국내 KC는 별도입니다. 수입 통관 시 확인됩니다."),
               ("무선 모듈 탑재 IoT 기기", "Wi-Fi·BLE 등 무선 모듈이 있으면 적합성평가 대상이 될 수 있습니다."),
               ("R&D 시제품 상용화", "과제 결과물을 제품으로 전환할 때 성적서와 함께 KC를 요구받습니다.")],
        cmp_label="TYPE", cmp_title="인증 유형, 우리 제품은 어느 쪽인가",
        cmp_lead="제품의 위험도와 용도에 따라 갈립니다. KTAR은 유형 판별 결과를 근거와 함께 문서로 드립니다.",
        cmp_head=["항목", "안전인증", "안전확인", "공급자적합성확인"], cmp_rec=2,
        cmp_rows=[("대상", "안전 위해 우려가 큰 제품", "안전 위해 우려가 비교적 낮은 제품", "위험도가 낮은 제품"),
                  ("확인 방식", "제품 시험 + 공장 심사", "제품 시험", "공급자 자체 확인"),
                  ("KTAR 역할", "유형 판별 · 시료·서류 준비 · 기관 접수 · 심사 대응", "유형 판별 · 시료·서류 준비 · 기관 접수", "유형 판별 · 확인 서류 정리"),
                  ("변경 시", "재인증 또는 변경인증", "변경신고", "변경신고")],
        cmp_note="※ 유형 구분과 시험 항목은 관련 고시에 따르며, 표는 구조 확인용 샘플입니다.",
        proc_title="유형 판별을 먼저 끝냅니다.<br>그래서 시험을 한 번만 합니다.",
        steps=[("견적 확인", "견적문의로 의뢰하시면 대상과 유형을 확인하고 견적을 안내합니다.", ["KTAR"]),
               ("계약 진행", "견적 확인 후 인증 진행 계약을 체결합니다.", ["의뢰자", "KTAR"]),
               ("인증 접수", "시험·인증기관에 접수합니다. 접수 서류는 KTAR이 준비합니다.", ["KTAR", "인증기관"]),
               ("필요 자료 제출", "시료 · 제품 사양서 · 회로도 · 사용자 설명서를 제출합니다. 양식 정리는 KTAR이 합니다.", ["의뢰자", "KTAR"]),
               ("시험·심사 진행", "기관이 시험과 심사를 진행합니다. 보완 요청 대응은 KTAR이 합니다.", ["인증기관"]),
               ("인증서 발급", "인증서 발급 후 KC마크·라벨 표시 방법을 안내합니다.", ["인증기관", "KTAR"])],
        docs_title="기업이 준비할 것",
        docs_lead="기관마다 요구 형식이 다릅니다. 기업은 설계 자료 원본만 주시면 KTAR이 기관 형식에 맞춰 정리합니다.",
        docs_you=[("시험용 시료 (완제품)", "2~3대"), ("제품 사양서 · 무선 모듈 정보", "모듈 인증번호 포함"),
                  ("회로도 · 부품 배치도 · 블록도", "있는 대로"), ("사용자 설명서 · 라벨 시안", "초안 가능"),
                  ("사업자등록증", "신청서 첨부")],
        docs_me=[("인증 신청서", "기관 양식"), ("시험 신청서", "기관별 양식"),
                 ("유형 판별 의견서", "상담 후 전달"), ("KC마크 · 라벨 표시 가이드", "발급 후 전달")],
        cta_title="제품 사양서만 보내주시면<br>영업일 2일 내 유형과 견적을 안내합니다",
        cta_lead="무선 모듈명과 전원 방식이 적힌 사양서면 충분합니다. 시제품 사진으로도 1차 판별이 가능합니다.",
    ),
    "cloud": dict(
        title="클라우드서비스확인제",
        lead="클라우드 서비스가 요구 기준을 갖췄는지 확인하고 확인서를 발급합니다. 도입 기관의 개별 검증 부담을 덜어 줍니다.",
        h1="클라우드서비스확인제,<br><em>기준 충족</em>을 문서로 증명합니다",
        desc="클라우드 서비스가 요구 기준을 갖췄는지 확인하고 확인서를 발급합니다.",
        facts=[("대상", "공공·민간에 제공하는 클라우드 서비스 (SaaS · PaaS · IaaS)"),
               ("목적", "서비스 품질과 정보보호 수준이 요구 기준에 부합함을 확인"),
               ("확인 영역", "서비스 품질 · 정보보호 · 운영 관리 · 고객 지원"),
               ("발급 문서", "서비스 확인서"),
               ("처리기간", "서비스 범위에 따라 상이 (견적 시 안내)"),
               ("유효기간", "서비스 변경 시 재확인 필요 (확정 시 정리)")],
        gain_title="확인서로 얻는 여섯 가지",
        gain_lead="도입을 검토하는 기관이 개별로 확인할 항목을 줄여, 도입 검토 단계에서 신뢰를 확보합니다.",
        gains=[("도입 검토 단계 단축", "확인서로 기본 요건 충족 여부를 먼저 보여줄 수 있습니다."),
               ("정보보호 체계 점검", "접근 통제와 데이터 보호 체계의 빈틈을 미리 확인합니다."),
               ("운영 절차 정비", "장애 대응과 변경 관리 절차를 문서로 정리하게 됩니다."),
               ("공공 도입 대응", "공공 도입 시 요구되는 증빙 자료로 활용할 수 있습니다."),
               ("고객 신뢰 확보", "제3자 확인 결과로 고객사에 설명하기 쉬워집니다."),
               ("개선 과제 도출", "확인 과정에서 발견된 보완점을 서비스 개선에 반영합니다.")],
        cmp_label="SCOPE", cmp_title="무엇을 확인하는가",
        cmp_lead="네 가지 영역을 기준으로 확인합니다. 서비스 형태에 따라 세부 항목은 상담 시 조정합니다.",
        cmp_head=["영역", "확인 내용", "주요 증빙"], cmp_rec=0,
        cmp_rows=[("서비스 품질", "서비스 수준과 안정적인 제공 체계", "서비스 수준 협약, 가용성 현황"),
                  ("정보보호", "데이터 보호와 접근 통제 체계", "보안 정책, 접근 통제 내역"),
                  ("운영 관리", "장애 대응과 변경 관리 절차", "운영 절차서, 장애 처리 이력"),
                  ("고객 지원", "이용자 문의와 지원 체계", "지원 채널, 처리 기준")],
        cmp_note="※ 확인 영역과 세부 항목은 제도 기준에 따라 확정하며, 표는 구조 확인용 샘플입니다.",
        proc_title="서비스 범위를 먼저 정합니다.<br>그래서 확인이 한 번에 끝납니다.",
        steps=[("견적 확인", "견적문의로 의뢰하시면 서비스 범위를 확인하고 견적을 안내합니다.", ["KTAR"]),
               ("계약 진행", "견적 확인 후 확인 진행 계약을 체결합니다.", ["의뢰자", "KTAR"]),
               ("자료 제출", "서비스 설명서와 운영 현황 자료를 제출합니다. 양식 정리는 KTAR이 합니다.", ["의뢰자", "KTAR"]),
               ("확인 수행", "기준에 따라 영역별 확인을 수행하고 보완 사항을 안내합니다.", ["KTAR"]),
               ("보완 대응", "보완 사항을 반영하고 재확인합니다.", ["의뢰자", "KTAR"]),
               ("확인서 발급", "결과를 검토한 뒤 확인서를 발급합니다.", ["KTAR"])],
        docs_title="기업이 준비할 것",
        docs_lead="서비스 형태에 따라 필요한 자료가 달라집니다. 가지고 계신 자료만 주시면 필요한 보완 목록을 안내합니다.",
        docs_you=[("서비스 설명서", "구성·제공 범위"), ("운영 현황 자료", "해당 시"),
                  ("보안 정책 문서", "있는 대로"), ("사업자등록증", "신청서 첨부")],
        docs_me=[("확인 신청서", "소정 양식"), ("영역별 점검표", "상담 후 전달"),
                 ("보완 사항 목록", "확인 중 전달"), ("서비스 확인서", "발급")],
        cta_title="서비스 개요만 보내주시면<br>영업일 2일 내 범위와 견적을 안내합니다",
        cta_lead="서비스 소개 자료나 구성도 정도면 1차 판단이 가능합니다.",
    ),
}

ANCHORS = [("gain", "취득 이점"), ("cmp", "비교"), ("proc", "프로세스"), ("docs", "준비 서류"), ("contact", "견적문의")]


def who(roles):
    return '<div class="who">' + "".join(f'<i class="{"me" if r == ROLE_ME else ""}">{r}</i>' for r in roles) + "</div>"


def build(slug, repo):
    d = PAGES[slug]
    t = d["title"]
    head = HEAD
    head = re.sub(r"<title>.*?</title>", f"<title>{t} | KTAR 한국시험평가원</title>", head)
    head = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{d["desc"]}">', head)
    head = head.replace('<li><a href="../cert/gs.html">', '<li class="is-current"><a href="../cert/gs.html">', 1)
    head = head.replace('<link rel="stylesheet" href="../css/sub.css">',
                        '<link rel="stylesheet" href="../css/sub.css">\n<link rel="stylesheet" href="../css/cert.css">')

    facts = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in d["facts"])
    tabs = "".join(f'<a href="#{i}">{n}</a>' for i, n in ANCHORS)
    sw = "".join(f'<a href="{s}.html"' + (' aria-current="page"' if s == slug else "") + f">{n}</a>" for n, s in SWITCH)
    gains = "".join(f'<li><span class="gain__no">{n:02d}</span><b>{a}</b><span>{b}</span></li>' for n, (a, b) in enumerate(d["gains"], 1))
    heads = ""
    for n, h in enumerate(d["cmp_head"]):
        if n == d["cmp_rec"] and n > 0:
            heads += f'<th scope="col" class="rec">{h}<small>다수 해당</small></th>' if slug != "kc" else f'<th scope="col" class="rec">{h}<small>다수 해당</small></th>'
        else:
            heads += f'<th scope="col">{h}</th>'
    rows = ""
    for r in d["cmp_rows"]:
        cells = f'<th scope="row">{r[0]}</th>'
        for n, c in enumerate(r[1:], 1):
            cells += f'<td class="{"rec" if n == d["cmp_rec"] else ""}">{c}</td>'
        rows += f"<tr>{cells}</tr>"
    steps = "".join(
        f'<li class="{"k" if ROLE_ME in r and len(r) == 1 else ""}"><span class="proc__no">{n}</span><b>{a}</b><p>{b}</p>{who(r)}</li>'
        for n, (a, b, r) in enumerate(d["steps"], 1))
    you = "".join(f"<li>{a}<span>{b}</span></li>" for a, b in d["docs_you"])
    me = "".join(f"<li>{a}<span>{b}</span></li>" for a, b in d["docs_me"])

    main = f'''<main class="cp">
  <section class="ph">
    <div class="inner ph__inner">
      <ol class="crumb" aria-label="현재 위치">
        <li><a href="../index.html">홈</a></li>
        <li>인증</li>
        <li aria-current="page">{t}</li>
      </ol>
      <div>
        <p class="eyebrow">CERTIFICATION</p>
        <h1>{d["h1"]}</h1>
        <p class="ph__lead">{d["lead"]}</p>
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
      <div class="atab__sw"><span>인증 서비스</span>{sw}</div>
    </div>
  </div>

  <section class="cs" id="gain">
    <div class="inner">
      <div class="kh"><p class="kh__label">BENEFIT</p><h2>{d["gain_title"]}</h2><p>{d["gain_lead"]}</p></div>
      <ol class="gain">{gains}</ol>
    </div>
  </section>

  <section class="cs cs--bg" id="cmp">
    <div class="inner">
      <div class="kh"><p class="kh__label">{d["cmp_label"]}</p><h2>{d["cmp_title"]}</h2><p>{d["cmp_lead"]}</p></div>
      <div class="cmp-wrap"><table class="cmp"><thead><tr>{heads}</tr></thead><tbody>{rows}</tbody></table></div>
      <p class="cmp-note">{d["cmp_note"]}</p>
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
      <div class="kh"><p class="kh__label">DOCUMENTS</p><h2>{d["docs_title"]}</h2><p>{d["docs_lead"]}</p></div>
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
        <p>{d["cta_lead"]}</p>
      </div>
      <div class="contact__side">
        <div class="contact__tel">대표전화<b>00-0000-0000</b></div>
        <a class="btn btn--fill" href="../index.html#inquiry">{t} 견적문의</a>
      </div>
    </div>
  </section>

  <div class="sample-wrap"><div class="inner"><p class="sample-note">※ 본 페이지의 문구·수치는 시안용 샘플입니다. 실제 내용 확정 후 교체됩니다.</p></div></div>
</main>'''
    path = f"{repo}/cert/{slug}.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + main + TAIL)
    return path


def build_all(repo):
    for slug in PAGES:
        print("wrote", build(slug, repo))
