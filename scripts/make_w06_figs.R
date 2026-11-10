# ─────────────────────────────────────────────────────────────────────────────
# W6 그림: 상황별로 기대되는 변이 대립유전자 빈도(VAF)
#
# 결과: assets/img/w06/vaf_expected.png
# 계산식 (두 벌 염색체에서 한쪽 대립유전자에만 변이가 있을 때)
#   생식세포 이형접합 변이:  VAF ≈ 0.5  (종양 세포든 정상 세포든 모두 가지고 있음)
#   체세포 변이:            VAF ≈ 종양 순도 × 그 변이를 가진 종양 세포 비율 × 0.5
# 실행: 저장소 맨 위 폴더에서  Rscript scripts/make_w06_figs.R
# 필요한 것: ggplot2, ragg
# ─────────────────────────────────────────────────────────────────────────────

library(ggplot2)

vaf <- data.frame(
  scenario = c("Germline heterozygous\n(any tumour purity)",
               "Somatic, all tumour cells\n(purity 100%)",
               "Somatic, all tumour cells\n(purity 60%)",
               "Somatic, 20% of tumour cells\n(purity 60%)"),
  vaf = c(0.5, 0.5, 0.6 * 1 * 0.5, 0.6 * 0.2 * 0.5),
  type = c("Germline", "Somatic", "Somatic", "Somatic")
)
vaf$scenario <- factor(vaf$scenario, levels = rev(vaf$scenario))

p <- ggplot(vaf, aes(x = vaf * 100, y = scenario, fill = type)) +
  geom_col(width = 0.6) +
  geom_text(aes(label = paste0(vaf * 100, "%")), hjust = 1.15, size = 4.5, colour = "white") +
  geom_vline(xintercept = 32, linetype = "dashed", colour = "grey40") +
  annotate("text", x = 33, y = 4.45, label = "Case: EGFR VAF 32%", hjust = 0,
           colour = "grey30", size = 4) +
  scale_fill_manual(values = c(Germline = "grey55", Somatic = "#B0283C")) +
  scale_x_continuous(limits = c(0, 62), breaks = seq(0, 60, 10)) +
  labs(x = "Expected variant allele frequency (%)", y = NULL, fill = NULL) +
  theme_minimal(base_size = 13) +
  theme(legend.position = "top")

dir.create("assets/img/w06", recursive = TRUE, showWarnings = FALSE)
ggsave("assets/img/w06/vaf_expected.png", p, width = 8, height = 4, dpi = 200,
       device = ragg::agg_png, bg = "white")
