---
layout: post
title: Distance matrix of the air500 complex network
categories: science
published: false
date: 2018-03-12
---

<blockquote>
"Download the airport distance matrix of the air500 network"
</blockquote>

The `air500` network is the adjacency matrix of the largest 500 airports in the world.
Unfortunately the original network provided  in the [https://www.dynamic-connectome.org/?page_id=25](https://www.dynamic-connectome.org/?page_id=25) had no latitude/longitude information. 
However the IATA names where available. 

I wrote a simple Python script to fetch the distances between the 500 airports in this network.
The script is based on the database provided at

[https://github.com/jpatokal/openflights/](https://github.com/jpatokal/openflights/)


I used Python and the `geopy` package to compute the distances between airports with the best resolution.

    {% highlight python %}
    import numpy as np
    import pandas as pd
    import geopy.distance

    # Read the airports.dat database as obtained from OpenFlights database
    # https://github.com/jpatokal/openflights/
    df_air = pd.read_csv('airports.dat',header=-1)
    # Here I just changed the IATA code of Hyderabad from HDD to HYD
    # and fixed the DOHA missing IATA

    Air500names = open('air500names.txt').read().split('\n')[0:-1]
    # create the distances matrix, set -1 as default value
    dij = -np.ones([len(Air500names),len(Air500names)])

    # Check if Air500 list
    for s in Air500names:
        if s not in set(df_air[4]):
            print(s,'not existent!')

    print(len(dij))
    # Create the distance matrix, based on geographical distance in kilometers

    for i,airport_iata_i in enumerate(Air500names):
        iata_i = np.where(df_air[4]==airport_iata_i)[0][0]
        print('Progress %.2f' % float(100.0*i/len(dij)) )
        for j,airport_iata_j in enumerate(Air500names):
            if j > i:
                try:
                    iata_j = np.where(df_air[4]==airport_iata_j)[0][0]
                    coord1 = df_air[6][iata_i], df_air[7][iata_i]
                    coord2 = df_air[6][iata_j], df_air[7][iata_j]
                    dij[i,j] = geopy.distance.vincenty(coord1,coord2).km
                except:
                    pass
    dij = dij + dij.T
    np.fill_diagonal(dij,0)
    np.savetxt('Air500_dist.txt', dij, delimiter=' ')
    {% endhighlight %}