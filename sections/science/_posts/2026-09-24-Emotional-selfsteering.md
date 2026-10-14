---
layout: post
title: "Emotional self-steering with a frozen LLM"
description: "A small activation-steering harness that reads the residual stream during decoding and edits a frozen Qwen3-0.6B only when it drifts from a calm and uncertainty axis."
date: 2026-09-24
published: false
categories:
  - science
  - deep-learning
---

I read a nice post by Madhukar Phatak, [Dynamic Abliteration via Multi-Layer
Engram Steering](https://blog.madhukaraphatak.in/non-destructive-refusal-supression-using-engram),
and I liked its plainness. It walks from a base model to a steering module in
small steps. This post does the same thing for a different goal. I do not want
to remove refusals. I want to move a model along an emotional axis, from
uncertainty toward calm, and touch its activations only when it drifts.

The model here is `Qwen/Qwen3-0.6B` on Apple Silicon. Every edit happens in the
residual stream at one layer, through a PyTorch forward hook. I did not run
fresh benchmarks for this post, so there are no result tables below. This is a
walk-through of the mechanism and its design choices.

## Step 1: load a frozen model

The base model is ordinary Qwen3. I load it once, set it to evaluation mode,
and never update its parameters.

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

name = "Qwen/Qwen3-0.6B"
tokenizer = AutoTokenizer.from_pretrained(name)
model = AutoModelForCausalLM.from_pretrained(
    name,
    dtype=torch.float32,
    attn_implementation="eager",
).to("mps").eval()
model.requires_grad_(False)
```

## Step 2: read one layer during decoding

The base object is a frozen transformer with two hooks on a chosen block. One
hook captures the last-token residual. The other adds a delta to it. Between
tokens the model is untouched.

```python
def capture(_m, _i, output):
    self._h = output[0] if isinstance(output, tuple) else output
    return output

def patch(_m, _i, output):
    if self._delta is None:
        return output
    hidden = (output[0] if isinstance(output, tuple) else output).clone()
    d = self._delta.to(device=hidden.device, dtype=hidden.dtype)
    hidden[:, -1] = hidden[:, -1] + d
    return (hidden, *output[1:]) if isinstance(output, tuple) else hidden
```

This is the same interception idea as the Engram post. The difference is what
decides the delta and when it is applied.

## Step 3: build the axis, then centre it

I do not subtract a raw difference of two prompts. Raw residuals in a
transformer carry a large shared offset, so a direction taken from raw
activations points mostly at that offset. I first remove the training mean, then
take the difference of class centroids in the centred space.

$$\boldsymbol{\theta} = \mathrm{normalize}(\boldsymbol{\mu}_{+} - \boldsymbol{\mu}_{-}), \qquad \mathbf{x}_c = \mathbf{x} - \boldsymbol{\mu}$$

Here $$\boldsymbol{\mu}_{+}$$ and $$\boldsymbol{\mu}_{-}$$ are the mean centred
residuals for the two classes, and $$\boldsymbol{\mu}$$ is the training mean I
keep for centring later.

```python
import torch.nn.functional as F

def steering_vector(h, y, positive, negative):
    mu = h.mean(0)
    hc = h - mu
    n = int(y.max()) + 1
    cents = torch.stack([hc[y == i].mean(0) for i in range(n)])
    return F.normalize(cents[positive] - cents[negative], dim=-1), mu
```

Both $$\boldsymbol{\theta}$$ and $$\boldsymbol{\mu}$$ travel together. Every read
and every edit that follows happens on centred activations.

## Step 4: sense the drift, do not just trigger on words

The Engram post recognises a refusal by hashing token n-grams. That fits its
task, because a refusal is bound to phrases like "I cannot". An emotion is not
bound to fixed tokens. So I read the model's own state instead. After each token
I project the centred residual onto the axis and smooth it with an exponential
moving average.

$$p(\mathbf{x}) = \frac{\mathbf{x}_c^{\top}\boldsymbol{\theta}}{\lVert\mathbf{x}_c\rVert_2}, \qquad \bar{p}_j = \gamma\, p(\mathbf{x}) + (1-\gamma)\,\bar{p}_{j-1}$$

```python
def score(self, h):
    hc = h.reshape(-1).float() - self.mu
    return float((hc * self.theta).sum() / hc.norm().clamp_min(1e-8))

def update_ema(self, h):
    p = self.score(h)
    self.score_bar = p if self.score_bar is None else self.alpha * p + (1 - self.alpha) * self.score_bar
    return float(self.score_bar)
```

This score comes from the normal, unpatched forward pass. In the current
skeleton, a closed-loop token therefore needs one normal forward pass to sense
the state and one more pass to generate with the patch. The extra pass is the
price of deciding from the current residual instead of from prompt keywords.

## Step 5: gate with a deadband, not a constant

A constant edit on every token is the failure mode the Engram post names, and I
agree with it. My answer is a hand-built deadband instead of a learned gate. The
gate fires when the smoothed score crosses a threshold $$\beta$$. Once active it
holds through a minimum duration and releases only after the score falls below
$$\beta - \eta$$, where $$\eta$$ is a hysteresis margin. After release it ignores
new firings for a cooldown. A strong margin picks a larger coefficient when the
drift is severe.

$$r = \mathrm{Gate}(\bar{p};\, \beta, \eta, \delta, D_{\min}, C) \in \{0,\, r_{\mathrm{w}},\, r_{\mathrm{s}}\}$$

```python
def gate(self, score):
    fire, reason = score >= self.beta, "below_threshold"
    if self.active:
        hold = self.duration < self.min_duration or score >= (self.beta - self.eta)
        fire, reason = (True, "hold") if hold else (False, "hysteresis_release")
    elif self.cooldown_left > 0:
        fire, reason = False, "cooldown"
        self.cooldown_left -= 1
    if fire:
        kind = "strong" if score >= self.beta + self.strong_margin else "weak"
        self.active, self.duration = True, self.duration + 1
        return kind, (self.r_strong if kind == "strong" else self.r_weak), reason
    if self.active:
        self.cooldown_left = self.cooldown
    self.active, self.duration = False, 0
    return "none", 0.0, reason
```

The Engram module learns this decision end-to-end. My version is six scalars in a
config file. That is a fair trade to make later: a learned gate would remove the
manual tuning, and I plan to test one against this rule under the same controls.

## Step 6: edit toward the axis, then clip

When the gate is on, I push the centred residual back along the axis, but only
against the offending component. I take the positive projection, scale it by the
coefficient, and clip the whole edit to a fraction $$\rho$$ of the residual norm.

$$\Delta\mathbf{x} = \mathrm{Clip}\!\left(-r\,\mathrm{ReLU}(\mathbf{x}_c^{\top}\boldsymbol{\theta})\,\boldsymbol{\theta},\ \rho\,\lVert\mathbf{x}_c\rVert_2\right)$$

```python
def patch(self, h, r):
    hc = h.reshape(-1).float() - self.mu
    if r == 0 or self.zero_strength:
        return torch.zeros_like(hc), 0.0
    dh = -r * (hc * self.theta).sum().clamp(min=0) * self.theta
    h_norm, dh_norm = hc.norm().clamp_min(1e-8), dh.norm().clamp_min(1e-8)
    dh = dh * min(1.0, float(self.rho * h_norm / dh_norm))
    return dh, float(dh.norm() / h_norm)
```

The clip is the safeguard against the second Engram failure mode, gibberish from
too large a push. The edit can never exceed a set share of the local residual.

## Step 7: fork the generation to prove the edit did it

This is the part the Engram post leaves out, and the part I care about most. If I
only compare steered text against unsteered text, I cannot say whether the change
came from the direction or from the mere act of adding a vector. So I decode a
shared prefix with no edits, then fork the same prefix four ways.

- Open-loop: keep decoding with no edit.
- Closed-loop: turn on the gated edit.
- Random direction: edit with a vector of matched norm but random direction.
- Zero strength: run the full sensor and gate, but set the edit to zero.

The random direction and the zero-strength run are negative controls. If the
steered fork moves and the random-direction fork does not, the axis did the
work. If the zero-strength fork matches open-loop, the sensor alone changes
nothing. The shared prefix keeps every fork identical up to the branch point.

## What I borrow from Engram

The Engram post and this harness agree on the core claim. Editing a frozen model
at inference works, and the edit must be conditional. We diverge on three
points. Engram triggers on token n-grams, and I sense the live residual, because
emotion is diffuse and refusal is not. Engram learns the gate, and I hand-tune a
deadband, for now. Engram compares steered against unsteered, and I add
matched-norm and zero-strength controls so a claim of causation survives.

The one idea I take straight from the post is multi-layer editing. Engram edits
layers 12 through 20 and shows that a single-layer edit gets rebuilt downstream.
I edit one layer today. Testing whether the emotion axis survives across a
window of layers is the next experiment.

I do not take the n-gram memory. It is a good trigger for phrase-bound
behaviour such as refusal. It is a poor sensor for an emotional state that can
appear in many different words. The residual stream already gives us a
context-dependent signal.

The other important difference is evaluation. A steered generation can differ
from an unsteered generation because of the direction, or because any extra
activation changed the trajectory. The matched-norm random branch and the
zero-strength branch help separate these explanations.

## Closing

The whole method is a small feedback loop around a frozen model:

1. Read the current residual.
2. Project it onto a contrastive emotional direction.
3. Decide whether the state has drifted.
4. Apply a clipped correction only when it has.

The model does not feel an emotion in this experiment. The harness reads a
representation associated with an emotion label and changes the next generation
step. That modest claim is also the useful one: it gives us a testable,
non-destructive control mechanism before we add a learned gate or several
intervention layers.
