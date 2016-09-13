---
layout: post
title: Delaunay triangulation and beautiful visual effects in Latex
categories: tech
date: 2016-09-13
---

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

<a href="//imgur.com/M3w46"></a></blockquote><script async src="//s.imgur.com/min/embed.js" charset="utf-8"></script>