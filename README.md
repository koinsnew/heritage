# 헤리티지 금융지사 홈페이지

신한라이프 헤리티지 금융지사 채용·소개 홈페이지 (정적 사이트)

## 구조

```
.
├── index.html      # 사이트 전체 (HTML + CSS + JS)
└── images/         # 이미지 37장
```

빌드 과정이 없는 순수 정적 사이트입니다. `index.html`만 열면 브라우저에서 바로 동작합니다.

## 배포

Vercel에 이 저장소를 연결하면 자동 배포됩니다.

- Framework Preset: **Other**
- Build Command: 없음 (비워둠)
- Output Directory: 없음 (비워둠)

GitHub에 커밋하면 Vercel이 자동으로 재배포합니다.

## 백엔드 (Supabase)

문의·지원서 제출 시 Supabase 테이블에 저장됩니다.

| 폼 | 테이블 |
|---|---|
| 문의하기 | `inquiries` |
| 입사지원서 | `recruits` |

`index.html` 안의 `SUPABASE_URL` / `SUPABASE_KEY` 설정을 사용합니다.
이 키는 publishable(공개용) 키라 코드에 포함되어도 안전하며,
실제 보안은 Supabase의 RLS 정책(등록만 허용, 조회 차단)이 담당합니다.

> `service_role` / `secret_` 로 시작하는 키는 절대 이 저장소에 넣지 마세요.

## 수정 방법

### 글자·내용 수정
GitHub에서 `index.html` 클릭 → 연필(✏️) 아이콘 → 수정 → Commit changes

### 이미지 교체
`images/` 폴더에서 같은 파일명으로 새 이미지를 업로드하면 교체됩니다.
파일명을 바꿀 경우 `index.html` 안의 경로도 함께 수정해야 합니다.

### 이미지 파일명 규칙

| 파일 | 위치 |
|---|---|
| `member-1` ~ `member-5` | 구성원 프로필 사진 |
| `competitive-1` ~ `competitive-6` | 헤리티지 경쟁력 |
| `sales-support-1` ~ `sales-support-4` | 영업지원 |
| `training-1` ~ `training-7` | 육성시스템 |
| `income-1` ~ `income-4` | 소득비전 |
| `promotion-1` ~ `promotion-4` | 프로모션 |
| `career-path-1` ~ `career-path-3` | Career Path |
| `welfare-1` ~ `welfare-4` | 복지제도 |
