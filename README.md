# Luke F. Miller - Professional Portfolio

This repository contains a static professional portfolio for GitHub Pages and
an example R data pipeline that refreshes a visualization automatically.

## Where to make changes

- `docs/index.html`: home page and resume summary
- `docs/experience.html`: work experience and sample projects
- `docs/research.html`: research interests and sample outputs
- `docs/visualizations.html`: live data visualization page
- `docs/assets/styles.css`: colors, typography, and layout
- `R/update_earthquakes.R`: data source, parsing, validation, and output
- `.github/workflows/update-data-and-deploy.yml`: schedule and deployment
- `docs/downloads/`: resume and downloadable project files

## Replace the example data source

The example uses the public USGS GeoJSON earthquake feed. To replace it:

1. Edit `source_url` near the top of `R/update_earthquakes.R`.
2. Replace the parsing section with fields from the new source.
3. Keep writing a CSV to `docs/data/earthquakes.csv`, or update
   `docs/assets/dashboard.js` to use your new filename and columns.
4. Run `Rscript R/update_earthquakes.R` locally.
5. Commit and push. The GitHub Action also runs the script automatically.

## Local preview

From the repository root:

```powershell
Rscript R/update_earthquakes.R
python -m http.server 8000 --directory docs
```

Then visit `http://localhost:8000`.

## Publishing

In the GitHub repository, choose **Settings > Pages > Build and deployment >
Source > GitHub Actions**. The workflow deploys `docs/` after each push to
`main`, on its schedule, or when started manually from the Actions tab.

