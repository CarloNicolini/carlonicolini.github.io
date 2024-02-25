---
title: Installing XFormers on Mac M1/M2
layout: post
date: 2024-02-02
published: True
---

# XFormers
`XFormers` is a deep learning library to implement many complex attention operations.
It focuses on providing the *Memory Efficient Attention* as well as many other operations.
For example it also has `BlockSparseAttention` support or any other forms of attention where the attention bias matrix induces a complex attention pattern, like for example in the sliding window attention used in Mistral models

These are my way to install XFormers on Mac M1:

```bash
brew install libomp
brew install llvm
export PATH="/opt/homebrew/opt/libomp/bin:$PATH"
export PATH="/opt/homebrew/opt/llvm/bin:$PATH
export CC=/opt/homebrew/opt/llvm/bin/clang
export CXX=/opt/homebrew/opt/llvm/bin/clang++
```
