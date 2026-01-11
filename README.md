# Business History Academics - Global Distribution Map

An interactive map showing the global distribution of 484 business historians across 16 locations worldwide.

**Privacy-focused:** Only displays aggregate counts by location. No individual names or email addresses.

## Live Demo

After deployment, your map will be accessible at:
```
https://yourusername.github.io/business-history-map/
```

## Features

✓ Interactive world map with zoom and pan  
✓ Numbered markers sized by population  
✓ Color-coded by size (blue: small, orange: medium, red: large)  
✓ Click markers to see location name and count  
✓ Mobile responsive  
✓ Privacy compliant - **no personal data displayed**  

## Data Summary

- **422** total business historians (from detailed directory)
- **119** locations worldwide (cities and countries)
- **92** city-level locations with precision data
- **27** country-level aggregates (where city data unavailable)
- **Top 5 locations:**
  1. USA (country-level): 38
  2. Newcastle, UK: 21
  3. London, UK: 19
  4. Canada (country-level): 13
  5. Reading, UK: 11

## Quick Start - Deploy to GitHub Pages

### Prerequisites
- GitHub account (free at github.com)
- These 2 files: `index.html` and `academics_data.json`

### Deployment Steps (10 minutes)

1. **Create GitHub account** at https://github.com (if needed)

2. **Create new repository:**
   - Click "New" repository
   - Name: `business-history-map` (or your choice)
   - Visibility: Public
   - Click "Create repository"

3. **Upload files:**
   - Click "uploading an existing file"
   - Drag both `index.html` and `academics_data.json`
   - Click "Commit changes"

4. **Enable GitHub Pages:**
   - Go to Settings → Pages
   - Source: "Deploy from a branch"
   - Branch: "main", Folder: "/ (root)"
   - Click "Save"

5. **Access your site:**
   - Wait 2-3 minutes
   - Refresh Settings → Pages
   - Your URL appears: `https://yourusername.github.io/business-history-map/`
   - Click to open

**Done!** Your map is now live.

## Files

- `index.html` (10 KB) - Complete website
- `academics_data.json` (12 KB) - Location counts with city-level detail
- `README.md` - This file

## Updating Data

To update counts:

1. Go to your repository
2. Click on `academics_data.json`
3. Click the pencil icon (Edit)
4. Update the counts
5. Click "Commit changes"
6. Wait 2-3 minutes for automatic rebuild

## Technology

- Leaflet.js 1.9.4 (interactive mapping)
- OpenStreetMap (map tiles)
- Pure HTML/CSS/JavaScript (no build process)
- GitHub Pages (free hosting)

## Privacy & Data

**What's displayed:**
- Location names (countries and cities where available)
- Aggregate counts per location
- Total number of historians

**What's NOT displayed:**
- Individual names
- Email addresses
- Institutional affiliations
- Any personally identifiable information

**Granularity:**
- City-level precision where available (92 cities)
- Country-level where city data not available (27 countries)

**Data source:** Derived from BH_AcademicDirectory_Jan26.xlsx "List" sheet

## Browser Support

Works on all modern browsers:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Cost

**$0** - Completely free with GitHub Pages

- No hosting fees
- No bandwidth charges
- Free SSL certificate (HTTPS)
- No maintenance costs

## Support

If you encounter issues:

1. **Map doesn't load:**
   - Check both files are uploaded
   - Wait 5 minutes after enabling Pages
   - Try a different browser
   - Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

2. **No markers appear:**
   - Verify `academics_data.json` is uploaded
   - Check browser console (F12) for errors
   - Ensure file is in same folder as index.html

3. **Numbers seem wrong:**
   - Total should be 484 historians
   - 16 locations should appear
   - Check your source data file

## Customization

To customize the map, edit `index.html`:

**Change title:**
Line 6: `<title>Your Title Here</title>`

**Change heading:**
Line 148: `<h1>Your Heading</h1>`

**Adjust map center:**
Line 202: `center: [35, 15],` (latitude, longitude)

**Change zoom level:**
Line 203: `zoom: 3,` (2=world, 5=continent, 10=city)

**Modify marker colors:**
Lines 110-123: CSS color properties

## License

Map code: Open for academic use  
Map tiles: © OpenStreetMap contributors  
Data: Aggregated business history academics directory  

## Updates

Last updated: January 2026  
Data version: January 2026 directory  

---

## Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| 404 error | Wait 5 minutes, check Pages settings |
| No data | Verify academics_data.json is uploaded |
| Slow loading | Normal for first visit, caches after |
| Mobile issues | Use latest browser version |

---

**Ready to deploy?**

1. Upload `index.html` and `academics_data.json` to GitHub
2. Enable Pages in repository Settings
3. Share your URL!

**Questions?** Check GitHub Pages documentation: https://docs.github.com/pages
