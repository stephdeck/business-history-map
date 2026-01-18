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

- **432** business historians with country data (from 468 total records)
- **126** markers displayed on map
  - **95** city-level markers (micro view - specific cities)
  - **31** country-level markers (macro view - country aggregates)
  
**How counting works:**
- Each person counted ONCE in the dataset (no double-counting)
- City markers show count for that specific city (e.g., "London, UK: 20")
- Country markers show TOTAL for entire country (e.g., "UK: 120" includes London's 20 + all other UK cities)
- **Total displayed: 432** (sum of country markers, which already include city counts)

**Top 10 markers:**
1. UK (country total): 120
2. USA (country total): 60
3. Italy (country total): 32
4. Spain (country total): 21
5. London, UK (city detail): 20
6. Sweden (country total): 18
7. Japan (country total): 18
8. Newcastle, UK (city detail): 17
9. Canada (country total): 16
10. France (country total): 15

## Quick Start - Deploy to GitHub Pages

### Prerequisites
- GitHub account (free at github.com)
- These 2 files: `index.html` and `academics_data.json`
- **Important:** Edit `index.html` to replace the form URL placeholder with your actual Google Form link

### Before Deployment
Open `index.html` in a text editor and find this line (around line 153):
```html
<a href="https://forms.gle/YourFormLinkHere" target="_blank"
```
Replace `YourFormLinkHere` with your actual Google Form ID.

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

- `index.html` (10 KB) - Complete website with corrected counting logic
- `academics_data.json` (15 KB) - 126 markers (95 cities + 31 country aggregates)
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

**Data source:**
- Compiled from public data sources (Google Scholar, university pages, academic fora)
- BH_AcademicDirectory_Jan26.xlsx "List" sheet (468 total, 432 with country)

**Opt-in/Opt-out:**
- Users can request inclusion of their details via form (link in map)
- Users can also request withdrawal via the same form
- Form link displayed on the map: "MOH Map – Fill out form"

**Granularity:**
- City-level markers for specific locations (95 cities)
- Country-level aggregate markers showing total for entire country (31 countries)
- Example: Click "UK" marker → see 120 (all UK historians). Zoom in → see individual cities like "London: 20", "Newcastle: 17"
- **No double-counting**: The 20 in London are part of the 120 in UK

**Data source:** BH_AcademicDirectory_Jan26.xlsx "List" sheet (468 total, 432 with country)

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

### Update Form Link

**Required before deployment:** Replace the placeholder form URL in `index.html`.

Find line ~153:
```html
<a href="https://forms.gle/YourFormLinkHere" target="_blank"
```

Replace with your actual Google Form short URL:
```html
<a href="https://forms.gle/abc123xyz" target="_blank"
```

### Other Customizations

To customize the map, edit `index.html`:

**Update form link (IMPORTANT):**
Line 169: Replace `https://forms.gle/YourFormLinkHere` with your actual Google Form link
- This is the opt-in/opt-out form for academics
- Create your form first, then update the link

**Change title:**
Line 6: `<title>Your Title Here</title>`

**Change heading:**
Line 161: `<h1>Your Heading</h1>`

**Adjust map center:**
Line ~220: `center: [35, 15],` (latitude, longitude)

**Change zoom level:**
Line ~221: `zoom: 3,` (2=world, 5=continent, 10=city)

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
