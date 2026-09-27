"""Statistical helpers (NumPy only).

Tests use the normal approximation with tie and continuity corrections. The
paper leads with effect sizes and bootstrap CIs, so p-values are secondary.
"""
import math
import numpy as np


# ------------------------------------------------------------------ basics
def _clean(x):
    return np.asarray([v for v in np.asarray(x, float) if not np.isnan(v)], float)


def describe(x):
    x = _clean(x)
    return dict(n=int(len(x)), mean=round(float(np.mean(x)), 2),
                sd=round(float(np.std(x, ddof=1)), 2) if len(x) > 1 else np.nan,
                median=float(np.median(x)), q1=float(np.percentile(x, 25)),
                q3=float(np.percentile(x, 75)), min=float(np.min(x)), max=float(np.max(x)))


def rankdata(a):
    a = np.asarray(a, float)
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a), float)
    sa = a[order]
    i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and sa[j + 1] == sa[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2.0 + 1
        i = j + 1
    return ranks


def _two_sided_p(z):
    return float(math.erfc(abs(z) / math.sqrt(2)))


# ------------------------------------------------------------------ bootstrap
def boot_ci(x, fn, rng, n=5000, alpha=0.05):
    """Percentile bootstrap CI for fn(x)."""
    x = _clean(x)
    if len(x) < 2:
        return (np.nan, np.nan)
    bs = [fn(rng.choice(x, len(x), replace=True)) for _ in range(n)]
    return (float(np.percentile(bs, 100 * alpha / 2)), float(np.percentile(bs, 100 * (1 - alpha / 2))))


# ------------------------------------------------------------------ two groups
def cliffs_delta(a, b):
    """Cliff's delta = P(a > b) - P(a < b)."""
    a, b = _clean(a), _clean(b)
    if len(a) == 0 or len(b) == 0:
        return np.nan
    diff = a[:, None] - b[None, :]
    return float(((diff > 0).sum() - (diff < 0).sum()) / (len(a) * len(b)))


def cliffs_ci(a, b, rng, n=5000):
    a, b = _clean(a), _clean(b)
    if len(a) < 2 or len(b) < 2:
        return (np.nan, np.nan)
    ds = [cliffs_delta(rng.choice(a, len(a), True), rng.choice(b, len(b), True)) for _ in range(n)]
    return (float(np.nanpercentile(ds, 2.5)), float(np.nanpercentile(ds, 97.5)))


def mannwhitney_p(a, b):
    a, b = _clean(a), _clean(b)
    n1, n2 = len(a), len(b)
    if n1 < 2 or n2 < 2:
        return np.nan
    allv = np.concatenate([a, b])
    r = rankdata(allv)
    u1 = r[:n1].sum() - n1 * (n1 + 1) / 2.0
    mu, n = n1 * n2 / 2.0, n1 + n2
    _, counts = np.unique(allv, return_counts=True)
    tie = (counts ** 3 - counts).sum()
    sigma = math.sqrt(n1 * n2 / 12.0 * ((n + 1) - tie / (n * (n - 1))))
    if sigma == 0:
        return np.nan
    return _two_sided_p((u1 - mu - math.copysign(0.5, u1 - mu)) / sigma)


def holm(pvals):
    """Holm step-down adjusted p-values (monotone), in the input order."""
    p = np.asarray(pvals, float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    running = 0.0
    for k, i in enumerate(order):
        running = max(running, min(1.0, (m - k) * p[i]))
        adj[i] = running
    return adj


# ------------------------------------------------------------------ paired
def wilcoxon_p(after, before):
    d = np.asarray(after, float) - np.asarray(before, float)
    d = d[d != 0]
    n = len(d)
    if n < 1:
        return 1.0
    r = rankdata(np.abs(d))
    w = r[d > 0].sum()
    mu = n * (n + 1) / 4.0
    _, counts = np.unique(np.abs(d), return_counts=True)
    tie = (counts ** 3 - counts).sum()
    sigma = math.sqrt(n * (n + 1) * (2 * n + 1) / 24.0 - tie / 48.0)
    if sigma == 0:
        return np.nan
    return _two_sided_p((w - mu - math.copysign(0.5, w - mu)) / sigma)


def rank_biserial_paired(after, before):
    d = np.asarray(after, float) - np.asarray(before, float)
    d = d[d != 0]
    if len(d) == 0:
        return 0.0
    r = rankdata(np.abs(d))
    return float((r[d > 0].sum() - r[d < 0].sum()) / r.sum())


# ------------------------------------------------------------------ reliability
def cronbach_alpha(items):
    """items: 2-D array (respondents x items), complete cases only."""
    x = np.asarray(items, float)
    k = x.shape[1]
    item_var = x.var(axis=0, ddof=1).sum()
    total_var = x.sum(axis=1).var(ddof=1)
    return float(k / (k - 1) * (1 - item_var / total_var))


def omega_total(items, max_iter=500, tol=1e-6):
    """McDonald's omega (total) from a one-factor principal-axis solution on
    the Pearson correlation matrix; communalities are capped below 1 to avoid
    Heywood cases."""
    r = np.corrcoef(np.asarray(items, float), rowvar=False)
    h2 = np.clip(1 - 1 / np.diag(np.linalg.pinv(r)), 0.05, 0.995)   # SMC start
    for _ in range(max_iter):
        reduced = r.copy()
        np.fill_diagonal(reduced, h2)
        vals, vecs = np.linalg.eigh(reduced)
        lam = vecs[:, -1] * math.sqrt(max(vals[-1], 0))
        new = np.clip(lam ** 2, 0.0, 0.995)
        if np.max(np.abs(new - h2)) < tol:
            h2 = new
            break
        h2 = new
    lam = np.abs(lam)
    s = lam.sum()
    return float(s ** 2 / (s ** 2 + (1 - lam ** 2).sum()))


def boot_reliability_ci(items, fn, rng, n=5000):
    x = np.asarray(items, float)
    vals = []
    for _ in range(n):
        s = x[rng.integers(0, len(x), len(x))]
        if np.all(s.var(axis=0) > 0):
            vals.append(fn(s))
    return (float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5)))
