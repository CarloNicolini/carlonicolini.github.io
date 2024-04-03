---
title: PySpark initialization outside the Pyspark shell
date: 2024-04-03
published: true
---

How you do it with the [findspark](https://pypi.org/project/findspark/) package without the need to startup a Spark shell with the options to load within a jupyterlab session.

```python
try:
    import findspark
    findspark.init()
except ImportError:
    pass

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
import os

spark = (
    SparkSession
    .builder
    .master("local[*]")
    .appName("exercises_notebook")
    .config("spark.sql.catalogImplementation","in-memory")
    .config("spark.sql.warehouse.dir", os.getcwd())
    .getOrCreate()
)
```
