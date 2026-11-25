#!/usr/bin/env python3
"""인증 상세 3종(GS·KC·클라우드) 생성기. gen_subpages.py 가 호출한다.
구성: 히어로+핵심정보 패널 → 앵커 탭 → 이점 → 비교표 → 프로세스 → 준비 서류 → 문의.
문구는 「KTAR 홈페이지 수정 작업지시서 2차 · 문구 확정본」 기준. 디자인·배치는 유지한다."""
import os, re

SP = os.path.dirname(os.path.abspath(__file__))
HEAD = open(f"{SP}/tpl_head.html", encoding="utf-8").read()
TAIL = open(f"{SP}/tpl_tail.html", encoding="utf-8").read()

SWITCH = [("GS인증", "gs"), ("KC인증", "kc"), ("클라우드서비스확인제", "cloud")]

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
        anchors=[("gain", "필요 상황"), ("cmp", "등급 기준"), ("check", "점검항목")],
        gain_title="GS인증이 필요한 여섯 가지 상황",
        gain_lead="GS인증은 소프트웨어 제품의 품질을 객관적으로 검증하는 국가 소프트웨어 품질인증 제도입니다. 공공조달, 판로 확대 및 제품 경쟁력 확보에 활용할 수 있습니다.",
        gains=[("공공기관 납품 및 조달시장 진출", "나라장터 등록 및 공공기관 대상 소프트웨어 공급을 준비하는 경우"),
               ("우선구매 및 수의계약 활용", "GS인증을 활용한 공공기관 우선구매 및 수의계약 제도 적용을 검토하는 경우"),
               ("입찰 및 발주처 요구 대응", "입찰 참가 또는 제품 납품 시 발주처에서 GS인증을 요구하는 경우"),
               ("소프트웨어 품질 입증", "제품의 기능, 성능, 신뢰성, 보안성 등 소프트웨어 품질을 객관적으로 입증하고자 하는 경우"),
               ("정부 R&amp;D 과제 성과 확보", "정부 연구개발 과제의 성과지표 또는 사업화 목표로 GS인증 획득이 필요한 경우"),
               ("제품 경쟁력 및 대외 신뢰도 확보", "소프트웨어 제품의 품질 신뢰도를 높이고 신규 고객 확보 및 판로 확대를 추진하는 경우")],
        gain_note="※ 인증에 따른 제도적 혜택은 인증 등급, 제품 유형 및 관련 제도의 적용 요건에 따라 달라질 수 있습니다.",
        cmp_title="GS인증 등급별 평가 기준 및 준비사항",
        cmp_lead="GS인증은 1등급과 2등급으로 구분되며, 등급별 평가 방식과 점수 기준에 차이가 있습니다. 원활한 인증 획득을 위해서는 평가 기준에 대한 이해와 체계적인 사전 준비가 필요합니다.",
        cmp_head=["구분", "1등급", "2등급"], cmp_rec=0,
        cmp_rows=[("평가 방식", "소프트웨어 품질평가", "품질평가 및 업무적합성 평가"),
                  ("평가 비중", "품질평가 100%", "품질평가 60% + 업무적합성 평가 40%"),
                  ("평가점수 기준", "80점 이상", "합산 70점 이상"),
                  ("평가 대상", "제품설명서, 사용자취급설명서 및 실행 소프트웨어", "소프트웨어 품질 및 업무적합성"),
                  ("추가 제출서류", "해당 없음", "업무적합성 기술서")],
        cmp_note="※ 인증 취득 여부는 평가 기준 충족 및 인증기관의 심의 결과에 따라 결정됩니다.<br>"
                 "※ 등급별 신청 가능 여부는 인증기관에 따라 확인이 필요합니다.",
        check=dict(
            title="필수 준비사항 및 점검항목",
            lead="원활한 인증 진행을 위해 제품 관련 문서와 소프트웨어 기능에 대한 체계적인 사전점검이 필요합니다.",
            stats=[("56", "전체 점검항목"), ("32", "필수 점검항목")],
            head=["구분", "전체 항목", "필수 항목", "주요 점검 내용"],
            rows=[("제품설명서", "28개", "12개", "식별자, 공급자 정보, 운영환경, 설치절차 등"),
                  ("사용자취급설명서", "13개", "9개", "전 기능 사용법, 목차, 색인, 용어 등"),
                  ("기능 요구사항", "15개", "11개", "접근통제, 감사기록, 암호화, 인증규칙 등"),
                  ("합계", "56개", "32개", "전체 점검항목 중 필수 32개")],
            note="※ 상기 점검항목은 당사의 GS인증 지원 시 활용하는 사전점검 자료 기준이며, 인증 등급, 제품 특성 및 인증기관에 따라 세부 적용 항목이 달라질 수 있습니다.",
            cta_title="체계적인 사전 준비부터 인증 획득까지",
            cta_text="KTAR는 대상 제품 검토, 신청자료 준비, 사전점검, 인증기관 연계 및 결함 보완 대응까지 GS인증 획득 전 과정을 지원합니다.",
            cta_btn="GS인증 상담 및 견적 문의"),
        proc_title="신청 요건을 확인하고,<br>인증기관 절차에 맞춰 진행합니다",
        proc_ban="제품 정보와 인증 목적을 남겨주시면 GS인증 획득에 필요한 전 과정을 지원합니다.",
        steps=[("문의 접수", "소프트웨어 제품 정보, 인증 목적 및 희망 인증등급을 확인합니다."),
               ("대상 제품 검토", "제품 기술 검토, 소프트웨어 규모 및 기능 수 산정, 요구사항 범위 검토를 진행합니다."),
               ("접수 서류 안내·검토", "제품설명서 및 사용자취급설명서 양식을 제공하고 인증 신청에 필요한 제출자료 준비와 검토를 지원합니다."),
               ("인증 접수 및 일정 조율", "지정 인증기관에 인증 신청을 접수하고 시험 일정 및 보완 요청사항을 확인합니다."),
               ("결함 안내·대응", "결함보고서 분석 및 개선 방향 안내, 문서·시스템 보완 지원, 평가 중지 조건 모니터링을 진행합니다."),
               ("GS인증서 발급", "인증기관의 심의를 거쳐 인증이 확정되면 GS인증서 및 시험성적서가 발급됩니다.")],
        proc_note="※ 인증 진행 기간은 제품 규모, 결함 보완 소요 기간 및 인증기관의 평가 일정에 따라 달라질 수 있습니다.<br>"
                  "※ 품질평가, 인증 심의 및 GS인증서 발급은 과학기술정보통신부 지정 인증기관에서 수행합니다.",
        docs_title="기업이 준비할 것",
        docs_lead="신청 시 필요한 자료는 제품 및 인증기관에 따라 달라집니다. 보유 자료를 먼저 공유해 주시면 필수 제출사항을 안내드립니다.",
        docs_you=[("제품 실행 파일 또는 접속 정보", "시험용"), ("기능 목록 및 제품 소개자료", "보유 자료"),
                  ("사용자·설치 설명서", "초안 가능"), ("시험환경 정보", "OS·DB·브라우저 등"),
                  ("신청 기업 기본정보", "필요 시")],
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
        cmp_head=["비교 항목", "안전인증대상", "안전확인대상", "공급자적합성확인대상"], cmp_rec=0,
        # 셀 안 줄바꿈 위치를 열끼리 맞춘다(Figma 코멘트: 문단 나눔 통일)
        cmp_rows=[("적용 대상", "관련 법령에서 안전인증 대상으로 <br>지정한 제품", "관련 법령에서 안전확인 대상으로 <br>지정한 제품", "관련 법령에서 공급자적합성확인 대상으로 <br>지정한 제품"),
                  ("이행 방식", "지정기관의 제품검사 및 <br>해당 시 공장심사 등", "지정 시험기관의 시험 후 <br>안전확인 신고 등", "공급자가 기준 적합 여부를 확인하고 <br>관련 서류를 보관"),
                  ("KTAR 지원", "제품 유형 검토·기관 연계 <br>서류 및 일정 관리", "시험기관 연계 <br>신고 관련 자료 준비 지원", "적용 기준 검토 <br>필요 자료 정리 지원"),
                  ("변경 시", "관련 법령에 따라 <br>변경 절차 검토", "관련 법령에 따라 <br>변경 절차 검토", "관련 법령에 따라 <br>변경사항 검토")],
        cmp_note="※ 위 표는 전기용품 안전관리 절차의 개요입니다. 방송통신기자재 적합성평가는 별도 제도로 적용 여부와 절차를 확인해야 합니다.",
        proc_title="제품별 적용 절차를 확인하고,<br>기관과 연계해 진행합니다",
        proc_ban="제품 사양을 남겨주시면 적용 제도와 필요한 시험·인증 절차를 검토해 안내드립니다.",
        steps=[("문의 접수", "제품명, 사용 용도 및 주요 사양을 확인합니다."),
               ("제도 검토·견적", "적용 법령과 인증·적합성평가 유형을 검토하고 시험기관과 비용·일정을 협의합니다."),
               ("접수 준비", "필요한 신청서, 제품자료, 시료 목록을 확인하고 접수 준비를 지원합니다."),
               ("시험·심사 접수", "해당 시험·인증기관의 절차에 따라 접수하고 일정과 보완사항을 안내합니다."),
               ("시험·심사 수행", "해당 기관이 관련 기준에 따라 시험 또는 심사를 수행합니다. KTAR은 진행상황을 관리합니다."),
               ("KC 인증서 발급", "해당 기관의 시험·심사 결과에 따라 인증서 또는 적합성평가 관련 문서가 처리되며, KTAR은 후속 절차를 안내합니다.")],
        docs_title="기업이 준비할 것",
        docs_lead="기업은 제품의 기본 사양과 보유 자료를 준비해 주세요. 실제 필요 서류와 시료 수량은 제품별 적용 제도 및 담당기관에 따라 안내드립니다.",
        docs_you=[("제품명·용도·기본 사양", "형식 자유"), ("시험용 시료 및 제품 사진", "필요 수량은 기관 확인 후 안내"),
                  ("회로도·블록도·부품 정보", "해당 시"), ("사용자 설명서·표시사항 시안", "보유 자료"),
                  ("사업자등록 관련 자료", "필요 시")],
        cta_title="KC 적용 대상 여부부터<br>확인해 드립니다",
        cta_lead="회사명과 제품명, 사용 용도를 남겨주시면 담당자가 연락드려 필요한 시험·인증 절차를 안내합니다.",
        cta_btn="KC인증 문의하기",
    ),
    "cloud": dict(
        title="클라우드서비스확인제",
        lead="클라우드서비스 확인제의 신청 요건과 제출자료를 검토하고, 한국인공지능클라우드산업협회(KACI)의 평가 절차에 맞춰 신청 준비부터 확인서 발급까지 지원합니다.",
        h1="클라우드서비스 확인제,<br><em>신청 준비</em>부터 확인서 발급까지 지원합니다",
        facts=[("대상", "IaaS·PaaS·SaaS 등 클라우드서비스"),
               ("목적", "클라우드서비스의 필수 요건 충족 여부를 확인하고 객관적인 검증자료 확보"),
               ("기준", "ISO/IEC 22123-2 기반 클라우드서비스 확인 기준"),
               ("수행기관", "한국인공지능클라우드산업협회(KACI)"),
               ("결과 문서", "클라우드서비스 확인서 및 검증결과서"),
               ("소요기간", "서비스 준비 현황, 보완 소요 기간 및 평가 일정에 따라 안내")],
        anchors=[("gain", "필요 상황"), ("cmp", "취득 이점")],
        gain_title="클라우드서비스 확인서 취득이 필요한 여섯 가지 상황",
        gain_lead="클라우드서비스를 제공하는 기업이 서비스의 적합성을 입증하고 객관적인 검증자료를 확보하고자 하는 경우 활용할 수 있습니다.",
        gains=[("클라우드서비스 적합성 입증", "제공 중인 서비스가 클라우드서비스의 필수 요건을 충족하는지 확인해야 하는 경우"),
               ("디지털서비스 등록 준비", "디지털서비스 심사 및 등록을 위해 클라우드서비스 관련 증빙자료가 필요한 경우"),
               ("공공기관 및 기업 대상 공급", "공공기관 또는 민간기업에 클라우드서비스 공급을 준비하는 경우"),
               ("신규 클라우드서비스 출시", "IaaS, PaaS, SaaS 등 신규 클라우드서비스의 개발을 완료하고 상용화를 준비하는 경우"),
               ("정부지원사업 및 과제 대응", "정부지원사업 또는 연구개발 과제에서 클라우드서비스 확인서를 요구하는 경우"),
               ("발주처 및 고객사 요구 대응", "사업 제안이나 계약 과정에서 클라우드서비스의 적합성을 입증해야 하는 경우")],
        cmp_title="클라우드서비스 확인서 취득의 주요 이점",
        cmp_lead="국제표준 기반의 검증을 통해 클라우드서비스의 적합성과 운영 신뢰성을 확보하고 기업의 시장 경쟁력을 강화할 수 있습니다.",
        cmp_cards=[("국제표준 기반 적합성 확보", "ISO/IEC 22123-2 기반의 검증을 통해 클라우드서비스의 필수 역량을 입증할 수 있습니다."),
                   ("디지털서비스 등록 활용", "디지털서비스 심사 및 등록 준비 시 클라우드서비스 관련 증빙자료로 활용할 수 있습니다."),
                   ("공공·민간시장 경쟁력 강화", "객관적인 검증 결과를 기반으로 사업 제안 및 서비스 공급 시 경쟁력을 강화할 수 있습니다."),
                   ("서비스 운영 역량 강화", "클라우드서비스의 핵심 기능 및 운영체계를 점검하여 서비스 관리 수준을 향상할 수 있습니다."),
                   ("보안취약점 사전 확인", "보안취약점 점검을 통해 잠재적인 보안 위험과 개선 필요사항을 파악할 수 있습니다."),
                   ("대외 신뢰도 확보", "확인서 및 검증결과서를 활용하여 고객사의 신뢰도와 기업의 대외 경쟁력을 높일 수 있습니다.")],
        cmp_note="※ 확인서의 활용 범위는 관련 사업 및 발주기관의 적용 요건에 따라 달라질 수 있습니다.",
        proc_title="문의 접수부터 클라우드서비스 확인서 발급까지 함께합니다.",
        proc_ban="서비스 정보와 확인서 취득 목적을 남겨주시면 신청 준비부터 확인서 발급까지 단계별로 지원합니다.",
        steps=[("문의 접수", "클라우드서비스 유형(IaaS, PaaS, SaaS 등) 및 확인서 취득 목적을 확인합니다."),
               ("대상 서비스 검토 및 견적", "서비스의 주요 기능, 시스템 구성 및 확인제 적용 요건을 검토하고 비용과 일정을 안내합니다."),
               ("신청자료 준비 및 접수", "신청서, 자가진단표, 서비스 소개자료 등 제출서류의 준비 및 신청 접수를 지원합니다."),
               ("사전 검토 및 평가 준비", "제출서류와 발표자료의 검토를 지원하고 현장 평가 일정 및 시연 준비사항을 확인합니다."),
               ("현장 평가 및 보완 대응", "서비스 발표·시연 및 보안취약점 점검에 필요한 준비와 평가 과정에서 발생하는 보완사항에 대한 대응을 지원합니다."),
               ("클라우드서비스 확인서 발급", "심의위원회의 심의를 거쳐 발급 기준을 충족한 경우 KACI에서 클라우드서비스 확인서 및 검증결과서를 발급합니다.")],
        proc_note="※ 진행 기간은 서비스 준비 현황, 보완 소요 기간 및 평가 일정에 따라 달라질 수 있습니다.<br>"
                  "※ 공식 평가 및 확인서 발급 절차는 한국인공지능클라우드산업협회(KACI)의 기준에 따릅니다.",
        docs_title="기업이 준비할 것",
        docs_lead="필요 서류는 서비스 유형과 확인제 신청 요건에 따라 달라집니다. 최초 문의 시에는 상세 보안자료 업로드가 필요하지 않습니다.",
        docs_you=[("서비스 소개 및 제공 범위", "보유 자료"), ("시스템 구성도·운영 현황", "해당 시"),
                  ("보안 정책 및 접근관리 자료", "보유 자료"), ("장애·변경관리 절차 관련 자료", "해당 시")],
        cta_title="클라우드서비스 확인제<br>신청 절차를 안내합니다",
        cta_lead="서비스명과 제공 형태(SaaS·PaaS·IaaS 등), 문의 목적을 남겨주시면 담당자가 확인 후 연락드립니다.",
        cta_btn="클라우드서비스 확인제 문의하기",
    ),
}

ANCHORS = [("gain", "취득 이점"), ("cmp", "비교"), ("proc", "프로세스"), ("docs", "준비 서류"), ("contact", "견적문의")]
INQUIRY = "../index.html#inquiry"


def plain(s):
    """메타 설명용: 태그 제거."""
    return re.sub(r"<[^>]+>", "", s)


def anchors_html(d):
    """기본 앵커에 페이지별 라벨 덮어쓰기(anchors) 적용. 새 id 는 '비교' 뒤에 끼운다."""
    labels = dict(ANCHORS)
    extra = []
    for i, n in d.get("anchors", []):
        if i in labels:
            labels[i] = n
        else:
            extra.append((i, n))
    order = [i for i, _ in ANCHORS]
    order = order[:2] + [i for i, _ in extra] + order[2:]
    labels.update(extra)
    return "".join(f'<a href="#{i}">{labels[i]}</a>' for i in order)


def cards_html(items):
    """번호 카드 3열(이점·필요 상황 공용)."""
    lis = "".join(f'<li><span class="gain__no">{n:02d}</span><b>{a}</b><span>{b}</span></li>'
                  for n, (a, b) in enumerate(items, 1))
    return f'<ol class="gain">{lis}</ol>'


def table_html(head, rows, rec=0, cls="", sum_last=False):
    rec_attr = ' class="rec"'
    heads = "".join(f'<th scope="col"{rec_attr if n == rec and n > 0 else ""}>{h}</th>'
                    for n, h in enumerate(head))
    body = ""
    for k, r in enumerate(rows):
        cells = f'<th scope="row">{r[0]}</th>' + "".join(
            f'<td class="{"rec" if n == rec else ""}">{c}</td>' for n, c in enumerate(r[1:], 1))
        is_sum = sum_last and k == len(rows) - 1
        body += f'<tr class="is-sum">{cells}</tr>' if is_sum else f"<tr>{cells}</tr>"
    return (f'<div class="cmp-wrap"><table class="cmp{(" " + cls) if cls else ""}">'
            f"<thead><tr>{heads}</tr></thead><tbody>{body}</tbody></table></div>")


def steps_html(steps):
    """6단계 카드. (제목, 본문[, 보조 안내]) — 역할 표기 박스는 Figma 코멘트로 전 페이지 삭제."""
    out = ""
    for n, st in enumerate(steps, 1):
        sub = f'<small class="proc__sub">{st[2]}</small>' if len(st) > 2 else ""
        out += f'<li><span class="proc__no">{n}</span><b>{st[0]}</b><p>{st[1]}</p>{sub}</li>'
    return f'<ol class="proc">{out}</ol>'


def note_html(text, cls="cmp-note"):
    return f'<p class="{cls}">{text}</p>' if text else ""


def docs_html(title, lead, items, note):
    """준비 서류: 제목·설명은 왼쪽, 항목은 오른쪽에 세로 카드로 쌓는다(코서트 발급 프로세스 형식)."""
    lis = "".join(f'<li><span class="docs2__no">{n}</span><div><b>{a}</b><span>{b}</span></div></li>'
                  for n, (a, b) in enumerate(items, 1))
    return f'''<section class="cs cs--bg" id="docs">
    <div class="inner docs2">
      <div class="docs2__head">
        <h2>{title}</h2>
        <p>{lead}</p>
        <p class="docs-note">{note}</p>
        <a class="btn btn--fill" href="{INQUIRY}">견적문의</a>
      </div>
      <ol class="docs2__list">{lis}</ol>
    </div>
  </section>'''


def check_html(c):
    """GS 필수 준비사항·점검항목: 숫자 카드 2개 + 세부 표(합계 행 강조) + 상담 유도."""
    key_attr = ' class="is-key"'
    stats = "".join(f'<div{key_attr if n else ""}><b>{v}<small>개</small></b><span>{k}</span></div>'
                    for n, (v, k) in enumerate(c["stats"]))
    return f'''<div class="chk" id="check">
        <div class="kh"><h2>{c["title"]}</h2><p>{c["lead"]}</p></div>
        <div class="chk__stats">{stats}</div>
        {table_html(c["head"], c["rows"], cls="cmp--chk", sum_last=True)}
        {note_html(c["note"])}
        <div class="proc-ban chk__cta"><div><b>{c["cta_title"]}</b><p>{c["cta_text"]}</p></div><a href="{INQUIRY}">{c["cta_btn"]}</a></div>
      </div>'''


def build(slug, repo):
    d = PAGES[slug]
    t = d["title"]
    head = HEAD
    head = re.sub(r"<title>.*?</title>", f"<title>{t} | KTAR 한국시험평가원</title>", head)
    head = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{plain(d["lead"])}">', head)
    head = head.replace('<li><a href="../cert/gs.html">', '<li class="is-current"><a href="../cert/gs.html">', 1)
    head = head.replace('<link rel="stylesheet" href="../css/sub.css?v=20261124b">',
                        '<link rel="stylesheet" href="../css/sub.css?v=20261124b">\n<link rel="stylesheet" href="../css/cert.css?v=20261125c">')

    facts = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in d["facts"])
    sw = "".join(f'<a href="{s}.html"' + (' aria-current="page"' if s == slug else "") + f">{n}</a>" for n, s in SWITCH)
    if d.get("cmp_cards"):
        cmp_body = cards_html(d["cmp_cards"])
    else:
        cmp_body = table_html(d["cmp_head"], d["cmp_rows"], d["cmp_rec"])
    check = check_html(d["check"]) if d.get("check") else ""
    # 인증 공통 안내는 '인증서'를 명시하므로, 결과 문서가 확인서인 클라우드에는 넣지 않는다(작업지시서 4 주의)
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
          <a class="btn btn--fill" href="{INQUIRY}">{t} 견적문의</a>
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
      <nav aria-label="페이지 내 이동">{anchors_html(d)}</nav>
      <div class="atab__sw"><span>인증 서비스</span>{sw}</div>
    </div>
  </div>

  <section class="cs" id="gain">
    <div class="inner">
      <div class="kh"><h2>{d["gain_title"]}</h2><p>{d["gain_lead"]}</p></div>
      {cards_html(d["gains"])}
      {note_html(d.get("gain_note"))}
    </div>
  </section>

  <section class="cs cs--bg" id="cmp">
    <div class="inner">
      <div class="kh"><h2>{d["cmp_title"]}</h2><p>{d["cmp_lead"]}</p></div>
      {cmp_body}
      {note_html(d["cmp_note"])}
      {check}
    </div>
  </section>

  <section class="cs" id="proc">
    <div class="inner">
      <div class="kh"><h2>{d["proc_title"]}</h2></div>
      <div class="proc-ban"><b>{d["proc_ban"]}</b><a href="{INQUIRY}">견적문의</a></div>
      {steps_html(d["steps"])}
      {note_html(d.get("proc_note"))}
    </div>
  </section>

  {docs_html(d["docs_title"], d["docs_lead"], d["docs_you"], DOCS_NOTE)}

  <section class="contact" id="contact">
    <div class="inner contact__inner">
      <div>
        <h2>{d["cta_title"]}</h2>
        <p>{d["cta_lead"]}</p>
        {note}
      </div>
      <div class="contact__side">
        <a class="btn btn--fill" href="{INQUIRY}">{d["cta_btn"]}</a>
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
