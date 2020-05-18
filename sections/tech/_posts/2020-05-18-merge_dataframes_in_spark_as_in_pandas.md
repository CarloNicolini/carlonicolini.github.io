---
title: How to merge Dataframes in spark as in Pandas
date: 2020-05-18
layout: post
---

This is how you do it:

	def merge(left: Dataset, right: Dataset, left_on: Seq[String], right_on: Seq[String], how: String): Dataset =
	{
		import org.apache.spark.sql.functions.lit
		val joinExpr = left_on.zip(right_on).foldLeft(lit(true)) { case (acc, (lkey, rkey)) => acc and (left(lkey) === right(rkey)) }
		left.join(right, joinExpr, how).toDS
	}


You can use different keys on the left and on the right, as in pandas `pd.merge`
