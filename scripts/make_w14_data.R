# ─────────────────────────────────────────────────────────────────────────────
# W14 실습용 가상 자료 만들기
#
# 결과
#   data/w14_cdiff_snp.tsv     C. difficile 분리주 5개 사이의 유전체 SNV 거리 (가상)
#   data/w14_gut_genera.tsv    대변 16S 시료 15개 × 장내 세균 속(genus) 40개의 read 수 (가상)
#
# 무엇이 진짜이고 무엇이 가상인가
#   - 두 파일 모두 실습용 가상 자료다. 실제 환자 자료가 아니다.
#   - 세균 속 이름은 사람 장에서 실제로 흔히 보고되는 이름을 썼다.
#   - 시간에 따른 변화의 방향은 발표된 관찰을 따랐다:
#       항생제 뒤 다양성 감소, Enterococcus·Enterobacteriaceae 같은 속이 차지함,
#       대변 미생물 이식(FMT) 뒤 다양성이 공여자 수준으로 회복
#       (van Nood et al., N Engl J Med 2013; doi:10.1056/NEJMoa1205037).
#     구체적인 비율과 read 수는 무작위로 만들었다.
#   - SNV 거리 기준(전파된 분리주 사이 0–2개)은 Eyre et al., N Engl J Med 2013
#     (doi:10.1056/NEJMoa1216064)을 따랐다. 거리 값 자체는 가상이다.
#
# 실행: 저장소 맨 위 폴더에서  Rscript scripts/make_w14_data.R
# 필요한 것: base R만
# ─────────────────────────────────────────────────────────────────────────────

set.seed(1314)
dir.create("data", showWarnings = FALSE)

# ── 1. C. difficile 분리주 사이 SNV 거리 ─────────────────────────────────────
isolates <- c("A_day12", "A_day75", "B", "C", "D")
snv <- matrix(c(
   0,  0,  1, 27, 31,
   0,  0,  1, 27, 31,
   1,  1,  0, 28, 32,
  27, 27, 28,  0,  2,
  31, 31, 32,  2,  0),
  nrow = 5, byrow = TRUE, dimnames = list(isolates, isolates))
write.table(data.frame(isolate = isolates, snv, check.names = FALSE),
            "data/w14_cdiff_snp.tsv", sep = "\t", quote = FALSE, row.names = FALSE)

# ── 2. 장내 세균 속(genus) read 수 ───────────────────────────────────────────
# 건강한 성인의 평균 구성 (대략적인 상대 비율, 합은 아래에서 1로 맞춤)
healthy_base <- c(
  Bacteroides = 0.20, Prevotella = 0.05, Faecalibacterium = 0.08,
  Agathobacter = 0.04, Roseburia = 0.04, Blautia = 0.05,
  Ruminococcus = 0.04, Eubacterium = 0.03, Coprococcus = 0.02,
  Alistipes = 0.04, Parabacteroides = 0.025, Bifidobacterium = 0.03,
  Akkermansia = 0.02, Lachnospira = 0.02, Dorea = 0.015,
  Subdoligranulum = 0.025, Oscillibacter = 0.01, Dialister = 0.012,
  Phascolarctobacterium = 0.012, Collinsella = 0.01, Odoribacter = 0.006,
  Butyricicoccus = 0.006, Anaerostipes = 0.01, Fusicatenibacter = 0.012,
  Barnesiella = 0.006, Sutterella = 0.006, Bilophila = 0.003,
  Desulfovibrio = 0.002, Megamonas = 0.004, Holdemanella = 0.004,
  `Escherichia-Shigella` = 0.005, Klebsiella = 0.001, Enterobacter = 0.0005,
  Enterococcus = 0.0005, Lactobacillus = 0.001, Streptococcus = 0.003,
  Veillonella = 0.002, Erysipelatoclostridium = 0.002,
  Clostridioides = 0, Haemophilus = 0.001
)
genera <- names(healthy_base)

# 항생제 뒤 구성: 소수의 속이 자리를 차지하고 많은 속이 사라짐
dysbiosis_base <- setNames(rep(0, length(genera)), genera)
dysbiosis_base[c("Enterococcus", "Escherichia-Shigella", "Klebsiella", "Lactobacillus",
                 "Clostridioides", "Streptococcus", "Enterobacter", "Veillonella",
                 "Bacteroides", "Erysipelatoclostridium", "Bifidobacterium", "Haemophilus")] <-
  c(0.45, 0.22, 0.10, 0.08, 0.05, 0.04, 0.03, 0.015,
    0.01, 0.005, 0.003, 0.002)

rdirichlet1 <- function(alpha) { x <- rgamma(length(alpha), shape = alpha); x / sum(x) }
draw <- function(base, concentration) {
  p <- base / sum(base)
  out <- setNames(rep(0, length(p)), names(p))
  keep <- p > 0
  out[keep] <- rdirichlet1(p[keep] * concentration)
  out
}
reads <- function(p) as.vector(rmultinom(1, size = round(runif(1, 15000, 30000)), prob = p))

# 건강한 성인 8명: 사람마다 차이가 큼 (일부는 Prevotella가 많음)
healthy <- lapply(1:8, function(i) {
  b <- healthy_base
  if (i %in% c(3, 7)) b[c("Prevotella", "Bacteroides")] <- c(0.22, 0.05)
  draw(b, concentration = 60)
})

# 환자 입원 시(항생제 전)와 공여자
patient_d0 <- draw(healthy_base, 60)
donor <- draw(healthy_base, 60)

# 항생제 뒤 세 번의 감염 시점: 비슷한 붕괴 상태, 조금씩 다름
cdi <- lapply(1:3, function(i) draw(dysbiosis_base, 25))

# FMT 뒤: 2주 후는 공여자와 거의 같고, 10주 후는 공여자와 환자 원래 구성이 섞임
fmt_2wk <- 0.85 * donor + 0.15 * draw(healthy_base, 60)
fmt_10wk <- 0.6 * donor + 0.4 * patient_d0

profiles <- c(list(patient_d0), cdi, list(fmt_2wk, fmt_10wk, donor), healthy)
info <- data.frame(
  sample = c("P_day0", "P_day12", "P_day40", "P_day75", "P_day94", "P_day150",
             "Donor", sprintf("H%d", 1:8)),
  person = c(rep("Patient", 6), "Donor", rep("Healthy", 8)),
  timepoint = c("Admission", "CDI", "Relapse 1", "Relapse 2", "FMT +2 wk", "FMT +10 wk",
                "Donor", rep("Healthy", 8)),
  day = c(0, 12, 40, 75, 94, 150, NA, rep(NA, 8)),
  state = c("Before antibiotics", rep("CDI", 3), rep("After FMT", 2),
            "Donor", rep("Healthy", 8)),
  stringsAsFactors = FALSE
)
counts <- t(vapply(profiles, reads, numeric(length(genera))))
colnames(counts) <- genera

out <- cbind(info, counts)
write.table(out, "data/w14_gut_genera.tsv", sep = "\t", quote = FALSE,
            row.names = FALSE, na = "NA")
cat("wrote data/w14_cdiff_snp.tsv and data/w14_gut_genera.tsv (",
    nrow(out), "samples x", length(genera), "genera )\n")
