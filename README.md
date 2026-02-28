# Multi-Omics Showcase — Deployment Checklist & README

## Folder Structure

```
multiomics_app/
├── app.py                  # Main Streamlit application (single file)
├── content_config.yaml     # All text content, citations, findings, impact — edit here
├── requirements.txt        # Python dependencies
├── data/
│   ├── expression_matrix.csv   # Mock expression data (replace with real)
│   ├── metabolite_table.csv    # Mock metabolite data (replace with real)
│   └── candidate_genes.csv     # Mock candidate list (replace with real)
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
- [ ] Verify all 7 sidebar pages render without errors
- [ ] Test all 3 CSV download buttons
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

### Replacing mock data with real data
Drop real CSV files into `data/` with the same column names (or update 
the column references in `page_findings()` data preview section).

---

## Data File Schemas

### expression_matrix.csv
| Column | Type | Description |
|--------|------|-------------|
| gene_id | str | Unique gene identifier |
| gene_name | str | Short gene name |
| annotation | str | Functional annotation |
| [tissue]_[stage]_r[N] | float | TPM value per replicate |
| module | str | WGCNA module assignment |
| r_nobiletin | float | Pearson r vs. nobiletin |
| r_tangeretin | float | Pearson r vs. tangeretin |

### metabolite_table.csv
| Column | Type | Description |
|--------|------|-------------|
| metabolite_id | str | Internal ID |
| metabolite_name | str | Compound name |
| class | str | Chemical class (PMF, Flavanone, etc.) |
| formula | str | Molecular formula |
| exact_mass_da | float | Exact monoisotopic mass |
| adduct | str | MS adduct form |
| [tissue] | float | Normalized peak area |
| annotation_source | str | Database used |
| confidence_level | str | Level 1–4 per Metabolomics Standards Initiative |

### candidate_genes.csv
| Column | Type | Description |
|--------|------|-------------|
| gene_id | str | Unique gene ID |
| gene_family | str | Enzyme family |
| chromosome | str | Chromosome location |
| module | str | WGCNA module |
| pearson_r_nobiletin | float | Correlation with nobiletin |
| module_membership | float | kME value (0–1) |
| in_vitro_validated | bool | Enzymatic activity confirmed |
| priority_rank | int | 1 = highest priority |
