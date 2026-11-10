# ─────────────────────────────────────────────────────────────────────────────
# W5 실습용 가상 관상동맥질환(CAD) GWAS 요약 통계 만들기
#
# 결과: data/w05_cad_gwas.tsv
#   한 줄 = 변이 하나의 연관 검정 결과 (유럽계 환자군 vs 대조군을 가정한 가상 GWAS)
#   열: snp, chrom, pos(GRCh38), locus, beta(log 오즈비), se, p
#
# 무엇이 진짜이고 무엇이 가상인가
#   - 모든 p값과 효과 크기는 가상이다. 실제 GWAS 결과가 아니다.
#   - 대부분의 줄(배경 변이)은 위치를 무작위로 고른 가상 변이이고 snp 이름이 "."이다.
#     실제 GWAS는 수백만 개 변이를 검정하지만, 실습용으로 약 7만 개만 만들었다.
#   - 신호가 나오는 10개 locus는 실제로 관상동맥질환 GWAS에서 반복 보고된 곳이다.
#     아래 rs 번호와 GRCh38 위치는 NCBI dbSNP(E-utilities)에서 확인했다(2026-11-10).
#       9p21   CDKN2B-AS1  rs1333049  chr9:22125504   rs10757278 chr9:22124478
#                          rs4977574  chr9:22098575
#       6q25   LPA         rs10455872 chr6:160589086
#       1p13   SORT1       rs646776   chr1:109275908  rs599839   chr1:109279544
#       6p24   PHACTR1     rs9349379  chr6:12903725   rs12526453 chr6:12927312
#       19p13  LDLR        rs1122608  chr19:11052925
#       9q34   ABO         rs579459   chr9:133278724
#       1p32   PCSK9       rs11206510 chr1:55030366
#       12q24  SH2B3       rs3184504  chr12:111446804
#       1q41   MIA3        rs17465637 chr1:222650187
#       10p11  JCAD        rs2505083  chr10:30046193
#     locus 이름은 문헌에서 흔히 부르는 후보 유전자다. dbSNP가 붙이는 가장 가까운
#     유전자와 다를 수 있다(예: rs646776 → CELSR2, rs1122608 → SMARCA4).
#   - locus 주변 변이(snp ".")는 연관 불평형을 흉내 내려고 리드 변이에서 멀어질수록
#     신호가 약해지게 만든 가상 변이다.
#   - 15번 염색체에 기준(5×10⁻⁸)에 못 미치는 가상 신호를 하나 넣었다(locus "suggestive").
#
# 실행: 저장소 맨 위 폴더에서  Rscript scripts/make_w05_cad_gwas.R
# 필요한 것: base R만
# ─────────────────────────────────────────────────────────────────────────────

set.seed(2026)

# GRCh38 상염색체 길이 (NCBI nuccore, GRCh38.p14)
chr_len <- c(248956422, 242193529, 198295559, 190214555, 181538259, 170805979,
             159345973, 145138636, 138394717, 133797422, 135086622, 133275309,
             114364328, 107043718, 101991189, 90338345, 83257441, 80373285,
             58617616, 64444167, 46709983, 50818468)

# p값 ↔ z값
p_to_z <- function(p) qnorm(p / 2, lower.tail = FALSE)
z_to_p <- function(z) 2 * pnorm(-abs(z))

# ── 배경 변이: 신호 없음 (p ~ 균등분포) ─────────────────────────────────────
n_bg <- 70000
bg_chrom <- sample(1:22, n_bg, replace = TRUE, prob = chr_len)
bg_pos <- vapply(bg_chrom, function(ch) sample.int(chr_len[ch] - 1e5, 1) + 5e4, numeric(1))
bg_p <- runif(n_bg)
bg_se <- runif(n_bg, 0.010, 0.035)
bg_beta <- sign(rnorm(n_bg)) * p_to_z(bg_p) * bg_se
background <- data.frame(snp = ".", chrom = bg_chrom, pos = bg_pos, locus = ".",
                         beta = bg_beta, se = bg_se, p = bg_p)

# ── 실제 locus의 리드 변이 (p값과 효과 크기는 가상) ──────────────────────────
leads <- data.frame(
  snp   = c("rs1333049", "rs10455872", "rs646776", "rs9349379", "rs1122608",
            "rs579459", "rs11206510", "rs3184504", "rs17465637", "rs2505083"),
  chrom = c(9, 6, 1, 6, 19, 9, 1, 12, 1, 10),
  pos   = c(22125504, 160589086, 109275908, 12903725, 11052925,
            133278724, 55030366, 111446804, 222650187, 30046193),
  locus = c("CDKN2B-AS1", "LPA", "SORT1", "PHACTR1", "LDLR",
            "ABO", "PCSK9", "SH2B3", "MIA3", "JCAD"),
  beta  = c(0.25, 0.40, 0.12, 0.11, 0.11, 0.09, 0.08, 0.07, 0.07, 0.06),
  p     = c(1e-60, 2e-30, 4e-22, 2e-20, 3e-15, 6e-14, 2e-12, 8e-11, 5e-10, 3e-9),
  width = c(150e3, 80e3, 100e3, 120e3, 80e3, 80e3, 80e3, 100e3, 80e3, 80e3)
)
leads$se <- leads$beta / p_to_z(leads$p)

# 같은 locus의 다른 실제 변이 (리드와 연관 불평형이 강한 것으로 가정)
partners <- data.frame(
  snp   = c("rs10757278", "rs4977574", "rs599839", "rs12526453"),
  chrom = c(9, 9, 1, 6),
  pos   = c(22124478, 22098575, 109279544, 12927312),
  locus = c("CDKN2B-AS1", "CDKN2B-AS1", "SORT1", "PHACTR1"),
  beta  = c(0.25, 0.24, 0.12, 0.10),
  p     = c(3e-59, 2e-55, 1e-21, 5e-18)
)
partners$se <- partners$beta / p_to_z(partners$p)

# ── locus 주변 변이: 리드에서 멀수록 신호가 약해짐 ─────────────────────────
# 리드 변이가 그 locus에서 가장 강한 신호가 되도록 z값의 상한을 둔다
make_peak <- function(lead, n = 45) {
  z_lead <- p_to_z(lead$p)
  d <- runif(n, -lead$width, lead$width)
  r2 <- exp(-abs(d) / (lead$width / 4)) * runif(n, 0.15, 1)
  z <- pmin(sqrt(r2) * z_lead + rnorm(n, 0, 0.7), 0.97 * z_lead)
  se <- lead$se * runif(n, 0.9, 1.3)
  data.frame(snp = ".", chrom = lead$chrom, pos = round(lead$pos + d), locus = lead$locus,
             beta = sign(lead$beta) * z * se, se = se, p = pmin(1, z_to_p(z)))
}
peaks <- do.call(rbind, lapply(seq_len(nrow(leads)), function(i) make_peak(leads[i, ])))

# ── 기준에 못 미치는 가상 신호 (15번 염색체) ────────────────────────────────
sugg_lead <- data.frame(chrom = 15, pos = 67000000, locus = "suggestive",
                        beta = 0.05, p = 3e-7, width = 80e3)
sugg_lead$se <- sugg_lead$beta / p_to_z(sugg_lead$p)
sugg <- make_peak(sugg_lead, n = 25)

gwas <- rbind(background, peaks, sugg,
              leads[, c("snp", "chrom", "pos", "locus", "beta", "se", "p")],
              partners[, c("snp", "chrom", "pos", "locus", "beta", "se", "p")])
gwas <- gwas[!duplicated(gwas[, c("chrom", "pos")], fromLast = TRUE), ]
gwas <- gwas[order(gwas$chrom, gwas$pos), ]
gwas$beta <- round(gwas$beta, 4)
gwas$se <- round(gwas$se, 4)
gwas$p <- signif(gwas$p, 3)

dir.create("data", showWarnings = FALSE)
write.table(gwas, "data/w05_cad_gwas.tsv", sep = "\t", quote = FALSE, row.names = FALSE)
cat("wrote", nrow(gwas), "variants to data/w05_cad_gwas.tsv\n")
