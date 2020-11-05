---
title: Cryptography introduction for bitcoin
layout: post
date: 2020-10-23
published: false
---

[Cryptoassetlab](https://cryptoassetlab.diseade.unimib.it/) centro ricerca congiunto Prometeia-Bicocca, European commission co-organizer

Slide 1:

## Discrete logarithm problem on finite fields and elliptic curves

Asymmetric cryptography: private key -> one-way-function -> public key, funzione non invertibile, invertire la funzione è intrattabile.

Asymmetric cryptography is based on one-way functions, to derive the private key from the corresponding public key is equivalent to solve a computational problem believed to be intractable.
Asymm. crypt. is the same as public-key cryptography, different from symmetric cryptography where the only encryption key cannot be public as it must be secret (private).

Asymm. crypt. makes it possible to do digital signing of documents.

## Sets and binary operator
We use two sets, natural numbers and points on a curve. Cardinality is the number of elements in the set.
Binary operator operates on two elements of the set, returning an element from the set.

A group $(G,\dot)$ is a non-empty set (finite or infinite) with a binary operator also known as *group law* with the following properties.

1. Closure $\forall a,b \in G, a \dot b \in G$
2. Associativity $\forall a,b,c \in G, (a\dot b) \dot c = a\dot(b \dot c)
3. Identity
4. Invertibility: $\forall a \in G, \exists a^{-1} \vert a \dot a^{-1} = a^{-1} \dot a = 1$


A group order is the cardinality of the set.

A cyclic (sub)-group is the subet $\langle g \rangle = g^k$, for $k\in \mathbb{Z}$ is a subgroup of order $|g| \leq | G| $.

$$
\forall a \in \langle g \rangle = 
$$

All cyclic groups are commutative, not all commutative groups are cyclic.

If a group has finite cardinality $N=|G|$, the order $n=|g|$,
When $|G|$ is prime, the group is cyclic with no cyclic subgroups (cofactor $h=1$) and any non neutral element is a generator:
multiplying any element to itself successively, all elements of the set are recovered.

## Discrete logarithm problem.

In a multiplicative group, $(G,\dot)$, for any positive integer $k \in \mathbb{N}-\{0\}$

$$
a = b^k
$$

to calculate $k = \log_b a$ given $a,b \in G$ is the discrete logarithm problem in $(G,\dot)$.

Discrete logarithms are quickly computable in a few special cases, however no efficient method is present.
Discrete logarithm is different from logarithms in real numbers.

*Discrete logarithm crypto systems* are based on finite cyclic subgroup with a generator $g$ of prime order $|g|=n$.

We want for security the DLP in $|g|$ must be intractable, however the opposite must be easy, i.e. given $a=g^k$ 

- A private key is an integer  $k$ in $[1,n-1]$ 
- A public key is $a=g^k$

For computational efficiency we use isomorphisms, basically all cyclic groups of order $n$n are essentially the same. They are basically different representations of the same structure.

## Additive or multiplicative notation

Using additive or multiplicative notation is arbitrary. Insteaf of reverse we could speak about opposite and viceversa.

Integer, real, rational numbers are an additive group of finite order.

Applying DLP problem in additive notation (instead of saying $a=b^k$ we use $a=kb$) we also speak about DLP, even if no logarithm is implied!

# Modular arithmetic
Two numbers are congruent modulo $m$ is $a\equiv r (\mod m)$.
Not necessarily $r$ must be hte remainder of the division of $a$ by $m$. For example $12,7,2$ are congruent modulo $5$.
It is a convention to say that $12 \equiv 2 \mod 5$.

Computation in finite sets:
For a given modulus $m$ it does not matter which element froma  congruence class we choose for a given computation.

$81 \cdot 47 - 280 = 3527 = 2 (mod 5)$

or alternatively $B \cdot C - A = C$, for example $3^10 = 59049 = 4 (mod 5)$

there is a simple way of computing modular arithmetic calculations in finite sets, even if the number of elements is huge.

## Congruence and remainders

If $a_1 \equiv b_1 (mod n)$ and $a_2 \equiv b_2 (mod n$)$ then

$a_1+a_2 \equiv b_1 + b_2$

Ina  few words, applying mod before or after it does not matter.

The set of integer numbers under addition modulo $m$m is a commutative cyclin group of order $m$.
-  the additive neutral element is zero
- the additive inverse of any element $a$ is $m-a$
- $1$ is an obvious generator

$\mathbb{Z} / m \mathbb{Z}$

If $m$ is a prime number, the cyclic number has no subgroups! This means that each element can be used as a generator.
In general 

$$
7 a = 0
$$

in other words, if the order is prime, then $pa=0$. Since $p$ is odd, negation modulo $p$ will map even numbers to odd numbers the other way around: $if $a$ is even, then $-a = p-a$ is odd.
Every even number has an odd opposite.

*All cyclic groups of order $p$ are isomorphic to $\mathbb{Z}/p \mathbf{Z}$

For any prime $p$, $\mathbb{Z}^\star / p  \mathbb{Z}: (\{ 1, \ldots, p-1 \}, \cdot)$ is a commutative group.

- order $p-1$
- thanks to $p$ primality for any element $a$, $gcd(a,p$)=1$, i.e. there exist the inverse $b$ such that $ab=1 \mod p$.

## Fermat little theorem

When $p$ is prime, for each $a$:

$$
a^{p-1} = 1 \mod p
$$

for example $a=4, p=7 \to 3^6 = 1$.

## Field operations in $F_p$
Addition: 4+3 % 7 = 0 means that 3 is the opposite of 4.

Square root in $F_p$ exists but not everywhere.


$\mathbb{Z}/p$ is the most-popular group of a finite field.

Homework: calculate the table of opposites, inverses and square roots for the finite fields $F_{19}$ and $F_{23}$

# Elliptic curves over real nubmers

Defined by the Weierstrass equation:

\begin{equation}
y^2 = x^3 + a x + b
\end{equation}

The curve is non-singular if $\Delta = -16(4a^3 + 27 b^2) \neq 0$. Both $(x,y)$ are affine coordinates, but other coordinates are possible.
We define a group on elliptic curves.

### Point addition P+Q=R

Some resources:
[https://andrea.corbellini.name/2015/05/17/elliptic-curve-cryptography-a-gentle-introduction/](https://andrea.corbellini.name/2015/05/17/elliptic-curve-cryptography-a-gentle-introduction/)

[https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication](https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication)

![https://andrea.corbellini.name/images/point-addition.png](https://andrea.corbellini.name/images/point-addition.png)

### Point doubling Q+Q = R

### Infinity point (aka group identity or neutral element)

Summing two points with same x but opposite y, it shoots the infinity point. Here every point has its opposite, then doubling the point $(x,0)$ also shoots at $\infty$.
This means that $\infty$ is a neutral element


- Elliptic curve points are a commutative group of infinite order.
- The group law is arbitrarily named addition: it could have been called multiplication instead.
- In multiplicative notation doublind would have been called squaring.
- Opposite of point $Q$. The infinity point (zero in additive notation) is providing the oppostive formula:

$$
P+Q = \infty \rightarrow P=-Q
$$

it means $Q$ and $-Q$ have the same $x_Q$ coordinate, therefore the $y$ coordinates are the positive/negative roots of the elliptic curve.

### Scalar multiplication $R = mQ$
It's simply the iteration of the addition operation.

[https://andrea.corbellini.name/ecc/interactive/reals-add.html](https://andrea.corbellini.name/ecc/interactive/reals-add.html)

Clearly $k$ is the private key, while $R$ is the public key.
Il numero di operazioni è polinomiale nel numero di bit per rappresentare $k$.

For any $k\in \mathbb{N}$ double and add allows an efficient computation of $R=kQ$.
To infer $k$ from $\{R,Q\}$ can only be attempted brute-force: for large numbers it becomes computationally infeasible.

On ellpitic curves notation is additive not multiplicative.

Elliptic curves are defined on $F_p$ instead of real-numbers, but on $F_p$ not all numbers have a root.
If $\sqrt(y^2)$ does not exist, then $x$ is not a valid coordinate.


# Bitcoin curve: Koblitz curve secp256k1

We need 256 bit to express $p$, $F_p$ is defined by $p=$ FFFFFFF FFFFFFF FFFFFF FFFFFFFF FFFFFFF FFFFFFF FFFFFFF FFFFFFFE FFFFFFC2F

is a very large prime number.

- The elliptic curve defined over $F_p$ is $y^2 = x^3 + 7$
- the generation point $G$ 


Homework assignment: y^2 = x^3 + 2x +2 over $F_{17}$
- List all its points
- it does not have subgroups, why?



{% highlight python %}
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# elliptic curve
def curve(x,a,b):
    v = np.sqrt(x**3 + a*x + b)
    return v,-v



{% endhighlight %}


# Hash function

Merkle-Damgard hash construction

A hash functin is usually a non-invertible function, should be collision resistant.
Output is so unpredictable that it looks like it was chosen uniformly at random.

Clearly, with SHA256 using 2^130 randomly chosen inputs, there is 99.8% chance to find a collision.

RSA (Rivest Shamir Adleman) cryptography is based on integer factorization. Computing the product of two large numbers is easy, however factorizing is much more complicated.
Diffie-Hellmann key agreement, ElGamal encryption, Digital Signature Algorithm (DSA)

ECDSA = elliptic curve digital signature algorithm, 1985 by Koblitz and Miller is the idea behind Bitcoin.

Key size at comparable security levels indicates how many iterations are needed to crack.

In symmetric cryptography security bits are the number of bits of the keys, while.

DSA is a precise algorithm, faster than RSA, invented to go around the Schnorr method which is patented.


# Notebook

[https://colab.research.google.com/drive/1IxL0ecWxAI9lRXYdAXhDdg5BzsCW4MHd](https://colab.research.google.com/drive/1IxL0ecWxAI9lRXYdAXhDdg5BzsCW4MHd)


# Digital signature scheme


{% highlight python %}

from btclib import dsa
from btclib.curve import mult
from btclib.curves import secp256k1 as ec
from btclib.dh import ansi_x964_kdf

msg = "Hello I'm Alice"
print('ECDSA')

dsa_prv, dsa_pub = dsa.gen_keys()

print('prv', hex(dsa_prv))
print('pub', hex(dsa_pub[0]), hex(dsa_pub[1])) # x,y coordinates of public key

dsa_sig = dsa.sign(msg, dsa_prv)

dsa_valid = dsa.verify(msg, dsa_pub, dsa_sig)
print('Valid ECDSA sig:", dsa_valid')
{% endhighlight %}

# SSA

{% highlight python %}

from btclib import ssa
from btclib.curve import mult
from btclib.curves import secp256k1 as ec
from btclib.dh import ansi_x964_kdf

msg = "Hello I'm Alice"
print('ECDSA')

ssa_prv, ssa_pub = ssa.gen_keys()

print('prv', hex(ssa_prv))
print('pub', hex(ssa_pub))

ssa_sig = ssa.sign(msg, ssa_prv)

ssa_valid = dsa.verify(msg, ssa_pub, ssa_sig)
print('Valid ECSSA sig:", ssa_valid')
{% endhighlight %}


# ECBMS
print('ECBMS')

{% highlight python %}
from btclib import bms
from btclib.curve import mult
from btclib.curves import secp256k1 as ec
from btclib.dh import ansi_x964_kdf

msg = "Hello I'm Alice"
print('ECDSA')

bms_prv, bms_pub = bms.gen_keys()

print('prv', hex(bms_prv))
print('pub', hex(bms_pub))

bms_sig = bms.sign(msg, bms_prv)

print("rf:", bms_prv)
print("rf:", bms_pub)

bms_valid = dsa.verify(msg, bms_pub, bms_sig)
print('Valid ECbms sig:", bms_valid')

{% endhighlight %}

# Diffie-Hellman key exchange

The key-exchange is as hard as the DLP, but not harder.

- Signal protocol uses ECDH to obtain post-compromise security.
Implementations of this protocol are found in Signal, WhatsApp, Facebook messenger.

*Standards for efficient cryptography* while the shared secret key may be used directly as a key, it can be desirable to hash it to remove weak bits.

Weak bits are a subset of the domain.


# Advanced encryption standard (AES)

- Established by NIST in 2001
- Is a subset of the Rijndael block cipher
- AES is the most widely used symmetric cipher

- Applications:
* US government
* Internet security standard Ipsec, TLS
* Wifi-encryption
* Whatsapp, Facebook messenger, Signal

# Counter Mode (CTR) 1/2

CTR turns a block cipher into a stream cipher
Message is divided into  smaller pieces (128 bit)

- It generates the next keystream block by encrypting successive values of a counter
- The counter can be any function which produces a sequence which is guaranteeed to to repeat for a long time, an actual increment-by-one counter is the simplest and most popular.

{% highlight python %}
import secrets
import pyaes
msg = "ciao ciccio"
aes_encrypt = pyaes.AESModeOfOperationCTR(key_256)
aes_decrypt = pyaes.AESModeOfOperationCTR(key_256)
encrypted_msg = aes_encrypt.encrypt(msg)
encrypted_msg.hex()
aes_decrypt.decrypt(encrypted_msg)
{% endhighlight %}

