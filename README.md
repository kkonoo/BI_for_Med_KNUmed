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
- 이론 장의 개념 그림은 `scripts/figs/`의 Python 스크립트로 만듭니다(공용 스타일 `medfig.py`, 슬라이드 갤러리 크림슨). 다시 만들려면 matplotlib와 [Pretendard](https://github.com/orioncactus/pretendard) 글꼴(`~/.fonts/`)이 필요하고, `scripts/figs/`에서 `python3 wNN_이름.py`를 실행합니다.
- 이론 장 끝의 `🔑 핵심 용어` 표는 본문에서 해당 용어가 나올 때마다 마우스를 올리면 뜻이 뜨는 데 쓰입니다(`assets/key-terms.html`). 실습 장은 바로 앞 이론 장의 표를 씁니다.

## 실습 서버(JupyterHub) 준비

학생은 수업용 JupyterHub 계정으로 R 커널 노트북을 씁니다. 실습 장의 코드는 아래 패키지가 서버에 미리 설치되어 있다고 가정합니다.

| 주차 | R 패키지 |
|------|----------|
| W3 | readr, dplyr, ggplot2 (tidyverse) |
| W5 | readr, dplyr, ggplot2 (tidyverse) |
| W7 | readr, dplyr, ggplot2 (tidyverse) |
| W10 | DESeq2 (Bioconductor), readr, dplyr, ggplot2, ggrepel, tibble |
| W12 | Seurat (SeuratObject 포함), dplyr, ggplot2 |
| W14 | readr, dplyr, tidyr, ggplot2, vegan, phyloseq (고쳐 보기만) |

실습 데이터는 `data/`에 있고 사이트에도 함께 올라갑니다(`_quarto.yml`의 `resources`). 학생은 장의 링크로 내려받아 JupyterHub 파일 창에 올립니다.

## 장 작성

새 장을 쓰거나 고칠 때는 프로젝트 스킬 `.claude/skills/med-bi-chapter/`를 따릅니다. 이론 장과 실습 장의 템플릿, 대상 수준, 문체, 디자인 규칙이 들어 있습니다.

## 현재 상태

- 완료: 사이트 틀, 홈 강의계획, W1–W14 전 장(이론 7, 실습 6)
- 실습 데이터와 만든 방법

| 주차 | 데이터 | 실제/가상 | 생성 스크립트 |
|------|--------|-----------|---------------|
| W3 | `w03_variants.tsv` — 가상 환자 엑솜 변이표 | 가상 (실제 변이 삽입) | `scripts/make_w03_variants.R` |
| W5 | `w05_cad_gwas.tsv` — 관상동맥질환 GWAS 요약 통계 | 가상 (실제 위험 위치 좌표) | `scripts/make_w05_cad_gwas.R` |
| W7 | `w07_luad_mutations.tsv`, `w07_luad_samples.tsv` — TCGA 폐선암 | 실제 (UCSC Xena) | `scripts/make_w07_luad.R` |
| W10 | `w10_brca_counts.tsv`, `w10_brca_samples.tsv` — TCGA 유방암 | 실제 (UCSC Xena) | `scripts/make_w10_brca.R` |
| W12 | `w12_pbmc3k.tar.gz` — 10x pbmc3k | 실제 (10x Genomics 공개) | `scripts/fetch_w12_pbmc3k.py` |
| W14 | `w14_cdiff_snp.tsv`, `w14_gut_genera.tsv` — 병동 분리주, 장내 세균 | 가상 | `scripts/make_w14_data.R` |

- 남은 일: 웹 도구(OncoKB, cBioPortal, CPIC, GWAS/PGS Catalog, GEO, Enrichr, CELLxGENE, Nextstrain, CARD) 화면은 만들 때 열어 보지 못해 메뉴 이름을 일반적으로 적었습니다. 수업 전에 한 번 확인이 필요합니다.
