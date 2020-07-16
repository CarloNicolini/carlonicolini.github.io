---
layout: post
title: Installing Jupyter with a Scala + Spark kernel
date: 2020-04-01
---

Installazione SCALA + SPARK + Jupyter

1. Conda
Istruzioni installazione conda e creazione environment con Jupyter-lab

2. Creazione tunnel tramite Putty SSH


3. Installazione almond

 $ ./coursier launch almond:0.9.1 --scala 2.12.10 -- --install --force


jupyter lab --port=8888 --no-browser

2. Aprire un notebook con Kernel Scala (dovrebbe apparire nella scelta)

Importare Spark

>> import $ivy.`org.apache.spark::spark-sql:2.4.0` 
>> import $ivy.`sh.almond::almond-spark:0.9.1`

https://gist.github.com/shadaj/323ad2393b46c1b71df435728a052c24
