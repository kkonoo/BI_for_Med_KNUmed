# ─────────────────────────────────────────────────────────────────────────────
# W10 실습용 유방암 RNA-seq 자료 만들기
#
# 결과
#   data/w10_brca_counts.tsv   유전자 × 시료 count 표 (행 = 유전자 기호, 열 = 시료 24개)
#   data/w10_brca_samples.tsv  시료 정보 (PAM50 아형, ER·PR·HER2 상태, 진단 나이, TCGA 바코드)
#
# 출처 (모두 공개 자료, 2026-11-10 내려받음)
#   - TCGA-BRCA STAR gene counts, GDC 공개 자료를 UCSC Xena GDC hub가 정리한 파일
#     https://gdc-hub.s3.us-east-1.amazonaws.com/download/TCGA-BRCA.star_counts.tsv.gz
#     값은 log2(count + 1) → 2^x - 1로 되돌리면 정수 count
#   - 유전자 ID → 유전자 기호: GENCODE v36 probemap (같은 hub)
#     https://gdc-hub.s3.us-east-1.amazonaws.com/download/gencode.v36.annotation.gtf.gene.probemap
#   - PAM50 아형과 수용체 상태: UCSC Xena TCGA legacy hub의 BRCA clinical matrix
#     https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.BRCA.sampleMap%2FBRCA_clinicalMatrix
#   - 단백질 암호화 유전자 목록: scripts/w03_gene_coords.tsv (NCBI Gene)
#   TCGA 자료: The Cancer Genome Atlas Network (https://www.cancer.gov/tcga), 공개 접근 자료
#
# 시료 고르기
#   원발 종양(Primary Tumor) 가운데
#   - Luminal A (PAM50Call_RNAseq = LumA) 이면서 ER 양성, HER2 면역조직화학 음성
#   - Basal-like (PAM50Call_RNAseq = Basal) 이면서 ER·PR·HER2 모두 음성(삼중음성)
#   에서 무작위로 12명씩 (set.seed(2026)). PAM50 아형 자체가 발현으로 정한 이름이라는 점에 주의.
#
# 실행: 저장소 맨 위 폴더에서  Rscript scripts/make_w10_brca.R
# 필요한 것: R 패키지 readr, dplyr. 내려받는 파일 약 140 MB (끝나면 지움)
# ─────────────────────────────────────────────────────────────────────────────

suppressMessages({
  library(readr)
  library(dplyr)
})

set.seed(2026)
tmp <- tempfile("w10_")
dir.create(tmp)
get <- function(url, name) {
  path <- file.path(tmp, name)
  download.file(url, path, mode = "wb", quiet = TRUE)
  path
}

clin_file <- get("https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.BRCA.sampleMap%2FBRCA_clinicalMatrix",
                 "clinical.tsv")
probe_file <- get("https://gdc-hub.s3.us-east-1.amazonaws.com/download/gencode.v36.annotation.gtf.gene.probemap",
                  "probemap.tsv")
count_file <- get("https://gdc-hub.s3.us-east-1.amazonaws.com/download/TCGA-BRCA.star_counts.tsv.gz",
                  "counts.tsv.gz")

# ── 시료 고르기 ───────────────────────────────────────────────────────────────
clin <- read_tsv(clin_file, show_col_types = FALSE, guess_max = 5000) |>
  transmute(
    sample15 = sampleID,
    sample_type,
    pam50 = PAM50Call_RNAseq,
    er_status = breast_carcinoma_estrogen_receptor_status,
    pr_status = breast_carcinoma_progesterone_receptor_status,
    her2_status = lab_proc_her2_neu_immunohistochemistry_receptor_status,
    age = age_at_initial_pathologic_diagnosis
  )

count_header <- names(read_tsv(count_file, n_max = 0, show_col_types = FALSE))
available <- tibble(tcga_barcode = count_header[-1]) |>
  filter(substr(tcga_barcode, 14, 16) == "01A") |>          # 원발 종양, 첫 번째 vial
  mutate(sample15 = substr(tcga_barcode, 1, 15)) |>
  distinct(sample15, .keep_all = TRUE)

eligible <- function(subtype, er, pr = c("Positive", "Negative")) {
  clin |>
    filter(sample_type == "Primary Tumor", pam50 == subtype, er_status == er,
           pr_status %in% pr, her2_status == "Negative") |>
    inner_join(available, by = "sample15")
}
pool <- bind_rows(eligible("LumA", "Positive"),
                  eligible("Basal", "Negative", pr = "Negative"))

# ── count 읽기: 후보 시료의 열만 ──────────────────────────────────────────────
raw <- read_tsv(count_file, col_select = all_of(c("Ensembl_ID", pool$tcga_barcode)),
                show_col_types = FALSE)
back <- 2^as.matrix(raw[, -1]) - 1               # log2(count + 1) → count

# 일부 시료는 여러 분주(aliquot)의 평균이라 정수가 아님 → 정수로 정확히 되돌아오는 시료만
integral <- apply(back, 2, function(v) all(abs(v - round(v)) <= 1e-9 * pmax(v, 1)))
pool <- pool |> filter(integral[tcga_barcode])

samples <- pool |>
  group_by(pam50) |>
  slice_sample(n = 12) |>
  ungroup() |>
  mutate(pam50 = factor(pam50, levels = c("LumA", "Basal"))) |>
  arrange(pam50, tcga_barcode) |>
  mutate(pam50 = as.character(pam50),
         sample = c(sprintf("LumA_%02d", 1:12), sprintf("Basal_%02d", 1:12))) |>
  select(sample, pam50, er_status, pr_status, her2_status, age, tcga_barcode)

mat <- round(back[, samples$tcga_barcode])

# ── 유전자 기호 붙이기, 단백질 암호화 유전자만 ────────────────────────────────
probe <- read_tsv(probe_file, show_col_types = FALSE)
coding <- read.delim("scripts/w03_gene_coords.tsv", comment.char = "#")$symbol
symbol <- probe$gene[match(raw$Ensembl_ID, probe$id)]
keep <- !is.na(symbol) & symbol %in% coding & !grepl("_PAR_Y$", raw$Ensembl_ID)
mat <- mat[keep, ]
symbol <- symbol[keep]

# 같은 기호가 두 번 나오면 count 합이 큰 쪽만
ord <- order(-rowSums(mat))
mat <- mat[ord, ]
symbol <- symbol[ord]
first <- !duplicated(symbol)
mat <- mat[first, ]
symbol <- symbol[first]

# 24개 시료를 다 합쳐도 10개 미만인 유전자는 뺌 (파일 크기)
expressed <- rowSums(mat) >= 10
mat <- mat[expressed, ]
symbol <- symbol[expressed]

colnames(mat) <- samples$sample
counts <- tibble(gene = symbol) |>
  bind_cols(as_tibble(mat)) |>
  arrange(gene)

dir.create("data", showWarnings = FALSE)
write_tsv(counts, "data/w10_brca_counts.tsv")
write_tsv(samples, "data/w10_brca_samples.tsv")
unlink(tmp, recursive = TRUE)
cat("wrote", nrow(counts), "genes x", ncol(counts) - 1, "samples\n")
