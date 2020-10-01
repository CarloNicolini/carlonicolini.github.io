---
title: How to force adding prefixes when merging two dataframes in Pandas 
date: 2020-10-01
categories: tech
layout: post
published: false
---


This is how you do:

	def merge_force_prefix(left, right, **kwargs):
	    left_on_col = kwargs['left_on']
	    right_on_col = kwargs['right_on']
	    prefix_tuple = kwargs['prefixes']
	
	    def prefix_col(col, prefix):
	        if col not in left_on_col + right_on_col:
	            return prefix + str(col)
	        else:
	            return col
	
	    left_prefixed = left.rename(columns=lambda x: prefix_col(x, prefix_tuple[0]))
	    right_prefixed = right.rename(columns=lambda x: prefix_col(x, prefix_tuple[1]))
	    del kwargs['prefixes']
	    return pd.merge(left_prefixed, right_prefixed, **kwargs)

