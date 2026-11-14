import numpy as np
import pandas as pd
from scipy import stats

DATA = "cookie_cats.csv"
rng = np.random.default_rng(42)

df = pd.read_csv(DATA)
print("=== 1. Data checks ===")
print("Rows:", len(df))
print("Missing values:", int(df.isna().sum().sum()))
print("Duplicate user ids:", int(df["userid"].duplicated().sum()))
print("Groups:\n" + df["version"].value_counts().to_string())

# sample ratio mismatch: were users split about 50/50?
counts = df["version"].value_counts().sort_index()
chi = stats.chisquare(counts.values)
print(f"\nSample ratio check (expected 50/50): chi-square p-value = {chi.pvalue:.3f}")

print("\nGame rounds (the metric has extreme values):")
print(df["sum_gamerounds"].describe().round(1).to_string())
top = df.nlargest(1, "sum_gamerounds")[["userid", "version", "sum_gamerounds"]]
print("Largest value:", top.to_dict("records")[0])
print("Players with 0 rounds:", int((df["sum_gamerounds"] == 0).sum()))

a = df[df["version"] == "gate_30"]
b = df[df["version"] == "gate_40"]

print("\n=== 2. Retention (share of players who came back) ===")


def compare_rates(col):
    pa, pb = a[col].mean(), b[col].mean()
    na, nb = len(a), len(b)
    table = [[a[col].sum(), na - a[col].sum()], [b[col].sum(), nb - b[col].sum()]]
    p_value = stats.chi2_contingency(table, correction=False)[1]
    se = np.sqrt(pa * (1 - pa) / na + pb * (1 - pb) / nb)
    diff = pb - pa
    lo, hi = diff - 1.96 * se, diff + 1.96 * se
    print(f"{col}: gate_30 = {pa:.2%}, gate_40 = {pb:.2%}, difference (40 minus 30) = {diff * 100:+.2f} points, "
          f"95% CI [{lo * 100:+.2f}, {hi * 100:+.2f}], p = {p_value:.4f}")
    return p_value


p1 = compare_rates("retention_1")
p7 = compare_rates("retention_7")

print("\n=== 3. Game rounds (skewed, so medians and a rank test) ===")
print(f"Median rounds: gate_30 = {a['sum_gamerounds'].median():.0f}, gate_40 = {b['sum_gamerounds'].median():.0f}")
print(f"Mean rounds:   gate_30 = {a['sum_gamerounds'].mean():.1f}, gate_40 = {b['sum_gamerounds'].mean():.1f}")
mw = stats.mannwhitneyu(a["sum_gamerounds"], b["sum_gamerounds"], alternative="two-sided")
print(f"Mann-Whitney U test p-value = {mw.pvalue:.3f}")

print("\n=== 4. Bootstrap check for 7-day retention ===")
boots = []
for _ in range(2000):
    sa = a["retention_7"].sample(len(a), replace=True, random_state=int(rng.integers(1e9))).mean()
    sb = b["retention_7"].sample(len(b), replace=True, random_state=int(rng.integers(1e9))).mean()
    boots.append(sb - sa)
boots = np.array(boots)
print(f"Share of resamples where gate_40 retains LESS than gate_30: {(boots < 0).mean():.1%}")

print("\n=== 5. Three metrics were tested, so adjust for that ===")
alpha = 0.05 / 3
print(f"Bonferroni threshold: p < {alpha:.4f}")
print(f"retention_1 significant: {p1 < alpha} | retention_7 significant: {p7 < alpha} | game rounds significant: {mw.pvalue < alpha}")