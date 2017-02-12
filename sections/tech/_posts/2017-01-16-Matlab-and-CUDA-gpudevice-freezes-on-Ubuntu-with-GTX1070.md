---
layout: post
title: Matlab and CUDA gpudevice freezes on Ubuntu 14.04 with GTX 1070
categories: tech
date: 2017-01-16
---

In Ubuntu 14.04 with MATLAB R2016b it may happen that after an installation of CUDA8 and NVidia drivers 367, the calls to specific CUDA functions such as `gpudevice` or `gpuArray` are very slow the first time you call them.
This is because MATLAB R2016b it's not built against the latest CUDA drivers so fat binaries have to be built once.
In this case, MATLAB is using a CUDA toolkit (7.5) which does not support the new Pascal architecture on my Geforce GTX 1070.
This operation may take some minutes to end, as nearly 400 MB have to be compiled and saved in `.nv/ComputeCache`.
In theory this cache is built once and every successive instance of MATLAB should not take too long for first calling CUDA functions.
Anyway it is the case that this is not completely true.

If you like me are facing this issue, some environment variables have to be set (as suggested from NVIDIA developer site)

    export CUDA_CACHE_MAXSIZE=2147483648
    export CUDA_CACHE_DISABLE=0
    export CUDA_CACHE_PATH=$HOME/.nv/ComputeCache

I'm hoping that the next MATLAB release will support CUDA8.
