# 헤리티지 금융지사 홈페이지 — 작업 규칙

신한라이프 헤리티지 금융지사의 채용·소개용 정적 사이트입니다.
빌드 과정이 없으며, `index.html` 하나에 HTML·CSS·JS가 모두 들어 있습니다.

## 구조

```
index.html       # 사이트 전체
images/          # 이미지 37장
```

## 반드시 지킬 것

- **줄바꿈은 CRLF**입니다. 파일을 다시 쓸 때 LF로 바꾸지 마세요.
- **이미지를 base64로 HTML에 넣지 마세요.** 반드시 `images/` 폴더에 파일로 두고
  `<img src="images/파일명.jpg">` 로 참조합니다. (예전에 base64로 넣어 3MB까지 커진 이력이 있습니다)
- 모달 안의 이미지에는 `loading="lazy" decoding="async"` 를 유지합니다.
  단, 구성원 프로필 사진(`member-*`)은 제외합니다.
- 수정은 **요청받은 부분만** 최소 범위로 합니다. 디자인 톤이나 레이아웃을 임의로 바꾸지 마세요.

## 이미지 이름 규칙

| 접두어 | 섹션 |
|---|---|
| `member-1` ~ `member-5` | 구성원 프로필 |
| `competitive-*` | 헤리티지 경쟁력 |
| `sales-support-*` | 영업지원 |
| `training-*` | 육성시스템 |
| `income-*` | 소득비전 |
| `promotion-*` | 프로모션 |
| `career-path-*` | Career Path |
| `welfare-*` | 복지제도 |

HTML에 나타나는 순서 = 모달에서 보이는 순서입니다.
"소득비전 2번째 이미지" 같은 요청은 `income-2`가 아니라 **HTML상의 두 번째 img 태그**를 의미할 수 있으니,
순서를 바꾸는 작업이면 어떤 파일을 가리키는지 PR 설명에 명시하세요.

## 폼과 백엔드

- 문의 폼(`inquiryForm`) → Supabase `inquiries` 테이블
- 지원서 폼(`applyForm`) → Supabase `recruits` 테이블
- 기존 Google Apps Script 전송(`GAS_URL`)도 함께 유지되고 있습니다. 임의로 제거하지 마세요.

`SUPABASE_KEY`는 publishable(공개용) 키라 코드에 있어도 됩니다.
`service_role` / `secret_` 로 시작하는 키는 **절대 코드나 저장소에 넣지 마세요.**

## 디자인 톤

- 배경 다크(`#0a0a0a` 계열), 포인트 골드(`#b8975a`)
- 제목 영문: Montserrat / Cormorant Garamond, 본문 한글: Noto Sans KR
- 모바일 대응이 중요합니다. 가로 스크롤이 생기지 않도록 유지하세요.
