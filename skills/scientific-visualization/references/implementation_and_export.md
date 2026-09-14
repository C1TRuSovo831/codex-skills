# Scientific figure implementation and export

Read the sections relevant to the requested workflow. Paths and command examples
are relative to the skill directory unless stated otherwise.

### 4. Implement with scoped styles

Use Matplotlib's object-oriented API and temporary style contexts:

```python
import matplotlib.pyplot as plt

from style_presets import style_context

with style_context("default", palette_name="okabe_ito_on_white"):
    fig, ax = plt.subplots(
        figsize=(89 / 25.4, 60 / 25.4),
        layout="constrained",
    )
    ax.plot(x, y, marker="o", label="Observed")
    ax.set(xlabel="Time (hours)", ylabel="Response (unit)")
    ax.legend()
```

`layout="constrained"` supports colorbars, nested GridSpec, subfigures, and `subplot_mosaic`. Do not call `tight_layout()` afterward; it disables constrained layout.

For exact physical dimensions, do not use `bbox_inches="tight"` unless the changed page size is intentional.

#### Color normalization

```python
import matplotlib as mpl

norm = mpl.colors.TwoSlopeNorm(vmin=-2, vcenter=0, vmax=5)
cmap = mpl.colormaps["RdBu_r"].with_extremes(bad="#777777")
image = ax.imshow(values, norm=norm, cmap=cmap, interpolation="nearest")
fig.colorbar(image, ax=ax, label="Change (unit)")
```

Use `LogNorm`, `CenteredNorm`, `SymLogNorm`, `BoundaryNorm`, or `TwoSlopeNorm` only when its mapping matches the scientific meaning.

#### Seaborn

Seaborn 0.13.2 uses the current `errorbar` API:

```python
sns.lineplot(
    data=frame,
    x="time",
    y="response",
    hue="treatment",
    style="treatment",
    markers=True,
    errorbar=("ci", 95),
    n_boot=5000,
    seed=20260723,
    ax=ax,
)
```

Axes-level functions fit custom Matplotlib layouts; figure-level functions create their own figures/facets. Do not customize Seaborn's internal artist lists as if they were stable API.

#### Plotly

- Use `write_html()` for interaction and `write_image()`/`plotly.io.write_images()` for static output.
- Kaleido 1.3.0 requires Chrome/Chromium; it no longer bundles Chrome.
- Current static formats: PNG, JPEG, WebP, SVG, PDF. EPS is Kaleido v0-only.
- Do not pass deprecated `engine=` or use Orca/`plotly.io.kaleido.scope`.
- `width`, `height`, and `scale` control pixels; `scale=3` is not inherently “300 DPI.”
- WebGL traces embed raster content in PDF/SVG.
- Fully offline exports need local external assets when a figure references MathJax/topojson/tiles.

### 5. Export explicitly and record provenance

```python
from figure_export import export_figure

report = export_figure(
    fig,
    "outputs/figure1",
    formats=["pdf", "png"],
    dpi=600,
    bbox_inches=None,  # preserve figure page dimensions
    provenance={
        "raw_data": "data/source.csv",
        "transformations": ["predeclared QC filter", "group mean"],
        "uncertainty": "95% bootstrap CI; seed 20260723",
        "missing_data": "retained as gaps",
    },
    write_manifest=True,
)
```

The exporter refuses implicit overwrite, writes atomically, keeps vector DPI for embedded rasters, uses TIFF LZW, and can use PDF/PS Type 42 fonts. It does not validate scientific content or publisher acceptance.

For editable fonts:

- PDF/PS Type 42 embeds TrueType fonts.
- `svg.fonttype="none"` keeps text editable/searchable but does not embed fonts; appearance depends on installed fonts.
- `svg.fonttype="path"` preserves glyph appearance as paths but loses editable/searchable text.

Use an opaque explicit background unless transparency is required; blending against another background changes apparent contrast.
