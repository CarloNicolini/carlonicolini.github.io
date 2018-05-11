---
layout: post
title: Inequalities, traces, densities, matrices
categories: science
published: false
date: 2018-05-11
---

Let us compute the following quantity:


$$
\mathbb{E}\left [S\left (\boldsymbol \rho \| \boldsymbol \sigma\right )\right ]
$$


this could in principle be computed as

$$
\mathbb{E}\left [S\left (\boldsymbol \rho \| \boldsymbol \sigma\right )\right ] = \frac{1}{|G|} \sum \limits_{g \in G} S\left (\boldsymbol \rho \| \boldsymbol \sigma\left (\mathbf{L}_g\right )\right )
$$


Let us define:

$$
\boldsymbol \sigma\left (\mathbf{X}\right ) = \frac{e^{-\beta \mathbf{X}}}{\tr \left \lbrack e^{-\beta \mathbf{X}} \right \rbrack}
$$

\mathbf{I}f Jensen inequality holds here (and it should by the transfer rule for positive definite matrices) then we have:

$$
\mathbb{E}\left \lbrack\boldsymbol \sigma\left (\mathbf{L}\right )\right \rbrack \geq \boldsymbol \sigma \left (\mathbb{E}\left \lbrack \mathbf{L}\right \rbrack\right )
$$

where the inequality is considered on the spectral norm, i.e. the largest eigenvalue.

Expand it and exploit the positivity of relative entropy:

$$
\tr \left \lbrack \boldsymbol \rho \log \boldsymbol \rho \right \rbrack \geq \frac{1}{|G|} \sum \limits_{g \in G}  \tr \left \lbrack\boldsymbol \rho \log\left( \boldsymbol \sigma\left (\mathbf{L}_g\right ) \right) \right \rbrack
$$

the right hand side can be written as:

$$
\frac{1}{|G|} \sum \limits_{g \in G}  \tr \left \lbrack\boldsymbol \rho \log\left( \boldsymbol \sigma\left (\mathbf{L}_g\right ) \right) \right \rbrack = \tr \left \lbrack \boldsymbol \rho \mathbb{E}\left \lbrack \log \boldsymbol \sigma\left (\mathbf{L}\right ) \right \rbrack \right \rbrack
$$

because $$\boldsymbol \rho$$ is a constant matrix and trace and expectations commute.

Now we would like to find some bound on the term $$\mathbb{E}\left \lbrack \log \boldsymbol \sigma\left (\mathbf{L}\right ) \right \rbrack$$.
For positive definite matrices is simple to show that:

$$
\mathbb{E} \left \lbrack \log \left (\boldsymbol \sigma\left (\mathbf{L}\right )\right ) \right \rbrack = \mathbb{E} \left \lbrack \log \frac{e^{-\beta \mathbf{L}}}{\tr \left \lbrack e^{-\beta \mathbf{L}} \right \rbrack}  \right \rbrack = \mathbb{E} \left \lbrack -\beta \mathbf{L} - \mathbf{I}\log\left ( \tr e^{-\beta \mathbf{L}} \right )  \right \rbrack =
$$

$$
= -\beta \mathbb{E}\left \lbrack \mathbf{L} \right \rbrack - \mathbb{E}\left \lbrack \mathbf{I} \log\left ( \tr e^{-\beta \mathbf{L}} \right )\right \rbrack
$$

Now we would like to find an expression for $$\mathbb{E}\left \lbrack \mathbf{I} \log\left ( \tr\left \lbrack e^{-\beta \mathbf{L}} \right \rbrack \right )\right \rbrack$$ that highlights the presence of the term $$\mathbb{E}[\mathbf{L}]$$, so we could find some inequality for the relative entropy that we can use.
By the Peierls-Bogoliubov inequality, the quantity $$\log\left ( \tr\left \lbrack e^{-\beta \mathbf{L}}\right \rbrack \right )$$ is convex, so we can use the Jensen inequality to get:

$$
\mathbb{E}\left \lbrack  \mathbf{I} \log\left ( \tr\left [ e^{-\beta \mathbf{L}}\right ] \right )\right \rbrack \geq \mathbf{I} \log \mathbb{E}\left \lbrack \tr \left \lbrack e^{-\beta \mathbf{L}}\right \rbrack \right \rbrack = \mathbf{I} \log \tr \left \lbrack \mathbb{E}\left \lbrack e^{-\beta \mathbf{L}} \right \rbrack \right \rbrack
$$

but also again by Jensen for convex function:

$$
\mathbb{E}\left \lbrack e^{-\beta \mathbf{L}}\right \rbrack \geq e^{-\beta \mathbb{E}\left [\mathbf{L}\right ]}
$$

and because the log-trace is a monotone growing function we can say:

$$
\log \tr \left \lbrack \mathbb{E}\left \lbrack e^{-\beta \mathbf{L}} \right \rbrack\right \rbrack \geq \log \tr \left \lbrack e^{-\beta \mathbb{E}\left [\mathbf{L}\right ]} \right \rbrack
$$

We now know that $$\log e^{-\beta \mathbb{E}\left [\mathbf{L}\right ]} = -\beta \mathbb{E}\left [\mathbf{L}\right ]$$ and start to substitute it back til the expression for the relative entropy:

We have:

$$
\mathbb{E}\left \lbrack \mathbf{I} \log\left ( \tr e^{-\beta \mathbf{L}} \right )\right \rbrack \geq \log \mathbb{E}\left \lbrack \left ( \tr e^{-\beta \mathbf{L}} \right )\right \rbrack = \log \tr \left \lbrack \mathbb{E}\left \lbrack e^{-\beta \mathbf{L}} \right \rbrack \right \rbrack \geq \log \tr \left \lbrack e^{-\beta \mathbb{E}\left [\mathbf{L}\right ]} \right \rbrack
$$

Multiply by $$\boldsymbol \rho$$ and take the trace on both sides, to get:

$$
\tr \left \lbrack \boldsymbol \rho \mathbb{E}\left \lbrack \mathbf{I} \log\left ( \tr e^{-\beta \mathbf{L}} \right )\right \rbrack \right \rbrack \geq
\tr \left \lbrack \boldsymbol \rho \log \tr \left \lbrack e^{-\beta \mathbb{E}\left [\mathbf{L}\right ]} \right \rbrack \right \rbrack
$$

Now change sign (and also direction of the inequality) and then add the term $$\tr \left [\boldsymbol \rho \log \boldsymbol \rho\right ]$$ to both sides, to get:

$$
\tr \left \lbrack \boldsymbol \rho \log \boldsymbol \rho \right \rbrack - \tr \left \lbrack \boldsymbol \rho \mathbb{E}\left \lbrack \log\left ( \tr e^{-\beta \mathbf{L}} \right )\right \rbrack \right \rbrack \leq
\tr \left \lbrack \boldsymbol \rho \log \boldsymbol \rho \right \rbrack - \tr \left \lbrack \boldsymbol \rho \mathbf{I} \log \tr \left \lbrack e^{-\beta \mathbb{E}\left [\mathbf{L}\right ]} \right \rbrack \right \rbrack
$$

in other words we get:

$$
\mathbb{E}\left \lbrack S(\boldsymbol \rho \| \boldsymbol \sigma(\mathbf{L})) \right \rbrack \leq S(\boldsymbol \rho \| \boldsymbol \sigma(\mathbb{E}[\mathbf{L}]))
$$

Maybe there is an error: we know that the relative entropy is jointly convex so we must have (and it's verified numerically):

$$
\mathbb{E}\left \lbrack S(\boldsymbol \rho \| \boldsymbol \sigma(\mathbf{L})) \right \rbrack \geq S(\boldsymbol \rho \| \mathbb{E}[\boldsymbol \sigma(\mathbf{L})])
$$
