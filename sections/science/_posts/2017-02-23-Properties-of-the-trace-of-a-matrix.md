---
layout: post
title: Properties of the trace of a matrix
categories: science
published: false
date: 2017-02-24
--- 

Here is a list of the properties of the trace of a matrix.

The trace is a linear operator
- $$\tr(\mathbf{A}+\mathbf{B}) = \tr(\mathbf{A}) + \tr(\mathbf{B})$$
but instead it is true that the trace of the Kronecker product of two matrices is the product of the traces:
$$\tr(A \otimes B)=\tr(A)\tr(B)$$.
- Differently from the determinant, the trace of the product is different than the product of the traces: $$\tr(AB) \neq \tr(A)\tr(B) $$ but $$\tr(\mathbf{AB})=\tr(\mathbf{BA})$$.
- $$\tr(\alpha  \mathbf{A}) = \alpha \tr(\mathbf{A})$$ where $$\alpha$$ is a scalar.
- The trace is equal to the sum of eigenvalues $$\tr(\mathbf{A}) = \sum \limits_i^n \lambda_i(\mathbf{A})$$ 
- A useful relation between the trace of a matrix and the determinant is the Jacobi formula:

$$
\frac{d}{d t} \det(\mathbf{A}(t) = \tr(\mathbf{A(t)})
$$

- If $$A$$ is symmetric and $$B$$ is antisymmetric then $$\tr(AB)=0$$.
- $$\tr(A^k) = \sum_{i=0}^N \lambda_i^k$$

- The Golden-Thompson inequality, for any complex matrices: 
$$ \tr( \exp{(A+B)}) \leq \tr e^A e^B$$.

- The Gibbs variational principle: let $$H$$ be a self-adjoint operator such that $$e^{-H}$$ is trace class, then for any $$\gamma \geq 0$$ with $$\tr \gamma = 1$$, then $$ \tr(\gamma H) + \tr(\gamma \log(\gamma)) \geq - \log(\tr(e^{-H}))$$.