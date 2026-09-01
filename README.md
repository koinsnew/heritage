# 헤리티지 금융지사 홈페이지

신한라이프 헤리티지 금융지사 채용·소개 홈페이지 (정적 사이트)

## 배포 구조 (2단계로 분리)

```
[방문자] → Vercel(index.html + images) ──POST──▶ Apps Script(code.gs) ─▶ Google Sheet + 메일
                                        └───────▶ Supabase (inquiries / recruits)
```

| 파일 | 배포처 | 역할 |
|---|---|---|
| `index.html` + `images/` | **GitHub → Vercel** | 화면(프론트엔드) |
| `code.gs` | **Google Apps Script** | 지원서·문의 접수 API(시트 저장 + 메일 발송) |
| — | Supabase | 폼 데이터 DB 저장 |

`code.gs`는 이 저장소에 두지 않아도 됩니다(Apps Script 편집기에서 관리).

## ① 프론트엔드 배포 (GitHub → Vercel)

이 폴더(`index.html`, `images/`)를 GitHub에 올리고 Vercel에 연결합니다.

- Framework Preset: **Other**
- Build/Output: 비워둠 (빌드 없는 정적 사이트)

GitHub에 커밋하면 Vercel이 자동 재배포합니다.

## ② 백엔드 배포 (Google Apps Script)

1. Apps Script 편집기에 `code.gs` 내용을 붙여넣기
2. 상단 `SPREADSHEET_ID`, `ADMIN_EMAIL` 확인
3. **배포 → 배포 관리 → 편집 → 버전: 새 버전 → 배포**
4. 액세스 권한: **모든 사용자**

> index.html은 더 이상 Apps Script로 서빙하지 않습니다. code.gs는 폼 POST만 처리합니다.
> index.html 안의 `GAS_URL` 이 이 웹앱의 `/exec` 주소와 일치해야 합니다.

## 백엔드 (Supabase)

| 폼 | 테이블 |
|---|---|
| 문의하기 | `inquiries` |
| 입사지원서 | `recruits` |

`SUPABASE_KEY`는 publishable(공개용) 키라 코드에 있어도 안전하며, 실제 보안은 RLS 정책이 담당합니다.
`service_role` / `secret_` 키는 절대 저장소에 넣지 마세요.

## 수정 방법

### 글자·내용 수정
GitHub에서 `index.html` 클릭 → 연필(✏️) → 수정 → Commit changes

### 이미지 교체
`images/` 폴더에 같은 파일명으로 새 이미지를 업로드하면 교체됩니다.

### 이미지 파일명 규칙

| 파일 | 위치 |
|---|---|
| `member-1` ~ `member-5` | 구성원 프로필 |
| `tour-*` | 지사 둘러보기 |
| `competitive-*` | 헤리티지 경쟁력 |
| `sales-support-*` | 영업지원 |
| `training-*` | 육성시스템 |
| `income-*` | 소득비전 |
| `promotion-*` | 프로모션 |
| `career-path-*` | Career Path |
| `welfare-*` | 복지제도 |
