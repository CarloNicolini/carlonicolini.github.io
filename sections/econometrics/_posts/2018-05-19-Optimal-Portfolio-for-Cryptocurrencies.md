---
layout: post
title: Optimal portfolio for cryptocurrencies
categories: science
published: false
use_math: true
date: 2018-05-19

---

This blog post will cover some aspects related to mathematical finance, applied to the design of the optimal portfolio in terms of the Markovitz mean-variance theory.

We make use of some famous Python packages, to prepare for the blog post we need to install *scikit-learn*

# Preparation
Let us install some data analysis Python packages first, here are the instructions to work out this thing in Ubuntu.

{% highlight bash %}
pip install numpy pandas scikit-learn
{% endhighlight %}

Fortunately, numerical routines of modern portfolio theory are already implemented in the nice `portfolioopt` package:

{% highlight bash %}
pip install portfolioopt
{% endhighlight %}

For the moment we don't need many other packages.

# Modern Portfolio Theory
We start from the Wikipedia definitions of what is meant by modern portfolio theory:

> Modern portfolio theory (MPT), or mean-variance analysis, is a mathematical framework for assembling a portfolio of assets such that the expected return is maximized for a given level of risk. 

> It is a formalization and extension of diversification in investing, the idea that owning different kinds of financial assets is less risky than owning only one type. 

> Its key insight is that an asset's risk and return should not be assessed by itself, but by how it contributes to a portfolio's overall risk and return. It uses the variance of asset prices as a proxy for risk.

The target of our work is to define the best combinations of stocks or cryptoassets to maximize the portfolio return, keeping the risk as measured by the variance, small.
Hence, a portfolio is a linear combination of the assets' returns.


In visual terms, we want to find the portfolio as the weighted combination of assets such that no further increase in the return can happen without an increase in the risk.

![here](https://uk.scalable.capital/images/3x3i7a9xgm11/2s6len2dpSIM46oGkEQQ4A/5cb73a8b6812dc4b5a0621b57c6c3788/makowitz_efficient_frontier_hd-2.png)



# Code and simulations
	#!/usr/bin/env python3
	# -*- coding: utf-8 -*-
	"""
	Created on Fri Jan 26 17:05:54 2018

	@author: carlo
	"""

	import numpy as np
	import pandas as pd
	import portfolioopt as pfopt
	from sklearn.covariance import LedoitWolf, OAS, EmpiricalCovariance
	from itertools import combinations
	from CryptoMath import cov2cor, cov_robust, corr_robust, is_pos_def

	import logging
	logger = logging.getLogger(__name__)

	# https://plot.ly/ipython-notebooks/markowitz-portfolio-optimization/
	class CryptoPortfolio(object):
	    def __init__(self, returns, method='markowitz', target_return=0.01, **kwargs):
	        self._returns = returns
	        self._avg_returns = self._returns.mean()
	        self._num_assets = len(returns.columns)
	        self._num_samples = returns.shape[0]
	        self._target_return = target_return
	        self._options = kwargs # Optimizer options
	        self._portfolio_method = method
	        if 'cov_estimation' in kwargs.keys():
	            if kwargs['cov_estimation'] == 'OAS': # use Oracle Shrinkage Approximation by sklearn
	                self._returns_cov = self._estimate_cov_oas()
	            elif kwargs['cov_estimation'] == 'LedoitWolf':
	                self._returns_cov = self._estimate_cov_ledoitwolf()
	            elif kwargs['cov_estimation'] == 'Empirical':
	                self._returns_cov = self._estimate_cov_empirical()
	            elif kwargs['cov_estimation'] == 'rmt':
	                self._returns_cov = self._estimate_cov_rmt()
	            else:
	                raise Exception('Must select a covariance estimation method: the following are supported\n\'OAS\'\n\'LedoitWolf\'\n\'Empirical\n\'rmt')
	        else:
	            self._returns_cov = returns.cov()
	        # switch on portfolio optimization method
	        if method == 'markowitz':
	            self._weights = self.markowitz_portfolio(self._options.get('allow_short', False),self._options.get('market_neutral', False))
	        elif method == 'tangency':
	            self._weights = self.tangency_portfolio(allow_short=self._options.get('allow_short'))
	        elif method == 'random':
	            self._weights = self.rand_weights()
	        elif method == 'min_var':
	            self._weights = self.min_var_portfolio()
	        elif method == 'equal':
	            self._weights = np.ones(self._num_assets) / self._num_assets
	        else:
	            raise Exception('Must select a portfolio optimization method\n\'markowitz\'\n\'tangency\'\n\'random\n\'min_var\n\'equal\'')

	        if 'custom_weights' in self._options:
	            self._weights = self._options['custom_weights']

	        # Compute the expected portfolio return given weights
	        self._port_return = (self._weights * self._avg_returns).sum()
	        # Compute the portfolio standard deviation
	        self._port_std = (self._weights * self._returns).sum(1).std()
	        # Compute the Sharpe ratio. Here the risk-free rate is 0
	        self._sharpe = self._port_return / self._port_std * np.sqrt(self._num_samples)

	    def __str__(self):
	        return self.print_portfolio_info()

	    def print_portfolio_info(self):
	        out = 'Portfolio type:' + self._portfolio_method + '\nOptions: ' + str(self._options) +'\nOptimal weights:\n{}\n'.format(self._weights) + ('Target return: {}\n'.format(self._target_return)) + ('Expected return: {}\n'.format(self._port_return)) + ('Expected variance: {}\n'.format(self._port_std**2)) + ('Expected Sharpe: {}\n'.format(self._sharpe))
	        print(out)

	    def get_weights(self):
	        return self._weights

	    def get_sharpe(self):
	        return self._sharpe

	    def get_num_assets(self):
	        return self._num_assets

	    def plot(self):
	        self._weights.plot.bar(stacked=True,grid=True,figsize=(12,12))

	    def markowitz_portfolio(self, allow_short=False, market_neutral=False):
	        return pfopt.markowitz_portfolio(self._returns_cov, self._avg_returns, self._target_return, allow_short, market_neutral)

	    def tangency_portfolio(self, allow_short=False):
	        return pfopt.tangency_portfolio(self._returns_cov, self._avg_returns, allow_short)

	    def min_var_portfolio(self):
	        return pfopt.min_var_portfolio(self._returns_cov)

	    def rand_weights(self):
	        ''' Produces n random weights that sum to 1 '''
	        n = self._num_assets
	        k = np.random.rand(n)
	        return k / np.sum(k)

	    # Construction of covariance estimators
	    def _estimate_cov_oas(self):
	        logger.debug('Covariance estimator OAS')
	        return pd.DataFrame(OAS(assume_centered=self._options.get('assume_centered',False)).fit(self._returns).covariance_,index=self._returns.columns, columns=self._returns.columns)

	    def _estimate_cov_ledoitwolf(self):
	        logger.debug('Covariance estimator LedoitWolf')
	        return pd.DataFrame(LedoitWolf(assume_centered=self._options.get('assume_centered',False)).fit(self._returns).covariance_,index=self._returns.columns, columns=self._returns.columns)
	        
	    def _estimate_cov_empirical(self):
	        logger.debug('Covariance estimator EmpiricalCovariance')
	        return pd.DataFrame(EmpiricalCovariance(assume_centered=self._options.get('assume_centered',False)).fit(self._returns).covariance_,index=self._returns.columns, columns=self._returns.columns)

	    def _estimate_cov_rmt(self):
	        from finrmt import finrmt
	        corr = finrmt(self._returns.values)
	        return pd.DataFrame(corr, index=self._returns.columns, columns=self._returns.columns)

	    def optimize_portfolio_bruteforce(self):
	        # The idea has been taken here:
	        # https://www.quantopian.com/posts/calculating-sharpe-ratio-2
	        import ffn
	        ffn.calc_sharpe(self._port_return, rf=0.0)
	        # Here we compute a number of different portfolios with the selected assets
	        portfolio_size = 2

	        # Create all possible combinations of the assets for the given portfolio size.
	        portfolios = list(combinations(range(0, self._num_assets), portfolio_size))
	        #print(portfolios)

	        sorted_sharpe_indices_complete = np.argsort(sharpe_ratios)[::-1] 
	        # Compute the Sharpe ratios of all these portfolios

	        #print(combinations(portfolios[0],2))
	        # For each possible combination of the assets, add up all the correlations
	        # between the 'portfolio_size' coins
	        total_corr = [sum([self._returns_cov.values[x[0]][x[1]] for x in combinations(p, 2)]) for p in portfolios]
	        #total_corr = [sum([C[x[0]][x[1]] for x in combinations(p, 2)]) for p in portfolios]

	        # The number of porfolios is:
	        #n list(zip(total_corr, portfolios))

	        # Find the portfolio with the smallest sum of correlations, and convert that back into  
	        # the instrument names via a lookup in the symbols array  
	        best_portfolio=[self._returns.columns[sorted_sharpe_indices[i]] for i in portfolios[total_corr.index(np.nanmin(total_corr))]]
	        #print(best_portfolio)

	        # for symbol in best_portfolio:  
	        #     print "symbol={} average_return={} ret_stddev={} sharpe={} avg_vol={}".format(  
	        #         symbol,  
	        #         average_returns[symbol_to_symbols_index[symbol]],  
	        #         return_stdev[symbol_to_symbols_index[symbol]],  
	        #         sharpe_ratios[symbol_to_symbols_index[symbol]],  
	        #         average_volume[symbol_to_symbols_index[symbol]])  

