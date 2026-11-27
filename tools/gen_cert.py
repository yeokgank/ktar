#!/usr/bin/env python3
"""인증 상세 3종(GS·KC·클라우드) 생성기. gen_subpages.py 가 호출한다.
구성: 히어로+핵심정보 패널 → 앵커 탭 → 이점 → 비교표 → 프로세스 → 준비 서류 → 문의.
문구는 「KTAR 홈페이지 수정 작업지시서 2차 · 문구 확정본」 기준. 디자인·배치는 유지한다."""
import os, re

SP = os.path.dirname(os.path.abspath(__file__))
HEAD = open(f"{SP}/tpl_head.html", encoding="utf-8").read()
TAIL = open(f"{SP}/tpl_tail.html", encoding="utf-8").read()

SWITCH = [("GS인증", "gs"), ("KC인증", "kc"), ("클라우드서비스확인제", "cloud")]

# 하단 견적문의 CTA — 서브페이지 전 페이지 공통 (Figma 11-25 #68)
CTA_TITLE = "문의 내용을 남겨주시면<br>3영업일 이내 견적을 안내드립니다"
CTA_LEADS = ["회사명, 담당자 연락처 및 문의 내용을 남겨주세요.",
             "세부 검토에 필요한 추가 자료는 담당자가 별도로 안내드립니다."]
CTA_NOTE = "시험·인증 목적에 따른 기술 검토부터 일정 관리 및 결과 문서 확보까지 체계적으로 진행합니다."
CTA2 = "진행 절차 보기"  # 히어로 보조 버튼 (Figma 11-25 히어로 이미지 공통)

PAGES = {
    "gs": dict(
        title="GS인증",
        # Figma 11-25 #85 히어로
        lead="소프트웨어 제품의 특성과 품질 요구사항을 검토하고, 신청자료 준비부터 시험평가 대응 및 인증서 발급까지 단계별로 관리합니다.",
        h1="GS인증,<br><em>신청 준비</em>부터<br>인증서 발급까지<br>체계적으로 진행합니다",
        facts=[("대상", "상용 소프트웨어 등 GS인증 대상 제품"),
               ("목적", "소프트웨어 제품의 품질 확보 및 객관적인 품질 입증"),
               ("평가기준", "소프트웨어 품질인증 운영에 관한 지침 및 ISO/IEC 국제표준"),
               ("인증기관", "과학기술정보통신부 지정 인증기관"),
               ("소요기간", "제품 규모, 평가 범위 및 인증기관 일정에 따라 상이"),
               ("결과문서", "GS인증서 및 시험성적서")],
        # #86 탭 (띄어쓰기는 "필요 상황 / 진행 절차"로 통일)
        tabs=[("gain", "필요 상황"), ("cmp", "등급별 비교"), ("check", "평가항목"), ("proc", "진행 절차"),
              ("docs", "준비자료"), ("contact", "견적 문의")],
        gain_title="GS인증이 필요한 여섯 가지 상황",
        gain_lead="GS인증은 소프트웨어 제품의 품질을 객관적으로 검증하는 국가 소프트웨어 품질인증 제도입니다. 공공조달, 판로 확대 및 제품 경쟁력 확보에 활용할 수 있습니다.",
        gains=[("공공기관 납품 및 조달시장 진출", "나라장터 등록 및 공공기관 대상 소프트웨어 공급을 준비하는 경우"),
               ("우선구매 및 수의계약 활용", "GS인증을 활용한 공공기관 우선구매 및 수의계약 제도 적용을 검토하는 경우"),
               ("입찰 및 발주처 요구 대응", "입찰 참가 또는 제품 납품 시 발주처에서 GS인증을 요구하는 경우"),
               ("소프트웨어 품질 입증", "제품의 기능, 성능, 신뢰성, 보안성 등 소프트웨어 품질을 객관적으로 입증하고자 하는 경우"),
               ("정부 R&amp;D 과제 성과 확보", "정부 연구개발 과제의 성과지표 또는 사업화 목표로 GS인증 획득이 필요한 경우"),
               ("제품 경쟁력 및 대외 신뢰도 확보", "소프트웨어 제품의 품질 신뢰도를 높이고 신규 고객 확보 및 판로 확대를 추진하는 경우")],
        gain_note="※ 인증에 따른 제도적 혜택은 인증 등급, 제품 유형 및 관련 제도의 적용 요건에 따라 달라질 수 있습니다.",
        # #59
        cmp_title="GS인증 등급별 평가 기준 및 주요 차이점",
        cmp_lead="GS인증은 1등급과 2등급으로 구분되며, 등급에 따라 평가 방식, 평가 비중 및 인증 기준에 차이가 있습니다. "
                 "아래 등급별 비교를 통해 주요 평가 기준과 제출서류를 확인할 수 있습니다.",
        cmp_head=["구분", "1등급", "2등급"], cmp_rec=0,
        cmp_rows=[("평가 방식", "소프트웨어 품질평가", "품질평가 및 업무적합성 평가"),
                  ("평가 비중", "품질평가 100%", "품질평가 60% + 업무적합성 평가 40%"),
                  ("평가점수 기준", "80점 이상", "합산 70점 이상"),
                  ("평가 대상", "제품설명서, 사용자취급설명서 및 실행 소프트웨어", "소프트웨어 품질 및 업무적합성"),
                  ("추가 제출서류", "해당 없음", "업무적합성 기술서")],
        cmp_note="※ 인증 취득 여부는 평가 기준 충족 및 인증기관의 심의 결과에 따라 결정됩니다.<br>"
                 "※ 등급별 신청 가능 여부는 인증기관에 따라 확인이 필요합니다.",
        # #60 — 56개/32개 숫자 카드 삭제, 평가 체계도 + 평가 대상별 점검항목 표
        check=dict(
            title="GS인증 1등급 사전 준비 및 점검항목",
            lead="GS인증 1등급 취득을 위해 제품 관련 문서와 실행 소프트웨어의 품질 요구사항을 사전에 점검하고 준비해야 합니다.",
            map_title="GS인증 1등급 평가 체계",
            map_top="GS인증 품질평가",
            map_targets=[("제품설명서", False), ("사용자취급설명서", False), ("실행 소프트웨어", True)],
            map_traits_title="8대 소프트웨어 품질특성",
            map_traits=["기능적합성", "성능효율성", "호환성", "사용성", "신뢰성", "보안성", "유지보수성", "이식성"],
            table_title="평가 대상별 주요 점검항목",
            head=["평가 대상", "주요 점검 내용"],
            rows=[("제품설명서", "제품 식별정보, 공급자 정보, 주요 기능, 성능, 운영환경 등"),
                  ("사용자취급설명서", "설치 및 사용방법, 기능별 설명, 문서의 정확성 및 완전성 등"),
                  ("실행 소프트웨어", "기능 구현, 처리 성능, 시스템 안정성, 접근통제, 오류 대응 등")],
            note="※ 과학기술정보통신부 고시 「소프트웨어 품질인증 운영에 관한 지침」을 기반으로 평가 체계를 재구성한 자료입니다.<br>"
                 "※ 세부 점검항목 및 적용 기준은 소프트웨어의 유형과 특성에 따라 달라질 수 있습니다."),
        # #61
        proc_title="인증 상담부터 GS인증서 발급까지,<br>체계적으로 진행합니다",
        proc_ban="제품 정보와 인증 목적을 남겨주시면 인증 요건 및 진행 절차를 안내드립니다.",
        steps=[("문의 접수", "소프트웨어 제품 정보, 인증 목적 및 희망 인증등급을 확인합니다."),
               ("대상 제품 검토", "제품의 기술적 특성, 소프트웨어 규모 및 기능 범위를 검토합니다."),
               ("접수 서류 안내·검토", "제품설명서 및 사용자취급설명서 등 인증 신청에 필요한 제출자료를 안내하고 검토합니다."),
               ("인증 접수 및 일정 조율", "지정 인증기관의 신청 절차에 따라 접수를 진행하고 시험 일정 및 보완 요청사항을 관리합니다."),
               ("결함 분석 및 대응", "결함보고서를 분석하고 개선 방향, 문서 보완사항 및 평가 진행 현황을 관리합니다."),
               ("GS인증서 발급", "지정 인증기관의 심의를 거쳐 인증이 확정되면 GS인증서 및 시험성적서가 발급됩니다.")],
        proc_note="※ 인증 진행 기간은 제품 규모, 결함 보완 소요기간 및 인증기관의 평가 일정에 따라 달라질 수 있습니다.<br>"
                  "※ 품질평가, 인증 심의 및 GS인증서 발급은 지정 인증기관에서 수행합니다.",
        # #62
        docs_title="GS인증 신청 시 준비자료",
        docs_leads=["신청에 필요한 자료는 제품의 특성 및 인증기관에 따라 달라질 수 있습니다.",
                    "현재 보유 중인 자료를 공유해 주시면 필요한 제출서류와 준비사항을 안내드립니다."],
        docs_note="보안이 필요한 기술자료는 담당자 안내에 따라 별도로 전달해 주세요.",
        docs_you=[("실행 소프트웨어", "설치파일, 실행파일 또는 접속 정보 등"),
                  ("제품설명서", "제품명, 버전, 주요 기능 및 제품 특성 등"),
                  ("사용자취급설명서", "설치방법, 기능별 사용방법 및 운영 안내 등"),
                  ("시험환경 정보", "운영체제(OS), DB, 브라우저 및 시스템 구성 등"),
                  ("신청 기업 기본정보", "회사명, 사업자등록증 및 신청 관련 정보")],
        cta_btn="GS인증 문의하기",
    ),
    "kc": dict(
        title="KC인증",
        # #83 히어로
        lead="KC는 관련 법령에서 정한 대상 제품에 적용되는 의무 안전관리 및 적합성평가 제도입니다. "
             "제품별 적용 제도와 요구사항을 검토하고, 시험·인증에 필요한 절차와 일정을 체계적으로 관리합니다.",
        h1="KC인증,<br><em>적용 요건 검토</em>부터<br>의무절차 이행까지 체계적으로 진행합니다",
        facts=[("대상", "관련 법령에 따른 안전관리 및 적합성평가 대상 제품"),
               ("목적", "제품 안전성 및 전자파·무선 관련 법적 요구사항 충족"),
               ("적용제도", "안전인증·안전확인·공급자적합성확인 및 방송통신기자재 적합성평가 등"),
               ("수행주체", "적용 제도에 따른 시험·인증기관 또는 제조·수입업자 등"),
               ("소요기간", "제품 유형, 시험항목 및 평가 일정에 따라 상이"),
               ("사후관리", "제품 변경에 따른 변경신고 및 추가 시험 등 해당 의무 확인")],
        # #84
        tabs=[("gain", "필요 상황"), ("cmp", "제도별 비교"), ("proc", "진행 절차"), ("docs", "준비자료"), ("contact", "견적 문의")],
        # #73
        gain_title="KC인증이 필요한 주요 상황",
        gain_lead="KC 적용 대상 제품은 관련 법령에 따른 인증·확인·등록 등 의무 절차를 이행해야 합니다. "
                  "제품의 유형과 특성에 따라 적용 제도 및 요구사항이 달라집니다.",
        gains=[("국내 제조 제품을 출시할 때", "전기용품, 생활용품, 어린이제품 등 국내 제조 제품의 출고 전 안전관리 요건 확인"),
               ("해외 제품을 수입할 때", "해외 제조 제품의 국내 안전기준 적합 여부 및 통관에 필요한 인증 요건 확인"),
               ("제품을 판매·유통할 때", "온·오프라인 판매에 필요한 KC 관련 증빙서류 및 제품 표시사항 확인"),
               ("기존 제품의 사양을 변경할 때", "인증 제품의 주요 부품, 구조 및 모델 변경에 따른 추가 시험 또는 변경 절차 확인"),
               ("무선·통신 제품을 출시할 때", "Wi-Fi, Bluetooth 등 무선 기능과 전자파 관련 방송통신기자재 적합성평가 요건 확인"),
               ("R&amp;D 시제품을 상용화할 때", "연구개발 제품의 양산 전 적용 안전기준, 시험항목 및 설계 보완사항 확인")],
        gain_note="※ KC 적용 대상 및 세부 이행 절차는 제품 유형, 용도, 사양 및 관련 법령에 따라 달라질 수 있습니다.",
        # #74
        cmp_title="KC 안전관리 제도별 주요 차이점",
        cmp_lead="전기용품의 안전관리 제도는 관련 법령에 따라 안전인증, 안전확인, 공급자적합성확인으로 구분되며, "
                 "적용 대상에 따라 제품시험 및 안전관리 절차가 달라집니다.",
        cmp_head=["비교 항목", "안전인증대상", "안전확인대상", "공급자적합성확인대상"], cmp_rec=0,
        cmp_rows=[("적용 대상", "제품시험과 공장심사를 통해 화재·감전 등의 위해를 방지할 수 있는 전기용품",
                   "지정기관의 제품시험을 통해 화재·감전 등의 위해를 방지할 수 있는 전기용품",
                   "제조업자 또는 수입업자의 자체시험이나 제3자 의뢰시험을 통해 위해를 방지할 수 있는 전기용품"),
                  ("제품 시험", "안전인증기관의 제품시험", "안전확인시험기관의 제품시험", "자체시험 또는 제3자 의뢰시험"),
                  ("공장 심사", "실시", "해당 없음", "해당 없음"),
                  ("이행 절차", "제품시험 및 공장심사 후 안전인증", "제품시험 후 안전확인신고", "안전기준 적합 확인 후 공급자적합성확인신고"),
                  ("결과 문서", "안전인증서", "안전확인신고 증명서", "공급자적합성확인신고 확인증명서"),
                  ("정기 검사", "2년에 1회 실시", "해당 없음", "해당 없음")],
        cmp_note="※ 본 표는 「전기용품 및 생활용품 안전관리법」 및 같은 법 시행규칙에 따른 전기용품 안전관리 제도를 기준으로 작성되었습니다.<br>"
                 "※ 제품 유형에 따라 세부 적용 요건 및 면제사항이 달라질 수 있으며, 방송통신기자재 적합성평가는 별도로 적용됩니다.",
        # #75
        proc_title="인증 상담부터 KC 의무절차 이행까지,<br>체계적으로 진행합니다",
        proc_ban="제품 정보와 주요 사양을 남겨주시면 적용 제도 및 시험·인증 견적을 안내드립니다.",
        steps=[("인증 상담", "제품명, 사용 용도, 주요 사양 및 제조·수입 정보를 확인합니다."),
               ("제도 검토 및 견적 안내", "관련 법령과 적용 제도를 검토하고 필요한 시험항목, 비용 및 일정을 안내합니다."),
               ("접수자료 준비", "신청서, 제품 사양서, 기술자료 및 시험에 필요한 시료를 준비합니다."),
               ("시험·인증 접수", "해당 시험·인증기관의 절차에 따라 신청자료를 접수하고 세부 일정을 확정합니다."),
               ("시험·심사 수행", "해당 기관에서 제품시험 및 필요한 심사를 수행하며, KTAR는 진행 일정과 보완사항을 관리합니다."),
               ("인증·신고 및 결과 확인", "적용 제도에 따른 인증, 신고, 등록 또는 적합성확인 결과를 확인하고 관련 문서와 표시사항을 안내합니다.")],
        proc_note="※ 세부 진행 절차 및 소요기간은 제품 유형, 적용 제도 및 시험·인증기관의 일정에 따라 달라질 수 있습니다.",
        # #76
        docs_title="KC인증 진행 시 준비자료",
        docs_leads=["제품의 기본정보와 기술자료를 준비해 주시면 적용 제도 및 시험·인증 요건을 보다 정확하게 검토할 수 있습니다.",
                    "최초 문의 시에는 보유 중인 자료만 전달해 주셔도 되며, 추가 제출서류와 시료 수량은 적용 제도에 따라 안내드립니다."],
        docs_note="보안이 필요한 기술자료는 담당자와 협의 후 별도로 전달해 주세요.",
        docs_you=[("제품 기본정보", "제품명, 모델명, 사용 용도, 정격 및 주요 사양"),
                  ("시험용 시료 및 제품 사진", "완제품, 구성품 및 제품 내·외부 사진 등"),
                  ("제품 기술자료", "회로도, 블록도, 주요 부품 목록 등"),
                  ("사용자 설명서 및 표시사항", "사용설명서, 제품 라벨 및 표시사항 시안 등"),
                  ("사업자등록증 및 신청서류", "사업자등록증, 제도별 신청서 및 관련 서류")],
        cta_btn="KC인증 문의하기",
    ),
    "cloud": dict(
        title="클라우드서비스확인제",
        # #81 히어로
        lead="클라우드서비스의 특성과 운영환경을 기반으로 적용 요건을 검토하고, 신청자료 준비부터 평가 대응 및 확인서 발급까지 단계별로 진행합니다.",
        h1="클라우드서비스 확인제,<br><em>신청 준비</em>부터 확인서<br>발급까지 체계적으로 진행합니다",
        cta1="견적문의",
        facts=[("대상", "IaaS·PaaS·SaaS 등 클라우드서비스"),
               ("목적", "클라우드서비스 필수 요건 충족 여부 확인"),
               ("기준", "ISO/IEC 22123-2 기반 확인 기준"),
               ("수행기관", "한국인공지능클라우드산업협회(KACI)"),
               ("결과문서", "클라우드서비스 확인서 및 검증결과서"),
               ("소요기간", "서비스 준비 현황 및 평가 일정에 따라 상이")],
        # #82
        tabs=[("gain", "필요 상황"), ("cmp", "기대효과"), ("proc", "진행 절차"), ("docs", "준비자료"), ("contact", "견적 문의")],
        # #77
        gain_title="클라우드서비스 확인서가 필요한 주요 상황",
        gain_lead="클라우드서비스의 필수 요건 충족 여부와 운영 신뢰성을 확인하고, 사업 추진 및 대외 제출에 필요한 객관적인 증빙자료로 활용할 수 있습니다.",
        gains=[("서비스 적합성을 입증해야 할 때", "클라우드서비스의 필수 기능, 제공 방식 및 운영 요건에 대한 객관적인 확인"),
               ("디지털서비스 등록을 준비할 때", "디지털서비스 심사·선정 과정에서 활용할 수 있는 서비스 관련 증빙자료 확보"),
               ("공공·민간 사업에 참여할 때", "입찰공고 및 제안요청서에서 요구하는 클라우드서비스 관련 증빙자료 확보"),
               ("신규 서비스를 상용화할 때", "개발 완료 후 클라우드서비스의 기능 구현 및 운영체계에 대한 사전점검"),
               ("정부지원사업 및 과제를 수행할 때", "사업계획서상 요구사항 충족 및 연구개발 성과 평가에 필요한 증빙자료 확보"),
               ("고객사에 신뢰성을 제시해야 할 때", "서비스 도입 검토, 계약 협의 및 영업 활동에 활용할 수 있는 제3자 확인자료 확보")],
        gain_note="※ 확인서의 제출 필요 여부 및 인정 범위는 사업별 평가 기준과 제출기관의 요구사항에 따라 달라질 수 있습니다.",
        # #78
        cmp_title="클라우드서비스 확인서 취득에 따른 기대효과",
        cmp_lead="국제표준 기반의 검증을 통해 클라우드서비스의 필수 역량을 확인하고, 서비스 운영체계 개선과 대외 신뢰도 확보에 활용할 수 있습니다.",
        cmp_cards=[("국제표준 기반 적합성 입증", "ISO/IEC 22123-2를 기반으로 클라우드서비스의 필수 요건 충족 여부 입증"),
                   ("객관적인 검증자료 확보", "확인서 및 검증결과서를 통한 서비스 특성과 검증 결과의 객관적 제시"),
                   ("대외 신뢰도 향상", "제3자 검증 결과를 활용한 고객사 및 사업 파트너의 신뢰 확보"),
                   ("서비스 운영체계 개선", "서비스 제공 방식과 자원 관리체계 점검을 통한 개선사항 파악"),
                   ("보안취약점 사전 파악", "보안취약점 점검을 통한 잠재적 보안 위험 및 보완사항 확인"),
                   ("사업 경쟁력 강화", "객관적인 서비스 검증자료를 활용한 기술제안 및 영업 경쟁력 제고")],
        cmp_note="※ 확인서의 활용 및 인정 범위는 관련 사업과 제출기관의 요구사항에 따라 달라질 수 있습니다.<br>"
                 "※ 클라우드서비스 확인제는 클라우드서비스 보안인증(CSAP)과 별개의 제도입니다.",
        # #79
        proc_title="서비스 상담부터 클라우드서비스 확인서 발급까지,<br>체계적으로 진행합니다",
        proc_ban="서비스 정보와 확인서 취득 목적을 남겨주시면 적용 요건 및 견적을 안내드립니다.",
        steps=[("서비스 상담", "클라우드서비스 유형(IaaS, PaaS, SaaS 등), 제공 현황 및 확인서 취득 목적을 확인합니다."),
               ("서비스 검토 및 견적 안내", "서비스 구성과 확인제 적용 요건을 검토하고 예상 비용 및 일정을 안내합니다."),
               ("신청자료 준비 및 접수", "신청서, 자가진단표 및 관련 기술자료를 준비하여 신청 절차를 진행합니다."),
               ("사전 검토 및 평가 준비", "KACI의 사전 검토에 따라 발표자료, 서비스 시연환경 및 평가 일정을 준비합니다."),
               ("현장평가 및 보완 대응", "전문평가단의 서비스 평가 및 보안취약점 점검에 따른 진행 현황과 보완사항을 관리합니다."),
               ("클라우드서비스 확인서 발급", "심의위원회의 심의를 거쳐 발급 기준을 충족하면 KACI에서 확인서 및 검증결과서를 발급합니다.")],
        proc_note="※ 진행 기간은 서비스 준비 현황, 보완 소요기간 및 평가 일정에 따라 달라질 수 있습니다.<br>"
                  "※ 공식 평가 및 확인서 발급은 한국인공지능클라우드산업협회(KACI)의 확인제 운영 기준에 따릅니다.",
        # #80
        docs_title="클라우드서비스 확인서 신청 시 준비자료",
        docs_leads=["최초 문의 시에는 현재 보유 중인 서비스 소개자료만 전달해 주셔도 됩니다.",
                    "신청 및 평가에 필요한 세부 제출서류는 서비스 유형과 운영환경에 따라 안내드립니다."],
        docs_note="보안이 필요한 기술자료는 담당자 안내에 따라 별도로 전달해 주세요.",
        docs_you=[("서비스 소개자료", "서비스 유형, 주요 기능 및 제공 범위 등"),
                  ("시스템 구성 및 운영자료", "시스템 구성도, 자원 관리 및 운영 현황 등"),
                  ("보안 및 관리체계 자료", "접근관리, 보안 정책, 장애·변경관리 절차 등"),
                  ("신청서 및 자가진단표", "보안취약점 점검 동의서 등 지정 양식"),
                  ("사업자등록증", "신청 기업의 사업자등록증 사본")],
        cta_btn="클라우드서비스 확인제 문의하기",
    ),
}

INQUIRY = "../index.html#inquiry"


def plain(s):
    """메타 설명용: 태그 제거."""
    return re.sub(r"<[^>]+>", "", s)


def tabs_html(tabs):
    """페이지 내 앵커 탭. tabs = [(섹션 id, 라벨), ...] — 페이지별로 고객사 지정 순서를 그대로 쓴다."""
    return "".join(f'<a href="#{i}">{n}</a>' for i, n in tabs)


def contact_html(cta_btn):
    """하단 견적문의 CTA — 서브페이지 전 페이지 공통 문구(#68), 버튼만 페이지별."""
    paras = "".join(f"<p>{x}</p>" for x in CTA_LEADS)
    return f'''<section class="contact" id="contact">
    <div class="inner contact__inner">
      <div>
        <h2>{CTA_TITLE}</h2>
        {paras}
        <p class="contact__note">{CTA_NOTE}</p>
      </div>
      <div class="contact__side">
        <a class="btn btn--fill" href="{INQUIRY}">{cta_btn}</a>
      </div>
    </div>
  </section>'''


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


def docs_html(title, leads, items, note=None):
    """준비 서류: 제목·설명은 왼쪽, 항목은 오른쪽에 세로 카드로 쌓는다(코서트 발급 프로세스 형식).
    leads 는 설명 문단 목록, note 는 작은 글씨 보조 안내(없으면 생략)."""
    lis = "".join(f'<li><span class="docs2__no">{n}</span><div><b>{a}</b><span>{b}</span></div></li>'
                  for n, (a, b) in enumerate(items, 1))
    paras = "".join(f"<p>{x}</p>" for x in leads)
    note_p = f'<p class="docs-note">{note}</p>' if note else ""
    return f'''<section class="cs cs--bg" id="docs">
    <div class="inner docs2">
      <div class="docs2__head">
        <h2>{title}</h2>
        {paras}
        {note_p}
        <a class="btn btn--fill" href="{INQUIRY}">견적문의</a>
      </div>
      <ol class="docs2__list">{lis}</ol>
    </div>
  </section>'''


def check_html(c):
    """GS 1등급 사전 준비·점검항목: 평가 체계도(품질평가 → 평가 대상 3종 → 8대 품질특성) + 점검항목 표."""
    targets = "".join(f'<li{" class=is-key" if key else ""}>{name}</li>' for name, key in c["map_targets"])
    traits = "".join(f"<li>{x}</li>" for x in c["map_traits"])
    return f'''<div class="chk" id="check">
        <div class="kh"><h2>{c["title"]}</h2><p>{c["lead"]}</p></div>
        <figure class="gsmap" aria-label="{c["map_title"]}">
          <figcaption class="gsmap__title">{c["map_title"]}</figcaption>
          <div class="gsmap__top">{c["map_top"]}</div>
          <ul class="gsmap__targets">{targets}</ul>
          <div class="gsmap__arrow" aria-hidden="true"></div>
          <div class="gsmap__traits"><b>{c["map_traits_title"]}</b><ul>{traits}</ul></div>
        </figure>
        <h3 class="chk__sub">{c["table_title"]}</h3>
        {table_html(c["head"], c["rows"], cls="cmp--chk")}
        {note_html(c["note"])}
      </div>'''


def build(slug, repo):
    d = PAGES[slug]
    t = d["title"]
    head = HEAD
    head = re.sub(r"<title>.*?</title>", f"<title>{t} | KTAR 한국시험평가원</title>", head)
    head = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{plain(d["lead"])}">', head)
    head = head.replace('<li><a href="../cert/gs.html">', '<li class="is-current"><a href="../cert/gs.html">', 1)
    head = head.replace('<link rel="stylesheet" href="../css/sub.css?v=20261127a">',
                        '<link rel="stylesheet" href="../css/sub.css?v=20261127a">\n<link rel="stylesheet" href="../css/cert.css?v=20261127a">')

    facts = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in d["facts"])
    sw = "".join(f'<a href="{s}.html"' + (' aria-current="page"' if s == slug else "") + f">{n}</a>" for n, s in SWITCH)
    if d.get("cmp_cards"):
        cmp_body = cards_html(d["cmp_cards"])
    else:
        cmp_body = table_html(d["cmp_head"], d["cmp_rows"], d["cmp_rec"])
    check = check_html(d["check"]) if d.get("check") else ""
    cta1 = d.get("cta1", f"{t} 견적문의")

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
          <a class="btn btn--fill" href="{INQUIRY}">{cta1}</a>
          <a class="btn btn--line" href="#proc">{CTA2}</a>
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
      <nav aria-label="페이지 내 이동">{tabs_html(d["tabs"])}</nav>
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

  {docs_html(d["docs_title"], d["docs_leads"], d["docs_you"], d.get("docs_note"))}

  {contact_html(d["cta_btn"])}
</main>'''
    path = f"{repo}/cert/{slug}.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + main + TAIL)
    return path


def build_all(repo):
    for slug in PAGES:
        print("wrote", build(slug, repo))
