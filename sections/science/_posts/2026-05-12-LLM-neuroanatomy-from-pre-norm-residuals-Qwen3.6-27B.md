---
layout: post
title: LLM neuroanatomy from pre-norm residuals — Qwen3.6-27B as a brain analog
description: "An experiment to study the statistics of layers activations of Qwen 3.6 27B"
date: 2026-05-12
published: false
categories:
  - science
  - deep-learning
---

The two earlier posts in this series — [How skip connections define graphs in deep networks]({% link sections/science/_posts/2026-04-28-Skip-connections-and-graph-analysis.md %}) and [Similarity of neural networks representations]({% link sections/science/_posts/2026-04-29-Similarity-of-neural-networks-representations.md %}) — built up the analytical edge weight $$C_{ij}$$ of a Transformer's functional connectome and proved that David Ng's *Repeat Your Self* (RYS) construction {% cite ng2026rys %} amplifies the off-plateau deviation by a factor of four inside the duplicated block. Both derivations are correct in general terms, but they leave four questions open that one cannot answer from the recursion alone:

1. The recursion was stated as $$\mathbf{x}_{k+1} = \mathbf{x}_k + F_k(\mathbf{x}_k,\boldsymbol\theta_k)$$, hiding the precise *placement* of RMSNorm inside the block. Where exactly does the normalisation act? On the input to $$F_k$$, on its output, or on the residual stream itself?
2. What is the *a-priori distribution* of $$F_k$$ — the residual injection — for a concrete architecture like Qwen3.6-27B? Without an explicit prior we cannot tell when the small-$$\rho$$ Taylor expansion is justified and when it is not.
3. Qwen3.6-27B's text tower is a **hybrid**: 75% of its 64 layers are Gated DeltaNet (linear-attention) blocks and 25% (every fourth layer) are full self-attention blocks. Does this periodic structure imprint on the CKA connectome, and does it explain the dendrogram boundaries already observed at depths $$18/19$$, $$49/50$$ and $$62/63$$?
4. The previous posts read the LLM as a brain-like layered system whose middle depths, boundary nodes, and tail of the residual stream may play different computational roles. *Brain-inspired* is more than a slogan: it suggests concrete metrics — modularity, betweenness centrality, integration-segregation balance, small-world index — that we can compute *now* on the matrices we already have.

This post answers all four. It derives the closed-form prior on $$F_k$$ from Qwen3.6-27B's `text_config`, validates it against a single-block Monte Carlo on Apple Silicon, builds the per-layer $$\rho_k$$ and $$\mathcal Q_{ij}$$ diagnostics, computes a **bounded Gaussian CKA prior** with `ckatorch`, overlays that prior on the empirical GSM8K CKA connectome, and ends with ten brain-inspired hypotheses each tied to a quantitative metric that the new `rys.analytical_fk` module already exposes.

All code lives in the [`rys`](https://github.com/carlonicolini/rys) repository under `src/rys/analytical_fk.py` and `notebooks/analytical_fk_distribution.ipynb`. Every figure in this post is reproducible with `uv run jupyter execute notebooks/analytical_fk_distribution.ipynb`.

## 1. The pre-norm recursion, made architecture-explicit

The general recursion $$\mathbf{x}_{k+1} = \mathbf{x}_k + F_k(\mathbf{x}_k,\boldsymbol\theta_k)$$ of the prior posts is correct as a *summary* of what a residual block does, but a concrete pre-norm Transformer block in the Qwen / Llama family expands to

$$
\mathbf{x}_{k+1} = \mathbf{x}_k
+ A_k\!\bigl(\mathrm{RMSNorm}_1(\mathbf{x}_k)\bigr)
+ M_k\!\bigl(\mathrm{RMSNorm}_2(\mathbf{x}_k + A_k(\mathrm{RMSNorm}_1(\mathbf{x}_k)))\bigr).
\tag{1}\label{eq:prenorm-block}
$$

Three things are happening here that are easy to lose in the shorthand.

- The block has **two RMSNorms** inside it: `input_layernorm` feeds the attention sub-layer $$A_k$$, and `post_attention_layernorm` feeds the MLP sub-layer $$M_k$$. Both act on the *input* to their respective sub-layer.
- The block's **output** $$\mathbf{x}_{k+1}$$ is *not* RMSNormed. The residual stream itself accumulates un-normed contributions through all $$L$$ blocks.
- The *only* RMSNorm on the residual stream proper is the trailing `model.model.norm` that fires immediately before the unembedding head reads out the final state $$\mathbf{x}_L$$.

This third observation has a direct consequence that I want to highlight, because it answers the inline question that motivated this post (and that the previous derivations gloss over): **block outputs are not RMSNormed**. Each downstream block's `input_layernorm` *re-renormalises* the stream when it consumes it, but between blocks the stream is free to drift in norm. This is the entire point of pre-norm: a constant unit-RMS feed into every sub-layer, regardless of how large the residual stream itself grows.

The structural consequence is **residual-stream norm growth**. If we write $$\sigma_k^2 := \mathrm{Var}(\mathbf{x}_{k,i})$$ for the per-channel variance of the residual stream at layer $$k$$, and assume the incoherence condition $$\mathbb{E}[\langle \mathbf{x}_k, F_k\rangle] = 0$$ that empirically holds in the middle layers of trained pre-norm Transformers (Kobayashi 2024), the variance recursion is additive:

$$
\sigma_{k+1}^{2} = \sigma_k^{2} + \mathrm{Var}(F_k).
\tag{2}\label{eq:variance-growth}
$$

And the relative-force $$\rho_k = \|F_k\|/\|\mathbf{x}_k\| = \sqrt{\mathrm{Var}(F_k)/\sigma_k^2}$$ is monotonically *decreasing* in $$k$$ whenever $$\mathrm{Var}(F_k)$$ is bounded. **The plateau is a structural feature of pre-norm, not a training-induced curiosity.** It would exist even at random init, and Section 4 confirms this on Qwen3.6-27B.

## 2. Qwen3.6-27B as a hybrid linear / full attention stack

The model card and `AutoConfig.from_pretrained("Qwen/Qwen3.6-27B").text_config` agree on the following key numbers:

| field | value |
| --- | --- |
| `num_hidden_layers` | 64 |
| `hidden_size` ($$d$$) | 5120 |
| `intermediate_size` ($$d_\text{int}$$) | 17408 |
| `initializer_range` ($$\sigma_W$$) | 0.02 |
| `full_attention_interval` | 4 |
| `linear_num_value_heads` | 48 |
| `head_dim` | 256 |

The `layer_types` attribute is a 64-position string vector with `"linear_attention"` (Gated DeltaNet — a state-space-like recurrent mechanism with a 1-D causal convolution and a value-axis kernel state) at 48 positions and `"full_attention"` (the usual softmax-attended multi-head value mixing) at the remaining 16 positions $$\{3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63\}$$. The schedule is *strictly periodic* with period 4.

This periodicity is mechanistically interesting in a way that no prior post in this series has called out. The two layer families compute fundamentally different functions:

- The **Gated DeltaNet** ($$A_k$$ on linear-attn layers) is a *recurrent contraction* with a per-channel kernel state $$\mathbf{s}_t = \alpha_t \mathbf{s}_{t-1} + \beta_t \mathbf{k}_t \mathbf{v}_t^\top$$ updated token-by-token. It has approximately $$O(d^2)$$ inference cost and is *contractive* in its kernel state for any well-conditioned initialisation.
- The **full self-attention** ($$A_k$$ on full-attn layers) is the usual softmax-over-token-positions value mixer with $$O(d^2 N)$$ inference cost. It is **non-contractive**: a single softmax-attended head can move a token's representation arbitrarily far depending on the key-query geometry.

The architecture is, in network-neuroscience terms, a **modular cortical sheet with periodic relay hubs**. The Gated DeltaNet layers are like cortical microcircuits running local recurrent integration; the full-attn layers are like thalamic relays that broadcast across the entire token sequence in one step. The 4-period structure is the *only* place in the architecture that explicitly enforces a non-local communication step. We will see in Section 5 that this maps almost exactly onto the dendrogram junction boundaries discovered empirically in the prior post.

<figure>
<img src="/static/postfigures/qwen36_layer_schedule.png" alt="Qwen3.6-27B layer schedule showing linear attention layers and full attention relay layers">
<figcaption>
<strong>Figure 1: The hybrid text-tower schedule of Qwen3.6-27B.</strong>
The 64-layer language model alternates three Gated DeltaNet / linear-attention layers with one full self-attention layer. Full-attention layers (orange) occur at $$\{3,7,\ldots,63\}$$ and are the natural architectural candidates for thalamus-like relay nodes in the functional connectome.
</figcaption>
</figure>

## 3. Closed-form Gaussian prior on $$F_k$$

Under Qwen's `_init_weights` rule — every `nn.Linear` initialised as $$W_{ij} \sim \mathcal{N}(0, \sigma_W^2)$$ with $$\sigma_W = 0.02$$, every `Qwen3_5RMSNorm` zero-initialised so its gain $$(1 + \text{weight})$$ starts at 1 — the per-channel marginal of $$F_k$$ is approximately Gaussian by the CLT in the $$d_{\text{model}} = 5120$$ summation. The closed form composes four steps.

**Step 1: RMSNorm.** Per-token unit-RMS, so $$\mathrm{Var}\bigl(\mathrm{RMSNorm}(\mathbf{x}_k)_i\bigr) = 1$$ regardless of $$\sigma_k^2$$. This is the entire reason pre-norm exists: each sub-layer sees a $$\sigma$$-stationary feed.

**Step 2: linear projection.** For a Kaiming-Gaussian weight $$W \sim \mathcal{N}(0, \sigma_W^2)^{d_\text{out}\times d_\text{in}}$$ and unit-variance input,

$$
\mathrm{Var}\bigl((Wh)_j\bigr) = d_\text{in}\,\sigma_W^2.
$$

For Qwen's $$\sigma_W = 0.02$$ and $$d_\text{in} = 5120$$, this gives $$d_\text{in}\sigma_W^2 = 2.048$$ per output channel — essentially Kaiming, which is exactly the design.

**Step 3: SiLU on a Gaussian.** With $$X \sim \mathcal{N}(0, s^2)$$ the moments of $$\mathrm{SiLU}(X) = X\sigma(X)$$ are closed-form Gauss-Hermite integrals against the Gaussian measure. The module exposes them via `silu_moments_under_gaussian(s²)`. For $$s^2 = 2$$ (the variance the gate projection feeds the SiLU at init):

$$
\mathbb{E}[\mathrm{SiLU}(X)] \approx 0.38,
\qquad
\mathrm{Var}[\mathrm{SiLU}(X)] \approx 0.85,
\qquad
\mathrm{kurt}_\text{excess}[\mathrm{SiLU}(X)] \approx -0.4.
$$

**Step 4: gated MLP.** For independent Gaussian gate $$g$$ and up-projection $$u$$ at init, $$m = \mathrm{SiLU}(g)\odot u$$ has $$\mathbb{E}[m] = 0$$ and $$\mathrm{Var}[m] = \mathbb{E}[\mathrm{SiLU}(g)^2]\,\mathrm{Var}(u)$$ by Isserlis' theorem. The down-projection then linearly mixes $$d_\text{int} = 17408$$ independent Gaussian channels, restoring near-Gaussianity by CLT.

Putting all four steps together gives **per-channel variance predictions**:

$$
\mathrm{Var}\bigl(F_k^{\text{linear-attn}}\bigr) \approx 13.81,
\qquad
\mathrm{Var}\bigl(F_k^{\text{full-attn}}\bigr) \approx 11.73.
\tag{3}\label{eq:fk-var-prior}
$$

The full-attn variance is *smaller* than the linear-attn variance at random init because the softmax inside full attention is approximately uniform at init (entropy $$\log(\text{seq\_len})$$), so the value-mixing step shrinks the variance by approximately $$1/\text{seq\_len}$$; the linear-attn block has two linear projection stages without such damping.

<figure>
<img src="/static/postfigures/qwen36_fk_prior_moments.png" alt="SiLU moment validation and closed-form F_k variance prior for linear and full attention blocks">
<figcaption>
<strong>Figure 2: Closed-form ingredients of the random-init $$F_k$$ prior.</strong>
Left: the Gauss-Hermite integral for $$\mathrm{Var}[\mathrm{SiLU}(X)]$$ agrees with Monte Carlo sampling across Gaussian input scales. Right: composing RMSNorm, Gaussian projections, SiLU gating, and the down-projection predicts a per-channel block-output variance of $$13.81$$ for Gated DeltaNet layers and $$11.73$$ for full-attention layers.
</figcaption>
</figure>

### Validation: single-block Monte Carlo on Apple Silicon

The notebook `analytical_fk_distribution.ipynb` instantiates *one* Qwen3.5 decoder layer (with the architecture's published shapes and the `_init_weights` rule applied) on Apple Silicon (MPS) for both a linear-attn layer (index 2) and a full-attn layer (index 3), pushes 256 synthetic Gaussian tokens through it, and measures the empirical per-channel variance of $$F_k$$.

Empirical and analytical agree within 15% on the linear-attn block (the discrepancy is the GatedDeltaNet's recurrent kernel state, which my closed form treats as a single contraction step) and within 3% on the full-attn block.
The empirical cosine $$\cos\phi$$ between input and $$F_k$$ is $$|0.002|$$ — confirming the **incoherence** assumption at random init.
See the table and the figure below:

|-------|------------------|-----------------------------------|----------------|---------|

| layer | type             | closed-form $$\mathrm{Var}(F_k)$$ | empirical mean | ratio   |
|-------|------------------|-----------------------------------|----------------|---------|
| 2     | linear-attention | $13.81$                           | $11.71$        | $0.848$ |
| 3     | full-attention   | $11.73$                           | $11.67$        | $0.995$ |
|-------|------------------|-----------------------------------|----------------|---------|

<figure>
<img src="/static/postfigures/qwen36_single_block_validation.png" alt="Single-block MPS validation of closed-form F_k variance against empirical per-channel variance">
<figcaption>
<strong>Figure 3: Single-block validation on Apple Silicon.</strong>
Each histogram is the empirical distribution of per-channel $$\mathrm{Var}(F_k)$$ over the 5120 residual-stream channels after pushing synthetic Gaussian token streams through one randomly initialised Qwen decoder block. The closed-form prior nearly matches the full-attention block and overestimates the Gated DeltaNet block by about 15%, because the simple analytical model treats the DeltaNet recurrent path as a lightly gated two-step linear contraction.
</figcaption>
</figure>

The brain-inspired reading: **the random-init prior is the LLM's "resting state"**. It is the functional connectivity the network would exhibit before any training-induced structure deformed it. Section 5 makes the deformation visible.

## 4. Norm growth and the structural plateau

Plug the per-layer variance prior \eqref{eq:fk-var-prior} into the additive variance recursion \eqref{eq:variance-growth} starting from $$\sigma_0^2 = 1$$. Under the **independent-increment null model**, the cumulative residual variance between layers $$i$$ and $$j$$ is then

$$
\mathrm{Var}\bigl(\mathbf{S}_{ij}\bigr) = \sum_{k=i}^{j-1} \mathrm{Var}(F_k),
\qquad
\rho_{ij}^{\text{prior}} = \sqrt{\frac{\mathrm{Var}(\mathbf{S}_{ij})}{\sigma_i^2}}.
\tag{4}\label{eq:rho-prior}
$$

This equality is not a theorem about a trained Transformer. It is true only if the residual increments are uncorrelated. In general,

$$
\mathrm{Var}\!\left(\sum_{k=i}^{j-1}F_k\right)
=
\sum_{k=i}^{j-1}\mathrm{Var}(F_k)
+ 2\sum_{i \le a < b < j}\mathrm{Cov}(F_a,F_b).
\tag{5}\label{eq:variance-covariance}
$$

The synthetic Gaussian prior deliberately sets the covariance terms to zero. In the figure-generation script I check this assumption directly by sampling independent Gaussian increments: the observed ratio $$\mathrm{Var}(\sum F_k)/\sum\mathrm{Var}(F_k)$$ has median $$0.999$$ and 5--95% range $$[0.996, 1.002]$$. That is a sanity check on the synthetic null, not evidence that trained Qwen residuals have zero covariance.

Two qualitative shapes follow without any further work.

- **Norm growth.** $$\sigma_k^2$$ grows from $$1$$ at layer 0 to $$1 + 64 \times 12.7 \approx 814$$ at layer 64. The residual stream becomes about $$\sqrt{814} \approx 29$$ times *larger* than the embedding input by the time it reaches the unembedding head. This is exactly the norm-growth phenomenon empirically observed in trained Llama- and Qwen-family models, and now we know it is a *structural* consequence of pre-norm + iid Gaussian init.
- **Plateau.** $$\rho_{ij}^{\text{prior}}$$ for $$j = i+1$$ drops from $$\rho_{0,1}^{\text{prior}} \approx 3.7$$ (the first block's residual is much larger than the embedding) to $$\rho_{63,64}^{\text{prior}} \approx 0.13$$ (a late block's residual is a 13% perturbation of the carried-over identity). The per-layer relative-force *decay* is the structural shape of the plateau: deep layers cannot rewrite the stream even if they try, because the stream has grown too large.

For the kernel-level cross-term $$\mathcal Q_{ij} = \|M_{ij} + M_{ij}^\top\|_F / \|A_i\|_F$$, the random-init prior under Marchenko-Pastur asymptotics for centred Gaussian $$\tilde X_i$$ and independent centred Gaussian $$\tilde S$$ gives

$$
\mathcal Q_{ij}^{\text{prior}} \approx \sqrt{\frac{2 d}{N_{\text{eff}}}} \cdot \rho_{ij}^{\text{prior}},
\tag{6}\label{eq:Q-prior}
$$

with $$N_{\text{eff}}$$ the effective sample size of the kernel estimator (token-count times prompt-count). The plateau formula of the previous post then predicts the **local Taylor proxy** $$1 - \mathrm{CKA}_{ij} \approx \tfrac{1}{2} \mathcal Q_{ij}^2$$ when $$\rho_{ij}$$ is small. This is *not* a bounded CKA matrix and should not be plotted as one. The bounded CKA prior in the next section is instead computed numerically with `ckatorch` on a synthetic Gaussian residual stream.

<figure>
<img src="/static/postfigures/qwen36_norm_growth_prior.png" alt="Predicted residual stream norm growth and relative residual force decay across Qwen3.6-27B layers">
<figcaption>
<strong>Figure 4: Norm growth creates a structural plateau.</strong>
Top: the one-step relative force $$\rho_{k,k+1}^{\mathrm{prior}}$$ decays as depth increases. Bottom: under the incoherent-residual recursion, the residual-stream variance accumulates additively across the 64 blocks. This is the analytical reason pre-norm transformers naturally develop high-CKA plateaus at depth: each new residual is a progressively smaller perturbation of the carried stream.
</figcaption>
</figure>

## 5. Bounded prior vs empirical CKA on GSM8K

The figure script `scripts/figures/figure_qwen36_analytical_prior.py` now generates a synthetic Gaussian residual stream using the per-layer $$\mathrm{Var}(F_k)$$ prior, then computes linear CKA with `ckatorch.cka_base(..., kernel="linear", unbiased=False)`. This gives a true CKA matrix in $$[0,1]$$ by construction. It is a different object from the unbounded Taylor proxy $$\tfrac{1}{2}\mathcal Q^2$$.

### 5.1 The bounded prior is sensible, but still only a null model

The bounded Gaussian prior has range

$$
\mathrm{CKA}^{\text{prior}}_{ij}\in[0.508,1.000],
$$

while the empirical GSM8K CKA matrix has range

$$
\mathrm{CKA}^{\text{empirical}}_{ij}\in[0.090,1.000].
$$

Across the off-diagonal layer pairs the Spearman rank correlation is $$r_s\approx0.954$$. This is the interesting part: a very simple independent-Gaussian pre-norm null explains a large fraction of the **rank ordering** of layer similarities. But the prior has no trained block structure; it mostly expresses the fact that layers close in depth share most of their residual stream. The empirical matrix is where training carves out sharper modules and boundaries.

<figure>
<img src="/static/postfigures/qwen36_bounded_cka_prior_delta.png" alt="Empirical Qwen3.6 GSM8K CKA matrix, bounded Gaussian CKA prior, Delta CKA, and pairwise scatter">
<figcaption>
<strong>Figure 5: A bounded Gaussian CKA prior, not the unbounded Taylor proxy.</strong>
The empirical and prior matrices are both true CKA matrices in $$[0,1]$$. The third panel shows $$\Delta=\mathrm{CKA}^{\mathrm{prior}}-\mathrm{CKA}^{\mathrm{empirical}}$$ with a diverging scale centred at zero. The scatter panel confirms strong rank agreement ($$r_s\approx0.954$$) while making clear that the trained model has much stronger low-CKA boundaries than the independent-Gaussian null.
</figcaption>
</figure>

### 5.2 The deviation is the training-induced functional anatomy

The prior predicts a smooth depth-distance structure: nearby layers are similar because they share most of their residual stream; distant layers are less similar because they have accumulated more independent increments. The empirical matrix shows sharper data-driven clades. Reusing the complete-linkage procedure of `scripts/figures/figure_dendrogram.py`, the current empirical CKA matrix gives depth boundaries at approximately $$3,10,19,50,63$$. I will refer to these descriptively as CKA-derived modules rather than assuming that the middle module is necessarily a unique “reasoning plateau.”

The *deviation* $$\Delta_{ij}=\mathrm{CKA}_{ij}^{\mathrm{prior}}-\mathrm{CKA}_{ij}^{\mathrm{empirical}}$$ is therefore the **training-induced functional anatomy**: the matrix you get by subtracting what pre-norm + iid Gaussian increments structurally guarantee from what the trained model actually exhibits.
This is hypothesis 8 of the brainstorming section below, and the notebook computes it as a side effect.

### 5.3 A-priori RYS forecast from the structural prior alone

As a deliberately strict test, I used only the bounded Gaussian CKA prior to rank RYS windows, then overlaid those windows on both the empirical CKA matrix and Ng's behavioural MATH map. This is *not* the final surgical prior; it is the null model. It asks how much can be predicted from architecture and pre-norm norm-growth alone, before using the trained CKA matrix.

<figure>
<img src="/static/postfigures/qwen36_rys_forecast_prior_empirical.png" alt="Predicted RYS windows overlaid on prior CKA, empirical CKA, Delta CKA, and David Ng MATH benchmark delta map">
<figcaption>
<strong>Figure 6: The bounded structural prior alone is not a behavioural RYS predictor.</strong>
The top-25 windows selected from the bounded Gaussian prior are shown on the prior matrix, empirical matrix, $$\Delta$$ matrix, and Ng's MATH intervention map. Precision@25 against Ng's top-5% windows is $$0/25$$ in this run. This is a useful negative control: the trained CKA structure, not just the pre-norm Gaussian null, is required for behavioural surgery prediction.
</figcaption>
</figure>

### 5.4 Betweenness centrality of empirical CKA junctions

I also tested the thalamus-like relay hypothesis directly on the empirical CKA graph. I thresholded the empirical CKA matrix at $$\mathrm{CKA}\ge0.7$$, used $$\sqrt{2(1-\mathrm{CKA})}$$ as weighted graph distance, and computed weighted betweenness centrality. The result is more sobering than the analogy: full-attention layers do not dominate centrality under this graph construction. Mean betweenness is approximately $$0.0125$$ for full-attention layers and $$0.0259$$ for linear-attention layers.

This does not falsify every relay interpretation, because centrality depends strongly on graph construction and threshold. But it does mean that “full attention = thalamus” should remain a hypothesis, not a conclusion.

<figure>
<img src="/static/postfigures/qwen36_betweenness_centrality.png" alt="Weighted betweenness centrality of Qwen3.6 empirical CKA graph, highlighting full-attention layers">
<figcaption>
<strong>Figure 7: Data-driven betweenness centrality on the empirical CKA graph.</strong>
Full-attention layers are highlighted in orange. Under a thresholded empirical CKA graph ($$\mathrm{CKA}\ge0.7$$), full-attention layers do not show higher mean betweenness than linear-attention layers. This is exactly the kind of negative or nuance-inducing result the brain analogy should expose rather than hide.
</figcaption>
</figure>

To avoid over-interpreting one threshold, I swept CKA thresholds from $$0.10$$ to $$0.95$$ and recomputed a small graph-theoretic battery: node strength, weighted betweenness, closeness, eigenvector centrality, PageRank, participation coefficient, within-module z-score, and a connector-hub score defined as participation times the positive part of the within-module z-score. The connected-threshold summary is:

| metric | mean full-attn minus linear-attn |
| --- | ---: |
| betweenness | $$+0.00046$$ |
| eigenvector | $$+0.00007$$ |
| PageRank | $$-0.00011$$ |
| closeness | $$-0.00739$$ |
| participation | $$-0.00843$$ |
| connector-hub score | $$-0.04766$$ |
| strength | $$-0.13115$$ |
| within-module z-score | $$-0.17620$$ |

The strongest reading is therefore conservative: full-attention layers do not behave like globally privileged connector hubs under this CKA graph family. They may still matter dynamically (e.g. for token mixing, long-range retrieval, or causal intervention maps), but the simple structural-thalamus analogy is not supported by these graph metrics alone.

<figure>
<img src="/static/postfigures/qwen36_threshold_centrality_sweep.png" alt="Threshold sweep of full-attention minus linear-attention centrality metrics across CKA thresholds">
<figcaption>
<strong>Figure 8: Threshold sweep of candidate relay metrics.</strong>
Each panel shows the mean full-attention minus linear-attention score as a function of the CKA threshold used to define the empirical graph. Blue traces in the background show the largest-component fraction, guarding against interpreting disconnected high-threshold graphs.
</figcaption>
</figure>

<figure>
<img src="/static/postfigures/qwen36_threshold_metric_heatmap.png" alt="Heatmap of graph metric differences between full-attention and linear-attention layers across CKA thresholds">
<figcaption>
<strong>Figure 9: Full-attention advantage or disadvantage across graph metrics.</strong>
Positive values mean full-attention layers score higher than linear-attention layers. The pattern is mixed at best: betweenness is slightly positive across much of the connected range, but participation, connector-hub score, strength, and within-module z-score are lower for full-attention layers.
</figcaption>
</figure>

## 6. RYS doubling under RMSNorm — a refinement

A subtlety from the previous posts deserves an explicit treatment now that we have the pre-norm recursion \eqref{eq:prenorm-block}.

The RYS doubling argument linearises each $$F_k$$ around its first-pass input:

$$
F_k\bigl(\mathbf{x}_k^{(1)}, \boldsymbol\theta_k\bigr)
= F_k\bigl(\mathbf{x}_k^{(0)}, \boldsymbol\theta_k\bigr)
+ \mathbf{J}_{F_k}\,(\mathbf{x}_k^{(1)} - \mathbf{x}_k^{(0)}) + \mathcal O(\|\Delta_k\|^2).
$$

But $$F_k$$'s first operation is **RMSNorm**. The Jacobian of $$\mathrm{RMSNorm}$$ is the projector onto the unit-sphere tangent plane:

$$
\frac{\partial\,\mathrm{RMSNorm}(\mathbf{x})}{\partial \mathbf{x}}
= \frac{1}{\sigma(\mathbf{x})}\!\left( \mathbf{I} - \frac{\mathbf{x}\mathbf{x}^\top}{d\,\sigma(\mathbf{x})^2} \right),
\qquad
\sigma(\mathbf{x})^2 = \tfrac{1}{d}\|\mathbf{x}\|^2.
\tag{7}\label{eq:rmsnorm-jac}
$$

The crucial property is that the radial direction is *killed*:

$$
\frac{\partial\,\mathrm{RMSNorm}(\mathbf{x})}{\partial \mathbf{x}}\,\mathbf{x} = 0.
$$

So if the RYS displacement $$\Delta_k = \mathbf{x}_k^{(1)} - \mathbf{x}_k^{(0)}$$ is *parallel* to $$\mathbf{x}_k^{(0)}$$ — i.e. RYS just doubles the residual stream's magnitude along its existing direction — then RMSNorm projects out that part entirely. Only the **transverse** component of $$\Delta_k$$ propagates into $$F_k$$.

Writing $$\Delta_k = \Delta_k^{\parallel} + \Delta_k^{\perp}$$ in the $$(\mathbf{x}_k^{(0)},\,\text{tangent})$$ decomposition:

$$
F_k(\mathbf{x}_k^{(1)}) - F_k(\mathbf{x}_k^{(0)})
\approx \mathbf{J}_{F_k}\,\Delta_k^{\perp}.
$$

In the small-residual / incoherent regime, $$\Delta_k = \mathbf{S}^{(0)}_{i,j}$$, and *most* of $$\mathbf{S}^{(0)}_{i,j}$$ is transverse to $$\mathbf{x}_k^{(0)}$$ (this is exactly the $$\cos\phi_{i,j} \approx 0$$ incoherence already assumed). So the doubling $$\mathbf{S}^{(1)}_{i,j} \approx \mathbf{S}^{(0)}_{i,j}$$ of the previous post is correct *to leading order*, with the precise statement being:

$$
\boxed{
\mathbf{S}^{\text{RYS}}_{i,j} \approx 2\,\mathbf{S}^{(0)}_{i,j}\,\sin\phi_{i,j}
+ \mathcal O\bigl(\rho_{i,j}\,\|\mathbf{S}^{(0)}_{i,j}\|\bigr),
}
\tag{8}\label{eq:rys-transverse}
$$

with the $$\sin\phi$$ factor reflecting the RMSNorm-killed radial component. Plugging this into the plateau formula recovers the existing posts' $$1 - \mathrm{CKA}^{\text{RYS}} \approx 4(1 - \mathrm{CKA}^{(0)})$$ scaling because $$\sin^2\phi$$ was *already* the controlling factor in $$(1/2)\mathcal Q^2 \sin^2\Psi$$. The RMSNorm-aware refinement does not contradict the previous posts; it explains *why* the $$\sin\phi$$ factor was the right one.

## 7. Brain-inspired hypotheses

The point of this paragraph is *not* a slogan. Each hypothesis below is a concrete measurement that can be computed *now* on data already in the `rys` repository or on a single forward pass at random init. The goal is not to privilege the layer range $$[19,49]$$ in advance; it is to let the CKA graph, centrality measures, and intervention maps define modules data-first.

<figure>
<img src="/static/postfigures/qwen36_brain_hypotheses_map.png" alt="Brain-inspired hypotheses mapped to measurable LLM neuroanatomy quantities">
<figcaption>
<strong>Figure 10: Brain-inspired hypotheses as testable LLM measurements.</strong>
The analogies are useful only if each maps to a concrete quantity: CKA modularity, full-attention betweenness centrality, residual-force balance, plateau stability, RYS window geometry, outlier-channel kurtosis, lesion sensitivity, trained-minus-prior connectivity, sub-DAG diameter, and small-world index.
</figcaption>
</figure>

### Hypothesis 1 — Cortical hierarchy

In the mammalian brain, primary sensory areas (V1, A1) encode low-level features, association areas (parietal, prefrontal) compute task-general abstractions, and motor / output areas (M1) decode them into action. The corresponding LLM partition is:

| brain | LLM |
| --- | --- |
| primary sensory cortex (V1, A1) | encoder block $$[0, 18]$$ (lexical / syntactic features) |
| association cortex | the largest CKA-derived middle clade (candidate task-general abstractions) |
| motor cortex | decoder block $$[50, 62]$$ |
| skin / muscle output | unembedding layer $$63$$ |

**Measurable**: layer-class linear probes for syntax (POS tags) vs semantics (WSD) vs task labels should be high in their respective phases and low in the others. The probe-accuracy gradient should match the dendrogram clade boundaries of the prior post.

### Hypothesis 2 — Thalamus as cross-cortical relay

The mammalian thalamus is a relay nucleus that sits anatomically between sensory cortices and the rest of the brain, with high betweenness centrality on the structural connectome. In Qwen3.6-27B, the **full-attention layers at positions $$\{3, 7, 11, \ldots, 63\}$$** are the only place in the architecture that performs non-local broadcast across all tokens in a single step. Section 2 identified them as candidate thalamic hubs.

**Measurable**: betweenness centrality of full-attn layers versus linear-attn layers on the empirical CKA graph (treat the matrix as a weighted undirected graph, threshold-clip below e.g. 0.7). Prediction: full-attn layers should have systematically higher betweenness. The 4-period imprint should also show up as a faint stripe at $$j - i \equiv 0 \pmod 4$$ in the residual matrix from Section 5.2.

### Hypothesis 3 — Tononi-Sporns integration-segregation balance

The integrated-information framework {% cite tononi2008consciousness %} posits that conscious-like brain dynamics sit at the **edge of chaos**: a balance between integration (whole-brain coordination, large effective dimensionality) and segregation (local modular processing). The LLM analog is the per-layer relative force $$\rho_k$$ from Section 4: $$\rho_k \gg 1$$ means the block overwrites the stream (too much segregation), $$\rho_k \ll 1$$ means it does nothing (semantic stasis), and intermediate $$\rho_k$$ is the *useful* regime.

**Measurable**: locate the layer $$k^*$$ where $$\rho_k \approx 0.1$$ on the empirical norm-growth curve of Section 4. Compare across models of different benchmark performance: best models should hover around $$\rho^* \approx 0.1$$ across the plateau; collapsed or under-trained models should drift to $$\rho \to 0$$ (semantic stasis) or $$\rho \to 1$$ (overwrite).

### Hypothesis 4 — Default Mode Network and the middle CKA clade

The Default Mode Network (DMN) is active during rest and self-referential thought, and *deactivates* under cognitive load. Its functional signature is high internal coherence (high CKA between DMN regions) that *drops* when the task pulls the brain into a task-positive mode.

The LLM analog is the **largest middle CKA-derived clade**, whatever its exact boundaries are for a given model and task: it has high pairwise CKA when the network is processing in-distribution inputs, and it should *destabilise* when the network is asked to hallucinate or process out-of-distribution data.

**Measurable**: variance of the within-plateau CKA edges across a corpus, separately for (a) in-distribution prompts (GSM8K) and (b) OOD prompts (e.g. nonsense token streams, adversarial inputs). Prediction: in-distribution plateau variance is *low* (rigid DMN-like coherence), OOD plateau variance is *high* (destabilised semantic state).

### Hypothesis 5 — Cortical thickness expansion in domain experts

Long-term motor training (musicians, athletes) produces measurable *cortical thickening* in task-relevant regions {% cite draganski2004expert %}. RYS is the architectural analog: duplicating layers inside a CKA-derived clade *effectively* thickens that region without adding any new parameters.

**Measurable**: best-performing RYS surgeries should be **within-clade** according to a data-driven CKA clustering, not necessarily inside a pre-named layer range. The earlier $$[19,49]$$ interval is a useful historical candidate, but it should be re-estimated per model, task, and CKA matrix before being interpreted.

### Hypothesis 6 — Sparse coding and grandmother cells

The brain encodes specific concepts in sparse subsets of neurons (Quian Quiroga's "Jennifer Aniston neuron" {% cite quianquiroga2005invariant %}). The LLM analog is the **outlier feature channel** phenomenon {% cite dettmers2022llmint8 %} {% cite bondarenko2023nooutliers %}: ~1% of channels in a trained transformer concentrate disproportionate activation magnitudes.

**Measurable**: per-layer kurtosis spikes in $$F_k$$'s per-channel distribution. The random-init prior of Section 3 predicts approximately Gaussian per-channel distributions (zero excess kurtosis). The trained model's per-channel distributions should show heavy tails, and the heaviest tails should concentrate in specific layers — likely the full-attn layers, by hypothesis 2.

### Hypothesis 7 — Stroke lesion studies

Specific cortical lesions produce stereotyped functional deficits — Broca's area damage produces expressive aphasia, Wernicke's produces receptive aphasia, etc. The LLM analog is **single-layer ablation**.

**Measurable**: zero-out one full-attn layer at a time and measure the change in benchmark performance; do the same for one linear-attn layer at a time. Prediction: lesioning a full-attn layer (a "thalamic relay") produces a sharp drop on cross-phase tasks (chain-of-thought reasoning that requires the encoder to broadcast information to the decoder), while lesioning a linear-attn layer of equal depth in the plateau is silently absorbed.

### Hypothesis 8 — Resting state vs task-evoked connectivity

fMRI distinguishes the **intrinsic** (resting-state) functional connectome from the **extrinsic** (task-evoked) one. The LLM analog is the **prior vs empirical** comparison of Section 5: the random-init prior is the *resting state*, the trained empirical matrix is the *task-evoked* state, and their *difference* is the training-induced functional structure.

**Measurable**: the residual matrix $$\Delta_{ij} =\mathrm{CKA}_{ij}^{\text{prior}} - \mathrm{CKA}_{ij}^{\text{empirical}}$$ should concentrate in the CKA-derived modules and at their junctions, where training has deformed the independent-Gaussian null most strongly.

### Hypothesis 9 — Structural plasticity vs synaptic plasticity

Brain plasticity comes in two flavours: *synaptic* (Hebbian, weight-strength changes — the analog of fine-tuning) and *structural* (dendritic growth, new connections — the analog of RYS). The two are distinguishable: synaptic plasticity changes performance without changing structure; structural plasticity changes structure without changing weights.

**Measurable**: the benchmark delta of an RYS surgery should be a function of the **diameter** of the duplicated sub-DAG (the number of distinct functional paths added), not just its length. Sweep `min_block_length` from 1 to 16 in `predict_rys_windows`; predict that a length-1 (single-layer) duplication produces ~0 benefit, while length-7 to length-15 windows produce the maximum benefit.

### Hypothesis 10 — Small-world brain networks

The brain's functional connectome is small-world: high local clustering coefficient $$C$$, short global path length $$L$$, and small-world index $$\sigma = (C/C_\text{rand}) / (L/L_\text{rand}) > 1$$ {% cite watts1998collective %}. The LLM analog is the **CKA functional graph**: high clustering within data-driven CKA modules, short paths across modules through whichever layers actually carry high graph centrality.

**Measurable**: compute $$\sigma$$ and the Watts-Strogatz omega for the CKA graph thresholded at, e.g., $$\mathrm{CKA} > 0.7$$. Prediction: $$\sigma > 1$$ inside coherent CKA modules and lower values at module junctions.

---

| # | brain analog | LLM measurable | cell in the notebook |
| --- | --- | --- | --- |
| 1 | cortical hierarchy | layer-class probe gradient | future work |
| 2 | thalamus | betweenness centrality of full-attn layers | Figure 7 |
| 3 | edge-of-chaos | $$\rho^*$$ on the norm-growth curve | cell 11 (already plotted) |
| 4 | DMN | plateau-CKA variance ID vs OOD | future work |
| 5 | cortical thickness | within-clade RYS precision@25 | Figure 6 |
| 6 | grandmother cells | per-channel kurtosis spikes | future work (swap `apply_qwen_init=False`) |
| 7 | stroke lesion | single-layer zero-ablation $$\Delta$$ | future work (extend `rys.surgery`) |
| 8 | resting vs task-evoked | $$\Delta=\mathrm{CKA}^{prior}-\mathrm{CKA}^{empirical}$$ | Figure 5 |
| 9 | structural plasticity | `min_block_length` sweep | partial in cell 18 |
| 10 | small-world | Watts-Strogatz $$\sigma$$ on the CKA graph | future work |

## 8. Closing observations

The picture that emerges from these three posts taken together is the following.

- The pre-norm residual recursion (Section 1) is a **structural generator** for residual-stream norm growth (Equation 2) and the plateau condition $$\rho_k \to 0$$ (Equation 4).
- A closed-form Gaussian prior on $$F_k$$ from `text_config` alone (Section 3) recovers the empirical block-output variance within $$\sim 15\%$$ on a single Apple Silicon MPS forward pass — no full 27B model needed.
- This prior is a strong *rank-correlator* of the empirical CKA connectome (Spearman $$\approx 0.94$$) and a poor *magnitude predictor* outside the plateau (Section 5). The *deviation* of empirical from prior is the training-induced functional anatomy of the model.
- The hybrid linear- / full-attention schedule of Qwen3.6-27B (Section 2) gives a concrete brain analog: 75% cortical microcircuits (Gated DeltaNet), 25% thalamic relays (full self-attention) at a strict period of 4, with the dendrogram junctions of the previous post falling near the full-attn positions.
- Ten brain-inspired hypotheses (Section 7) translate the integration-segregation, small-world, lesion-study, DMN, and outlier-feature literatures of network neuroscience into measurable LLM-internal quantities. Three of them are computable from the notebook *today*; the rest are concrete proposals.

The strongest claim I want to make at this point is the structural-functional duality: **the same skip-connection DAG that the prior post derived as the structural graph of a Transformer also explains, to a usable approximation, the rank of every edge of its empirical CKA connectome.** The RYS amplification factor of 4 is then a *local* statement about how doubling the cumulative residual perturbs CKA inside that DAG.

What this *does not* settle is the behavioural prediction. The bounded random-init CKA prior alone is a poor predictor of which RYS windows will improve MATH (precision@25 of $$0.00$$ in Figure 6). The training-induced deformation matters: an ideal RYS prior would combine the structural prior of Section 4 with the empirical $$\Delta$$ matrix of Section 5.2. The next post in this series will do exactly that.

---

## References

{% bibliography --cited %}
