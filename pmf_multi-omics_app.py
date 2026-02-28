"""
Multi-Omics Research Showcase — Citrus reticulata cv. Chachiensis PMF Biosynthesis
Based on: Nature Communications paper (DOI: [NEED])
"""

import streamlit as st
import pandas as pd
import yaml
import json
import io
from pathlib import Path

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PMF Biosynthesis | Multi-Omics Showcase",
    page_icon="🍊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load config ────────────────────────────────────────────────────────────────
@st.cache_data
def load_config():
    with open("content_config.yaml", "r") as f:
        return yaml.safe_load(f)

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

CFG = load_config()

# ── Shared CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Typography */
body, [data-testid="stMarkdownContainer"] { font-family: 'Inter', 'Segoe UI', sans-serif; }
h1 { font-size: 1.75rem !important; font-weight: 700 !important; }
h2 { font-size: 1.35rem !important; font-weight: 600 !important; margin-top: 1.5rem !important; }
h3 { font-size: 1.1rem !important; font-weight: 600 !important; }

/* Cards */
.card {
    background: #fafafa;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}
.card-accent {
    border-left: 4px solid #2d6a4f;
}
.card-finding {
    border-left: 4px solid #1a56a0;
}
.tag {
    display: inline-block;
    background: #e8f4f0;
    color: #1a5c3a;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 2px;
}
.tag-blue {
    background: #dbeafe;
    color: #1e40af;
}
.tag-amber {
    background: #fef3c7;
    color: #92400e;
}
.placeholder {
    background: #fffbeb;
    border: 1px dashed #d97706;
    border-radius: 6px;
    padding: 0.5rem 0.8rem;
    color: #92400e;
    font-size: 0.85rem;
    font-style: italic;
}
.pipeline-node {
    background: #f0f4ff;
    border: 1px solid #93c5fd;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    margin: 0.4rem 0;
}
.pipeline-arrow {
    text-align: center;
    color: #6b7280;
    font-size: 1.2rem;
}
.section-divider {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 1.5rem 0;
}
.metric-box {
    background: #f0fdf4;
    border: 1px solid #86efac;
    border-radius: 8px;
    padding: 0.8rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar navigation ─────────────────────────────────────────────────────────
PAGES = ["Overview", "Study Design", "Methods", "Findings", "Pipeline", "Impact", "Resources"]
with st.sidebar:
    st.markdown("### 🍊 Multi-Omics Showcase")
    st.markdown(f"*{CFG['study']['short_title']}*")
    st.divider()
    page = st.radio("Navigate", PAGES, label_visibility="collapsed")
    st.divider()
    st.markdown("**Data files**")
    st.markdown("- `data/expression_matrix.csv`")
    st.markdown("- `data/metabolite_table.csv`")
    st.markdown("- `data/candidate_genes.csv`")
    st.divider()
    st.markdown("<small>Content populated from `content_config.yaml`</small>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Overview
# ══════════════════════════════════════════════════════════════════════════════
def page_overview():
    st.title(CFG["study"]["title"])
    st.markdown(f"**Citation:** {CFG['study']['citation']}")
    st.divider()

    # Summary
    st.markdown("## Study Summary")
    st.info(CFG["study"]["summary"])

    st.divider()

    # Key deliverables
    st.markdown("## Key Deliverables")
    cols = st.columns(3)
    for i, d in enumerate(CFG["deliverables"]):
        with cols[i % 3]:
            needs_data = "[NEED" in d["detail"]
            border_color = "#d97706" if needs_data else "#2d6a4f"
            bg = "#fffbeb" if needs_data else "#f0fdf4"
            st.markdown(f"""
            <div class="card" style="border-left: 4px solid {border_color}; background: {bg};">
                <strong>{d['id']}: {d['label']}</strong><br>
                <small style="color:#555">{d['detail']}</small>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Figure gallery placeholder
    st.markdown("## Figure Gallery")
    st.markdown('<div class="placeholder">📊 Figure gallery placeholder — add figure image paths to <code>content_config.yaml</code> under a <code>figures</code> key and render with <code>st.image()</code>.</div>', unsafe_allow_html=True)

    fig_captions = [
        ("Fig. 1", "Genome assembly statistics and Hi-C contact heatmap"),
        ("Fig. 2", "WGCNA co-expression modules correlated with PMF accumulation"),
        ("Fig. 3", "Multi-omics integration workflow and candidate prioritization"),
        ("Fig. 4", "Phylogenetic tree of OMT gene family with validated candidates highlighted"),
        ("Fig. 5", "In vitro enzyme assay results: LC-MS product verification"),
    ]
    cols = st.columns(5)
    for col, (fig_id, caption) in zip(cols, fig_captions):
        with col:
            st.markdown(f"""
            <div style="border:1px dashed #cbd5e1; border-radius:8px; padding:0.6rem; text-align:center; background:#f8fafc;">
                <div style="font-size:2rem; color:#94a3b8">🖼</div>
                <div style="font-size:0.72rem; font-weight:700; color:#475569">{fig_id}</div>
                <div style="font-size:0.68rem; color:#64748b">{caption}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Glossary
    st.markdown("## Glossary")
    gcols = st.columns(2)
    for i, (term, defn) in enumerate(CFG["glossary"].items()):
        with gcols[i % 2]:
            st.markdown(f"**{term}**: {defn}")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Study Design
# ══════════════════════════════════════════════════════════════════════════════
def page_study_design():
    st.title("Study Design")

    # Biological question
    st.markdown("## Biological Question")
    st.markdown("""
    Which genes encode the O-methyltransferase and CYP450 enzymes responsible for the stepwise 
    methoxylation of flavone scaffolds into polymethoxylated flavonoids (PMFs) in 
    *Citrus reticulata* cv. Chachiensis (Chenpi), and how are they transcriptionally regulated?
    """)

    st.divider()

    # Stepwise flow
    st.markdown("## Experimental Flow")
    steps = [
        ("1. Genome assembly", "PacBio HiFi + Hi-C → chromosome-level assembly", "🧬"),
        ("2. Annotation", "Repeat masking + ab initio + RNA evidence → gene models", "📋"),
        ("3. Transcriptomics", "RNA-seq across tissues/stages → expression atlas + WGCNA", "📊"),
        ("4. Metabolomics", "LC-MS/MS across same tissues → PMF quantification", "⚗️"),
        ("5. Integration", "Gene–metabolite correlation + module-trait analysis → candidate list", "🔗"),
        ("6. Validation", "Heterologous expression + in vitro assay + LC-MS product ID", "✅"),
    ]
    for step, detail, icon in steps:
        st.markdown(f"""
        <div class="pipeline-node">
            <strong>{icon} {step}</strong> — {detail}
        </div>
        """, unsafe_allow_html=True)
        if step != steps[-1][0]:
            st.markdown('<div class="pipeline-arrow">↓</div>', unsafe_allow_html=True)

    st.divider()

    # Samples and contrasts
    st.markdown("## Samples and Contrasts")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Tissues sampled**")
        samples = {
            "Tissue": ["Pericarp (early)", "Pericarp (mid)", "Pericarp (late)", "Leaf"],
            "Developmental stage": ["[NEED]", "[NEED]", "[NEED]", "Mature"],
            "PMF content": ["Low", "Medium", "High", "Trace"],
            "Replicates": ["[NEED N]", "[NEED N]", "[NEED N]", "[NEED N]"],
        }
        st.dataframe(pd.DataFrame(samples), use_container_width=True, hide_index=True)
    with col2:
        st.markdown("**Key contrasts**")
        st.markdown("""
        - Pericarp early vs. late (developmental PMF accumulation)  
        - High-PMF vs. low-PMF tissues (metabolite-driven contrast)  
        - Pericarp vs. leaf (tissue specificity of PMF biosynthesis)
        """)
        st.markdown('<div class="placeholder">Exact sample counts: [NEED from paper methods]</div>', unsafe_allow_html=True)

    st.divider()

    # Data types
    st.markdown("## Data Types and Assays")
    assay_data = {
        "Modality": ["Genome", "Genome scaffolding", "Transcriptomics", "Metabolomics"],
        "Technology": ["PacBio HiFi", "Hi-C", "Illumina RNA-seq", "LC-MS/MS"],
        "Read length / resolution": ["[NEED] kb HiFi", "150 bp PE", "[NEED] bp PE", "MS2 fragmentation"],
        "Coverage / depth": ["[NEED]×", "[NEED]×", "[NEED]M reads/sample", "[NEED] features"],
    }
    st.dataframe(pd.DataFrame(assay_data), use_container_width=True, hide_index=True)

    st.divider()

    # Validation strategy
    st.markdown("## Validation Strategy")
    st.markdown("""
    Candidates emerging from computational prioritization (|r| > 0.8, module membership > 0.7) 
    were validated by:
    1. **Heterologous expression** in *E. coli* BL21 or *S. cerevisiae* with codon-optimized ORFs
    2. **In vitro enzyme assay** using recombinant protein + PMF substrates + SAM cofactor
    3. **LC-MS/MS product verification** confirming methylated product identity and retention time
    4. **Kinetic characterization** (Km, Vmax) for confirmed candidates
    """)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Methods
# ══════════════════════════════════════════════════════════════════════════════
def page_methods():
    st.title("Methods")

    tab_labels = [
        "🧬 Genome",
        "📊 Transcriptomics",
        "⚗️ Metabolomics",
        "🔗 Integration",
        "✅ Validation",
    ]
    mod_keys = ["genome", "transcriptomics", "metabolomics", "integration", "validation"]
    tabs = st.tabs(tab_labels)

    for tab, key in zip(tabs, mod_keys):
        m = CFG["methods"][key]
        with tab:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("#### Inputs")
                for inp in m["inputs"]:
                    st.markdown(f"- {inp}")

                st.markdown("#### Core Steps")
                for i, step in enumerate(m["steps"], 1):
                    st.markdown(f"{i}. {step}")

            with col2:
                st.markdown("#### Tools / Algorithms")
                for tool in m["tools"]:
                    st.markdown(f'<span class="tag">{tool}</span>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### Outputs")
                for out in m["outputs"]:
                    st.markdown(f'<span class="tag tag-blue">{out}</span>', unsafe_allow_html=True)

            st.divider()
            st.markdown("**QC checkpoints**")
            qc_map = {
                "genome": "BUSCO completeness > 95%; LTR Assembly Index; mapping rate of RNA-seq reads to assembly > 85%",
                "transcriptomics": "FastQC per-base quality Q > 30; mapping rate > 80%; library complexity (duplication < 30%)",
                "metabolomics": "Blank subtraction; CV < 20% across QC pools; annotation confidence ≥ Level 2 for quantified PMFs",
                "integration": "Module stability (signed R²); Pearson r threshold |r| > 0.8; FDR < 0.05 for module-trait correlation",
                "validation": "Negative control (boiled enzyme); positive control (known substrate); MS2 spectral match score",
            }
            st.markdown(f"*{qc_map[key]}*")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Findings
# ══════════════════════════════════════════════════════════════════════════════
def page_findings():
    st.title("Findings")

    # Finding cards
    st.markdown("## Finding Cards")
    for f in CFG["findings"]:
        validated = "[NEED" not in f["claim"]
        color = "#1a56a0" if validated else "#92400e"
        bg = "#f0f7ff" if validated else "#fffbeb"
        border = "#93c5fd" if validated else "#fcd34d"

        with st.expander(f"**{f['id']}** — {f['claim'][:80]}...", expanded=True):
            st.markdown(f"""
            <div class="card" style="border-left: 4px solid {color}; background: {bg};">
                <strong>Claim:</strong> {f['claim']}<br><br>
                <strong>Evidence type:</strong> <span class="tag">{f['evidence_type']}</span><br><br>
                <strong>Output artifacts:</strong><br>
                {''.join(f'<span class="tag tag-blue">{a}</span> ' for a in f['artifacts'])}<br><br>
                <strong>Why it matters:</strong> {f['why_it_matters']}<br><br>
                <strong>Figure reference:</strong> <span class="tag tag-amber">{f['figure_ref']}</span>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Evidence map
    st.markdown("## Evidence Map")
    st.markdown("*Linking findings to evidence types and artifact categories.*")

    evidence_rows = []
    for f in CFG["findings"]:
        for artifact in f["artifacts"]:
            evidence_rows.append({
                "Finding": f["id"],
                "Claim (short)": f["claim"][:60] + "…",
                "Evidence type": f["evidence_type"].split(";")[0].strip(),
                "Artifact": artifact,
                "Figure": f["figure_ref"],
            })
    ev_df = pd.DataFrame(evidence_rows)
    st.dataframe(ev_df, use_container_width=True, hide_index=True)

    st.divider()

    # Data preview
    st.markdown("## Data Previews")
    dtab1, dtab2, dtab3 = st.tabs(["Expression matrix", "Metabolite table", "Candidate genes"])
    with dtab1:
        df = load_csv("data/expression_matrix.csv")
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption("Mock data — schema: gene_id, gene_name, annotation, [sample columns], module, r_nobiletin, r_tangeretin")

    with dtab2:
        df = load_csv("data/metabolite_table.csv")
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption("Mock data — schema: metabolite_id, metabolite_name, class, formula, [tissue columns], annotation_source, confidence_level")

    with dtab3:
        df = load_csv("data/candidate_genes.csv")
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption("Mock data — schema: gene_id, gene_family, chromosome, module, pearson_r, module_membership, in_vitro_validated, priority_rank")

        # Validated vs. pending
        st.markdown("### Validated vs. pending candidates")
        val_df = df[["gene_id", "gene_name", "gene_family", "pearson_r_nobiletin",
                      "module_membership", "in_vitro_validated", "priority_rank"]].sort_values("priority_rank")
        def highlight_validated(row):
            if row["in_vitro_validated"] == True:
                return ["background-color: #f0fdf4"] * len(row)
            return [""] * len(row)
        st.dataframe(val_df.style.apply(highlight_validated, axis=1),
                     use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Pipeline
# ══════════════════════════════════════════════════════════════════════════════
def page_pipeline():
    st.title("End-to-End Pipeline")

    stages = [
        {
            "name": "1 · Raw Data Ingestion",
            "inputs": "PacBio HiFi FASTQ, Hi-C FASTQ, RNA-seq FASTQ, LC-MS raw files",
            "outputs": "Raw FASTQ archives, .raw / .mzML metabolomics files",
            "repro": "MD5 checksums; archived in [NEED repository]",
            "color": "#e0f2fe",
        },
        {
            "name": "2 · QC & Preprocessing",
            "inputs": "Raw reads; raw MS spectra",
            "outputs": "Trimmed FASTQ; filtered/aligned BAM; centroided mzML",
            "repro": "FastQC HTML reports; MZmine batch XML stored in repo",
            "color": "#ede9fe",
        },
        {
            "name": "3 · Feature Generation",
            "inputs": "Trimmed reads; centroided mzML",
            "outputs": "Gene count matrix; metabolite feature table; genome FASTA + GFF3",
            "repro": "Snakemake rules per modality; tool versions pinned in conda env",
            "color": "#fef3c7",
        },
        {
            "name": "4 · Integration Analyses",
            "inputs": "Count matrix; metabolite table; module eigengenes",
            "outputs": "Co-expression modules; gene–metabolite correlation table; PCA/PLS-DA",
            "repro": "R scripts in `analysis/integration/`; set.seed documented",
            "color": "#dcfce7",
        },
        {
            "name": "5 · Candidate Prioritization",
            "inputs": "Correlation table; module memberships; functional annotations",
            "outputs": "Ranked candidate list; phylogenetic tree; filtered OMT/CYP450 shortlist",
            "repro": "Filter thresholds in `config/prioritization.yaml`; reproducible with `make candidates`",
            "color": "#fee2e2",
        },
        {
            "name": "6 · Experimental Validation",
            "inputs": "Prioritized candidate ORFs; PMF substrates; SAM cofactor",
            "outputs": "LC-MS spectra; kinetic parameter table; confirmed activity list",
            "repro": "Plasmid maps deposited; raw LC-MS .raw files archived",
            "color": "#fce7f3",
        },
        {
            "name": "7 · Reporting & Handoff",
            "inputs": "All analysis outputs; validated candidates",
            "outputs": "Manuscript figures; supplementary tables; public data depositions",
            "repro": "Figure scripts in `figures/`; rendered with R/ggplot2 + Illustrator",
            "color": "#f0f4ff",
        },
    ]

    for i, stage in enumerate(stages):
        st.markdown(f"""
        <div class="pipeline-node" style="background: {stage['color']}; border-color: #94a3b8;">
            <strong>{stage['name']}</strong><br>
            <span style="font-size:0.82rem">
                <b>In:</b> {stage['inputs']}<br>
                <b>Out:</b> {stage['outputs']}<br>
                <b>Reproducibility:</b> <em>{stage['repro']}</em>
            </span>
        </div>
        """, unsafe_allow_html=True)
        if i < len(stages) - 1:
            st.markdown('<div class="pipeline-arrow">↓</div>', unsafe_allow_html=True)

    st.divider()

    # Reproducibility block
    st.markdown("## Reproducibility Block")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Environment")
        st.code("""# conda environment
name: pmf_multiomics
channels:
  - bioconda
  - conda-forge
dependencies:
  - python=3.10
  - snakemake=7.x
  - hisat2=2.2.1
  - subread=2.0.3          # featureCounts
  - busco=5.x
  - r-base=4.3
  - bioconductor-deseq2
  - bioconductor-wgcna
  - r-ggplot2""", language="yaml")

    with col2:
        st.markdown("#### Container strategy")
        st.code("""# Docker image (conceptual)
FROM continuumio/miniconda3
COPY environment.yaml .
RUN conda env create -f environment.yaml
SHELL ["conda", "run", "-n", "pmf_multiomics", "/bin/bash", "-c"]

# Push to Docker Hub / Quay.io:
# docker push [NEED registry]/pmf_multiomics:1.0.0""", language="dockerfile")

        st.markdown("#### To rerun (high-level)")
        st.code("""# 1. Clone repo
git clone [NEED GitHub URL]
cd pmf_multiomics

# 2. Restore environment
conda env create -f environment.yaml

# 3. Place raw data under data/raw/
# (download accessions listed in resources page)

# 4. Run pipeline
snakemake --cores 32 --use-conda all

# 5. Generate candidates
make candidates

# 6. Render figures
Rscript figures/render_all.R""", language="bash")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Impact
# ══════════════════════════════════════════════════════════════════════════════
def page_impact():
    st.title("Impact")

    impact_map = {
        "🔬 Scientific Impact": (CFG["impact"]["scientific"], "#f0fdf4", "#86efac"),
        "🗄️ Resource Impact":   (CFG["impact"]["resource"], "#eff6ff", "#93c5fd"),
        "🏭 Translational / Application Impact": (CFG["impact"]["translational"], "#fdf4ff", "#d8b4fe"),
    }

    for header, (bullets, bg, border) in impact_map.items():
        st.markdown(f"## {header}")
        for b in bullets:
            st.markdown(f"""
            <div class="card" style="background:{bg}; border-left: 4px solid {border};">
                {b}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    st.divider()

    st.markdown("## What This Enables Next")
    for i, fu in enumerate(CFG["impact"]["follow_ups"], 1):
        st.markdown(f"""
        <div class="card card-accent">
            <strong>→ {i}.</strong> {fu}
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Resources
# ══════════════════════════════════════════════════════════════════════════════
def page_resources():
    st.title("Resources")
    r = CFG["resources"]

    # Primary links
    st.markdown("## Primary Links")
    link_data = {
        "Resource": ["Paper (DOI)", "GitHub Repository", "Genome Accession", "RNA-seq Accession", "Metabolomics Accession"],
        "Link / Accession": [
            r["paper_doi"], r["github"], r["genome_accession"],
            r["rnaseq_accession"], r["metabolomics_accession"]
        ],
        "Status": ["[NEED]", "[NEED]", "[NEED]", "[NEED]", "[NEED]"],
    }
    st.dataframe(pd.DataFrame(link_data), use_container_width=True, hide_index=True)

    st.divider()

    # Supplementary tables
    st.markdown("## Supplementary Tables")
    for t in r["supplementary_tables"]:
        st.markdown(f"""
        <div class="card">
            <strong>{t['label']}</strong> — 
            <a href="{t['url']}" target="_blank">{t['url']}</a>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Downloads
    st.markdown("## Download Mock Data Files")
    st.markdown("*Real data files will replace these mock templates after public deposition.*")

    dl_col1, dl_col2, dl_col3 = st.columns(3)

    with dl_col1:
        df_exp = load_csv("data/expression_matrix.csv")
        csv_exp = df_exp.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Expression matrix (CSV)",
            data=csv_exp,
            file_name="expression_matrix_mock.csv",
            mime="text/csv",
        )

    with dl_col2:
        df_met = load_csv("data/metabolite_table.csv")
        csv_met = df_met.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Metabolite table (CSV)",
            data=csv_met,
            file_name="metabolite_table_mock.csv",
            mime="text/csv",
        )

    with dl_col3:
        df_cand = load_csv("data/candidate_genes.csv")
        csv_cand = df_cand.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Candidate gene list (CSV)",
            data=csv_cand,
            file_name="candidate_genes_mock.csv",
            mime="text/csv",
        )

    st.divider()

    # Config download
    st.markdown("## Content Configuration")
    with open("content_config.yaml", "r") as f:
        config_text = f.read()
    st.download_button(
        label="⬇ Download content_config.yaml",
        data=config_text.encode("utf-8"),
        file_name="content_config.yaml",
        mime="text/yaml",
    )

    st.markdown('<div class="placeholder">PDF one-page summary: [NEED — generate from manuscript or create bespoke summary PDF]</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# Router
# ══════════════════════════════════════════════════════════════════════════════
router = {
    "Overview":      page_overview,
    "Study Design":  page_study_design,
    "Methods":       page_methods,
    "Findings":      page_findings,
    "Pipeline":      page_pipeline,
    "Impact":        page_impact,
    "Resources":     page_resources,
}
router[page]()
