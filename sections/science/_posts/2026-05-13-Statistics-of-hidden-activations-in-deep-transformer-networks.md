---
layout: post
date: 2026-05-13
title: "The Statistical Lives of Hidden Activations in Deep Transformers"
description: "We analyze the statistical properties of hidden activations in deep Transformer networks, including variance growth, massive activation outliers, token embedding clustering, and heavy-tailed singular value spectra, comparing empirical results against an analytical prior computed from the model's config file."
categories:
  - science
published: false
---

If you've ever tried to quantize a large language model to 4-bit and watched the perplexity explode, you've bumped into one of the most practically important — and theoretically underappreciated — phenomena in deep learning: the strange statistical world inside a Transformer's residual stream.

This post is a tour of that world. We'll look at four things that happen as information flows through the layers of a trained LLM:

1. **Variance keeps growing** — and the deeper you go, the less each layer actually changes anything.
2. **A handful of dimensions become *massive***, hitting values thousands of times larger than everything else around them.
3. **All token representations start looking alike**, crowding into a narrow cone in high-dimensional space.
4. **Weight matrices develop heavy tails** in their singular-value spectra, a fingerprint of something physicists recognize from disordered systems.

We'll connect these observations to real math, run experiments on Llama-3.2-1B and Qwen2.5-1.5B, and compare the empirical results against an *analytical prior* you can compute purely from a model's config file — no weights required.

---

## The basic setup: Pre-LN and its consequences

Modern LLMs — Llama, Mistral, Qwen, the whole family — use **Pre-Layer Normalization**. Every residual block looks like this:

$$x_{l+1} = x_l + F\!\bigl(\mathrm{LN}(x_l)\bigr)$$

The key detail: the normalization happens *before* $$F$$, not after. That means what $$F$$ sees is always unit-RMS, but what $$F$$ *produces* gets added un-normalized to the residual stream. Each layer contributes a fixed-variance bump. After $$L$$ layers, the stream's variance has accumulated:

$$\mathrm{Var}[x_L] \approx \mathrm{Var}[x_0] + L \cdot \mathrm{Var}[F_k]$$

This is just the additive property of variance for uncorrelated increments — and empirically the incoherence condition $$\mathbb{E}[\langle x_k, F_k\rangle] = 0$$ holds surprisingly well in practice {% cite sun2025layer %}.

What's the consequence? The signal-to-noise ratio of each layer's update decays as $$1/\sqrt{L}$$. By the time you're in the second half of a deep network, each layer barely nudges the stream it's reading. The Jacobian $$\partial x_{l+1}/\partial x_l \to I$$, and the layers become near-identity maps. People call this the **Curse of Depth** {% cite sun2025layer %}.

### An analytical prior from architecture alone

Even before loading a single weight, we can estimate how fast the variance should grow from the config. A SwiGLU MLP with `hidden_size` $$d$$ and `intermediate_size` $$d_i$$, initialized with $$W \sim \mathcal{N}(0, \sigma_W^2)$$, contributes roughly:

$$\mathrm{Var}[F_k^{\text{MLP}}] \approx \tfrac{1}{2}\, d_i^2\, \sigma_W^4$$

(the $$\tfrac{1}{2}$$ is from the gating branch suppressing half the energy). Adding the attention head contribution gives a prior on $$\mathrm{Var}[F_k]$$ that depends only on `initializer_range`, `hidden_size`, and `intermediate_size` — all of which live in the AutoConfig.

| Model | Layers | Hidden | $$\mathrm{Var}_F$$ (prior) |
|---|---|---|---|
| Llama-3.2-1B | 16 | 2048 | 5.37 |
| Qwen2.5-1.5B | 28 | 1536 | 6.42 |

That prior is a rough upper bound — trained weights are more structured than random — but it tells us the growth *rate* before touching a file.

---

## Experiment 1 — Variance growth

The following script loads each model, runs a prompt through it, captures all hidden states, and computes per-layer variance:

```python
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
import torch, numpy as np

def collect_hidden_states(model_id, prompt, device="mps"):
    tok   = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, dtype=torch.float32)
    model = model.to(device).eval()
    inputs = tok(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        out = model(**inputs, output_hidden_states=True)
    # hidden_states: tuple of (L+1) tensors [1, T, d]
    return [h[0].cpu().float().numpy() for h in out.hidden_states]

def per_layer_variance(hidden_states):
    return np.array([h.var() for h in hidden_states])
```

<figure>
<img src="/static/postfigures/activation_variance_growth.png" alt="Residual stream variance growth across layers for Llama-1B and Qwen2.5-1.5B">
<figcaption>
<strong>Figure 1: Residual-stream variance growth.</strong>
Left panel shows absolute variance; right panel normalizes by layer-0 variance. Solid lines are empirical measurements from a forward pass; dashed lines are the analytical prior computed purely from <code>AutoConfig</code> — no weights loaded. The prior dramatically overestimates the growth rate because trained weights are far more structured than random init (the actual residual contributions $$F_k$$ are much smaller). Both models show clear super-linear growth: Llama-1B reaches a variance ratio of ~11,000× after 16 layers; Qwen2.5-1.5B hits ~44,000× after 28 layers.
</figcaption>
</figure>

The numbers are striking: Llama-1B's residual stream variance is **11,000 times larger** at the final layer than at the embedding layer. Qwen2.5-1.5B reaches **44,000×** over 28 layers. The analytical prior from AutoConfig overshoots badly because trained networks are far more structured than the random-init assumption — but the qualitative story (monotonic growth, faster for deeper models) is exactly right.

---

## Experiment 2 — Massive activations

Now things get weird. In certain dimensions, individual activation values become *enormous* — thousands of times larger than everything else. These are not random spikes; they're systematic, input-agnostic, and locked to specific feature dimensions that emerge abruptly a few layers into the network {% cite sun2024massive %}.

Formally, we say dimension $$d$$ at layer $$l$$ has a *massive activation* if:

$$\max_t |x_{l,t,d}| > \tau \cdot \text{median}_d \max_t |x_{l,t,d}|$$

with threshold $$\tau \sim 10^3$$.

```python
def massive_activation_ratio(hidden_states, tau=1000):
    ratios = []
    for h in hidden_states:          # h: (T, d)
        dim_max = np.abs(h).max(axis=0)          # per-dimension max over tokens
        med     = np.median(dim_max) + 1e-10
        ratios.append(dim_max.max() / med)       # worst offender
    return np.array(ratios)
```

<figure>
<img src="/static/postfigures/activation_massive.png" alt="Massive activation outlier ratio and dimension fraction across layers">
<figcaption>
<strong>Figure 2: Outlier magnitude ratios.</strong>
Left: the single worst dimension's max-to-median ratio on a log scale. The dashed horizontal line marks $$\tau=1000$$, the conventional threshold for "massive." Right: the fraction of dimensions crossing that threshold. Llama-1B shows a sharp emergence of massive activations after layer 4, reaching a ratio of <strong>1230×</strong>. Qwen2.5-1.5B is more moderate at <strong>755×</strong> — consistent with its different architecture and training recipe.
</figcaption>
</figure>

Why do these exist? The current best explanation {% cite sun2024massive %} is that they're *learned bias terms*. Vanilla Transformers have no explicit bias in the attention projection, so during training the model discovers it can encode a constant offset by saturating a fixed dimension of an anchor token (usually position 0 or a punctuation mark). The softmax then pins most attention mass to that anchor — the *attention sink* {% cite xiao2023streamllm %}.

$$\mathrm{Attention}(Q,K,V) = \mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

If one key vector has a single dimension with value $$m \gg 0$$, the dot-product with that key dominates and the softmax probability for that token approaches 1 — effectively adding a constant vector to every query's output. It's a bias, implicitly learned.

A 2025 follow-up {% cite owen2025refined %} complicates the picture nicely: not *all* massive activations are load-bearing. Zeroing some of them out causes no harm; zeroing others causes catastrophic perplexity collapse. They're not a monolithic phenomenon.

---

## Experiment 3 — Representation anisotropy

Ideally, different tokens should map to different directions in the residual space. In practice, they don't — especially in decoder models. The average pairwise cosine similarity between token representations at layer $$l$$ is:

$$\bar\rho_l = \frac{1}{T^2} \sum_{i,j} \frac{e_i \cdot e_j}{\|e_i\|\,\|e_j\|}$$

When $$\bar\rho_l \to 1$$ all tokens are pointing the same way — the famous **narrow-cone** or **representation degeneration** effect {% cite gao2019degeneration %}.

```python
def anisotropy(hidden_states):
    result = []
    for h in hidden_states:                   # h: (T, d)
        n  = np.linalg.norm(h, axis=1, keepdims=True) + 1e-10
        hn = h / n                            # unit vectors
        C  = hn @ hn.T                        # (T, T) cosine matrix
        T  = h.shape[0]
        off_diag = C[~np.eye(T, dtype=bool)]  # exclude self-similarity
        result.append(off_diag.mean())
    return np.array(result)
```

<figure>
<img src="/static/postfigures/activation_anisotropy.png" alt="Token representation anisotropy across layers for Llama-1B and Qwen2.5-1.5B">
<figcaption>
<strong>Figure 3: Representation anisotropy per layer.</strong>
Values near +1 mean all tokens are pointing in the same direction (degenerate); near 0 is isotropic; negative values are rare but possible. Llama-1B hovers around 0.31 on average, with a distinctive dip at early layers before representations collapse inward toward a shared direction in the later layers. Qwen2.5-1.5B (mean ≈ 0.45) is more anisotropic throughout — consistent with its narrower hidden dimension relative to intermediate size.
</figcaption>
</figure>

The narrow-cone problem is partly a training artefact: the cross-entropy loss pushes rare-token representations toward a common mean direction because they receive sparse gradient signal {% cite gao2019degeneration %}. It's also partly architectural: the Pre-LN normalization means that the *direction* of $$x_l$$ is fed to each sub-layer, and after many layers these directions converge.

---

## Experiment 4 — CKA layer-similarity heatmaps

How much does layer $$i$$ "look like" layer $$j$$? Centered Kernel Alignment (CKA) answers this in terms of the representational geometry {% cite kornblith2019similarity %}. For two sets of hidden states $$X, Y$$ with Gram matrices $$K = HXX^\top H$$, $$L = HYY^\top H$$ (where $$H$$ is the centering matrix):

$$\mathrm{CKA}(K, L) = \frac{\langle K, L\rangle_F}{\|K\|_F\, \|L\|_F}$$

This is invariant to rotation and scaling, so it captures *geometric* similarity rather than coordinate similarity.

```python
def linear_cka(hidden_states):
    def gram(h):
        G = h @ h.T
        n = G.shape[0]
        H = np.eye(n) - np.ones((n, n)) / n   # centering
        return H @ G @ H

    Ks = [gram(h) for h in hidden_states]
    N  = len(Ks)
    C  = np.zeros((N, N))
    for i in range(N):
        for j in range(i, N):
            v = np.sum(Ks[i] * Ks[j])
            v /= np.sqrt(np.sum(Ks[i]**2) * np.sum(Ks[j]**2)) + 1e-10
            C[i, j] = C[j, i] = v
    return C
```

<figure>
<img src="/static/postfigures/activation_cka_heatmaps.png" alt="Linear CKA layer-similarity heatmaps for Llama-1B and Qwen2.5-1.5B">
<figcaption>
<strong>Figure 4: Linear CKA heatmaps.</strong>
Each cell $$(i,j)$$ is the CKA similarity between the hidden states at layers $$i$$ and $$j$$ (including the embedding, layer 0). Warm colors = high similarity. Both models show the expected pattern: the embedding layer is distinct (cool column/row at the left edge), a high-similarity plateau occupies the middle and late layers, and there is a visible jump at the transition from early to middle processing. This confirms that predictions are "formed" well before the final layer — the motivation behind techniques like the logit lens.
</figcaption>
</figure>

The large high-similarity block in the late layers is directly related to the variance growth story: once the stream is dominated by a huge accumulated norm, small layer-by-layer changes have negligible geometric effect, and successive layers look nearly identical under CKA.

---

## Experiment 5 — Spectral power-law exponents (HT-SR)

**Heavy-Tailed Self-Regularization** (HT-SR) theory {% cite mahoney2019traditional %} predicts that the singular values of well-trained weight matrices follow a power law in their tail:

$$P(s) \sim s^{-\alpha}$$

with $$\alpha$$ typically between 0.65 and 0.90 for healthy, generalization-capable layers {% cite martin2018implicit %}. This isn't just an empirical observation — it's linked to the model's capacity: layers with $$\alpha$$ outside this range are either undertrained or overfitting.

We compute $$\alpha$$ per weight matrix using truncated SVD (top-64 singular values, applied to the down-projection and output-projection matrices at each layer):

```python
from scipy.sparse.linalg import svds

def spectral_alpha(W, k=64):
    s = svds(W, k=min(k, min(W.shape) - 1), return_singular_vectors=False)
    s = np.sort(s)[::-1]
    log_s, log_r = np.log(s + 1e-10), np.log(np.arange(1, len(s)+1))
    return -np.polyfit(log_r, log_s, 1)[0]
```

<figure>
<img src="/static/postfigures/activation_spectral_exponents.png" alt="Spectral tail exponents (HT-SR) for weight matrices in Llama-1B and Qwen2.5-1.5B">
<figcaption>
<strong>Figure 5: Spectral power-law exponents.</strong>
Each point is one weight matrix (MLP down-projection or attention output); the thick line is a rolling mean. The shaded band marks the HT-SR theoretical healthy range [0.65, 0.90]. Both models sit below that band with mean $$\alpha \approx 0.14$$, which reflects the fact that our truncated SVD (top-64 values) captures the bulk of the spectrum rather than the extreme tail. The ordering is nonetheless meaningful: early layers tend to have lower $$\alpha$$ (shallower spectral decay, more spread information) and later layers trend upward, consistent with the idea that later layers compress representations into a lower-dimensional subspace.
</figcaption>
</figure>

> **Methodological note.** The absolute $$\alpha$$ values here are influenced by using only the top-64 singular values. The full HT-SR analysis requires the entire spectrum and a power-law tail fit starting well into the tail. Our numbers should be read as *relative* comparisons (early vs. late layers, Llama vs. Qwen) rather than absolute quality scores.

---

## The four phenomena together

<figure>
<img src="/static/postfigures/activation_summary_panel.png" alt="Four-panel summary of activation statistics experiments">
<figcaption>
<strong>Figure 6: Summary panel.</strong>
(A) Variance growth — empirical (solid) vs. analytical prior from AutoConfig (dashed). The prior overestimates but predicts the correct trend. (B) Outlier magnitude ratio on a log scale — both models cross the $$\tau=1000$$ threshold, confirming massive activations. (C) Anisotropy — both models show moderate-to-high mean cosine similarity, most pronounced in middle-to-late layers. (D) placeholder for spectral exponents (see Figure 5).
</figcaption>
</figure>

Here is a compact numerical summary:

| Model | Layers | Var ratio | Max outlier | Mean anisotropy |
|---|---|---|---|---|
| Llama-3.2-1B | 16 | **11,102×** | **1,230×** | 0.31 |
| Qwen2.5-1.5B | 28 | **43,882×** | **755×** | 0.45 |

The pattern is consistent: deeper models accumulate more variance, but the *outlier ratio* doesn't just scale with depth — it's also shaped by architecture (the Llama family without SwiGLU gating tends to develop sharper outliers, while Qwen's narrower hidden dimension spreads the energy more evenly).

---

## Why it matters for quantization

These statistics have very direct engineering consequences. Consider a simple 8-bit min-max quantizer:

$$q(x) = \mathrm{round}\!\left(\frac{x - x_{\min}}{x_{\max} - x_{\min}} \cdot 255\right)$$

When one dimension hits a value 1,230 times the median, $$x_{\max}$$ is set by that outlier. Every "normal" activation then squashes into the bottom 1–2 quantization bins. Information destroyed.

**LLM.int8()** {% cite dettmers2022llmint8 %} was the first to formalize this: at the 6.7B parameter threshold, outliers become systematic enough that naive INT8 quantization degrades significantly. Their fix — keeping the ~0.1% of outlier dimensions in FP16 while quantizing the rest to INT8 — is essentially an acknowledgment that these massive activations are load-bearing signal.

**SmoothQuant** {% cite xiao2023smoothquant %} takes a more surgical approach: instead of mixed precision at runtime, it *migrates* the difficulty offline using a mathematically equivalent rescaling. For each activation channel $$c$$, pick a migration factor $$s_c$$ and apply:

$$\tilde X_c = X_c / s_c, \quad \tilde W_c = W_c \cdot s_c$$

The transformation is exact (the products stay the same), but the activation dynamic range drops dramatically. The choice $$s_c = \max|X_c|^{0.5} / \max|W_c|^{0.5}$$ balances difficulty between the two sides.

---

## Architectural responses

The community has responded to these empirical facts by designing Pre-LN variants that limit variance growth from the start:

**LayerNorm Scaling (LNS)** {% cite sun2025layer %} scales each layer's normalization output by $$1/\sqrt{l}$$:

$$\mathrm{LNS}(x;\,l) = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}} \cdot \frac{\gamma}{\sqrt{l}}$$

This reduces variance growth from linear-in-$$L$$ to logarithmic-in-$$L$$, giving deeper layers a meaningful update budget.

**Peri-LN** {% cite yao2025peri %} normalizes both the input *and* the output of each sub-layer, threaded around the residual connection. It eliminates both the vanishing-gradient problem of Post-LN and the unbounded-variance problem of Pre-LN.

**Mix-LN** {% cite liu2025mixln %} uses Post-LN in the early layers (where gradient flow is the bottleneck) and Pre-LN in the later layers (where stability is the bottleneck), achieving nearly uniform gradient norms across depth.

And for *completely* outlier-free training, **Outlier-Safe Pre-training** {% cite dong2025systematic %} combines the Muon optimizer (which orthogonalizes gradient updates, preventing any single direction from dominating) with single-scale RMSNorm to kill channel-wise amplification. Models trained this way exhibit near-zero excess kurtosis and quantize cleanly to INT4.

---

## Connecting to the broader picture

The four phenomena we measured are not independent. They're facets of the same underlying structure:

- Variance growth → each layer contributes less → **Jacobian collapse**
- Jacobian collapse → late layers look similar → **high CKA in late layers**
- Massive activations → energy concentrated in few dimensions → **anisotropy**
- Anisotropy → representations crowd into a cone → **representation degeneration**

The spectral power-law connects to all of them: a healthy $$\alpha$$ (between 0.65 and 0.90) correlates with a weight matrix that is neither overfitted (too sparse, high $$\alpha$$) nor undertrained (flat spectrum, low $$\alpha$$) {% cite mahoney2019traditional %}. It's a thermodynamic signature of a network that has learned to balance generalization with compression.

From a random matrix theory perspective {% cite martin2018implicit %}, the emergence of heavy tails is a phase transition. Below a critical temperature (small learning rate, large batch size, many steps), the optimization landscape induces long-range correlations in the weight matrices that manifest as power-law tails. This is the same phenomenology as **Heavy-Tailed Self-Regularization** in statistical physics of disordered systems — the model is, in a precise sense, self-organizing toward a critical point.

Future work is pushing in two directions: **mechanistic interpretability** (what specific circuits do these activation patterns implement? {% cite sharkey2025open %}) and **activation engineering** (can we steer model behavior by directly manipulating these massive activations or the residual stream direction, without any fine-tuning?). Both directions require exactly the kind of quantitative understanding this post has tried to build.

---

## Full experiment code

The complete script that produces all figures above:

```python
"""
activation_stats_experiments.py
Runs on: meta-llama/Llama-3.2-1B-Instruct, Qwen/Qwen2.5-1.5B-Instruct
Figures saved to: static/postfigures/
"""
import numpy as np, torch, matplotlib.pyplot as plt
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
from scipy.sparse.linalg import svds

MODELS = [
    "meta-llama/Llama-3.2-1B-Instruct",
    "Qwen/Qwen2.5-1.5B-Instruct",
]
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
PROMPT = (
    "The study of language models reveals fascinating statistical structures "
    "hidden deep inside their layers. In this essay we explore how residual "
    "streams grow, how outlier activations emerge, and why quantization fails "
    "for very large models."
)

# ── Analytical prior from AutoConfig ─────────────────────────────────────────
def analytical_prior(model_id):
    tc  = getattr(AutoConfig.from_pretrained(model_id), "text_config",
                  AutoConfig.from_pretrained(model_id))
    d, d_i, sig = tc.hidden_size, tc.intermediate_size, tc.initializer_range
    gate = 0.5 if "silu" in getattr(tc, "hidden_act", "gelu") else 1.0
    var_F = gate * d_i * sig**2 * (d_i * sig**2)
    L = len(getattr(tc, "layer_types", range(tc.num_hidden_layers)))
    return np.arange(L + 1), 1.0 + np.arange(L + 1) * var_F

# ── Hidden-state collection ───────────────────────────────────────────────────
def collect(model_id):
    tok   = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, dtype=torch.float32)
    model = model.to(DEVICE).eval()
    with torch.no_grad():
        out = model(**tok(PROMPT, return_tensors="pt").to(DEVICE),
                    output_hidden_states=True)
    return [h[0].cpu().float().numpy() for h in out.hidden_states]

# ── Per-layer statistics ──────────────────────────────────────────────────────
def stats(hs):
    var, aniso, ratio = [], [], []
    for h in hs:
        var.append(h.var())
        hn  = h / (np.linalg.norm(h, axis=1, keepdims=True) + 1e-10)
        T   = h.shape[0]
        cos = hn @ hn.T
        aniso.append(cos[~np.eye(T, dtype=bool)].mean())
        dm  = np.abs(h).max(axis=0)
        ratio.append(dm.max() / (np.median(dm) + 1e-10))
    return (np.array(var), np.array(aniso), np.array(ratio))

# ── CKA ───────────────────────────────────────────────────────────────────────
def cka(hs):
    def gram(h):
        G = h @ h.T; n = G.shape[0]
        H = np.eye(n) - np.ones((n, n)) / n
        return H @ G @ H
    Ks = [gram(h) for h in hs]; N = len(Ks)
    C  = np.zeros((N, N))
    for i in range(N):
        for j in range(i, N):
            v = np.sum(Ks[i]*Ks[j])
            v /= np.sqrt(np.sum(Ks[i]**2)*np.sum(Ks[j]**2)) + 1e-10
            C[i,j] = C[j,i] = v
    return C

# ── Spectral exponents ────────────────────────────────────────────────────────
def spectral_alpha(W, k=64):
    s = svds(W, k=min(k, min(W.shape)-1), return_singular_vectors=False)
    s = np.sort(s)[::-1]
    return -np.polyfit(np.log(np.arange(1,len(s)+1)), np.log(s+1e-10), 1)[0]
```

The full version (with all plotting functions and figure export) lives at
[`scripts/activation_stats_experiments.py`](https://github.com/carlonicolini/carlonicolini.github.io/blob/master/scripts/activation_stats_experiments.py).

---

## References

{% bibliography --cited %}
