---
layout: post
title: "K-SAT, survey propagation, and the search for a second level of clusters"
description: "Why physicists care about random satisfiability, how belief propagation and survey propagation work, and what we found when we pushed survey propagation to two levels of replica symmetry breaking."
date: 2026-09-28
published: false
permalink: "/sections/science/2026/09/28/K-SAT-and-Survey-propagation.html"
categories:
  - science
  - physics
  - ai
  - math
---
This post explains a research project in plain language. The project sits between
computer science and statistical physics. It asks a simple question about a famous
algorithm: where does the physical picture behind survey propagation stop being
exact, and what replaces it? To get there, I start from the beginning. I explain
what K-SAT is, why it is hard, how physicists first attacked it with belief
propagation, and why they needed survey propagation. Then I describe the
thresholds of the problem and replica symmetry breaking. At the end I describe
our experiments with a two-level version of survey propagation, what is new in
them, and what is still open.

I keep the equations to the few that carry the ideas. The proofs and the long
tables are in the research paper.

## 1. What K-SAT is

You have $$N$$ Boolean variables $$x_1, \dots, x_N$$, each true or false. You
also have $$M$$ constraints, called clauses. A clause is an OR of $$K$$
literals, and a literal is a variable or its negation. For $$K = 3$$ a clause
looks like this:

$$
(x_1 \lor \lnot x_7 \lor x_{12}).
$$

The clause is satisfied if at least one of its three literals is true. It is
violated only in one of the $$2^3 = 8$$ assignments of its three variables. A
formula is the AND of all clauses. The question of K-SAT is: does an assignment
exist that satisfies every clause at the same time?

For $$K = 2$$ a fast algorithm answers this. For $$K \ge 3$$ the problem is
NP-complete. It was the first problem proved NP-complete, by Cook in 1971. If
you find a fast algorithm for 3-SAT that works on every formula, you also have
a fast algorithm for thousands of other problems, from scheduling to protein
folding models. Nobody expects that such an algorithm exists.

In practice SAT solvers are everywhere. Chip makers use them to make sure that a
circuit does what its specification says. Software tools use them to find bugs
and to plan. Industrial formulas with millions of variables are often solved in
seconds. So "NP-complete" does not mean "always hard". The interesting question
is which formulas are hard, and why.

## 2. Random formulas and a sharp threshold

To study typical hardness, we draw formulas at random. Each clause picks $$K$$
distinct variables at random, and each literal is negated with probability one
half. The only parameter is the clause density

$$
\alpha = \frac{M}{N}. \tag{1}
$$

At small $$\alpha$$ there are few constraints and almost every formula is
satisfiable. At large $$\alpha$$ there are too many constraints and almost no
formula is satisfiable. Experiments in the early 1990s showed that the change
is sharp when $$N$$ is large. For random 3-SAT it happens near
$$\alpha_s \approx 4.267$$. The hardest formulas for complete solvers sit close
to this threshold. There a solver cannot find a solution quickly, and it cannot
prove quickly that none exists.

A sharp transition as a parameter changes is exactly what physicists call a
phase transition. Water freezes at a precise temperature. Random 3-SAT "freezes"
at a precise clause density. This observation brought statistical physics into
the problem.

## 3. The physicist's view: energy and spin glasses

A physicist writes each variable as a spin $$\sigma_i = \pm 1$$. The energy of
an assignment is the number of violated clauses:

$$
E(\sigma) = \sum_{a=1}^{M} \mathbb{1}[\text{clause } a \text{ is violated by } \sigma]. \tag{2}
$$

A satisfying assignment is a ground state with zero energy. If the formula is
unsatisfiable, the ground-state energy is positive, and the best assignments
violate a few clauses. This is the MAX-SAT version of the problem.

With this energy, random K-SAT is a spin glass. The constraints pull variables
in conflicting directions, and the formula has no regular structure. Spin
glasses have a rich theory that Giorgio Parisi and many others built in the
1970s and 1980s. The main tools are the cavity method and the replica method.
From the physics side, K-SAT is a model system for disordered matter. From the
computer science side, the physics predicts thresholds and explains why
algorithms fail.

## 4. Belief propagation

A random formula is a sparse graph. Each variable sits in about $$K\alpha$$
clauses, and each clause touches $$K$$ variables. Locally the graph looks like
a tree, and loops are long, of length about $$\log N$$. On a tree you can count
solutions exactly by passing messages along the edges. Belief propagation (BP)
applies the same rules to the sparse graph and hopes that the long loops do not
matter.

Each clause $$a$$ sends a message to each of its variables $$i$$. The message
is the probability that clause $$a$$ needs $$i$$ to satisfy it, because all its
other variables fail it. Each variable combines the messages from its other
clauses, and it sends the result back. Schematically,

$$
\text{message}_{a \to i} = \prod_{j \in a \setminus i} P\big(j \text{ does not satisfy } a \,\big|\, \text{messages into } j \text{ from clauses other than } a\big). \tag{3}
$$

You iterate these equations until they stop changing. The fixed point gives
the marginal of each variable and the entropy, which is the logarithm of the
number of solutions. The same equations are the replica-symmetric solution of
the physicists. BP is exact on trees, and it is excellent on random graphs at
low density.

But BP fails at larger $$\alpha$$. The iteration stops converging, and the
entropy it predicts is wrong. The reason is geometric, and it is the heart of
this story.

## 5. Clusters and the thresholds of random 3-SAT

Look at the set of all solutions of one large formula. Two solutions are close
if they differ in few variables. At low density the solutions form one large
connected set. You can walk from any solution to any other by flipping a few
variables at a time and never break a clause for long.

At a density $$\alpha_d$$ the set breaks into an exponential number of
separate clusters. Inside a cluster, solutions are close. Different clusters are
far apart, at a distance proportional to $$N$$. To go from one cluster to
another you must violate many clauses on the way. A local search algorithm then
gets trapped, like a hiker in one valley of a mountain range.

The number of clusters grows as $$e^{N\Sigma}$$. The exponent $$\Sigma$$ is the
complexity. It is an entropy of clusters, not of solutions. As $$\alpha$$
grows, the clusters become fewer and smaller. The complexity of the dominant
clusters reaches zero at $$\alpha_s$$, and above it no cluster of solutions is
left.

<figure>
<img src="/assets/media/postfigures/ksat_thresholds.svg" alt="Thresholds of random 3-SAT" style="max-width: 100%;">
<figcaption>
<strong>Figure 1.</strong> Thresholds of random 3-SAT. Clusters appear at $$\alpha_d \approx 3.86$$. The satisfiability threshold is $$\alpha_s \approx 4.267$$. The one-step picture is unstable at zero energy above $$\alpha_m \approx 4.153$$. Its ground state at positive energy is unstable above $$\alpha_G \approx 4.39$$. The red line marks the density of our last experiment.
</figcaption>
</figure>

Figure 1 shows two more thresholds, $$\alpha_m$$ and $$\alpha_G$$. They are the
subject of this post, and I explain them in section 7.

## 6. Replica symmetry breaking and survey propagation

### Replica symmetry breaking in one sentence

BP assumes that the Gibbs measure, the uniform distribution over solutions, is
one "pure state". Clusters break this assumption: the measure is a mixture of
many pure states. The physicists call this replica symmetry breaking (RSB). The
name comes from the replica method. There you take $$n$$ copies of the system,
and the overlap between two copies stops being the same for every pair.

If the clusters themselves have no further structure, you have one step of RSB,
or 1RSB. Two random solutions are either in the same cluster, with a large
overlap $$q_1$$, or in different clusters, with a small overlap $$q_0$$. If
each cluster breaks again into sub-clusters, you have two steps, or 2RSB, with
three overlap values. Parisi's full solution of the Sherrington-Kirkpatrick
spin glass is the limit of infinitely many steps: a continuous hierarchy of
clusters inside clusters.

<figure>
<img src="/assets/media/postfigures/ksat_1rsb_2rsb.svg" alt="1RSB and 2RSB cluster structures" style="max-width: 100%;">
<figcaption>
<strong>Figure 2.</strong> A sketch of the two pictures. Left: in 1RSB the solutions form clusters, and the clusters have no inner structure. Right: in 2RSB each cluster (dashed circle) is itself a group of smaller sub-clusters.
</figcaption>
</figure>

### From beliefs to surveys

In 2002 Mézard, Parisi and Zecchina applied the 1RSB cavity method to K-SAT and
turned it into an algorithm: survey propagation (SP). The idea is to run BP one
level up. BP messages are probabilities over solutions. SP messages are
probabilities over clusters.

Inside one cluster, a variable is often frozen: it takes the same value in all
solutions of the cluster. So in a given cluster a clause either forces a
variable or it does not. This is a warning. The survey $$\eta_{a\to i}$$ is the
fraction of clusters in which clause $$a$$ sends a warning to variable $$i$$.
A clause warns $$i$$ only if every other variable of the clause is forced, by
its other clauses, to the value that violates $$a$$:

$$
\eta_{a\to i} = \prod_{j \in a\setminus i} \frac{\Pi^u_{j\to a}}{\Pi^u_{j\to a} + \Pi^s_{j\to a} + \Pi^0_{j\to a}}. \tag{4}
$$

Here $$\Pi^u$$ is the weight of clusters in which $$j$$ is forced to the value
that does not satisfy $$a$$, $$\Pi^s$$ is the weight in which it is forced to
satisfy $$a$$, and $$\Pi^0$$ is the weight in which it is free. Each weight is
a product of the incoming surveys from the other clauses of $$j$$. If $$j$$
gets warnings from both sides, the cluster has a contradiction.

At zero energy the contradictory clusters get weight zero. At positive energy
you keep them with a weight $$e^{-y}$$ per violated clause. The parameter
$$y$$ is an inverse pseudo-temperature for clusters, and the weight of a
cluster with energy $$E$$ is $$e^{-yE}$$. The SP free energy is a potential
$$\Phi(y)$$ with a Legendre structure:

$$
\Phi(y) = \Sigma(e) - y\,e, \qquad \Sigma = \Phi + y\,e. \tag{5}
$$

Here $$\Sigma(e)$$ is the complexity of clusters at energy density $$e$$. The
ground-state energy is where the complexity reaches zero, at a value
$$y = \mu_s$$. In this post I write $$\mu$$ for $$y$$, because at two levels we
need two of them.

### Survey propagation as an algorithm

The surveys also tell you which variables are most biased over all clusters.
Survey-inspired decimation fixes the most biased variable, simplifies the
formula, runs SP again, and repeats. With this method, formulas with a million
variables at $$\alpha = 4.2$$, very close to $$\alpha_s$$, became solvable,
where earlier algorithms failed. Backtracking survey propagation, by Marino,
Parisi and Ricci-Tersenghi, adds the option to undo earlier choices. It goes
even closer to the threshold. The code repository of this project started from
that algorithm.

## 7. Where 1RSB breaks

SP rests on the 1RSB picture. That picture is a hypothesis, and it can be
wrong. The way to test it is a stability analysis. Take the 1RSB solution,
perturb it in the direction of more structure, and see whether the
perturbation grows or dies.

Montanari, Parisi and Ricci-Tersenghi (MPRT) did this in 2003 and 2004. They
found two kinds of instability. The first splits clusters into smaller pieces.
Consider a small change in the surveys, and follow how it travels along the
graph. At each step it is multiplied by a growth factor. If the factor is
larger than one, the change grows and 1RSB is unstable. In random 3-SAT this
happens at zero energy above $$\alpha_m \approx 4.153$$. Between $$\alpha_m$$
and $$\alpha_s$$ the zero-energy 1RSB solution, which SP computes, is therefore
not exactly right.

The second is the Gardner instability of the ground state at positive energy.
It appears above $$\alpha_G \approx 4.39$$. There the lowest-energy clusters
are unstable. In spin glasses the Gardner transition is the classical sign that
a hierarchy of sub-clusters appears, which is the step from 1RSB toward
full RSB.

An instability tells you that 1RSB fails. It does not tell you what replaces
it. The natural next candidate is 2RSB. That is where our project starts.

## 8. What we set out to do

The plan had two parts.

### Part 1: a solvable dense limit

First we looked at a regime where calculations are cleaner: positive
temperature and a dense formula, in which each variable appears in many
clauses. There, an interpolation argument (in the style of Guerra and
Toninelli) shows that the K-SAT free entropy equals that of a mixed $$p$$-spin
Ising model, a classic spin glass, up to a small error that we bound
explicitly. The covariance of that model is

$$
\nu(q) = b^2\left[\left(\frac{1+q}{2}\right)^K - 2^{-K}\right], \qquad b^2 = \alpha\, c^2\, 2^{-K},\quad c = 1 - e^{-\beta}. \tag{6}
$$

In this limit we can ask exactly how a second level appears. We proved that a
popular small-overlap closure of the cavity hierarchy cannot produce a second
level. Its fixed points follow the Lambert-$$W$$ equation $$Q = A e^{Q}$$, which
has at most two solutions, and its only marginal point is a fold. The second
level appears elsewhere. The frozen 1RSB solution becomes unstable at a
Gardner line, and a new level is born continuously, with a breakpoint near
$$x = \tfrac12$$. This gave us a precise expectation for the sparse case: look
for the second level near a Gardner instability, and expect $$x$$ near one half.

### Part 2: two-step survey propagation at zero temperature

Then we went back to sparse random 3-SAT and wrote the 2RSB version of survey
propagation. At two levels, a survey is no longer a number. It becomes a
probability distribution of surveys: the law of the survey over the
sub-clusters of one cluster. The equations have two pseudo-temperatures,
$$\mu_1 \le \mu_2$$. The outer one weighs clusters and the inner one weighs
sub-clusters. Their ratio

$$
x = \frac{\mu_1}{\mu_2} \in (0, 1] \tag{7}
$$

is the Parisi breakpoint. The two-level potential is

$$
\Phi_2 = \lim_{N\to\infty}\frac1N\,\mathbb{E}\log\sum_{\text{clusters } c} \Big(\sum_{\text{sub-clusters } \gamma \in c} e^{-\mu_2 E_\gamma}\Big)^{x}. \tag{8}
$$

In the equations, the one-step update of Eq. (4) acts on one sub-cluster. The
new law of a survey is the old law tilted by the factor $$z^x$$, where $$z$$ is
the normalization of the one-step update. The one-step equations are always
solutions of the two-step ones, in two ways. In the corner embedding every law
is concentrated on 0 and 1, so the clusters have no inner structure. This is
1RSB at $$\mu_1$$. In the point embedding every law is a single point, so the
sub-clusters are what 1RSB calls clusters. This is 1RSB at $$\mu_2$$. A
genuine second level is a solution that is neither.

We solve the equations by population dynamics. Each survey law is stored as a
row of $$M$$ samples, called atoms, and the rows are updated by random draws on
the ensemble.

## 9. What we found

### An exact algorithm at x = 1, and a trap in the usual one

At $$x = 1$$ we proved that the means of the laws of surveys obey ordinary
one-step SP. This sounds technical, but it has two practical consequences.

First, it gives a population algorithm without weights, which has no bias.
Second, it exposes a problem of the standard weighted algorithm. With a finite
number of atoms per law, the standard algorithm produces spurious intermediate
solutions. They look like a second level, but they are an artifact of the
sample size. Any claim of 2RSB from the standard algorithm needs this test.

For $$x < 1$$ we built an exact rejection sampler. It keeps a candidate atom
with probability proportional to its tilt $$z^x$$, so it has no weight bias at
any $$x$$.

With these tools we measured the two thresholds again. We get
$$\alpha_m = 4.1531(2)$$ at zero energy, the MPRT value. The Gardner
threshold of the ground state is $$\alpha_G = 4.385(5)$$, and MPRT give
$$4.390(5)$$.

### Two directions of instability

A 2RSB solution can move away from 1RSB in two directions. In the splitting
direction, the clusters of the corner embedding break into sub-clusters. Its
growth rate is the one-step rate $$\lambda(\mu_1)$$ of MPRT. In the grouping
direction, the clusters of 1RSB at $$\mu_2$$ gather into super-clusters, and
this leaves the point embedding.

We proved that a displaced cluster moves by a reflection of its logit, and that
two reflections cost the weight $$e^{-\mu_1}$$. As a result, sparse
perturbations grow with the one-step rate for every $$x$$. So $$\alpha_m$$ does
not depend on $$x$$ at first order. The breakpoint shapes the second level,
but it does not decide where the second level appears.

### At zero energy, no genuine second level

Between $$\alpha_m$$ and $$\alpha_s$$ the zero-energy corners are unstable.
Where the population resolves the instability, the flow does not stop at a new
solution. It goes to the point embedding, which is ordinary 1RSB one level
down. The point embedding at zero energy has the same kind of instability as
before. So the instability moves down one level and does not go away.

We also proved a simple and general monotonicity result for finite systems.
The two-level free energy $$F_2 = -\Phi_2/\mu_1$$ satisfies

$$
\frac{\partial F_2}{\partial \mu_1} = \frac{\Sigma_{\text{ext}}}{\mu_1^2} \ge 0, \qquad \frac{\partial F_2}{\partial \mu_2} = \frac{s_{\text{in}}}{\mu_2^2} \ge 0. \tag{9}
$$

Here $$\Sigma_{\text{ext}}$$ is the complexity of the clusters, and
$$s_{\text{in}}$$ is the internal complexity, the complexity of the sub-clusters
inside one cluster. At zero energy both are positive, so $$F_2$$ has no
stationary point, and the variational principle does not fix $$x$$. At zero
energy $$x$$ is a Legendre parameter. It selects clusters with a given
internal complexity, like a temperature selects states with a given energy.
The output of 2RSB survey propagation at zero energy is a curve
$$\Sigma_{\text{ext}}(s_{\text{in}})$$, not one number.

### Above the Gardner point: a real second level

The monotonicity result also points to the place where $$x$$ is fixed: positive
energy. There an interior maximum of $$F_2$$ is possible, and at the maximum
both complexities vanish. So we went to $$\alpha = 4.46$$, above $$\alpha_G$$,
where the ground state is at $$\mu_s = 4.1$$ and the splitting rate is
$$\lambda(\mu_s) = +0.027$$.

There, at $$x = \tfrac12$$, both embeddings are unstable. The corners split,
and the point groups. So the flow of the exact two-step equations cannot end
at either embedding. We found that it ends at a new state near the corners.
Most atoms are within $$10^{-6}$$ of 0 or 1, but a few percent are far from
them, and they give the laws a small width. The main tests are these:

- The widths vanish at $$\mu_1 = 4.4$$ and $$4.7$$, where 1RSB is stable, and
  they decay at the predicted linear rate.
- The widths are larger where the instability is stronger: about
  $$3\times 10^{-3}$$ at $$\mu_1 = 3.8$$ against $$8\times10^{-4}$$ at
  $$\mu_1 = 4.1$$.
- Starts from the corners and from the point reach the same state.
- The widths are stationary over 400 sweeps, and they agree between 512 and
  1024 atoms per law. At 256 atoms they decay, and that decay is a finite-size
  effect.

The last point needed care. With too few atoms per law, the rare atoms far from
the corners are sampled badly, and a real state seems to die.

### What the second level changes

The last step was to compute the two complexities and the energy of this state.
This is harder than it looks. Every term of the potential is the logarithm of
an average over one atom from each of many laws, and the atoms that matter are
rare and carry large weights. Our first estimator gave a clear negative
internal complexity. A study with more samples showed that this was a bias of
the finite sample, not a physical signal. The final estimator uses an exact
fact. Each term is linear in each atom, so its average over the corners is the
one-step term, which has a closed form. Only the difference is sampled, and
Jensen's inequality makes that difference never negative. The estimate is
stable from 1024 to 4096 samples per term.

<figure>
<img src="/assets/media/postfigures/ksat_2rsb_shifts.svg" alt="Shifts of energy and free energy from 1RSB" style="max-width: 100%;">
<figcaption>
<strong>Figure 3.</strong> Change of the energy $$e$$ (circles) and of the two-level free energy $$F_2$$ (squares) of the new state, with respect to the 1RSB values at the same $$\mu_1$$. Here $$\alpha = 4.46$$ and $$x = 1/2$$. The energy goes down. At $$\mu_1 = 3.8$$ the shift is 12% of the 1RSB energy. The free energy does not change within $$10^{-4}$$.
</figcaption>
</figure>

Figure 3 shows the result. At fixed $$\mu_1$$ the second level selects clusters
with a lower energy: $$\delta e = -6.1(1.2)\times10^{-4}$$ at $$\mu_1 = 3.8$$,
which is 12% of the one-step energy. Both complexities also go down. But the
two changes compensate in the free energy

$$
F_2 = e - \frac{\Sigma_{\text{ext}} + x\, s_{\text{in}}}{\mu_1}, \tag{10}
$$

which stays at the 1RSB value within about $$10^{-4}$$.

There is a simple reason for this. The potential $$\Phi_2$$ is stationary with
respect to the laws at every solution of the equations, and the corners are a
solution. Call $$D$$ the amplitude of the state along the unstable direction.
Near the corners the potential then has no linear term:

$$
\Phi_2(D) \approx \Phi_1 + \frac{a}{2}D^2 + \frac{b}{3}D^3, \tag{11}
$$

and the new stationary point $$D^* = -a/b$$ shifts the potential by
$$a^3/(6b^2)$$. The curvature $$a$$ vanishes where the instability starts, so
it is proportional to the rate $$\lambda$$. The shift of the free energy is
then of order $$\lambda^3$$, while the energy moves at order $$\lambda^2$$.
Near the birth of the second level, the ground-state energy is almost blind to
it.

## 10. Why this matters, and what is new

Here is my summary of what is new in this work.

- An exact identity at $$x = 1$$, and an exact rejection sampler for every
  $$x$$. Together they remove a finite-sample bias of the standard 2RSB
  algorithm. That bias creates fake second levels.
- A proof that sparse perturbations grow at the one-step rate for every $$x$$.
  So the breakpoint does not move the threshold $$\alpha_m$$ at first order.
- A general monotonicity theorem, Eq. (9). At zero energy it turns $$x$$ into
  a Legendre parameter. At positive energy it fixes $$x$$.
- A negative result at zero energy: the zero-energy instability does not
  produce a stable two-step solution. It moves down one level.
- A positive result above the Gardner point: an exact two-step fixed point
  that is neither embedding. It is stable in the number of atoms, and it has a
  measurable effect on the energy and the complexities.
- A mechanism, stationarity, that explains why this second level leaves the
  ground-state free energy almost unchanged. This is a candidate reason why
  1RSB estimates of the ground-state energy stay precise beyond the Gardner
  point, even though 1RSB is unstable there.

This matters beyond 3-SAT. The same cavity equations describe coloring,
error-correcting codes, compressed sensing, and the energy landscapes of neural
networks. In all of them people use 1RSB results where 1RSB is known to be
unstable. They need to know how large the error is, and where it comes from.
Our results suggest a clear picture for random 3-SAT. The error in the energy
is of third order in the instability rate near its onset. The structure of the
clusters, their energy and their number change at lower order.

The algorithms also benefit. Survey propagation with decimation uses the
surveys to choose variables. A second level changes which clusters dominate at
fixed $$\mu_1$$. So it is a natural place to look for better decimation rules
near the threshold. For single formulas we already computed how the growth
factor of the instability changes when decimation fixes one variable.

## 11. How we made sure that the results hold

A project like this has many places where a sign or a factor of two can hide.
We used three kinds of control at each step.

The first is formal proof. All elementary lemmas are proved in Lean 4 with the
Mathlib library. These include the monotonicity identity (9), the Legendre
relation (10), the stationary-point shift $$a^3/(6b^2)$$ and the Jensen
inequality of the estimator. There are sixteen files, and none contains an
unproved step. The physics steps, for example the identification of the
cavity quantities with the true complexities, stay at the level of physics.
The paper keeps the two levels apart.

The second is numerical, with controls. Every positive result has a negative
control, for example a value of $$\mu_1$$ where 1RSB is stable and the widths
must vanish. Every measured quantity is repeated at larger sizes: more atoms
per law, more surveys, more samples per term.

The third is a rule about finite-size effects. Twice in this project a clear
signal at small size disappeared at larger size. One was the decay of the
widths at 256 atoms per law. The other was the negative internal complexity of
our first estimator. So we trust a signal only when it survives a doubling of
every size that can affect it.

## 12. What is still open

The results hold at one density, $$\alpha = 4.46$$, and one breakpoint,
$$x = \tfrac12$$. The change of the free energy is below our resolution, so we
cannot yet find the $$x$$ at which both complexities vanish. The
$$\lambda^3$$ law is an argument, not a measurement. The next step is to repeat
the computation at a larger density, where the instability rate is larger and
the free-energy shift grows like its cube. If we measure the shift there, with
its sign, we get the first quantitative test of how the second level corrects
the 1RSB ground state of random 3-SAT.

## References

- S. A. Cook, *The complexity of theorem-proving procedures*, STOC (1971).
- M. Mézard, G. Parisi, R. Zecchina, *Analytic and algorithmic solution of random satisfiability problems*, Science 297, 812 (2002).
- M. Mézard, R. Zecchina, *Random K-satisfiability problem: from an analytic solution to an efficient algorithm*, Phys. Rev. E 66, 056126 (2002).
- A. Montanari, G. Parisi, F. Ricci-Tersenghi, *Instability of one-step replica-symmetry-broken phase in satisfiability problems*, J. Phys. A 37, 2073 (2004).
- M. Mézard, G. Parisi, *The cavity method at zero temperature*, J. Stat. Phys. 111, 1 (2003).
- F. Krzakala, A. Montanari, F. Ricci-Tersenghi, G. Semerjian, L. Zdeborová, *Gibbs states and the set of solutions of random constraint satisfaction problems*, PNAS 104, 10318 (2007).
- R. Marino, G. Parisi, F. Ricci-Tersenghi, *The backtracking survey propagation algorithm for solving random K-SAT problems*, Nature Communications 7, 12996 (2016).
- F. Guerra, F. L. Toninelli, *The thermodynamic limit in mean field spin glass models*, Commun. Math. Phys. 230, 71 (2002).
