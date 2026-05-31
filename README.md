# OHN Global Map — Business History Academics Worldwide

An interactive map of researchers working in business history, management history, and organisational history, maintained by the [Organizational History Network (OHN)](https://www.theohn.com/).

**Live map:** [stephdeck.github.io/business-history-map](https://stephdeck.github.io/business-history-map/)

---

## Current data (May 2026)

| | |
|---|---|
| Total researchers | **1,366** |
| Countries | **57** |
| City-level markers | **330** |
| Named individual cards | **92** (opted-in, click purple markers) |

---

## How the map works

- **Blue/orange/red markers** — aggregate counts by country or city. Size and colour indicate volume.
- **Purple markers** — individual researchers who have opted in. Click to see name, affiliation and research interests.
- Country markers show the total for that country; city markers show the subset for that city.

---

## Opting in / out

Researchers can add or remove their name, institution and research interests via the Microsoft Forms link on the map. Consent options:

- **Option 1** — counted anonymously in location totals only
- **Option 2** — named card visible on map (name, affiliation, research interests)
- **Option 3/4** — removal from map / underlying database

---

## Updating the map

The master dataset is `BH_AcademicDirectory_v5.xlsx` (held locally, not in this repo). The workflow:

1. Update the master directory spreadsheet
2. Run the rebuild script to regenerate `academics_data.json`
3. Commit and push — GitHub Pages deploys automatically

**Do not edit `academics_data.json` directly on GitHub.** All changes should flow from the master directory to ensure consistency.

---

## Data sources

- Self-submissions via Microsoft Forms (opt-in)
- BHC 2026 conference participant list (anonymous counts only)
- Public institutional data (Google Scholar, university pages)

---

## Technology

- [Leaflet.js](https://leafletjs.com/) — interactive mapping
- [OpenStreetMap](https://www.openstreetmap.org/) — map tiles
- GitHub Pages — free hosting
- Plain HTML/CSS/JavaScript — no build process

---

## Privacy

Only aggregate location counts are displayed by default. Named researchers appear only with explicit Option 2 consent. No email addresses are ever displayed publicly. Individual data is held in a password-protected spreadsheet, not in this repository.

---

*Map tiles © OpenStreetMap contributors. Code: open for academic use.*
