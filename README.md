# Luke F. Miller - Professional Portfolio

This repository contains a static professional portfolio for GitHub Pages and
an example R data pipeline that refreshes a visualization automatically.

## Where to make changes

- `docs/index.html`: home page and resume summary
- `docs/experience.html`: work experience and sample projects
- `docs/research.html`: research interests and sample outputs
- `docs/visualizations.html`: live data visualization page
- `docs/assets/styles.css`: colors, typography, and layout
- `R/update_solar.R`: solar-forecast source, parsing, validation, and model
- `.github/workflows/update-data-and-deploy.yml`: schedule and deployment
- `docs/downloads/`: resume and downloadable project files

## Live energy demonstration

The site uses the public Open-Meteo forecast API to retrieve hourly solar
radiation, temperature, and cloud cover for four Hawai'i locations. The R
pipeline validates the feed and publishes a transparent illustrative PV model.
To adapt it:

1. Edit the locations, source, or assumptions in `R/update_solar.R`.
2. Revise the validation and transformation fields as needed.
3. Keep writing a CSV to `docs/data/hawaii_solar.csv`, or update
   `docs/assets/dashboard.js` to use your new filename and columns.
4. Run `Rscript R/update_solar.R` locally.
5. Commit and push. The GitHub Action also runs the script automatically.

## Local preview

From the repository root:

```powershell
Rscript R/update_solar.R
python -m http.server 8000 --directory docs
```

Then visit `http://localhost:8000`.

## Publishing

In the GitHub repository, choose **Settings > Pages > Build and deployment >
Source > GitHub Actions**. The workflow deploys `docs/` after each push to
`main`, on its schedule, or when started manually from the Actions tab.

