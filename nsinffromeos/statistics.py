#!/usr/bin/python
#__author__ = 'philippe.landry@ligo.org'
#__date__ = '07-2019'

import numpy as np
from scipy.stats import gaussian_kde
from scipy.integrate import simps as integrate
from scipy.optimize import minimize_scalar as findroot

# BASIC KDE-BASED STATS TOOLS

def prob(ydat,xgrid):

	return integrate(ydat,xgrid)

def kdeprob(xdat,res=1e3):

	kde = gaussian_kde(xdat)
	xgrid = np.linspace(min(xdat),max(xdat),res)
	ydat = kde(xgrid)

	return prob(ydat,xgrid)

def mode(ydat,xgrid):

	maxval = max(ydat)
	maxpos = list(ydat).index(maxval)

	return xgrid[maxpos]

def Lci(cl,xref,xdat,res=1e3):

	if not xref:
		xref = min(xdat)
		Lbnds = [xref,max(xdat)]
	else:
		Lbnds = [min(xdat),xref]
	
	kde = gaussian_kde(xdat)

	def cumprob(xbnd):
	
		xgrid = np.linspace(xref,xbnd,res)
		ydat = kde(xgrid)
		
		return abs(0.5*cl-abs(prob(ydat,xgrid)))
		
	rootL = findroot(cumprob,bounds=tuple(Lbnds),method='bounded',options={'xatol':1e-3})
	xbndL = rootL.x
	
	return xbndL
	
def Rci(cl,xref,xdat,res=1e3):

	if not xref:
		xref = max(xdat)
		Rbnds = [min(xdat),xref]
	else:
		Rbnds = [xref,max(xdat)]
		
	kde = gaussian_kde(xdat)

	def cumprob(xbnd):
	
		xgrid = np.linspace(xref,xbnd,res)
		ydat = kde(xgrid)
		
		return abs(0.5*cl-abs(prob(ydat,xgrid)))
		
	rootR = findroot(cumprob,bounds=tuple(Rbnds),method='bounded',options={'xatol':1e-3})
	xbndR = rootR.x
	
	return xbndR

def symci(cl,xref,xdat,res=1e3):

	xbndL = Lci(cl,xref,xdat,res)
	xbndR = Rci(cl,xref,xdat,res)
	
	return [xbndL,xref,xbndR]

def median(xdat,res=1e3):

	return Lci(1.0,False,xdat,res)

# BASIC DISCRETE STATS TOOLS

def median_sample(dat): # calculated from left

	dat.sort()
	mid = len(dat)/2 + 1
	med = dat[mid]

	return med
	
def quantile_sample(dat,quant): # calculated from left

	dat.sort()
	bnd = int(round(len(dat)*quant))
	quantile = dat[bnd]
	
	return quantile

def hpd_sample(dat,cl):

	dat = [datum for datum in dat if datum == datum]
	norm = len(dat)
	dat = np.array(dat)
	hist, bin_edges = np.histogram(dat,bins='auto')
	bins = [(bin_edges[i],bin_edges[i+1]) for i in range(len(bin_edges)-1)]
	hist_dat = zip(hist,bins)
	hist_dat.sort(reverse=True)
	hist, bins = zip(*hist_dat)
	hist = list(hist)
	bins = list(bins)
	
	for i in range(len(bins)):
		subdat = []
		for j in range(i+1):
			bin = bins[j]
			subdat.extend(dat[(dat >= bin[0]) & (dat < bin[1])])
		prob = float(len(list(subdat)))/norm
		if i == 0: maxap = 0.5*(min(subdat)+max(subdat))
		if prob >= cl: break
	
	lb, ub = min(subdat), max(subdat)

	return lb, maxap, ub	
