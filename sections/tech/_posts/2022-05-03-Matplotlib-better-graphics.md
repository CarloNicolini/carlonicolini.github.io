⸻
layout: post
title: Better graphics with matplotlib and seaborn
date: 2022-05-03
categories: tech
tags: [matplotlib, helvetica]
⸻

High–quality figures are not an aesthetic afterthought. In scientific communication they determine readability, reproducibility, and perceived rigor. Default matplotlib settings are optimized for quick inspection, not for publication. The configuration below standardizes typography, layout, and rendering so that figures are suitable for papers, slides, and vector export.

The recommendations focus on three aspects:
	1.	Vector rendering in notebooks.
	2.	Consistent sans-serif typography.
	3.	Explicit control of font sizes for publication scaling.

The following lines should be included at the beginning of a Jupyter notebook, particularly on macOS systems where Helvetica is typically available.

```python
sns.set_context("notebook") # makes the text in the plots larger, for better visibility
%config InlineBackend.figure_format = 'svg' # makes the plots HD in the notebook
mpl.rcParams["figure.autolayout"] = True # enables tigh layout. Better multiplots
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Helvetica'
```

On Linux (tested on Ubuntu 22.04)

*Helvetica* is not typically available on Linux distributions for licensing reasons. 
A robust substitute is TeX Gyre Heros, part of the TeX Gyre font family. It is metrically compatible with Helvetica and renders well in both raster and vector outputs.

Install the font:

```bash
sudo apt-get install fonts-texgyre
```

After installation, rebuild the system font cache if necessary and clear the matplotlib font cache (~/.cache/matplotlib) to avoid stale font references.

Then configure matplotlib as follows:

```python
sns.set_context("notebook")
%config InlineBackend.figure_format = 'svg'
mpl.rcParams["figure.autolayout"] = True
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = "Arial"
# Force a re-scan of the system fonts in this session
fm.fontManager.addfont('/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreheros-regular.otf')
plt.rcParams['font.family'] = 'TeX Gyre Heros'
```

Explicitly adding the font file ensures that the current Python session recognizes it without requiring a restart. This is useful in containerized or remote environments.

## Good settings for professional-looking figures in scientific papers

Font size calibration should be deliberate. Figures are often resized to fit column widths, typically 8–9 cm for single-column layouts. If fonts are too small at export time, they become unreadable after scaling.

The following configuration has proven effective for journal submissions and technical reports:

# Increase font sizes
```python
plt.rcParams["font.size"] = 16  # General font size
plt.rcParams["axes.titlesize"] = 18  # Title font size
plt.rcParams["axes.labelsize"] = 16  # Axis label font size
plt.rcParams["xtick.labelsize"] = 14  # X-axis tick label size
plt.rcParams["ytick.labelsize"] = 14  # Y-axis tick label size
plt.rcParams["legend.fontsize"] = 14  # Legend font size
plt.rcParams["legend.title_fontsize"] = 15  # Legend title font size
```

Avoid relying solely on DPI when targeting vector formats such as SVG or PDF, since text and lines remain resolution-independent. 
DPI primarily affects raster exports such as PNG.

### Additional Practical Recommendations

Ensure that line widths and marker sizes are increased proportionally when preparing publication figures. Default values are optimized for screen viewing and may appear thin in print.

Use consistent color palettes. Seaborn’s perceptually uniform palettes reduce ambiguity in grayscale printing and improve accessibility for color-vision deficiencies.

Finally, always verify exported figures independently of the notebook environment. Open the generated PDF or SVG directly and inspect it at typical journal column width. Visual inspection at the final scale is the only reliable validation step before submission.