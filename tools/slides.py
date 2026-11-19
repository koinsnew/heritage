"""'영업의 새로운 기준' 6개 메뉴용 슬라이드 생성기.

홍보영상(헤리티지 CIS) 자막 내용을 홈페이지와 같은 다크·골드 테마의 이미지로 만든다.
슬라이드마다 PC용 가로(1600x900)와 모바일용 세로(1080x1350) 두 장이 나온다.

사용:  python3 tools/slides.py            (images/ 폴더에 저장)
필요:  pip install playwright  (Chromium 필요), Google Fonts 접속
"""
import asyncio
import os
import sys

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;height:100%}
body{background:#0a0a0a;color:#fff;font-family:'Noto Sans KR',sans-serif;position:relative;overflow:hidden;word-break:keep-all}
body::before{content:'';position:absolute;inset:0;background:
  radial-gradient(ellipse at 82% 12%, rgba(184,151,90,.17), transparent 58%),
  linear-gradient(rgba(184,151,90,.045) 1px, transparent 1px),
  linear-gradient(90deg, rgba(184,151,90,.045) 1px, transparent 1px);
  background-size:auto, 80px 80px, 80px 80px}
body.wide{--pad:80px;--t:66px;--b:40px;--s:30px;--gap:34px;--num:290px}
body.tall{--pad:72px;--t:66px;--b:42px;--s:34px;--gap:30px;--num:270px}
main{position:absolute;inset:0;padding:var(--pad);padding-bottom:calc(var(--pad)*1.15);display:flex;flex-direction:column}
h1{font-size:var(--t);font-weight:700;line-height:1.28;letter-spacing:-.01em}
h1 em{font-style:normal;color:#d4b483}
h1::after{content:'';display:block;width:calc(var(--t)*1.5);height:3px;background:#b8975a;margin-top:calc(var(--t)*.38)}
.sub{font-size:var(--s);color:#bdbdbd;margin-top:calc(var(--s)*.9);line-height:1.5}
h1{flex:none;margin-bottom:22px;white-space:nowrap}
h1.two{white-space:normal;text-wrap:balance}
p,li,h3,.node small,.cell small,.row span small{text-wrap:balance}
.content{flex:1;display:flex;flex-direction:column;justify-content:center;gap:var(--gap);min-height:0}
.mark{position:absolute;right:var(--pad);bottom:calc(var(--pad)*.42);font-family:'Montserrat',sans-serif;font-weight:600;font-size:calc(var(--s)*.56);letter-spacing:.32em;color:rgba(212,180,131,.75)}
.cards{display:grid;grid-template-columns:repeat(var(--n),1fr);gap:var(--gap)}
.tall .cards{grid-template-columns:1fr}
.card{border:1px solid rgba(184,151,90,.42);background:rgba(255,255,255,.035);padding:calc(var(--b)*1.05) calc(var(--b)*1.1)}
.card h3{font-size:var(--b);font-weight:700;line-height:1.4}
.card p{font-size:var(--s);color:#c6c6c6;line-height:1.55;margin-top:.45em}
.card .k{display:block;font-family:'Cormorant Garamond',serif;font-weight:700;font-size:calc(var(--b)*2.5);line-height:1;color:#d4b483;margin-bottom:.12em}
.card .k small{font-family:'Noto Sans KR',sans-serif;font-size:.36em;font-weight:700;margin-left:.1em}
.rows{display:flex;flex-direction:column}
.row{display:grid;grid-template-columns:var(--lw) 1fr;align-items:baseline;column-gap:var(--gap);padding:calc(var(--b)*.6) 0;border-bottom:1px solid rgba(184,151,90,.28)}
.row:first-child{border-top:1px solid rgba(184,151,90,.28)}
.row b{font-size:var(--b);font-weight:700;color:#d4b483}
.row span{font-size:var(--b);font-weight:500;line-height:1.4}
.row.top b,.row.top span{color:#111}
.row.top{background:#b8975a;border-color:#b8975a;padding-left:calc(var(--b)*.6);padding-right:calc(var(--b)*.6)}
.big{display:flex;align-items:center;gap:calc(var(--gap)*2.2)}
.tall .big{flex-direction:column;align-items:flex-start;gap:var(--gap)}
.num{flex:none;font-family:'Cormorant Garamond',serif;font-weight:700;color:#d4b483;font-size:var(--num);line-height:.9;letter-spacing:-.01em}
.num small{font-size:.42em;margin-left:.04em}
.big .txt h3{font-size:calc(var(--b)*1.25);font-weight:700;line-height:1.35}
.big .txt p{font-size:var(--s);color:#c6c6c6;margin-top:.55em;line-height:1.6}
.brow{display:grid;grid-template-columns:var(--lw) 1fr;align-items:center;column-gap:var(--gap);margin-bottom:var(--gap)}
.brow:last-child{margin-bottom:0}
.brow b{font-size:var(--b);font-weight:700;color:#bdbdbd}
.brow.on b{color:#d4b483}
.bar{display:flex;gap:6px}
.bar i{font-style:normal;font-size:var(--s);font-weight:700;padding:calc(var(--s)*.75) 6px;text-align:center;background:rgba(255,255,255,.13);color:#e2e2e2;white-space:nowrap;overflow:hidden}
.bar i.fc{background:#b8975a;color:#111}
.tall .brow{grid-template-columns:1fr;row-gap:calc(var(--gap)*.5)}
.flow{display:flex;align-items:center}
.node{flex:1;border:1px solid rgba(184,151,90,.48);background:rgba(255,255,255,.035);padding:calc(var(--b)*1.05) calc(var(--b)*.6);text-align:center;font-size:var(--b);font-weight:700;line-height:1.4}
.node small{display:block;font-size:var(--s);font-weight:400;color:#c6c6c6;margin-top:.3em}
.node.on{background:#b8975a;border-color:#b8975a;color:#111}
.node.on small{color:#33270f}
.arrow{flex:none;width:calc(var(--b)*2.1);height:2px;background:#b8975a;position:relative}
.arrow::after{content:'';position:absolute;right:0;top:50%;width:calc(var(--b)*.36);height:calc(var(--b)*.36);border-top:2px solid #b8975a;border-right:2px solid #b8975a;transform:translateY(-50%) rotate(45deg)}
.tall .flow{flex-direction:column;align-items:stretch}
.tall .arrow{width:2px;height:calc(var(--b)*1.15);margin:0 auto}
.tall .arrow::after{right:50%;top:auto;bottom:0;transform:translateX(50%) rotate(135deg)}
.stairs{display:flex;align-items:flex-end;gap:14px;height:62%}
.stair{flex:1;display:flex;flex-direction:column;justify-content:flex-start;padding:calc(var(--s)*.8) calc(var(--s)*.75);height:calc(30% + var(--i)*17.5%);background:rgba(184,151,90,calc(.12 + var(--i)*.09));border-top:3px solid #b8975a}
.stair small{font-size:calc(var(--s)*.88);font-weight:700;color:#d4b483;letter-spacing:.02em}
.stair b{font-size:calc(var(--b)*.98);font-weight:700;line-height:1.3;margin-top:.15em}
.stair.top{background:#b8975a;color:#111}
.stair.top small{color:#33270f}
.tall .stairs{flex-direction:column-reverse;align-items:flex-start;height:auto;gap:16px}
.tall .stair{flex:none;height:auto;width:calc(56% + var(--i)*11%);border-top:none;border-left:4px solid #b8975a;padding:calc(var(--s)*.75) calc(var(--s)*.9)}
.chips{display:grid;grid-template-columns:repeat(2,1fr);gap:var(--gap)}
.chip{border:1px solid rgba(184,151,90,.48);background:rgba(255,255,255,.035);padding:calc(var(--b)*1.25) calc(var(--b)*.8);text-align:center;font-size:calc(var(--b)*1.18);font-weight:700;line-height:1.35}
.chip small{display:block;font-size:var(--s);font-weight:400;color:#c6c6c6;margin-top:.35em}
.tall .chips{grid-template-columns:1fr}
.note{font-size:var(--b);font-weight:500;color:#d4b483;line-height:1.5}
.row span small{display:block;font-size:var(--s);font-weight:400;color:#c6c6c6;margin-top:.25em;line-height:1.5}
.card.solo{text-align:center;padding:calc(var(--b)*1.7) calc(var(--b)*.6);display:flex;align-items:center;justify-content:center}
.card.solo h3{font-size:calc(var(--b)*1.05)}
.tall .card.solo{padding:calc(var(--b)*1.05) calc(var(--b)*.8)}
.card .tag{display:block;font-size:calc(var(--s)*.9);font-weight:700;color:#d4b483;letter-spacing:.04em;margin-bottom:.5em}
ul{list-style:none;margin-top:.5em}
li{font-size:var(--s);color:#d0d0d0;line-height:1.5;padding-left:.95em;position:relative;margin-top:.3em}
li::before{content:'';position:absolute;left:0;top:.62em;width:.34em;height:.34em;background:#b8975a}
.photos{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.photos img{width:100%;aspect-ratio:1.3;object-fit:cover;display:block;border:1px solid rgba(184,151,90,.42)}
.tall .photos img{aspect-ratio:.86}
.lead{font-size:var(--b);font-weight:500;line-height:1.6}
.lead em{font-style:normal;color:#d4b483}
.grid{display:grid;grid-template-columns:repeat(var(--n),1fr);gap:calc(var(--gap)*.6)}
.tall .grid{grid-template-columns:repeat(var(--nt),1fr)}
.cell{border:1px solid rgba(184,151,90,.34);background:rgba(255,255,255,.035);padding:calc(var(--b)*.75) 8px;text-align:center;font-size:calc(var(--b)*.88);font-weight:700;line-height:1.3}
.cell.hi{border-color:#b8975a;background:rgba(184,151,90,.2);color:#e3c898;padding:calc(var(--b)*1.05) 8px;font-size:var(--b)}
.cell small{display:block;font-size:calc(var(--s)*.86);font-weight:400;color:#c6c6c6;margin-top:.3em}
.cell .k{display:block;font-family:'Cormorant Garamond',serif;font-size:calc(var(--b)*1.7);line-height:1.05;color:#d4b483;margin:.1em 0}
.cell .k small{display:inline;font-family:'Noto Sans KR',sans-serif;font-size:.42em;font-weight:700;color:#d4b483;margin-left:.1em}
.split{display:grid;grid-template-columns:1fr 1fr;gap:var(--gap);align-items:stretch}
.tall .split{grid-template-columns:1fr}
.kv{display:flex;justify-content:space-between;gap:1em;font-size:var(--s);padding:.42em 0;border-bottom:1px solid rgba(255,255,255,.13);color:#d8d8d8}
.kv b{color:#d4b483;font-weight:700;white-space:nowrap}
.total{background:#b8975a;color:#111;text-align:center;padding:.55em .4em;font-size:calc(var(--b)*1.1);font-weight:700;margin-top:.7em}
.total small{display:block;font-size:calc(var(--s)*.86);font-weight:500;color:#33270f}
.exec{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;align-items:end}
.ex{border-top:3px solid #b8975a;background:rgba(184,151,90,calc(.1 + var(--i)*.07));padding:calc(var(--s)*.8) calc(var(--s)*.7)}
.ex small{font-size:calc(var(--s)*.72);font-weight:700;letter-spacing:.14em;color:#d4b483;font-family:'Montserrat',sans-serif}
.ex h3{font-size:calc(var(--b)*1.05);font-weight:700;margin-top:.1em}
.ex .m{font-size:var(--s);font-weight:700;color:#e3c898;padding-bottom:.45em;border-bottom:1px solid rgba(255,255,255,.2)}
.ex li{font-size:calc(var(--s)*.84);margin-top:.28em}
.wide .ex{padding-bottom:calc(var(--s)*(.9 + var(--i)*1.1))}
.tall .exec{grid-template-columns:1fr;gap:12px}
.tall .ex{border-top:none;border-left:4px solid #b8975a;display:grid;grid-template-columns:210px 1fr;column-gap:20px;align-items:center;padding:16px 20px}
.tall .ex .m{border:none;padding:0}
.tall .ex ul{grid-column:2;grid-row:1 / span 3;margin:0;display:grid;grid-template-columns:1fr 1fr;column-gap:14px}
.tall .ex li{font-size:calc(var(--s)*.86);margin-top:.12em}
.tri{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--gap)}
.tall .tri{grid-template-columns:1fr;gap:calc(var(--gap)*.5)}
.tall .tri .cell{display:grid;grid-template-columns:1fr 1fr;align-items:center;text-align:left;padding:14px 22px}
.tall .tri .cell small{grid-column:1 / -1}
.tall .tri .cell .k{text-align:right}
.tall .tri .cell .k small{grid-column:auto}
.chip .k{display:block;font-size:calc(var(--b)*1.9);font-weight:700;color:#d4b483;line-height:1.2}
.chip .tag{display:block;font-size:var(--s);color:#d4b483;font-weight:700;margin-bottom:.3em}
.fine{font-size:calc(var(--s)*.9);color:#a9a9a9;line-height:1.6;border-top:1px solid rgba(255,255,255,.16);padding-top:.8em}
.seg{display:flex;gap:6px;margin-top:.5em}
.seg i{flex:1;height:calc(var(--s)*.62);background:#b8975a}
.segrow{margin-bottom:var(--gap)}
.segrow h3{font-size:var(--b);font-weight:700;display:flex;justify-content:space-between;align-items:baseline}
.segrow h3 small{font-size:var(--s);font-weight:400;color:#bdbdbd}
"""

FINE = '<p class="fine">지급 기준은 회사 규정에 따르고, 실적에 따라 달라집니다. 소득을 보장한다는 뜻은 아닙니다.</p>'


def ul(items):
    return '<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'


def photo(name):
    import base64
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', name)
    with open(path, 'rb') as f:   # 렌더링용 임시 HTML에만 쓰입니다(사이트 HTML에는 넣지 않음)
        return 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode()


def cards(items, n=None):
    """items: (제목, 설명 문자열 또는 목록[, 큰 숫자[, 위쪽 꼬리표]])"""
    n = n or len(items)
    out = f'<div class="cards" style="--n:{n}">'
    for it in items:
        k = f'<span class="k">{it[2]}</span>' if len(it) > 2 and it[2] else ''
        tag = f'<span class="tag">{it[3]}</span>' if len(it) > 3 else ''
        body = it[1]
        p = (ul(body) if isinstance(body, list) else f'<p>{body}</p>') if body else ''
        solo = '' if (p or k) else ' solo'
        out += f'<div class="card{solo}">{tag}{k}<h3>{it[0]}</h3>{p}</div>'
    return out + '</div>'


def rows(items, lw_wide='200px', lw_tall='190px', top_last=False):
    out = f'<div class="rows" style="--lw:{lw_wide}" data-lw-tall="{lw_tall}">'
    for i, (a, b) in enumerate(items):
        cls = ' top' if top_last and i == len(items) - 1 else ''
        out += f'<div class="row{cls}"><b>{a}</b><span>{b}</span></div>'
    return out + '</div>'


def flow(nodes):
    out = '<div class="flow">'
    for i, n in enumerate(nodes):
        on = ' on' if n.startswith('*') else ''
        out += f'<div class="node{on}">{n.lstrip("*")}</div>'
        if i < len(nodes) - 1:
            out += '<div class="arrow"></div>'
    return out + '</div>'


def stairs(items):
    out = '<div class="stairs">'
    for i, (a, b) in enumerate(items):
        top = ' top' if i == len(items) - 1 else ''
        out += f'<div class="stair{top}" style="--i:{i}"><small>{a}</small><b>{b}</b></div>'
    return out + '</div>'


# (파일 접두어, [(제목, 본문 HTML, 대체 텍스트[, {'wide': CSS 변수, 'tall': CSS 변수}])])
# 홍보영상 내용 + 기존 홈페이지 슬라이드에만 있던 내용을 합친 것입니다.
SLIDES = {
    'sales-support': [
        ('헤리티지는 지사가 <em>직접 DB</em>를 만듭니다',
         cards([('재무설계 DB', ''), ('보장분석 DB', ''), ('숨은 보험금 찾기 DB', '')]) +
         '<div class="big"><div class="num" style="font-size:calc(var(--num)*.6)">0<small>원</small></div><div class="txt"><h3>DB 구매 비용 부담이 없습니다</h3><p>계약이 되면 나누는 방식이라 바로 쓰실 수 있습니다.<br>DB 배분과 진행 관리는 \'데이터 PRO\' 프로그램으로 합니다.</p></div></div>',
         '헤리티지는 지사가 직접 DB를 만들어 정기적으로 지원합니다. 재무설계 DB, 보장분석 DB, 숨은 보험금 찾기 DB. DB 구매 비용 부담이 없고, 계약이 되면 나누는 방식이라 바로 쓸 수 있습니다. DB 배분과 진행 관리는 데이터 PRO 프로그램으로 합니다.',
         {'tall': '--gap:24px'}),
        ('선배와 함께 가는 <em>조인트 워크</em>',
         flow(['미팅 준비', '상담 동행', '*계약까지']) +
         cards([('A to Z 밀착 동행', '경험 많은 전담 관리자와 선배가 미팅 준비부터 현장 동행, 계약 체결까지 함께합니다.'),
                ('합리적인 수익 공유', '발생한 수당을 투명하게 나누는 윈윈 구조입니다.'),
                ('가장 빠른 성장', '현장 선배들의 실전 노하우를 곁에서 직접 배웁니다.')]),
         '선배와 함께 가는 조인트 워크. 경험 많은 전담 관리자와 선배가 미팅 준비, 상담 동행, 계약까지 함께합니다. 발생한 수당은 투명하게 나누고, 현장 선배의 실전 노하우를 직접 배웁니다.',
         {'tall': '--gap:22px;--b:38px;--s:31px'}),
        ('<em>플랫폼 DB</em>도 준비하고 있습니다',
         cards([('군인 가족', ''), ('아파트 입주민', ''), ('육아 가정', '')]) +
         '<p class="note">신채널 차원에서 준비하고 있습니다.</p>',
         '플랫폼 DB도 준비하고 있습니다. 신채널 차원에서 군인 가족, 아파트 입주민, 육아 가정 플랫폼 DB를 준비하고 있습니다.'),
        ('상담을 돕는 <em>헤리티지 자체 프로그램</em>',
         cards([('헤리티지 보장분석', '기존 보험을 AI로 분석하고 리모델링 제안서까지 자동으로 만듭니다.', '', 'HERITAGE COVERAGE'),
                ('헤리티지 재무', '복잡한 계산 없이 클릭 한 번으로 고객 맞춤형 재무설계 포트폴리오를 만듭니다.', '', 'HERITAGE FINANCE'),
                ('헤리티지 프로', '내 발생 수수료와 유지 수수료를 실시간으로 확인합니다. 대기업 원수사도 아직 구현하지 못한 기능입니다.', '', 'HERITAGE PRO')]),
         '상담을 돕는 헤리티지 자체 프로그램. 헤리티지 보장분석은 기존 보험을 AI로 분석하고 리모델링 제안서를 자동으로 만들고, 헤리티지 재무는 클릭 한 번으로 맞춤형 재무설계 포트폴리오를 만들며, 헤리티지 프로는 발생 수수료와 유지 수수료를 실시간으로 확인합니다.',
         {'tall': '--gap:24px'}),
        ('FC <em>정착</em>을 위한 지원과 제도',
         cards([('B.M 전담 코칭', ['신인 입과 전부터 1년간 밀착 전담 코칭', '전산 · 원수사 교육', '청약 프로세스 동행 지원', '상품 라인업 · 보장분석 교육', '고객관리 프로세스 코칭'], '', '전문 관리자 지원'),
                ('FC 익월 소득 수준', '', '1,000<small>%</small>', 'FC 소득 체계'),
                ('신인 정착 지원', ['설계사 시험 합격 → 100만 원', '1차월 환산 30만 원 이상 → 100만 원', '2~6차월 환산의 100% 익월 지급'], '', '신인 정착 지원금')]) + FINE,
         'FC 정착을 위한 지원과 제도. 전문 관리자 B.M이 신인 입과 전부터 1년간 밀착 전담 코칭을 하며 전산과 원수사 교육, 청약 프로세스 동행, 상품 라인업과 보장분석 교육, 고객관리 프로세스 코칭을 지원합니다. FC 익월 소득 수준 1,000퍼센트. 신인 정착 지원은 설계사 시험 합격 시 100만 원, 1차월 환산 30만 원 이상 시 100만 원, 2에서 6차월 환산의 100퍼센트 익월 지급. 지급 기준은 회사 규정에 따르고 실적에 따라 달라집니다.',
         {'wide': '--s:26px;--b:34px;--gap:24px', 'tall': '--gap:18px;--b:36px;--s:28px;--t:60px'}),
    ],
    'training': [
        ('헤리티지의 <em>특별한</em> 육성 시스템',
         f'<div class="photos"><img src="{photo("training-photo-1.jpg")}"><img src="{photo("training-photo-2.jpg")}"><img src="{photo("training-photo-3.jpg")}"></div>'
         '<p class="lead">모든 FC를 똑같이 육성하는 것은 모순입니다.<br>헤리티지의 육성 시스템은 <em>맞춤식 교육</em>을 제공합니다.<br>AI 재무설계, AI 보장분석, 실시간 소득 관리, DB 프로그램이 성장을 돕습니다.</p>',
         '헤리티지의 특별한 육성 시스템. 교육 현장 사진 세 장. 모든 FC를 똑같이 육성하는 것은 모순입니다. 헤리티지의 육성 시스템은 맞춤식 교육을 제공하며 AI 재무설계, AI 보장분석, 실시간 소득 관리, DB 프로그램이 성장을 돕습니다.',
         {'wide': '--b:32px;--gap:24px', 'tall': '--b:38px'}),
        ('신채널 본사 교육 · <em>5일 과정</em>',
         rows([('1일차', '회사와 시장'), ('2일차', '세일즈 프로세스'), ('3일차', '시장 개발 · 목표 설정'),
               ('4일차', 'DB 시장 · AI 보장분석'), ('5일차', '상품 라인업 · 실습')]),
         '신채널 본사 교육 5일 과정. 1일차 회사와 시장, 2일차 세일즈 프로세스, 3일차 시장 개발과 목표 설정, 4일차 DB 시장과 AI 보장분석, 5일차 상품 라인업과 실습.'),
        ('지사 신입 교육 · <em>4주 과정</em>',
         rows([('1주차', '회사 소개 · 수당 체계<small>회사·지사 소개, 수당 체계, 업계 비전 · 생명·손해보험 설계사 시험 준비 시작</small>'),
               ('2주차', '보험 기초 · 지인 영업 · DB 영업<small>AP·RP·TA 영업 기초, 퍼미션 DB·이관 DB, \'데이터 PRO\'·\'비즈메모\' 사용법 · 생명보험 설계사 시험</small>'),
               ('3주차', '전산 · 보장분석 · 재무설계<small>본사 \'카스\', 지사 \'헤리티지 프로\'·\'헤리티지 재무\', \'오케이 마이보험\', \'베스트카 다이렉트 앱\' · 손해보험 설계사 시험</small>'),
               ('4주차', 'RP · 거절 처리<small>십자 RP, 달러종 RP, 변액 RP · TA 거절 처리, 미팅 거절 처리</small>'),
               ('수료', 'RP · 거절 처리 실전 테스트 → 수료')], lw_wide='150px', lw_tall='130px', top_last=True),
         '지사 신입 교육 4주 과정. 1주차 회사와 지사 소개, 수당 체계, 업계 비전과 설계사 시험 준비. 2주차 보험 기초, 지인 영업, DB 영업, 데이터 PRO와 비즈메모 사용법, 생명보험 설계사 시험. 3주차 전산 교육(카스, 헤리티지 프로, 지사 클라우드, 베스트카 다이렉트 앱), 보장분석(AI 자동 보장분석, 오케이 마이보험), 재무설계(헤리티지 재무), 손해보험 설계사 시험. 4주차 RP 교육(십자 RP, 달러종 RP, 변액 RP)과 거절 처리 교육. RP와 거절 처리 실전 테스트 후 수료.',
         {'wide': '--b:32px;--s:24px;--t:58px', 'tall': '--b:40px;--s:30px;--t:60px'}),
        ('교육이 끝난 뒤에도, <em>12개월</em>',
         '<div class="big"><div class="num">12<small>개월</small></div><div class="txt"><h3>담당 관리자의 밀착 관리</h3><p>교육을 마친 뒤에도 담당 관리자가 12개월 동안 곁에서 밀착 관리를 합니다.</p></div></div>',
         '교육이 끝난 뒤에도 12개월 동안 담당 관리자가 밀착 관리를 합니다.'),
        ('매일 아침 <em>Daily 교육</em>, 온라인으로도',
         rows([('매일 09:00', '원수사별 핵심 상품 · 판매 전략 교육'),
               ('매일 10:00', '실전 영업 사례 공유 · 동기부여<small>금융, 경제, 보장성 심화 학습</small>'),
               ('매주 수요일', '3-Step 전문가 커리큘럼')],
              lw_wide='270px', lw_tall='250px') +
         '<p class="note">모든 교육은 LIVE로 온라인 참여가 가능합니다.<br>이 시간만 성실히 참여해도 자연스럽게 전문가로 성장합니다.</p>',
         '매일 아침 Daily 교육. 매일 9시 원수사별 핵심 상품과 판매 전략 교육, 매일 10시 실전 영업 사례 공유와 동기부여, 금융·경제·보장성 심화 학습, 매주 수요일 3-Step 전문가 커리큘럼. 모든 교육은 LIVE로 온라인 참여가 가능합니다.',
         {'tall': '--b:38px;--s:30px'}),
        ('매주 수요일 · <em>3-Step</em> 전문가 커리큘럼',
         cards([('종합 재무설계 전문가', '금리, 채권, 주식, 펀드 기초부터 재무 컨설팅까지.', '', '1단계'),
                ('보장분석 전문가', 'AI 분석 시스템 활용, 복잡한 약관 해석과 최적의 보험금 수령 전략.', '', '2단계'),
                ('WM 영업 전문가', 'VIP 미팅 전략, 단체 세미나 스킬, 법인과 자산가 세금 컨설팅.', '', '3단계')]) +
         '<p class="note">여러분을 최고 수준의 \'전문 컨설턴트\'로 만들어 드립니다.</p>',
         '매주 수요일 3-Step 전문가 커리큘럼. 1단계 종합 재무설계 전문가, 2단계 보장분석 전문가, 3단계 WM 영업 전문가.'),
        ('<em>나에게 맞는</em> 영업 시장을 찾아 집중 육성',
         '<div class="grid" style="--n:3;--nt:3"><div class="cell hi">이관 고객</div><div class="cell hi">DB 고객</div><div class="cell hi">Joint Work</div></div>'
         '<div class="grid" style="--n:4;--nt:2"><div class="cell">주변 인맥</div><div class="cell">소개 마케팅</div><div class="cell">동호회 시장</div><div class="cell">SNS 시장</div>'
         '<div class="cell">재테크 박람회</div><div class="cell">제휴 마케팅</div><div class="cell">세미나 시장</div><div class="cell">개척 시장</div></div>',
         '나에게 맞는 영업 시장과 방향을 찾아 집중 육성합니다. 이관 고객, DB 고객, Joint Work, 주변 인맥, 소개 마케팅, 동호회 시장, SNS 시장, 재테크 박람회, 제휴 마케팅, 세미나 시장, 개척 시장.',
         {'tall': '--b:36px'}),
    ],
    'income': [
        ('수익 배분, <em>무엇이</em> 다른가',
         '<div class="bars" style="--lw:130px">'
         '<div class="brow"><b>일반</b><div class="bar"><i style="flex:24">회사 몫</i><i style="flex:24">지사 몫</i><i style="flex:52">남은 게 FC 몫</i></div></div>'
         '<div class="brow on"><b>직영</b><div class="bar"><i style="flex:17">회사 몫</i><i class="fc" style="flex:83">FC 몫 80~88%</i></div></div>'
         '</div><p class="note">헤리티지는 한국보험금융 본사 직영이라, 중간에서 떼는 몫을 줄였습니다.</p>',
         '수익 배분 비교. 일반 지사는 회사 몫과 지사 몫을 떼고 남은 것이 FC 몫입니다. 직영인 헤리티지는 회사 몫과 FC 몫으로 나뉘며 FC 몫이 80에서 88퍼센트입니다.'),
        ('한국보험금융 <em>수수료 지급 비율</em>',
         '<div class="big"><div class="num">92.85<small>%</small></div><div class="txt"><h3>2025년 공시 자료 기준</h3><p>회사가 받은 수수료 가운데 설계사에게 지급한 비율입니다.</p></div></div>',
         '한국보험금융 수수료 지급 비율 92.85퍼센트, 2025년 공시 자료 기준.'),
        ('많이 줘도, <em>중간</em>에서 가져가면',
         flow(['회사 수수료', '중간 몫<small>최소화</small>', '*FC 몫']) +
         '<p class="note">한 건을 계약해도 최대한 많이 가져가실 수 있게 했습니다.</p>'
         '<p class="fine" style="font-size:var(--s);color:#c6c6c6">환수도 마찬가지입니다. 회사가 더 많이 환수해 가는 방식이 아니라, 원수사 환수율을 그대로 적용합니다.</p>',
         '회사에서 수수료를 많이 줘도 중간에서 가져가면 의미가 없습니다. 헤리티지는 중간 몫을 최소화해 FC 몫을 키웠고, 환수도 원수사 환수율을 그대로 적용합니다.'),
        ('직영은 본사가 <em>직접 지급</em>합니다',
         flow(['한국보험금융 본사', '*FC']) +
         '<p class="note">약속된 날짜에, 정확하게.</p>'
         '<p class="sub" style="margin-top:0">땀 흘려 번 수수료는 지켜져야 합니다.</p>',
         '직영은 한국보험금융 본사가 FC에게 수수료를 직접 지급합니다. 약속된 날짜에 정확하게.'),
        ('수수료 제도가 바뀝니다 · <em>분급</em>',
         '<div><div class="segrow"><h3>4년 분급 <small>2027년부터</small></h3><div class="seg"><i></i><i></i><i></i><i></i></div></div>'
         '<div class="segrow" style="margin-bottom:0"><h3>7년 분급 <small>2029년부터</small></h3><div class="seg"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div></div></div>'
         '<p class="note">오늘 계약한 수수료가 몇 년에 걸쳐 나뉘어 들어옵니다.<br>그래서 끝까지 줄 수 있는 튼튼한 GA가 중요합니다.</p>',
         '수수료 제도가 분급으로 바뀝니다. 2027년부터 4년 분급, 2029년부터 7년 분급. 수수료가 몇 년에 걸쳐 나뉘어 들어오므로 끝까지 줄 수 있는 튼튼한 GA가 중요합니다.'),
    ],
    'promotion': [
        ('처음 시작하는 분을 위한 <em>루키 보너스</em>',
         cards([('등록 축하금', '등록하시면 드립니다.', '100<small>만 원</small>'),
                ('첫 달 추가 지급', '첫 달 환산 실적이 30만 원 이상이면.', '+100<small>만 원</small>'),
                ('2~6차월 활동 지원비', '환산 실적의 100%를 지원합니다.', '100<small>%</small>')]) + FINE,
         '루키 보너스. 등록 축하금 100만 원, 첫 달 환산 실적 30만 원 이상이면 100만 원 추가, 2에서 6차월에는 환산 실적의 100퍼센트를 활동 지원비로 지원합니다. 지급 기준은 회사 규정에 따르고 실적에 따라 달라지며 소득을 보장한다는 뜻은 아닙니다.',
         {'tall': '--t:58px;--gap:18px;--b:36px;--s:29px'}),
        ('루키 보너스 · <em>대상과 예시</em>',
         '<div class="split"><div class="card"><span class="tag">무경력 신인 대상</span><h3>3년 내 무경력 또는 3년 내 신계약 없음</h3>'
         + ul(['등록 축하금: 100만 원', '추가 인센티브: 등록 당월 환산 30만 원 이상 시 100만 원', '등록 2~6차월 활동 지원: 환산 × 100%']) +
         '</div><div class="card"><span class="tag">예시 · 손보 기준</span><h3>등록 당월 환산 30만 원</h3>'
         '<div style="margin-top:.6em"><div class="kv">등록 축하금<b>100만 원</b></div><div class="kv">등록 인센티브<b>100만 원</b></div>'
         '<div class="kv">수수료<b>250만 원</b></div><div class="kv">13회 유지 · 시책비<b>300만 원</b></div></div>'
         '<div class="total">총 750만 원<small>익월 450만 원 + 13회차 300만 원</small></div></div></div>' + FINE,
         '루키 보너스 대상과 예시. 무경력 신인 대상으로 기준은 3년 내 무경력 또는 3년 내 신계약 없음. 등록 축하금 100만 원, 등록 당월 환산 30만 원 이상 시 추가 인센티브 100만 원, 등록 2에서 6차월 활동 지원 환산의 100퍼센트. 손보 기준 등록 당월 환산 30만 원 예시: 등록 축하금 100만 원, 등록 인센티브 100만 원, 수수료 250만 원, 13회 유지·시책비 300만 원, 총 750만 원(익월 450만 원, 13회차 300만 원). 지급 기준은 회사 규정에 따르고 실적에 따라 달라집니다.',
         {'wide': '--b:30px;--s:23px;--t:54px;--gap:18px', 'tall': '--t:58px;--b:38px;--s:30px;--gap:20px'}),
        ('<em>장기 근속</em> 성장 지원금',
         flow(['1~12차월<small>1년 동안 체결한 총 보험료의 100%를 적립</small>', '*15차월부터<small>매달 차근차근 지급</small>']) +
         '<p class="note">단발성 이벤트가 아닙니다. 근속하시는 동안 계속 이어집니다.</p>' + FINE,
         '장기 근속 성장 지원금. 1년 동안 체결한 총 보험료의 100퍼센트를 적립해 15차월부터 매달 지급하며, 근속하는 동안 계속 이어집니다. 지급 기준은 회사 규정에 따르고 실적에 따라 달라집니다.'),
        ('<em>리크루팅</em> 보너스',
         '<div class="big"><div class="num" style="font-size:calc(var(--num)*.72)">20<small>%</small></div><div class="txt"><h3>내가 소개한 FC 환산 실적의 20%를 3년간</h3><p>영업 수입 옆에 세우는 또 하나의 기둥입니다.</p></div></div>'
         '<div class="tri"><div class="cell">입사 FC 1명<span class="k">10<small>만 원</small></span><small>환산 50만 원 기준</small></div>'
         '<div class="cell">입사 FC 5명<span class="k">50<small>만 원</small></span><small>각 환산 50만 원 기준</small></div>'
         '<div class="cell">입사 FC 10명<span class="k">100<small>만 원</small></span><small>각 환산 50만 원 기준</small></div></div>' + FINE,
         '리크루팅 보너스. 내가 소개한 FC 환산 실적의 20퍼센트를 3년간 드립니다. 환산 50만 원 기준으로 입사 FC 1명이면 10만 원, 5명이면 50만 원, 10명이면 100만 원. 지급 기준은 회사 규정에 따르고 실적에 따라 달라집니다.',
         {'wide': '--gap:24px;--b:36px;--s:27px', 'tall': '--gap:20px;--num:230px'}),
        ('잘하는 분은 <em>확실하게</em> 인정합니다 · 월간 지사 MVP',
         cards([('투명한 순위 공개', '매월 환산 실적, 총 수수료, 계약 건수 순위를 지사 안에서 투명하게 공개합니다.'),
                ('이달의 MVP', '지사 종합 실적 1위에게 소정의 선물과 MVP의 프라이드를 드립니다.'),
                ('함께 성장', '선의의 경쟁과 서로의 인정으로 조직 전체가 함께 성장합니다.')]),
         '월간 지사 MVP. 매월 환산 실적, 총 수수료, 계약 건수 순위를 지사 안에서 투명하게 공개하고, 지사 종합 실적 1위에게 소정의 선물과 MVP의 프라이드를 드립니다.',
         {'tall': '--t:58px'}),
        ('<em>천만 클럽</em> · <em>명인 클럽</em>',
         cards([('천만 클럽', ['대상: 익월 소득 1천만 원 이상 달성', '혜택: 천만 클럽 식사 초대'], '', '성실한 FC를 위한 우대'),
                ('명인 클럽', ['대상: 환산 100만 원 이상 또는 3W 4주 달성', '혜택: 이달의 우수사원(명인) 상장 수여, 명인 클럽 식사 초대'], '', '고능률 FC를 위한 우대')], n=2),
         '천만 클럽과 명인 클럽. 천만 클럽은 익월 소득 1천만 원 이상 달성자를 식사에 초대합니다. 명인 클럽은 환산 100만 원 이상 또는 3W 4주 달성자에게 이달의 우수사원 상장을 수여하고 식사에 초대합니다.'),
        ('한국보험금융 <em>직영 연도대상</em>',
         '<div class="tri"><div class="cell hi">챔피언 1위<span class="k">1,000<small>만 원</small></span></div><div class="cell hi">챔피언 2위<span class="k">500<small>만 원</small></span></div><div class="cell hi">챔피언 3위<span class="k">300<small>만 원</small></span></div></div>'
         '<div class="grid" style="--n:4;--nt:2"><div class="cell">Platinum <small style="display:inline">4~10위</small><span class="k">200<small>만 원</small></span></div><div class="cell">Gold <small style="display:inline">11~30위</small><span class="k">150<small>만 원</small></span></div>'
         '<div class="cell">Silver <small style="display:inline">31~40위</small><span class="k">100<small>만 원</small></span></div><div class="cell">Bronze <small style="display:inline">41~50위</small><span class="k">50<small>만 원</small></span></div></div>'
         '<p class="sub" style="margin-top:0">전 등급 공통: 해외여행 지원 · 상패와 상장 · 마케팅 임원 선발 우대<br>특별상(Special Award): 리크루팅, 3W 대상 10명 · 20만 원 · 상장, 상패</p>'
         '<p class="fine">평가 기간: 직전 1년 · 선발 인원: 50명(특별상 포함 총 60명) · 선발 기준: 환산월초 절대액(80점) + 리크루팅(20점) · 유지율, 불완전판매 실적 조정 적용</p>',
         '한국보험금융 직영 연도대상. 챔피언 1위 1,000만 원, 2위 500만 원, 3위 300만 원, Platinum 4에서 10위 200만 원, Gold 11에서 30위 150만 원, Silver 31에서 40위 100만 원, Bronze 41에서 50위 50만 원. 전 등급 해외여행 지원, 상패와 상장, 마케팅 임원 선발 우대. 특별상은 리크루팅과 3W 대상 10명에게 20만 원과 상장, 상패. 평가 기간 직전 1년, 선발 인원 50명(특별상 포함 총 60명), 선발 기준 환산월초 절대액 80점과 리크루팅 20점, 유지율과 불완전판매 실적 조정 적용.',
         {'wide': '--gap:20px;--b:33px;--s:24px;--t:58px', 'tall': '--gap:20px;--b:40px;--s:29px;--t:60px'}),
    ],
    'career-path': [
        ('PATH 1 · <em>관리자</em>의 길',
         stairs([('START', 'FC'), ('2명 도입', '지점장 후보자'), ('4명', '수석 지점장'), ('8명', '사업단장'), ('12명', '본부장')]) +
         '<p class="note">관리자 수수료 지급 · 관리자 전용 사원증과 명함 제공 · 관리자 공간 제공</p>',
         '관리자의 길. FC에서 시작해 2명 도입 시 지점장 후보자, 4명 수석 지점장, 8명 사업단장, 12명 본부장. 관리자 수수료 지급, 관리자 전용 사원증과 명함 제공, 관리자 공간 제공.'),
        ('PATH 2 · <em>영업 전문가</em>의 길 · 마케팅 임원',
         '<div class="exec">'
         + ''.join(f'<div class="ex" style="--i:{i}"><small>LEVEL {i+1}</small><h3>{n}</h3><div class="m">{m}</div>{ul(b)}</div>' for i, (n, m, b) in enumerate([
             ('명인', '월 100만 ↑', ['통신비 월 3만', '건강검진 A', '상조 지원']),
             ('이사', '월 200만 ↑', ['임원지원금 100만', '품위유지비 월 20만', '통신비 월 5만', '건강검진 C', '상조 지원']),
             ('상무', '월 400만 ↑', ['임원지원금 200만', '품위유지비 월 50만', '통신비 월 7만', '건강검진 C', '상조 지원']),
             ('전무', '월 800만 ↑', ['임원지원금 400만', '품위유지비 월 100만', '통신비 월 10만', '건강검진 C', '상조 지원']),
             ('부사장', '월 1,000만 ↑', ['임원지원금 1,000만', '품위유지비 월 100만', '통신비 월 10만', '건강검진 C', '상조 지원'])])) +
         '</div><p class="note">등급이 오를수록 임원 지원금, 건강검진 같은 혜택이 커집니다.</p>',
         '영업 전문가의 길, 마케팅 임원 제도. 명인(월 100만 이상): 통신비 월 3만, 건강검진 A, 상조 지원. 이사(월 200만 이상): 임원지원금 100만, 품위유지비 월 20만, 통신비 월 5만, 건강검진 C, 상조 지원. 상무(월 400만 이상): 임원지원금 200만, 품위유지비 월 50만, 통신비 월 7만, 건강검진 C, 상조 지원. 전무(월 800만 이상): 임원지원금 400만, 품위유지비 월 100만, 통신비 월 10만, 건강검진 C, 상조 지원. 부사장(월 1,000만 이상): 임원지원금 1,000만, 품위유지비 월 100만, 통신비 월 10만, 건강검진 C, 상조 지원.',
         {'wide': '--t:58px;--s:27px;--b:36px', 'tall': '--t:56px;--gap:18px;--s:31px'}),
    ],
    'welfare': [
        ('그리고, 쉴 때는 <em>쉬어야죠</em>',
         '<div class="chips"><div class="chip"><span class="tag">정기 휴가</span><span class="k">총 7일</span><small>사전 조율</small></div>'
         '<div class="chip"><span class="tag">프리데이</span><span class="k">매월 하루</span><small>사용 전날 22시까지 연락 필수</small></div></div>'
         '<p class="note">헤리티지가 보장하는 재충전 시간입니다. 건강검진과 경조사 지원까지 챙겨 드립니다.</p>',
         '복지제도. 헤리티지가 보장하는 재충전 시간. 정기 휴가 총 7일(사전 조율), 프리데이 매월 하루(사용 전날 22시까지 연락 필수). 건강검진과 경조사 지원도 있습니다.'),
        ('KMI <em>건강검진</em> 프리미엄 지원',
         cards([('A형', ['기준: 실동 인원', '월초 10만 달성 시 자기부담금 25만'], '60<small>만 원 상당</small>'),
                ('B형', ['기준: 환산 50만 ↑', '월초 50만 달성 시 자기부담금 17.5만'], '110<small>만 원 상당</small>'),
                ('C형', ['기준: 환산 100만 ↑', '월초 100만 달성 시 자기부담금 0원(전액 지원)'], '160<small>만 원 상당</small>')]) +
         '<p class="note">실적에 따라 달라지는 헬스케어 혜택입니다.</p>',
         'KMI 건강검진 프리미엄 지원. A형은 실동 인원 기준, 월초 10만 달성 시 자기부담금 25만, 검진 규모 60만 원 상당. B형은 환산 50만 이상, 월초 50만 달성 시 자기부담금 17.5만, 검진 규모 110만 원 상당. C형은 환산 100만 이상, 월초 100만 달성 시 자기부담금 0원 전액 지원, 검진 규모 160만 원 상당.',
         {'tall': '--gap:20px;--b:36px;--s:29px'}),
        ('삶의 <em>모든 순간</em>을 함께',
         cards([('경조수당', ['본인·자녀 결혼 20만 원 지급', '본인·배우자·자녀·부모 조의 20만 원 지급']),
                ('장례용품', ['20만 원 상당 현물 지원(택 1)', '일회용품 200인분 또는 유가족 고급 편의용품'])], n=2) +
         '<p class="note">직영만의 든든한 복리후생 지원 (삼우라이프 제휴)</p>'
         '<p class="fine">월 환산 30만 이상: 경조수당 + 장례용품 모두 지원 · 월 환산 30만 이하: 장례용품 단독 지원</p>',
         '삶의 모든 순간을 함께. 직영만의 복리후생 지원(삼우라이프 제휴). 경조수당은 본인·자녀 결혼 20만 원, 본인·배우자·자녀·부모 조의 20만 원 지급. 장례용품은 20만 원 상당 현물 지원으로 일회용품 200인분 또는 유가족 고급 편의용품 중 택 1. 월 환산 30만 이상은 경조수당과 장례용품 모두, 30만 이하는 장례용품 단독 지원.'),
    ],
}


def page(title, body, variant, opts=None):
    if variant == 'tall':
        import re
        body = re.sub(r'--lw:[^"]*" data-lw-tall="([^"]*)"', r'--lw:\1"', body)
    return ('<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">'
            '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Noto+Sans+KR:wght@400;500;700&family=Montserrat:wght@600&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style></head><body class="{variant}" style="{(opts or {}).get(variant, "")}"><main><h1><span>{title}</span></h1>'
            f'<div class="content">{body}</div></main><div class="mark">HERITAGE FINANCE</div></body></html>')


async def render(out_dir):
    from playwright.async_api import async_playwright
    os.makedirs(out_dir, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for variant, (w, h), suffix in (('wide', (1600, 900), ''), ('tall', (1080, 1350), '-m')):
            pg = await browser.new_page(viewport={'width': w, 'height': h})
            for prefix, slides in SLIDES.items():
                for i, sl in enumerate(slides, 1):
                    title, body = sl[0], sl[1]
                    await pg.set_content(page(title, body, variant, sl[3] if len(sl) > 3 else None), wait_until='networkidle')
                    await pg.evaluate('document.fonts.ready')
                    # 제목: 글자 크기를 줄여 한 줄에 맞추고, 그래도 길면 두 줄로 고르게 나눈다
                    tinfo = await pg.evaluate('''(()=>{const b=document.body,h=document.querySelector('h1'),sp=h.firstElementChild,
                      base=parseFloat(getComputedStyle(b).getPropertyValue('--t')),set=v=>b.style.setProperty('--t',v+'px'),
                      fits=()=>sp.getBoundingClientRect().width<=h.clientWidth+0.5;
                      let t=base;while(!fits()&&t>base*0.85){t-=1;set(t)}
                      if(fits())return '1줄 '+Math.round(t)+'px';
                      // 두 줄: ' · ' 가 있으면 그 자리에서 나눈다
                      const w=document.createTreeWalker(sp,NodeFilter.SHOW_TEXT);let last=null,n;
                      while(n=w.nextNode())if(n.nodeValue.includes(' · '))last=n;
                      if(last){const k=last.nodeValue.lastIndexOf(' · '),a=last.nodeValue.slice(0,k),c=last.nodeValue.slice(k+3);
                        const f=document.createDocumentFragment();f.append(a,document.createElement('br'),c);last.replaceWith(f);
                        t=base*0.92;set(t);while(!fits()&&t>base*0.6){t-=1;set(t)}}
                      else{h.classList.add('two');t=base*0.9;set(t);
                        const lh=()=>Math.round(sp.getClientRects().length);while(lh()>2&&t>base*0.6){t-=1;set(t)}}
                      return '2줄 '+Math.round(t)+'px'})()''')
                    # 넘치면 글자·간격을 조금씩 줄여 맞춘다
                    over = await pg.evaluate('''(()=>{const m=document.querySelector('.content'),b=document.body,
                      get=()=>m.scrollHeight-m.clientHeight;
                      for(let i=0;i<14&&get()>2;i++){const cs=getComputedStyle(b);
                        for(const v of ['--b','--s','--gap','--num'])b.style.setProperty(v,(parseFloat(cs.getPropertyValue(v))*0.96)+'px');}
                      return get()})()''')
                    path = os.path.join(out_dir, f'{prefix}-{i}{suffix}.jpg')
                    await pg.screenshot(path=path, type='jpeg', quality=86)
                    print(path, tinfo, 'OVERFLOW %dpx' % over if over > 2 else 'ok')
            await pg.close()
        await browser.close()


if __name__ == '__main__':
    asyncio.run(render(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'images')))
