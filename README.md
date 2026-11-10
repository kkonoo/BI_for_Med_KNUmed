# 의예과 생물정보학 @ KNUmed

https://kkonoo.github.io/BI_for_Med_KNUmed/

의예과 학생을 위한 15주 생물정보학 수업 사이트입니다. W1 개론 뒤로 이론 주와 실습 주가 번갈아 오고, W8에 중간고사, W15에 기말고사가 있습니다.

- **Part 1 · 유전체 의학 (W1–W7)**: 희귀질환 진단, 복합질환과 약물유전체, 암 유전체
- **Part 2 · 발현에서 미생물까지 (W9–W14)**: 전사체, 단일세포·공간 전사체, 마이크로바이옴과 감염 유전체

## 폴더 구조

```
_quarto.yml            사이트 설정 (렌더 대상, 내비게이션, 테마)
index.qmd              홈 — 수업 소개와 15주 강의계획
chapters/              주차별 장 (wNN_주제.qmd = 이론, wNN_주제_lab.qmd = 실습)
assets/                공용 CSS·스크립트·그림 (html.css, key-terms.html 등)
.claude/skills/        장을 같은 틀로 쓰기 위한 프로젝트 스킬
COURSE_SITE_PLAYBOOK.md  다른 수업 사이트와 공유하는 디자인 지침
```

## 렌더

```bash
quarto preview
```

`main`에 push하면 `.github/workflows/deploy.yml`이 사이트를 렌더해 GitHub Pages에 올립니다. 처음 한 번은 저장소 Settings → Pages → Source를 **GitHub Actions**로 바꿔야 합니다.

## 디자인

- 의과학과 수업 사이트들과 같은 공용 테마(`assets/html.css`, 생물정보학 crimson)를 씁니다. 자세한 규칙은 [COURSE_SITE_PLAYBOOK.md](COURSE_SITE_PLAYBOOK.md)에 있습니다.
- 한국어 전용 사이트라 EN/KO 언어 타일은 없고, 라이트/다크 테마 타일만 있습니다.
- 각 장 끝의 `🔑 핵심 용어` 표는 본문에서 해당 용어에 마우스를 올리면 뜻이 뜨는 데 쓰입니다(`assets/key-terms.html`).

## 장 작성

새 장을 쓰거나 고칠 때는 프로젝트 스킬 `.claude/skills/med-bi-chapter/`를 따릅니다. 이론 장과 실습 장의 템플릿, 대상 수준, 문체, 디자인 규칙이 들어 있습니다.

## 현재 상태

- 완료: 사이트 틀, 홈 강의계획, W1–W14 장 개요(뼈대)
- 준비 중: 각 장 본문. 개요만 있는 장은 맨 위에 `🚧 준비 중` 상자가 있습니다.
