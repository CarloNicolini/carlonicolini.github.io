---
layout: post
title: Matlab and CUDA gpudevice freezes on Ubuntu 14.04 with GTX 1070
categories: tech
date: 2017-01-16
---

I've recently installed a system for scientific computing that has a brand new NVidia GeForce GTX1070 at its core.
I'm using Ubuntu 14.04 with the latest compatbile NVidia drivers 361.

Starting from a fresh Ubuntu installation I did the following:

1. I went to "Additional Drivers" section and selected the NVidia Proprietary drivers, version 361.
2. I went to the NVIDia website and I've downloaded the CUDA8 installer, in particular I've chosen the .deb network installer as I think it will keep stuff up-to-date.

To install the CUDA 8.0 then I did:
    
    sudo dpkg -i cuda-repo-ubuntu1404_8.0.44-1_amd64.deb
    sudo apt-get update
    sudo apt-get install cuda

The CUDA files are now stored in `/usr/local/cuda` (a symlink linking to `/usr/local/cuda-8.0`).

Unfortunately, MATLAB R2016b with the parallel computing toolbox only supports CUDA 7.5 and this is a problem. Indeed, The reason for the slow performance observed is because of the one time compilation of the CUDA and MATLAB GPU libraries which may take several minutes. In this case, MATLAB is using a CUDA toolkit(7.5) which does not support the new Pascal architecture(GTX 1070).

To avoid this problem, before starting MATLAB you have to export an environment variable called `CUDA_CACHE_SIZE=
