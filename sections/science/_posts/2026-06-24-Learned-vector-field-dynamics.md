---
layout: post
title: Learned vector field dynamics for RYS
description: Mathematics of dynamical systems behind the RYS effect
date: 2026-06-24
published: false
---


# Dynamical systems view of learned vector fields in residual networks

This is a rich question. Let me unpack it in layers, because your setup — a learned vector field $$f_\theta:\mathbb{R}^n\to\mathbb{R}^n$$ realized through skip connections $$x_{t+1}=x_t+f_\theta(x_t)$$, plus a *telescoped* band $$x_j = x_i + \sum_{k=i}^j f_{\theta_k}(x_k)$$ that you want to treat as a reusable refinement operator — sits at a confluence of several literatures: continuous-time residual networks (Neural ODEs), monotone operator theory, contraction theory, Koopman/operator-theoretic analysis, and iterative refinement / fixed-point methods. Let me lay out the tools, what each one tells you, and how they connect to the "band duplication = stable refinement" hypothesis.

---

## 1. Reframe the discrete update as a flow, not just a map

The skip-connection update is the explicit Euler discretization of an ODE:

$$
\dot{x}(t) = f_{\theta}(x(t), t), \qquad x(t+\Delta t) \approx x(t) + \Delta t\, f_\theta(x(t),t).
$$

The telescoped form you wrote is exactly the discrete integral (a Riemann sum) of the time-augmented field $$f_{\theta_t}$$ along the trajectory. So a "band" $$[i,j]$$ is a *time window* of the flow, and duplicating that band is **re-running the flow over a repeated time interval** — i.e. composing the flow map $$\Phi_{j\leftarrow i}$$ with itself.

This immediately tells you what "stable refinement" must mean mathematically: the band flow map $$\Phi_{j\leftarrow i}:\mathbb{R}^n\to\mathbb{R}^n$$ must be a **contraction** (or at least non-expansive) in a suitable metric, so that repeated application converges to a fixed point that *is* the refined representation. This is the single most important reframing. Everything below is a way of testing or exploiting that.

---

## 2. The catalogue of dynamical-systems properties you asked for

For a generic learned field $$f_\theta$$, here are the properties worth measuring and the tool for each.

### (a) Contractivity vs. expansivity — the central one

The Jacobian $$J_f(x) = \partial f_\theta / \partial x$$ governs local behavior. The relevant quantities:

- **Operator norm (spectral radius of the symmetric part):** $$\mu_{\ast}(f) := \sup_x \lambda_{\max} \left( \tfrac{1}{2} (J_f + J_f^\top) \right )$$, the logarithmic norm (Coppel / Loewner measure). 
If $$\mu_\ast < 0$$ everywhere, the flow is **strongly contracting** with rate $$| \mu_\ast |$$.
Trajectories coalesce exponentially. If $$\mu_{\ast} > 0$$ somewhere, it's locally expansive there.

- **Lipschitz constant** $$L = \sup_x \|J_f(x)\|_2$$. For the *discrete* update $$x+f(x)$$, the relevant stability constant is $$\sup_x \|I + J_f(x)\|_2$$ — note this can be $$>1$$ even when $$f$$ is contracting, because the identity term dominates. This is why **small step sizes / many layers** are the natural regime for residual nets: you want $$\|I + \Delta t\, J_f\| \approx 1 + \Delta t\, \mu_\ast < 1$$.
- **Logarithmic Lipschitz constant in non-Euclidean metrics** (Juškevičiūtė–Lohmiller): $$\mu_P(f) = \sup_x \lambda_{\max}\!\left(P^{-1}\tfrac{1}{2}(J_f^\top P + P J_f)\right)$$ for some $$P\succ 0$$. The metric matters enormously: a field that looks expansive in the Euclidean metric can be strongly contracting in a learned or data-dependent metric. This connects directly to your "bands refine" intuition — the right metric is the one in which the band map is a contraction.

**Tool:** estimate $$\sup_x \lambda_{\max}(\text{sym}(J_f))$$ by sampling $$x$$ from the data manifold (or activations) and computing Jacobian-vector products (JVPs) with power iteration. No need to form $$J_f$$ explicitly; use a few Hutchinson/power iterations on $$v^\top \text{sym}(J_f) v$$.

### (b) Fixed points and attractors

A point $$x^\star$$ with $$f_\theta(x^\star)=0$$ is an equilibrium. For a *refinement* interpretation, you want the data manifold to be attracted to a low-dimensional set of such equilibria — these are the "refined representations." Stability is given by the eigenvalues of $$J_f(x^\star)$$: all in the left half-plane (for the continuous field) or inside the unit disk (for the discrete $$I+J_f$$ map).

**Tool:** find equilibria by running the flow to convergence (i.e. *unrolling the band many times* — which is exactly your duplication experiment!) and checking $$\|f_\theta(x)\|\to 0$$. Then linearize. This is also the practical diagnostic for "does duplication converge": if iterating the band map converges, you've found a fixed point of the band flow, and the convergence rate is the contraction modulus of the band.

### (c) Limit cycles

Periodic orbits occur when the field has rotational structure that overcomes dissipation — i.e. when the antisymmetric part $$\tfrac{1}{2}(J_f - J_f^\top)$$ dominates the symmetric part. The Poincaré map is the standard tool: take a transverse section $$\Sigma$$ to the flow and study the return map $$\Pi:\Sigma\to\Sigma$$. A period-$$T$$ orbit corresponds to a fixed point of $$\Pi^T$$.

**Tool:** if you suspect cycles, integrate the flow (run the band repeatedly with interpolation) and check for recurrence via a Poincaré section. In practice, for *contracting* fields you should not see cycles except degenerate ones — contraction forbids non-trivial recurrent dynamics. So detecting a limit cycle is itself evidence that the band is *not* purely contractive and contains a Hamiltonian/rotational component.

### (d) Volume change: dissipative vs. conservative

The trace $$\nabla\cdot f_\theta = \rm{Tr}[J_f]$$ is the instantaneous divergence; its integral along a flow gives log-volume-change (Liouville's formula). A dissipative band shrinks volumes (good for "settling" to a refined point); a volume-preserving band is Hamiltonian-like and will not converge under iteration.

**Tool:** estimate $$\mathbb{E}_x[\operatorname{tr} J_f(x)]$$ via Hutchinson's estimator $$\mathbb{E}[v^\top J_f v] = \operatorname{tr} J_f$$ with $$v$$ isotropic. This is one JVP per sample, cheap. Sign and magnitude are immediately informative: strongly negative trace ⇒ strongly dissipative ⇒ likely convergent under duplication.

### (e) Splitting into dissipative + conservative + gradient parts (Helmholtz–Weyl decomposition)

Any smooth field on $$\mathbb{R}^n$$ (with the standard metric) decomposes as

$$
f_\theta(x) = -\nabla \Phi(x) \;+\; \omega(x) \;+\; \nabla\cdot \tau(x),
$$

i.e. an irrotational (gradient) part, a solenoidal (rotational) part, and a harmonic part. The **gradient part is what makes the dynamics a gradient flow** $$-\nabla\Phi$$ and guarantees convergence to critical points of $$\Phi$$ (the refined representation). The **solenoidal part** is the cycle-generating, non-convergent component.

**Tool:** this is hard to compute exactly for a learned field, but you can *estimate* the relative weight of symmetric vs. antisymmetric Jacobian: $$\|\text{sym}(J_f)\|_F$$ vs $$\|\text{skew}(J_f)\|_F$$. If the field is dominated by its symmetric part and that part is negative-semidefinite, you're effectively in gradient-flow land and refinement is guaranteed.

### (f) Spectral properties of the *flow map*, not the field

What you actually iterate is the band map $$\Phi_{ j \leftarrow i }$$, not $$f$$ itself.
The relevant object is its Jacobian $$D\Phi_{j\leftarrow i}(x)$$, obtained by the variational equation (sensitivity propagation through the band). 
The eigenvalues of $$D\Phi$$ at a fixed point tell you the local attractor type: real $$<1$$ hence node, complex with $$|\lambda|<1$$ hence spiral, etc.

**Tool:** propagate a tangent matrix through the band via JVPs (this is just `jax.jvp` or `torch.autograd.functional.jvp` composed across the layers). Power-iterate to get the top singular/eigen values. The **spectral radius $$\rho(D\Phi)$$** is the cleanest scalar summary: $$\rho<1$$ ⇒ contraction ⇒ stable refinement under duplication.

---

## 3. Stability of the *band* as a refinement operator — the precise question

You want to know whether duplicating a band $$[i,j]$$ is a *stable refinement*. Using the telescoped form, the band defines a map

$$
\Phi_{j\leftarrow i}(x) \;=\; x + \sum_{k=i}^{j} f_{\theta_k}(x_k(x)).
$$

Duplication means iterating $$\Phi := \Phi_{j\leftarrow i}$$. Three mathematical frameworks give you the answer, in increasing strength:

### 3.1 Banach fixed-point / contraction mapping (strongest, simplest)

If $$\Phi$$ is a contraction in some complete metric — i.e. $$\exists\, q<1:\ \|\Phi(x)-\Phi(y)\| \le q\|x-y\|$$ for all $$x,y$$ on the data manifold — then iteration converges geometrically to the unique fixed point, and that fixed point is *the* refined representation. The contraction modulus $$q$$ is bounded by $$\sup_x \|D\Phi(x)\|$$. **This is the cleanest sufficient condition for "stable refinement."** Duplication pays off iff $$q<1$$; if $$q\ge 1$$, duplication either does nothing (q=1, non-expansive) or amplifies noise (q>1, expansive).

The subtlety: $$q$$ is a property of the *metric*. There may exist a metric $$P\succ 0$$ in which the same $$\Phi$$ contracts even though it looks expansive in Euclidean norm. This is exactly the **contraction-metric theorem** of Lohmiller–Slotine: a system is contracting iff there exists a uniformly positive-definite metric $$M(x)$$ such that $$\tfrac{1}{2}(\dot M + J_f^\top M + M J_f) \preceq -\lambda M$$ with $$\lambda>0$$. So the question "is this band a refinement operator?" is secretly the question "is there a contraction metric for this band?" — and that metric is itself a learnable / estimable object.

### 3.2 Monotone operator theory (most operational)

Residual updates are *proximal / forward* steps. The discrete update $$x_{t+1} = x_t + f(x_t)$$ is a forward step on operator $$-f$$. The band is a composition of such steps. Convergence theory for such compositions is **monotone operator theory** (Bauschke–Combettes). The relevant condition:

- $$f$$ is **$$\eta$$-cocoercive** if $$\langle f(x)-f(y), x-y\rangle \ge \eta \|f(x)-f(y)\|^2$$.
- $$f$$ is **$$m$$-strongly monotone** if $$\langle f(x)-f(y), x-y\rangle \ge m\|x-y\|^2$$, equivalently $$\text{sym}(J_f)\succeq m I$$.

For *refinement* (convergence to a fixed point) you want $$-f$$ (or the banded composition) to be **averaged** and **non-expansive**. The discrete step $$x+f(x)$$ being non-expansive is exactly $$\|I+J_f\|\le 1$$, the condition you can probe directly. Composition of averaged operators stays averaged (operator-sum theorem), so a band made of averaged layers is itself averaged — a sufficient condition for stable duplication. This is the most *operational* tool: it gives composition rules that tell you when concatenating/duplicating bands preserves the refinement property.

### 3.3 Input-to-state stability (ISS) and incremental stability

For a more robust (control-theoretic) notion: **incremental ISS** asks whether the distance between any two trajectories stays bounded and decays. For a contractive band this holds with a linear decay rate. ISS is what you want if you care about refinement being *robust* to perturbations in the input representation (e.g. adversarial noise), not just convergent on clean inputs. Tools: Lyapunov functions $$V(x,y)=\|x-y\|_P^2$$ and checking $$\dot V \le -\alpha V + \sigma(\|u\|)$$.

---

## 4. Connecting to learning theory and representation refinement

A few extra connections that make the "band = refinement block" story sharper.

### 4.1 The band as a denoising / proximal operator

If $$-f_\theta$$ is (approximately) the gradient of an energy $$\Phi$$, then the band is an approximate gradient-descent step on $$\Phi$$, and duplicating it is just iterating gradient descent. The fixed point is a (local) minimizer of $$\Phi$$ — i.e. the "refined" representation is the energy minimum. This is the **equilibrium-model** / **deep equilibrium (DEQ)** view (Bai, Kolter, Koltun): a residual stack that converges is computing the fixed point of a single learned operator, and you can replace the whole stack with a root-finder. Your "band duplication" is a rediscovery that *some sub-bands already behave like DEQ operators* — they have a stable fixed point worth iterating to.

Diagnostic: fit the hypothesis $$f_\theta(x)\approx -\nabla \Phi(x)$$ by checking how symmetric $$J_f$$ is (sect. 2e). The more symmetric-negative-definite, the more the band is a gradient-flow refinement and the better duplication will work.

### 4.2 Partial / incremental updates and Kaczmarz/Strohmer-Vershynin

Your "partial iterative update" intuition has a direct analog in **randomized Kaczmarz** and **incremental gradient** methods: each layer updates only "part" of the representation (a subspace, a subset of coordinates), and stability/convergence comes from averaging over many such partial updates. The relevant theoretical guarantees are:

- **Stochastic increment stability:** if each partial update is non-expansive on its active subspace and the subspaces span, the composition converges.
- **Jacobian low-rank / subspace structure:** if $$J_{f_k}$$ is low-rank (typical for transformer MLP/attention blocks), each layer is a *partial* update, and the band is a product of partial updates. Duplication helps when the partial updates within the band are *mutually complementary* (their active subspaces together cover the relevant directions) but *individually contractive*. This gives you a concrete spectral diagnostic: **the union of the top singular-vector subspaces of $$J_{f_k}$$ over the band**, and the contractivity on that union.

### 4.3 Reasoning blocks, iterative inference, and amortization

The "reasoning block" framing matches the literature on **iterative amortized inference** and **learned simulators of iterative algorithms** (e.g. Learned Simulators / Lugmayr et al., and the "diffusion as flow matching" line). A single forward pass *amortizes* what would otherwise be an iterative refinement; duplicating a band trades compute for **closer approximation to the fixed point**. The gain is large exactly when (i) the band is contractive (so iteration converges) and (ii) the amortization gap — distance between one-pass output and the fixed point — is large. You can measure (ii) directly as $$\|\Phi(x)-x\|$$ after one band pass; if it's already tiny, duplication won't help. If it's sizeable *and* the band contracts, duplication will help a lot.

This gives a clean two-parameter model of "when does band duplication help":
- $$\alpha := $$ contraction modulus of $$\Phi$$ (smaller is better),
- $$\delta_0 := \|\Phi(x_0)-x_0\|$$ (the one-pass residual, larger is better, up to the contractive regime),
- gain after $$r$$ duplications $$\approx \delta_0 \cdot \frac{1-\alpha^{r}}{1-\alpha}$$, capped by the data manifold's tolerance.

You can fit $$\alpha$$ and $$\delta_0$$ per band from activation statistics and *predict* which bands will benefit from duplication before running the downstream eval.

### 4.4 Physics: Onsager / fluctuation-dissipation and the antisymmetric part

If you think of $$f_\theta$$ as a generalized "force" on the representation, the symmetric-negative-definite part is dissipative (Onsager-like) and the antisymmetric part is a symplectic / magnetic drift. Refinement requires dissipation to dominate. There's a beautiful connection to **port-Hamiltonian** systems: $$f(x) = (J(x)-R(x))\nabla H(x)$$ with $$J$$ skew, $$R\succeq 0$$. Then $$H$$ is a Lyapunov function automatically, $$\dot H = -(\nabla H)^\top R (\nabla H) \le 0$$, and convergence follows. Estimating whether your band admits a port-Hamiltonian structure (i.e. whether $$f$$ factors through a gradient of some $$H$$ with a positive-semidefinite $$R$$) is a strong test of "stable refinement." Practically: check if $$J_f$$ admits a decomposition $$J_f = S - A$$ with $$S\succeq 0$$ and $$A$$ skew *and* $$f$$ is in the image of $$S-A$$ applied to a gradient — i.e. $$f$$ is a gradient field mod a rotation.

---

## 5. A concrete diagnostic battery for a band

Putting it together, here is the minimal set of measurements I would compute per band $$[i,j]$$, in order of bang-for-buck:

1. **Band contraction modulus** $$\hat q := \sup_{x\in\mathcal{D}} \|D\Phi_{j\leftarrow i}(x)\|_2$$ via power iteration on JVPs through the band. The single most informative number. $$\hat q<1$$ ⇒ duplication converges.
2. **One-pass residual** $$\hat\delta := \mathbb{E}_x\|\Phi(x)-x\|$$. Predicts the headroom for duplication.
3. **Divergence / trace** $$\mathbb{E}_x[\operatorname{tr}\, J_{f_\text{band}}(x)]$$ via Hutchinson. Sign tells dissipative vs. expansive.
4. **Symmetric-vs-skew split** $$\|\text{sym}(J)\|_F / \|\text{skew}(J)\|_F$$ at band granularity. High ratio + negative-definite sym ⇒ near-gradient-flow ⇒ safe to iterate.
5. **Spectral radius at the fixed point** $$\rho(D\Phi(x^\star))$$ where $$x^\star$$ is obtained by iterating the band to convergence. Tells you the *local* refinement rate and the attractor type (node vs. spiral).
6. **Contraction-metric search** (optional but powerful): solve a small SDP / learn a constant $$P\succ 0$$ minimizing $$\sup_x \lambda_{\max}(P^{-1}\text{sym}(J_f^\top P))$$ over sampled $$x$$. If the optimum is $$<0$$, you've proven contraction in a non-Euclidean metric even when Euclidean analysis fails.
7. **Recurrence / Poincaré check** if any of the above look non-contractive: run the band many times and look for periodic orbits — a red flag that duplication will oscillate, not refine.

If you plot $$\hat q$$, $$\hat\delta$$, and the symmetric-skew ratio *per band* across the network, the bands that benefit from duplication should light up as low-$$q$$, high-$$\delta$$, high-symmetric-ratio regions. That gives you a structural explanation of the empirical observation you started with.

---

## 6. Honest caveats

- **Sampling matters.** All these estimates are over the *data/activation distribution*. The field can be contracting on-manifold and wildly expansive off-manifold; you only care about the former for downstream quality, but off-manifold behavior matters for adversarial robustness.
- **The metric is learnable.** Conclusions of "expansive" in the Euclidean metric can flip in a learned metric. Always cross-check with the SDP-based metric search (item 6) before declaring a band non-refining.
- **Linearization is local.** Spectral diagnostics near a fixed point describe asymptotic behavior; global behavior may include multiple attractor basins. Duplication can *move* you between basins, which may or may not be desirable — it's refinement only if the target basin is the "right" one.
- **Composition vs. iteration.** Duplicating a band is iteration of a *fixed* map; *telescoping to compose* different bands is composition of different maps. The theory above covers both, but composition can be contracting even when no single band is, via the averaged-operator sum theorem — relevant if your downstream benefit comes from *rearranging* bands rather than repeating them.

---

## TL;DR

Treat each band as the flow map $$\Phi_{j\leftarrow i}$$ of the Euler-discretized ODE $$\dot x = f_\theta$$. The question "does duplicating this band give stable refinement?" reduces, in the strongest and cleanest form, to: **is $$\Phi_{j\leftarrow i}$$ a contraction in some metric?** The mathematical tools to answer this, in order of usefulness, are: (1) contraction theory / logarithmic norms (Coppel, Lohmiller–Slotine) for the field, (2) the spectral radius of the band's Jacobian $$D\Phi$$ via JVP power iteration, (3) monotone/averaged-operator theory for composition rules, (4) Helmholtz/port-Hamiltonian decomposition into dissipative vs. rotational parts, (5) divergence/trace (Hutchinson) for volume dissipation, and (6) Lyapunov/ISS for robustness. The downstream benefit you observed should correlate, per band, with (low contraction modulus) × (large one-pass residual) × (dominant symmetric-negative Jacobian) — and that triple gives you both a mechanistic explanation and a predictor of which bands are worth duplicating.

Key references to ground this: Lohmiller & Slotine (1998) on contraction analysis; Bai, Kolter & Koltun (2019) on deep equilibrium models; Bauschke & Combettes on monotone operators; Haber & Ruthotto on stable architectures for deep networks as ODEs; and the port-Hamiltonian neural network line (Toth et al.) for the energy/dissipation decomposition.

If you'd like, I can sketch (in Ask mode, no edits) the exact JVP/Hutchinson estimation code you'd run to compute items 1–4 above on a concrete model, or work through the SDP for the contraction-metric search in more detail.
