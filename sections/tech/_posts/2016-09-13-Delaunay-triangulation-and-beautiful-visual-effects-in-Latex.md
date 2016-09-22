---
layout: post
title: Delaunay triangulation and beautiful visual effects in Latex
categories: tech
date: 2016-09-13
---
Recently in the world of the Internet this very fancy coloured pattern appeared:

![Pattern](http://i.stack.imgur.com/hiAVb.png)

This beautiful pattern has been used in many situations and it is also inspiration of some Android OS background.
If you were wondering how to produce those nice patterns of triangles and shades that you see around the web, here is a nice version scripted in LateX.

    {% highlight latex %}
    \documentclass[tikz,border=10pt,multi,rgb]{standalone}
    \usepackage{svgcolor}
    \usetikzlibrary{calc}
    \definecolorseries{colours}{hsb}{grad}[hsb]{.575,1,1}{.987,-.234,0}
    \resetcolorseries[12]{colours}
    \tikzset{
      set my colour/.code={
        \colorlet{mycolour}{colours!!+},
      },
      my colour/.style={
        set my colour,
        bottom color=darkolivegreen!20!mycolour,
        top color=mycolour,
        left color=white!50,
        fill opacity=.5,
      },
    }
    \begin{document}
    \begin{tikzpicture}
      \foreach \i [evaluate={\ii=int(\i-1)}, remember=\i as \ilast] in {0,...,12}{
        \foreach \j [evaluate={\jj=int(\j-1)}, remember=\j as \jlast] in {0,...,12}{
          \coordinate[shift={(\j,\i)}] (n-\i-\j) at (\i*\i+\j*\j-1:\j+\j*\j*rnd);
          \ifnum\i>0
            \path [my colour] (n-\i-\j) -- (n-\ii-\j) -- (n-\ilast-\j) -- cycle;
          \fi
          \ifnum\j>0
            \path [my colour] (n-\i-\j) -- (n-\i-\jj) -- (n-\i-\jlast) -- cycle;
            \path [my colour] (n-\i-\jlast) -- (n-\i-\jj) -- (n-\i-\j) -- cycle;
            \ifnum\i>0
               \path [my colour] (n-\i-\j) -- (n-\i-\jj) -- (n-\ii-\j) -- cycle;
               \path [my colour] (n-\ilast-\j) -- (n-\ilast-\jj) -- (n-\i-\j) -- cycle;
              \pgfmathparse{int(rnd>.5)}
              \ifnum\pgfmathresult=0
                \path [my colour] (n-\ilast-\jlast) -- (n-\ilast-\jj) -- (n-\ii-\jj) -- cycle;
                \path [my colour] (n-\ilast-\j) -- (n-\ilast-\jj) -- (n-\ii-\jj) -- cycle;
                \path [my colour] (n-\i-\jlast) -- (n-\i-\jj) -- (n-\ii-\jj) -- cycle;
                \path [my colour] (n-\i-\j) -- (n-\i-\jj) -- (n-\ii-\jj) -- cycle;
                \path [my colour] (n-\ii-\j) -- (n-\i-\jj) -- (n-\i-\j) -- cycle;
              \else
                \path [my colour] (n-\ii-\j) -- (n-\i-\jj) -- (n-\i-\j) -- cycle;
                \path [my colour] (n-\i-\j) -- (n-\i-\jj) -- (n-\ii-\jj) -- cycle;
                \path [my colour] (n-\i-\jlast) -- (n-\i-\jj) -- (n-\ii-\jj) -- cycle;
                \path [my colour] (n-\ilast-\j) -- (n-\ilast-\jj) -- (n-\ii-\jj) -- cycle;
                \path [my colour] (n-\ilast-\jlast) -- (n-\ilast-\jj) -- (n-\ii-\jj) -- cycle;
              \fi
            \fi
          \fi
        }
      }
    \end{tikzpicture}
    \end{document}
    {% endhighlight %}
    

The result is nice:

<img src="http://i.stack.imgur.com/xJL7S.png" width="200px">

You can obviously change the arrangement of the random dots in the plane, for example by following some mathematical parametric function and then the triangulation happens on the specific parametric surface. For example if you want to arrange the points randomly inside a circle, you have to switch to polar coordinates etc.
To change the colors you should change how the colors are picked from a color map defined in the first lines:

    \definecolorseries{colours}{hsb}{grad}[hsb]{.575,1,1}{.987,-.234,0}

This code means that we are moving from a point `{.575,1,1}` to a point `{.987,-.234,0}` over the color map `hsb`.