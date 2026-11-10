# ─────────────────────────────────────────────────────────────────────────────
# W7 실습용 TCGA 폐선암(LUAD) 자료 만들기
#
# 결과
#   data/w07_luad_mutations.tsv  환자 종양별 체세포 변이 (아래 15개 유전자, 단백질을 바꾸는 변이만)
#   data/w07_luad_samples.tsv    환자 종양별 정보 (단백질을 바꾸는 체세포 변이 수, 흡연력, 인종, 병기)
#
# 출처 (모두 공개 자료, 2026-11-10 내려받음)
#   - 체세포 변이: UCSC Xena GDC hub, TCGA-LUAD "somatic mutation (SNVs and small INDELs)
#     - WXS", https://gdc-hub.s3.us-east-1.amazonaws.com/download/TCGA-LUAD.somaticmutation_wxs.tsv.gz
#   - 인종·병기: UCSC Xena GDC hub, TCGA-LUAD clinical,
#     https://gdc-hub.s3.us-east-1.amazonaws.com/download/TCGA-LUAD.clinical.tsv.gz
#   - 흡연력: UCSC Xena TCGA (legacy) hub, LUAD_clinicalMatrix의 tobacco_smoking_history,
#     https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.LUAD.sampleMap%2FLUAD_clinicalMatrix
#   이 자료는 The Cancer Genome Atlas(TCGA) Research Network가 만든 공개(open-access) 자료다.
#   쓰는 사람은 TCGA Research Network(https://www.cancer.gov/tcga)를 출처로 밝힌다.
#
# 가공
#   - 원발 종양(시료 바코드 14–15번째 글자 01)만 남김
#   - "단백질을 바꾸는 변이" = missense, stop_gained, frameshift, splice donor/acceptor,
#     in-frame 삽입·결실, start/stop lost, protein_altering. 동의 변이, 인트론, UTR 등은 뺌
#   - tobacco_smoking_history 코드: 1 = 평생 비흡연(Never), 2 = 현재 흡연(Current),
#     3·4·5 = 과거 흡연(Former)
#
# 실행: 저장소 맨 위 폴더에서  Rscript scripts/make_w07_luad.R
# 필요한 것: base R만 (인터넷 연결 필요)
# ─────────────────────────────────────────────────────────────────────────────

urls <- c(
  mut   = "https://gdc-hub.s3.us-east-1.amazonaws.com/download/TCGA-LUAD.somaticmutation_wxs.tsv.gz",
  clin  = "https://gdc-hub.s3.us-east-1.amazonaws.com/download/TCGA-LUAD.clinical.tsv.gz",
  smoke = "https://tcga-xena-hub.s3.us-east-1.amazonaws.com/download/TCGA.LUAD.sampleMap%2FLUAD_clinicalMatrix"
)
tmp <- tempfile(c("mut", "clin", "smoke"))
for (i in seq_along(urls)) download.file(urls[i], tmp[i], mode = "wb", quiet = TRUE)

mut <- read.delim(gzfile(tmp[1]), stringsAsFactors = FALSE, quote = "")
clin <- read.delim(gzfile(tmp[2]), stringsAsFactors = FALSE, quote = "", check.names = FALSE)
smoke <- read.delim(tmp[3], stringsAsFactors = FALSE, quote = "")

# ── 원발 종양만 ──────────────────────────────────────────────────────────────
mut <- mut[substr(mut$sample, 14, 15) == "01", ]
# 한 종양에서 여러 조각(vial A, B …)을 시퀀싱한 경우 첫 조각 하나만 남김
ids <- sort(unique(mut$sample))
keep <- ids[!duplicated(substr(ids, 1, 15))]
mut <- mut[mut$sample %in% keep, ]
mut$sample <- substr(mut$sample, 1, 15)          # TCGA-XX-XXXX-01

# ── 변이 종류: 효과(effect)의 첫 항목으로 분류 ────────────────────────────────
first_effect <- sub(";.*", "", mut$effect)
class_of <- c(
  missense_variant = "Missense", stop_gained = "Nonsense",
  frameshift_variant = "Frameshift", splice_acceptor_variant = "Splice site",
  splice_donor_variant = "Splice site", inframe_deletion = "In-frame indel",
  inframe_insertion = "In-frame indel", protein_altering_variant = "In-frame indel",
  start_lost = "Other", stop_lost = "Other"
)
mut$variant_class <- unname(class_of[first_effect])
nonsilent <- mut[!is.na(mut$variant_class), ]
# 같은 종양의 같은 변이가 여러 줄로 들어 있는 경우 한 줄만 남김
nonsilent <- nonsilent[!duplicated(nonsilent[, c("sample", "chrom", "start", "ref", "alt")]), ]

# ── 환자 종양별 정보 ─────────────────────────────────────────────────────────
samples <- data.frame(sample = sort(unique(mut$sample)), stringsAsFactors = FALSE)
counts <- table(nonsilent$sample)
samples$n_mutations <- as.integer(counts[samples$sample])
samples$n_mutations[is.na(samples$n_mutations)] <- 0L

smoke$sample <- smoke$sampleID
code <- smoke$tobacco_smoking_history[match(samples$sample, smoke$sample)]
samples$smoking <- ifelse(code == 1, "Never",
                   ifelse(code == 2, "Current",
                   ifelse(code %in% c(3, 4, 5), "Former", NA)))

clin$sample15 <- substr(clin$sample, 1, 15)
clin <- clin[substr(clin$sample15, 14, 15) == "01", ]
clin <- clin[!duplicated(clin$sample15), ]
k <- match(samples$sample, clin$sample15)
race <- clin[["race.demographic"]][k]
samples$race <- ifelse(race %in% c("", "not reported") | is.na(race), NA, race)
stage <- clin[["ajcc_pathologic_stage.diagnoses"]][k]
samples$stage <- ifelse(stage == "" | is.na(stage), NA, sub("^Stage ", "", stage))

# ── 실습에 쓰는 유전자의 변이만 ──────────────────────────────────────────────
genes <- c("TP53", "KRAS", "EGFR", "STK11", "KEAP1", "NF1", "BRAF", "SMARCA4",
           "PIK3CA", "MET", "ERBB2", "RBM10",          # 폐선암에서 알려진 driver 후보
           "TTN", "MUC16", "CSMD3")                     # 아주 긴 유전자 (passenger가 많이 쌓이는 곳)
out <- nonsilent[nonsilent$gene %in% genes,
                 c("sample", "gene", "Amino_Acid_Change", "variant_class", "dna_vaf")]
names(out) <- c("sample", "gene", "protein", "variant_class", "vaf")
out$vaf <- round(as.numeric(out$vaf), 3)
out <- out[order(out$gene, out$sample), ]

dir.create("data", showWarnings = FALSE)
write.table(out, "data/w07_luad_mutations.tsv", sep = "\t", quote = FALSE, row.names = FALSE)
write.table(samples, "data/w07_luad_samples.tsv", sep = "\t", quote = FALSE, row.names = FALSE)
cat("wrote", nrow(out), "mutations and", nrow(samples), "tumours\n")
