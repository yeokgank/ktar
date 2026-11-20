#!/usr/bin/env python3
"""인증 상세 3종(GS·KC·클라우드) 생성기. gen_subpages.py 가 호출한다.
구성: 히어로+핵심정보 패널 → 앵커 탭 → 이점 → 비교표 → 프로세스 → 준비 서류 → 문의.
문구는 「KTAR 홈페이지 수정 작업지시서 2차 · 문구 확정본」 기준. 디자인·배치는 유지한다."""
import os, re

SP = os.path.dirname(os.path.abspath(__file__))
HEAD = open(f"{SP}/tpl_head.html", encoding="utf-8").read()
TAIL = open(f"{SP}/tpl_tail.html", encoding="utf-8").read()

SWITCH = [("GS인증", "gs"), ("KC인증", "kc"), ("클라우드서비스확인제", "cloud")]
ROLE_ME = "KTAR"

# 작업지시서 7. 반복 안내 문구
CERT_COMMON_NOTE = "KTAR은 인증기관 연계와 신청·진행을 지원하며, 심사 및 인증서 발급은 해당 기관의 기준과 절차에 따라 진행됩니다."
DOCS_NOTE = "보안이 필요한 기술자료는 담당자 안내 후 별도 전달해 주세요."

PAGES = {
    "gs": dict(
        title="GS인증",
        lead="소프트웨어 품질인증을 위한 신청요건과 제출자료를 검토하고, 지정 인증기관의 시험·심사 절차에 맞춰 접수 및 진행을 지원합니다.",
        h1="GS인증,<br><em>신청 준비</em>부터 심사 대응까지 지원합니다",
        facts=[("대상", "GS인증 대상에 해당하는 소프트웨어 제품"),
               ("목적", "소프트웨어 제품의 품질 특성을 제3자 인증기관이 평가"),
               ("평가 기준", "해당 인증기관의 GS인증 적용 기준 및 절차"),
               ("인증기관", "GS인증 수행 권한을 보유한 지정 인증기관"),
               ("처리기간", "제품 유형·시험 범위·기관 일정에 따라 안내"),
               ("인증 결과", "해당 인증기관의 심사 결과에 따라 등급 및 인증 여부 결정")],
        gain_title="GS인증 준비가 필요한 여섯 가지 상황",
        gain_lead="GS인증은 소프트웨어 품질을 제3자에게 검증받는 제도입니다. 활용 가능 범위와 제도상 혜택은 해당 사업 및 적용 요건에 따라 달라집니다.",
        gains=[("공공 조달 준비", "공공 조달 또는 납품 과정에서 GS인증이 요구되거나 활용되는지 확인합니다."),
               ("제품 품질 검증", "소프트웨어의 기능 및 품질 특성을 지정 인증기관의 기준에 따라 평가받습니다."),
               ("고객사 요구 대응", "고객사나 발주기관에서 요구하는 인증 등급과 제출자료를 사전에 검토합니다."),
               ("출시 전 품질 점검", "인증 신청 전 제품 기능, 사용설명서, 시험환경 등 준비사항을 점검합니다."),
               ("인증 신청 서류 준비", "제품 설명자료 및 시험에 필요한 문서의 누락 여부를 확인합니다."),
               ("보완 요청 대응", "인증 과정에서 발생하는 보완 요구와 일정 변경사항을 관리합니다.")],
        cmp_title="GS인증 등급별 적용 기준을 확인하세요",
        cmp_lead="GS인증 등급과 시험범위는 해당 인증제도 및 인증기관의 적용 기준에 따라 정해집니다. 제품에 필요한 등급과 세부 시험항목을 사전 검토합니다.",
        cmp_head=["항목", "1등급", "2등급"], cmp_rec=0,
        cmp_rows=[("평가 기준", "해당 인증기관의 1등급 적용 기준", "해당 인증기관의 2등급 적용 기준"),
                  ("시험 범위", "제품 특성 및 적용 기준에 따라 결정", "제품 특성 및 적용 기준에 따라 결정"),
                  ("인증 결과", "인증기관의 시험·심사 결과에 따라 결정", "인증기관의 시험·심사 결과에 따라 결정"),
                  ("KTAR 지원", "신청 요건 검토·자료 준비·기관 연계", "신청 요건 검토·자료 준비·기관 연계"),
                  ("활용 여부", "발주처·조달사업의 개별 요건 확인", "발주처·조달사업의 개별 요건 확인")],
        cmp_note="※ 등급별 시험·심사 기준과 제도상 혜택은 해당 인증기관 및 관련 사업의 최신 기준을 확인해 적용합니다.",
        proc_title="신청 요건을 확인하고,<br>인증기관 절차에 맞춰 진행합니다",
        proc_ban="제품 정보와 인증 목적을 남겨주시면 신청 준비 및 진행 절차를 안내드립니다.",
        steps=[("문의 접수", "소프트웨어 제품, 활용 목적 및 희망 인증 등급을 확인합니다.", ["KTAR"]),
               ("요건 검토·견적", "제품 특성과 인증요건을 검토하고 인증기관과 비용·일정을 협의합니다.", ["KTAR", "인증기관"]),
               ("자료 준비", "제품 실행환경, 기능 목록 및 제출자료를 확인하고 신청 준비를 지원합니다.", ["의뢰자", "KTAR"]),
               ("인증 접수", "지정 인증기관에 신청서를 접수하고 시험 일정 및 보완 요청사항을 확인합니다.", ["인증기관", "KTAR"]),
               ("시험·심사 진행", "인증기관이 해당 기준에 따라 시험·심사를 수행합니다. KTAR은 진행사항을 관리합니다.", ["인증기관"]),
               ("인증 결과 안내", "인증기관이 심사 결과에 따라 인증서를 발급하며, KTAR은 결과 확인과 후속 절차를 지원합니다.", ["인증기관", "KTAR"])],
        docs_title="기업이 준비할 것",
        docs_lead="신청 시 필요한 자료는 제품 및 인증기관에 따라 달라집니다. 보유 자료를 먼저 공유해 주시면 필수 제출사항을 안내드립니다.",
        docs_you=[("제품 실행 파일 또는 접속 정보", "시험용"), ("기능 목록 및 제품 소개자료", "보유 자료"),
                  ("사용자·설치 설명서", "초안 가능"), ("시험환경 정보", "OS·DB·브라우저 등"),
                  ("신청 기업 기본정보", "필요 시")],
        docs_me=[("인증 신청 절차 안내", "인증기관 기준"), ("제출자료 목록 정리", "기관별 요구사항"),
                 ("신청·접수자료 작성 지원", "제공 자료 기준"), ("시험 일정 및 보완사항 관리", "진행 중"),
                 ("결과 확인 및 후속 안내", "기관 결과 기준")],
        cta_title="GS인증 신청 준비,<br>무엇부터 필요한지 안내합니다",
        cta_lead="회사명, 소프트웨어 제품명과 인증 목적을 남겨주시면 담당자가 확인 후 연락드립니다.",
        cta_btn="GS인증 문의하기",
    ),
    "kc": dict(
        title="KC인증",
        lead="KC는 법령에서 정한 대상 제품에 적용되는 의무 안전·적합성평가 제도입니다. KTAR은 제품 유형에 따른 적용 절차 검토와 시험·인증기관 연계, 접수 및 진행 관리를 지원합니다.",
        h1="KC인증,<br><em>제품별 의무 절차</em>부터 체계적으로 준비합니다",
        facts=[("대상", "관련 법령에 따라 KC 안전 또는 적합성평가 의무가 적용되는 제품"),
               ("목적", "제품 안전 및 전자파·무선 관련 필수 요건 확인"),
               ("적용 제도", "전기용품 안전인증·안전확인·공급자적합성확인 / 방송통신기자재 적합성평가 등"),
               ("수행기관", "해당 제도의 지정 시험·인증기관 또는 적합성평가 관련 기관"),
               ("처리기간", "제품 유형·시험항목·기관 일정에 따라 개별 안내"),
               ("사후관리", "제품 변경 및 적용 제도에 따른 변경신고·재평가 여부 확인")],
        gain_title="KC 의무 절차,<br>제품 특성에 맞춰 준비합니다",
        gain_lead="KC 적용 대상과 이행 절차는 제품 유형 및 관련 법령에 따라 달라집니다. 제품별 필수 요건부터 확인합니다.",
        gains=[("법정 의무 이행", "KC 적용 대상 제품은 국내 제조·수입·판매 전 관련 법령에 따른 인증·확인·등록 등 필수 절차를 이행해야 합니다."),
               ("제품 안전성 확인", "해당 제품군에 적용되는 안전 기준과 시험항목을 검토하여 필수 안전 요건 확인을 지원합니다."),
               ("국내 판매·유통 준비", "적용 제도에 따른 절차 이행 여부와 표시사항을 확인하여 출시 준비를 지원합니다."),
               ("수입 제품 적용 검토", "해외 제조·수입 제품의 국내 적용 요건과 필요한 시험·서류를 검토합니다."),
               ("무선·통신 기능 검토", "Wi-Fi·Bluetooth 등 무선 기능이 있는 제품의 방송통신기자재 적합성평가 해당 여부를 확인합니다."),
               ("R&D 시제품 상용화", "개발 제품의 양산·유통을 앞두고 적용되는 KC 절차와 예상 준비사항을 검토합니다.")],
        cmp_title="KC 적용 제도,<br>제품 유형에 따라 달라집니다",
        cmp_lead="전기용품의 안전관리 절차와 방송통신기자재 적합성평가는 서로 다른 제도입니다. 실제 적용 여부는 제품의 용도와 기술 사양을 기준으로 확인합니다.",
        cmp_head=["비교 항목", "안전인증", "안전확인", "공급자적합성확인"], cmp_rec=0,
        cmp_rows=[("적용 대상", "관련 법령에서 안전인증 대상으로 지정한 제품", "관련 법령에서 안전확인 대상으로 지정한 제품", "관련 법령에서 공급자적합성확인 대상으로 지정한 제품"),
                  ("이행 방식", "지정기관의 제품검사 및 해당 시 공장심사 등", "지정 시험기관의 시험 후 안전확인 신고 등", "공급자가 기준 적합 여부를 확인하고 관련 서류를 보관"),
                  ("KTAR 지원", "제품 유형 검토·기관 연계·서류 및 일정 관리", "시험기관 연계·신고 관련 자료 준비 지원", "적용 기준 검토·필요 자료 정리 지원"),
                  ("변경 시", "관련 법령에 따라 변경 절차 검토", "관련 법령에 따라 변경 절차 검토", "관련 법령에 따라 변경사항 검토")],
        cmp_note="※ 위 표는 전기용품 안전관리 절차의 개요입니다. 방송통신기자재 적합성평가는 별도 제도로 적용 여부와 절차를 확인해야 합니다.",
        proc_title="제품별 적용 절차를 확인하고,<br>기관과 연계해 진행합니다",
        proc_ban="제품 사양을 남겨주시면 적용 제도와 필요한 시험·인증 절차를 검토해 안내드립니다.",
        steps=[("문의 접수", "제품명, 사용 용도 및 주요 사양을 확인합니다.", ["KTAR"]),
               ("제도 검토·견적", "적용 법령과 인증·적합성평가 유형을 검토하고 시험기관과 비용·일정을 협의합니다.", ["KTAR", "협력기관"]),
               ("접수 준비", "필요한 신청서, 제품자료, 시료 목록을 확인하고 접수 준비를 지원합니다.", ["의뢰자", "KTAR"]),
               ("시험·심사 접수", "해당 시험·인증기관의 절차에 따라 접수하고 일정과 보완사항을 안내합니다.", ["협력기관", "KTAR"]),
               ("시험·심사 수행", "해당 기관이 관련 기준에 따라 시험 또는 심사를 수행합니다. KTAR은 진행상황을 관리합니다.", ["시험·인증기관"]),
               ("결과 문서 안내", "해당 기관의 시험·심사 결과에 따라 인증서 또는 적합성평가 관련 문서가 처리되며, KTAR은 후속 절차를 안내합니다.", ["해당 기관", "KTAR"])],
        docs_title="기업이 준비할 것",
        docs_lead="기업은 제품의 기본 사양과 보유 자료를 준비해 주세요. 실제 필요 서류와 시료 수량은 제품별 적용 제도 및 담당기관에 따라 안내드립니다.",
        docs_you=[("제품명·용도·기본 사양", "형식 자유"), ("시험용 시료 및 제품 사진", "필요 수량은 기관 확인 후 안내"),
                  ("회로도·블록도·부품 정보", "해당 시"), ("사용자 설명서·표시사항 시안", "보유 자료"),
                  ("사업자등록 관련 자료", "필요 시")],
        docs_me=[("적용 제도 검토 지원", "제품 유형별"), ("시험·인증기관 연계", "해당 기관 안내"),
                 ("신청·접수자료 정리 지원", "기관 요구양식 기준"), ("일정 및 보완 요청 관리", "진행 중"),
                 ("결과 문서 전달 및 후속 안내", "기관 발급·처리 후")],
        cta_title="KC 적용 대상 여부부터<br>확인해 드립니다",
        cta_lead="회사명과 제품명, 사용 용도를 남겨주시면 담당자가 연락드려 필요한 시험·인증 절차를 안내합니다.",
        cta_btn="KC인증 문의하기",
    ),
    "cloud": dict(
        title="클라우드서비스확인제",
        lead="클라우드 서비스의 적용 제도와 제출요건을 검토하고, 관련 평가·확인기관과 연계하여 자료 준비 및 진행 절차를 지원합니다.",
        h1="클라우드 서비스,<br><em>평가·확인 준비</em>부터 진행까지 지원합니다",
        facts=[("대상", "평가·확인 관련 요건 검토가 필요한 클라우드 서비스"),
               ("목적", "서비스에 적용되는 평가 기준 및 제출 요건 확인"),
               ("검토 영역", "서비스 품질·정보보호·운영관리 등 관련 제도에 따른 항목"),
               ("수행기관", "해당 제도의 평가·확인 권한을 가진 기관"),
               ("결과 문서", "해당 제도의 담당기관이 정한 결과 문서"),
               ("소요기간", "적용 제도와 평가 범위 확인 후 개별 안내")],
        gain_title="클라우드 서비스 평가 준비가 필요한 여섯 가지 상황",
        gain_lead="서비스 유형과 제출 목적에 따라 필요한 확인 항목이 달라집니다. 관련 제도와 준비자료부터 검토합니다.",
        gains=[("도입기관 요구 검토", "도입기관이 요구하는 서비스 평가·확인 항목과 제출자료를 확인합니다."),
               ("서비스 품질 점검", "가용성, 서비스 수준 및 고객지원 등 품질 관련 준비자료를 정리합니다."),
               ("정보보호 준비", "서비스의 보안정책 및 접근통제 등 관련 자료의 준비 여부를 확인합니다."),
               ("운영관리 체계 정리", "장애 대응, 변경관리 및 운영절차와 관련된 증빙을 정리합니다."),
               ("평가·확인 절차 대응", "해당 기관의 신청 요건과 제출 절차를 확인해 진행을 지원합니다."),
               ("보완사항 관리", "관련 기관의 보완 요청사항을 정리하고 제출 일정을 관리합니다.")],
        cmp_title="평가·확인 준비 시 검토하는 주요 영역",
        cmp_lead="아래는 일반적인 사전 검토 영역이며, 실제 심사·확인 항목은 적용 제도와 담당기관 기준에 따라 확정됩니다.",
        cmp_head=["영역", "검토 내용", "준비 자료 예시"], cmp_rec=0,
        cmp_rows=[("서비스 품질", "서비스 제공 수준 및 안정성 관련 자료 확인", "SLA·서비스 운영 현황"),
                  ("정보보호", "보안정책·접근통제·데이터 보호 관련 자료 확인", "보안정책·권한관리 자료"),
                  ("운영 관리", "장애·변경·백업 등 운영 절차 확인", "운영절차서·이력"),
                  ("고객 지원", "이용자 안내·문의·장애 접수 체계 확인", "고객지원 절차 및 연락체계")],
        cmp_note="※ 실제 적용 기준, 심사 항목 및 결과 문서 명칭은 해당 평가·확인제도와 담당기관의 현행 기준을 따릅니다.",
        proc_title="적용 제도를 검토하고,<br>관련 기관의 절차에 따라 진행합니다",
        proc_ban="서비스 개요를 남겨주시면 적용 가능한 평가·확인 절차를 검토해 안내드립니다.",
        steps=[("문의 접수", "서비스 유형과 확인 목적 및 요청기관의 요구사항을 확인합니다.", ["KTAR"]),
               ("제도 검토·안내", "적용 가능한 제도와 담당기관, 예상 절차 및 준비사항을 검토합니다.", ["KTAR", "관련기관"]),
               ("자료 준비", "서비스 설명서와 운영·보안 관련 제출자료를 정리합니다.", ["의뢰자", "KTAR"]),
               ("평가·확인 접수", "해당 제도의 담당기관에 신청하거나 필요한 제출 절차를 지원합니다.", ["담당기관", "KTAR"]),
               ("평가·보완 대응", "담당기관이 정해진 절차에 따라 평가하고, KTAR은 보완자료 및 일정을 관리합니다.", ["담당기관", "KTAR"]),
               ("결과 확인·안내", "담당기관의 평가 결과와 결과 문서 발급 여부를 확인하고 후속사항을 안내합니다.", ["담당기관", "KTAR"])],
        docs_title="기업이 준비할 것",
        docs_lead="필요 서류와 확인 절차는 적용 제도 및 서비스 유형에 따라 달라집니다. 최초 문의 시에는 상세 보안자료 업로드가 필요하지 않습니다.",
        docs_you=[("서비스 소개 및 제공 범위", "보유 자료"), ("시스템 구성도·운영 현황", "해당 시"),
                  ("보안 정책 및 접근관리 자료", "보유 자료"), ("장애·변경관리 절차 관련 자료", "해당 시")],
        docs_me=[("적용 제도 사전 검토", "문의 내용 기준"), ("기관별 제출자료 안내", "제도 확인 후"),
                 ("접수 자료 정리 지원", "보유 자료 기준"), ("보완 요청 및 일정 관리", "진행 중"),
                 ("결과 문서 수령 절차 안내", "담당기관 기준")],
        cta_title="클라우드 서비스의<br>평가·확인 절차를 안내합니다",
        cta_lead="서비스명과 제공 형태(SaaS·PaaS·IaaS 등), 문의 목적을 남겨주시면 담당자가 확인 후 연락드립니다.",
        cta_btn="클라우드 서비스 문의하기",
    ),
}

ANCHORS = [("gain", "취득 이점"), ("cmp", "비교"), ("proc", "프로세스"), ("docs", "준비 서류"), ("contact", "견적문의")]


def who(roles):
    return '<div class="who">' + "".join(f'<i class="{"me" if r == ROLE_ME else ""}">{r}</i>' for r in roles) + "</div>"


def plain(s):
    """메타 설명용: 태그 제거."""
    return re.sub(r"<[^>]+>", "", s)


def build(slug, repo):
    d = PAGES[slug]
    t = d["title"]
    head = HEAD
    head = re.sub(r"<title>.*?</title>", f"<title>{t} | KTAR 한국시험평가원</title>", head)
    head = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{plain(d["lead"])}">', head)
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
            heads += f'<th scope="col" class="rec">{h}</th>'
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
    # 인증 공통 안내는 '인증서'를 명시하므로, 결과 문서 명칭이 미확정인 클라우드에는 넣지 않는다(작업지시서 4 주의)
    note = "" if slug == "cloud" else f'<p class="contact__note">{CERT_COMMON_NOTE}</p>'

    main = f'''<main class="cp">
  <section class="ph ph--{slug}">
    <div class="inner ph__inner">
      <ol class="crumb" aria-label="현재 위치">
        <li><a href="../index.html">홈</a></li>
        <li>인증</li>
        <li aria-current="page">{t}</li>
      </ol>
      <div>
        <h1>{d["h1"]}</h1>
        <p class="ph__lead">{d["lead"]}</p>
        <div class="ph__cta">
          <a class="btn btn--fill" href="../index.html#inquiry">{t} 견적문의</a>
          <a class="btn btn--line" href="#proc">발급 프로세스 보기</a>
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
      <div class="atab__sw"><span>인증 서비스</span>{sw}</div>
    </div>
  </div>

  <section class="cs" id="gain">
    <div class="inner">
      <div class="kh"><h2>{d["gain_title"]}</h2><p>{d["gain_lead"]}</p></div>
      <ol class="gain">{gains}</ol>
    </div>
  </section>

  <section class="cs cs--bg" id="cmp">
    <div class="inner">
      <div class="kh"><h2>{d["cmp_title"]}</h2><p>{d["cmp_lead"]}</p></div>
      <div class="cmp-wrap"><table class="cmp"><thead><tr>{heads}</tr></thead><tbody>{rows}</tbody></table></div>
      <p class="cmp-note">{d["cmp_note"]}</p>
    </div>
  </section>

  <section class="cs" id="proc">
    <div class="inner">
      <div class="kh"><h2>{d["proc_title"]}</h2></div>
      <div class="proc-ban"><b>{d["proc_ban"]}</b><a href="../index.html#inquiry">견적문의</a></div>
      <ol class="proc">{steps}</ol>
    </div>
  </section>

  <section class="cs cs--bg" id="docs">
    <div class="inner">
      <div class="kh"><h2>{d["docs_title"]}</h2><p>{d["docs_lead"]}</p></div>
      <div class="docs">
        <div class="docs__col"><h3>기업<small>준비</small></h3><ul>{you}</ul></div>
        <div class="docs__col me"><h3>KTAR<small>지원</small></h3><ul>{me}</ul></div>
      </div>
      <p class="docs-note">{DOCS_NOTE}</p>
    </div>
  </section>

  <section class="contact" id="contact">
    <div class="inner contact__inner">
      <div>
        <h2>{d["cta_title"]}</h2>
        <p>{d["cta_lead"]}</p>
        {note}
      </div>
      <div class="contact__side">
        <a class="btn btn--fill" href="../index.html#inquiry">{d["cta_btn"]}</a>
      </div>
    </div>
  </section>
</main>'''
    path = f"{repo}/cert/{slug}.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + main + TAIL)
    return path


def build_all(repo):
    for slug in PAGES:
        print("wrote", build(slug, repo))
