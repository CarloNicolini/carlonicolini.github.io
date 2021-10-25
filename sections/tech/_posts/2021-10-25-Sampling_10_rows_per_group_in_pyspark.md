---
title: Sampling 10 rows per groupb in PySpark
date: 2021-10-15
layout: post
---

You need to use a window partition by and let the random number do the shuffle for you.


	from pyspark.sql import Window

	(
	  df
	  .withColumn(
	    "random_number", F.rand()
	  )
	  .withColumn(
	    "row_id",
	    F.row_number().over(
	      Window().partitionBy("level0", "level1", "level2").orderBy(F.col("random_number").desc())
	    )
	  ) 
	  .where(F.col("row_id") < 10)
	  .orderBy("level0", "level1", "level2")
	  .show()
	)

