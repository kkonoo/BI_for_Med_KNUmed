# ─────────────────────────────────────────────────────────────────────────────
# W3 실습용 가상 환자 변이표 만들기
#
# 결과: data/w03_variants.tsv
#   발달지연과 경련이 있는 세 살 아이(proband)와 부모의 엑솜 변이 약 2만 개.
#   한 줄 = 아이에게서 레퍼런스와 다르게 나온 위치 하나.
#
# 무엇이 진짜이고 무엇이 가상인가
#   - 배경 변이(대부분의 줄)는 가상이다. 유전자 이름과 유전자 구간은 실제(NCBI Gene,
#     GRCh38)지만, 그 안의 위치·염기·단백질 변화·집단 빈도는 무작위로 만들었다.
#     부모와 아이의 유전형은 멘델 유전을 따르도록 만들었다.
#   - 아래 세 변이는 ClinVar에 실제로 있는 변이를 그대로 넣었다(2026-11-10 확인).
#     학생이 gnomAD와 ClinVar에서 직접 찾아보는 대상이다.
#       SCN1A c.4219C>T p.(Arg1407Ter)  chr2:166002537 G>A  rs398123593
#             ClinVar 93649, Pathogenic (여러 기관 제출, 불일치 없음), gnomAD에 없음
#       SCN1A c.3199G>A p.(Ala1067Thr)  chr2:166036278 C>T  rs2298771
#             ClinVar 36753, Benign. 대체 대립유전자(T)가 오히려 다수형(gnomAD exome 약 0.70)
#       SCN2A c.5852T>C p.(Ile1951Thr)  chr2:165389658 T>C  rs1458271629
#             ClinVar 2948820, Uncertain significance, gnomAD exome 약 0.0000036
#   - 다음 세 줄은 가르치려고 넣은 가상 변이다(ClinVar·gnomAD에 없음).
#       FLNC: de novo 처럼 보이지만 품질이 낮은 호출(LowQual, depth 6)
#       TTN: de novo 동의 변이 (단백질 서열이 바뀌지 않음)
#       OR5A1: 후각 수용체 유전자의 de novo missense
#
# 실행: 저장소 맨 위 폴더에서  Rscript scripts/make_w03_variants.R
# 필요한 것: base R만 (추가 패키지 없음)
# ─────────────────────────────────────────────────────────────────────────────

set.seed(2026)

genes <- read.delim("scripts/w03_gene_coords.tsv", comment.char = "#",
                    stringsAsFactors = FALSE)

# 경련 관련 유전자와 성염색체는 배경에서 뺀다 (해석을 헷갈리게 하지 않도록)
panel <- c("SCN1A", "SCN2A", "SCN8A", "KCNQ2", "STXBP1", "CDKL5", "PCDH19", "SLC2A1")
genes <- genes[!(genes$symbol %in% panel) & genes$chrom %in% as.character(1:22), ]

n <- 20000

# ── 집단 빈도: 대부분 흔한 변이, 일부만 드문 변이 ─────────────────────────────
af_class <- sample(c("common", "low", "rare", "absent"), n, replace = TRUE,
                   prob = c(0.88, 0.08, 0.035, 0.005))
af <- numeric(n)
af[af_class == "common"] <- runif(sum(af_class == "common"), 0.01, 0.99)
af[af_class == "low"]    <- 10^runif(sum(af_class == "low"), -3, -2)
af[af_class == "rare"]   <- 10^runif(sum(af_class == "rare"), -5.5, -3)
af[af_class == "absent"] <- 0

# ── 유전형: 아이가 대체 대립유전자를 하나 이상 가진 자리만 표에 있다 ─────────
# 아이가 동형접합(1/1)일 확률 = af^2 / (af^2 + 2 af (1 - af))
p_hom <- ifelse(af > 0, af^2 / (af^2 + 2 * af * (1 - af)), 0)
child_hom <- runif(n) < p_hom

parent_gt <- function(transmitted_alt, af) {
  # 전달한 대립유전자를 알 때, 나머지 한 대립유전자는 집단 빈도를 따른다
  other_alt <- runif(length(af)) < af
  ifelse(transmitted_alt,
         ifelse(other_alt, "1/1", "0/1"),
         ifelse(other_alt, "0/1", "0/0"))
}
from_father <- runif(n) < 0.5
father_tx <- child_hom | from_father
mother_tx <- child_hom | !from_father
father <- parent_gt(father_tx, af)
mother <- parent_gt(mother_tx, af)
proband <- ifelse(child_hom, "1/1", "0/1")

# ── 변이의 결과(consequence)와 영향 등급(impact) ──────────────────────────────
csq_table <- data.frame(
  consequence = c("missense_variant", "synonymous_variant", "3_prime_UTR_variant",
                  "5_prime_UTR_variant", "intron_variant", "splice_region_variant",
                  "inframe_deletion", "stop_gained", "frameshift_variant",
                  "splice_donor_variant", "splice_acceptor_variant", "start_lost"),
  impact = c("MODERATE", "LOW", "MODIFIER", "MODIFIER", "MODIFIER", "LOW",
             "MODERATE", "HIGH", "HIGH", "HIGH", "HIGH", "HIGH"),
  prob = c(0.40, 0.38, 0.06, 0.02, 0.09, 0.034,
           0.01, 0.0025, 0.0025, 0.0006, 0.0006, 0.0003)
)
k <- sample(seq_len(nrow(csq_table)), n, replace = TRUE, prob = csq_table$prob)
consequence <- csq_table$consequence[k]
impact <- csq_table$impact[k]

# ── 위치와 염기 ──────────────────────────────────────────────────────────────
g <- genes[sample(seq_len(nrow(genes)), n, replace = TRUE,
                  prob = log10(genes$end - genes$start + 10)), ]
pos <- round(g$start + runif(n) * (g$end - g$start))
bases <- c("A", "C", "G", "T")
ref <- sample(bases, n, replace = TRUE)
alt <- vapply(ref, function(b) sample(setdiff(bases, b), 1), character(1))
is_del <- consequence %in% c("frameshift_variant", "inframe_deletion")
ref[is_del] <- paste0(ref[is_del],
                      vapply(which(is_del), function(i)
                        paste(sample(bases, ifelse(consequence[i] == "inframe_deletion", 3, 1),
                                     replace = TRUE), collapse = ""), character(1)))
alt[is_del] <- substr(ref[is_del], 1, 1)

# ── 단백질 변화 표기 ─────────────────────────────────────────────────────────
aa <- c("Ala", "Arg", "Asn", "Asp", "Cys", "Gln", "Glu", "Gly", "His", "Ile",
        "Leu", "Lys", "Met", "Phe", "Pro", "Ser", "Thr", "Trp", "Tyr", "Val")
aa_pos <- sample(2:1500, n, replace = TRUE)
aa1 <- sample(aa, n, replace = TRUE)
aa2 <- vapply(aa1, function(a) sample(setdiff(aa, a), 1), character(1))
protein <- rep(".", n)
protein[consequence == "missense_variant"] <- paste0("p.", aa1, aa_pos, aa2)[consequence == "missense_variant"]
protein[consequence == "synonymous_variant"] <- paste0("p.", aa1, aa_pos, "=")[consequence == "synonymous_variant"]
protein[consequence == "stop_gained"] <- paste0("p.", aa1, aa_pos, "Ter")[consequence == "stop_gained"]
protein[consequence == "frameshift_variant"] <- paste0("p.", aa1, aa_pos, "fs")[consequence == "frameshift_variant"]
protein[consequence == "inframe_deletion"] <- paste0("p.", aa1, aa_pos, "del")[consequence == "inframe_deletion"]
protein[consequence == "start_lost"] <- "p.Met1?"

# ── 호출 품질: 약 3%는 품질 미달(LowQual) ────────────────────────────────────
low_q <- runif(n) < 0.03
filter <- ifelse(low_q, "LowQual", "PASS")
depth <- ifelse(low_q, sample(3:12, n, replace = TRUE),
                pmax(15, round(rnorm(n, 60, 15))))

background <- data.frame(
  chrom = paste0("chr", g$chrom), pos = pos, ref = ref, alt = unname(alt),
  gene = g$symbol, consequence = consequence, impact = impact, protein = protein,
  gnomad_af = signif(af, 2), filter = filter, depth = depth,
  proband = proband, father = father, mother = mother,
  stringsAsFactors = FALSE
)

# ── 실제 변이 3개 + 가르치려고 넣은 가상 변이 3개 ────────────────────────────
special <- data.frame(
  chrom = c("chr2", "chr2", "chr2", "chr7", "chr2", "chr11"),
  pos = c(166002537, 166036278, 165389658, 128846120, 178612904, 59441237),
  ref = c("G", "C", "T", "C", "G", "C"),
  alt = c("A", "T", "C", "T", "A", "G"),
  gene = c("SCN1A", "SCN1A", "SCN2A", "FLNC", "TTN", "OR5A1"),
  consequence = c("stop_gained", "missense_variant", "missense_variant",
                  "stop_gained", "synonymous_variant", "missense_variant"),
  impact = c("HIGH", "MODERATE", "MODERATE", "HIGH", "LOW", "MODERATE"),
  protein = c("p.Arg1407Ter", "p.Ala1067Thr", "p.Ile1951Thr",
              "p.Gln871Ter", "p.Leu402=", "p.Ser187Cys"),
  gnomad_af = c(0, 0.70, 0.0000036, 0, 0, 0),
  filter = c("PASS", "PASS", "PASS", "LowQual", "PASS", "PASS"),
  depth = c(54, 61, 47, 6, 58, 49),
  proband = c("0/1", "1/1", "0/1", "0/1", "0/1", "0/1"),
  father = c("0/0", "0/1", "0/1", "0/0", "0/0", "0/0"),
  mother = c("0/0", "1/1", "0/0", "0/0", "0/0", "0/0"),
  stringsAsFactors = FALSE
)

variants <- rbind(background, special)
variants <- variants[!duplicated(variants[, c("chrom", "pos")]), ]
chrom_num <- as.integer(sub("chr", "", variants$chrom))
variants <- variants[order(chrom_num, variants$pos), ]

dir.create("data", showWarnings = FALSE)
write.table(variants, "data/w03_variants.tsv", sep = "\t", quote = FALSE,
            row.names = FALSE)
cat("wrote", nrow(variants), "variants to data/w03_variants.tsv\n")
