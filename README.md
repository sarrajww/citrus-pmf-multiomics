# Multi-Omics Showcase — Deployment Checklist & README

## Folder Structure

```
multiomics_app/
├── app.py                  # Main Streamlit application (single file)
├── content_config.yaml     # All text content, citations, findings, impact — edit here
├── requirements.txt        # Python dependencies
├── assets/                 # Place figure images here (PNG/SVG)
│   └── .gitkeep
└── README.md               # This file
```

---

## Streamlit Community Cloud Deployment Checklist

### Pre-deployment
- [ ] Push all files to a public GitHub repository
- [ ] Confirm `requirements.txt` lists all dependencies
- [ ] Confirm `content_config.yaml` is present at repo root (or update path in `app.py`)
- [ ] Confirm `data/` folder and all 3 CSV files are committed
- [ ] Replace all `[NEED ...]` placeholders in `content_config.yaml` with real values from the paper
- [ ] Add real figure images to `assets/` and update gallery section in `page_overview()`

### Streamlit Cloud setup
- [ ] Go to share.streamlit.io → "New app"
- [ ] Connect your GitHub repo
- [ ] Set **Main file path**: `app.py`
- [ ] Set **Python version**: 3.10 or 3.11
- [ ] Click Deploy

### Post-deployment
- [ ] Verify all sidebar pages render without errors
- [ ] Test `content_config.yaml` download button
- [ ] Check that `[NEED ...]` placeholders render with amber/yellow warning styling (not as broken UI)
- [ ] Share URL with collaborators for review

---

## Customization Guide

### Adding real figures
```python
# In page_overview(), replace placeholder with:
st.image("assets/fig1_genome.png", caption="Fig. 1 — Hi-C contact map and assembly statistics")
```

### Updating content without touching code
Edit `content_config.yaml` only. All text blocks, deliverable descriptions, 
finding claims, impact bullets, and resource links are driven from that file.

### Adding a new page
1. Add page name to `PAGES` list in `app.py`
2. Write a `page_newname()` function
3. Add entry to `router` dict


