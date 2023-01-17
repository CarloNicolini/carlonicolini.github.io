---
title: 
date: 2022-09-15
published: true
---


# Python dependencies for having detectron2 running on Mac OS

I am running on Mac M1 Pro, MacOS Monterey 12.3.
My conda environment has Python 3.8 installed. GRPC has been installed `grpcio`.

`CC=clang CXX=clang++ ARCHFLAGS="-arch x86_64" python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'`

I've followed this instruction for building `grpcio`.
If you have problems with it, please install it through `firebase-admin`

- [https://stackoverflow.com/questions/66640705/how-can-i-install-grpcio-on-an-apple-m1-silicon-laptop](https://stackoverflow.com/questions/66640705/how-can-i-install-grpcio-on-an-apple-m1-silicon-laptop)
- [https://github.com/facebookresearch/detectron2/issues/4183](https://github.com/facebookresearch/detectron2/issues/4183)


