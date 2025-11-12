"""
Author: Suhas Adiga
Affiliation: Theoretical Sciences Unit (TSU), JNCASR
Date: Nov 13, 2025
Description: Streamlit dashboard for the Text Mined Crystal Structure Database of Superconductors.
             Adds "View Structure" capability for rows where CIFs are available.
"""

from pathlib import Path
import io
import sys

import pandas as pd
import streamlit as st

# Optional libraries
try:
    from pymatgen.core.structure import Structure
except Exception:
    st.error("pymatgen is required for structure parsing. Install with `pip install pymatgen`.")
    raise

# Try to import crystal_toolkit; otherwise we'll fall back to py3Dmol
CRYSTAL_TOOLKIT_AVAILABLE = True
try:
    # crystal_toolkit is optional; if present, we'll use it
    # Import attempts below may vary slightly by crystal_toolkit version.
    # We try a minimal import pattern.
    from crystal_toolkit.core.scene import Scene
    from crystal_toolkit.core.util import structure_from_pymatgen
    from crystal_toolkit.widgets import StructureMoleculeComponent  # may exist depending on version
except Exception:
    CRYSTAL_TOOLKIT_AVAILABLE = False

# py3Dmol fallback for visualization
PY3DMOL_AVAILABLE = True
try:
    import py3Dmol
except Exception:
    PY3DMOL_AVAILABLE = False

# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title="Text Mined Crystal Structure Database of Superconductors",
    layout="wide",
)

ROOT = Path(".")
CS_CSV = ROOT / "SAUVW_full_crysdata.csv"
BENCH_CSV = ROOT / "SAUVW_Benchmark.csv"
CIF_DIR = ROOT / "crystal_structure"  # base directory for CIFs: crystal_structure/<material-id>.cif

# -------------------------
# Header (logo optional)
# -------------------------
logo_path = None
for name in ["LOGO.png", "LOGO.jpg", "LOGO.jpeg", "logo.png", "LOGO"]:
    p = ROOT / name
    if p.exists():
        logo_path = p
        break

col1, col2 = st.columns([1, 6])
with col1:
    if logo_path:
        st.image(str(logo_path), use_column_width=True)
with col2:
    st.title("🚀 Text Mined Crystal Structure Database of Superconductors")
    st.markdown(
        "Suhas Adiga<sup>1,2</sup> and Umesh V. Waghmare<sup>1</sup>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<sub>"
        "[1] Theoretical Sciences Unit, School of Advanced Materials (SAMat), JNCASR, Bengaluru 560064<br>"
        "[2] Chemistry and Physics of Materials Unit, JNCASR, Bengaluru 560064"
        "</sub>",
        unsafe_allow_html=True,
    )

st.divider()

# -------------------------
# Short description (static)
# -------------------------
st.markdown(
    """
The dataset is generated through text mining and benchmarking of **60 research articles**.

A total of **461 compositions** along with their Tc values were extracted.

- **97** have full crystal structure information  
- **54** have CIF files  
- **77** contain partial information  
- **287** have no crystal structure data  
"""
)

st.divider()

# -------------------------
# Load and display CSVs (simple)
# -------------------------
data_cs_f = None
data_benchmark = None

if CS_CSV.exists():
    try:
        data_cs_f = pd.read_csv(CS_CSV)
        st.header("📘 Full Crystal Data – SAUVW_full_crysdata.csv")
        st.dataframe(data_cs_f, use_container_width=True)
    except Exception as e:
        st.error(f"Failed to load `{CS_CSV.name}`: {e}")
else:
    st.warning(f"`{CS_CSV.name}` not found in repo root. Place it in the same folder as this app.")

st.divider()

if BENCH_CSV.exists():
    try:
        data_benchmark = pd.read_csv(BENCH_CSV)
        st.header("📗 Benchmark Results – SAUVW_Benchmark.csv")
        st.dataframe(data_benchmark, use_container_width=True)
    except Exception as e:
        st.error(f"Failed to load `{BENCH_CSV.name}`: {e}")
else:
    st.warning(f"`{BENCH_CSV.name}` not found in repo root. Place it in the same folder as this app.")

st.divider()

# -------------------------
# Prepare list of available CIFs
# -------------------------
def get_material_id_column(df: pd.DataFrame) -> str | None:
    """Return the likely material id column name or None."""
    candidates = ["Material-ID", "Material_ID", "material-id", "material_id", "materialid", "MaterialID", "Material Id"]
    for c in candidates:
        if c in df.columns:
            return c
    # fallback: try to find any column containing 'material' or 'id'
    for c in df.columns:
        if "material" in c.lower() and "id" in c.lower():
            return c
    return None


def get_cif_available_mask(df: pd.DataFrame) -> pd.Series:
    """Return boolean mask where CIF available is 'yes' (case-insensitive)."""
    # find column name
    candidates = ["cif_available", "cif available", "cif", "has_cif", "cif_available?"]
    col = None
    for c in candidates:
        if c in df.columns:
            col = c
            break
    if col is None:
        # fallback: try any column that contains 'cif' in name
        for c in df.columns:
            if "cif" in c.lower():
                col = c
                break
    if col is None:
        # no CIF column detected -> return all False
        return pd.Series([False] * len(df), index=df.index)
    mask = df[col].astype(str).str.strip().str.lower() == "yes"
    return mask


available_materials = []
material_id_col = None
if data_cs_f is not None:
    material_id_col = get_material_id_column(data_cs_f)
    mask = get_cif_available_mask(data_cs_f)
    if material_id_col is None:
        st.warning("Material ID column not detected automatically. Please ensure there is a column like 'Material-ID'.")
    else:
        # list of material ids with CIFs
        available_materials = data_cs_f.loc[mask, material_id_col].astype(str).tolist()

# -------------------------
# Visualization selector + viewer
# -------------------------
st.header("🔬 View Crystal Structure (CIF)")

if not available_materials:
    st.info("No CIFs detected in the table (or `cif_available` != 'yes'). Ensure `crystal_structure/<material-id>.cif` exists and `cif_available` column is 'yes'.")
else:
    st.markdown("Select a material (only entries with `cif_available == 'yes'` are shown):")
    chosen = st.selectbox("Material with CIF", options=available_materials, index=0)
    view_btn = st.button("🔍 View Structure")

    if view_btn:
        # build CIF path from chosen material-id
        # sanitize chosen string to filename-friendly (but do not change user's naming convention)
        matid = str(chosen)
        cif_path = CIF_DIR / f"{matid}.cif"
        if not cif_path.exists():
            # try slightly different namecases/replace spaces
            alt = CIF_DIR / f"{matid.replace(' ', '_')}.cif"
            if alt.exists():
                cif_path = alt
            else:
                st.error(f"CIF file not found at `{cif_path}`. Ensure CIF is present at `crystal_structure/{matid}.cif`")
        else:
            st.success(f"Found CIF: `{cif_path.relative_to(ROOT)}`")

        if cif_path.exists():
            # Try Crystal Toolkit path first
            if CRYSTAL_TOOLKIT_AVAILABLE:
                try:
                    # Read structure using pymatgen
                    structure = Structure.from_file(str(cif_path))

                    # Convert to Crystal Toolkit Scene (API may vary by ctk version)
                    # We'll attempt a generic approach: construct Scene and use StructureMoleculeComponent if available.
                    try:
                        # Newer ctk versions have helper functions; try a safe path:
                        scene = Scene()
                        # structure_from_pymatgen helper tries to convert pymatgen.Structure to ctk Structure
                        ctk_structure = structure_from_pymatgen(structure)
                        # add the structure to scene (name 'structure' here is arbitrary)
                        scene.add_structure(ctk_structure, name=str(matid))
                        # Render scene to HTML and embed
                        html = scene.to_html()  # may exist depending on version
                        st.components.v1.html(html, height=600, scrolling=True)
                    except Exception:
                        # fallback method: try StructureMoleculeComponent (older versions)
                        comp = StructureMoleculeComponent(structure=structure)
                        # This component may provide `_repr_html_()` or `render` methods
                        if hasattr(comp, "_repr_html_"):
                            html = comp._repr_html_()
                            st.components.v1.html(html, height=600, scrolling=True)
                        elif hasattr(comp, "show"):
                            comp.show()
                            st.info("Displayed via crystal_toolkit component.show()")
                        else:
                            st.warning("Crystal Toolkit is installed but rendering failed. Falling back to py3Dmol (if available).")
                            raise RuntimeError("Crystal Toolkit render failed")
                except Exception as e:
                    # fallback to py3Dmol if possible
                    st.write("Crystal Toolkit rendering failed or API mismatch:", e)
                    if PY3DMOL_AVAILABLE:
                        # Use py3Dmol fallback
                        try:
                            structure = Structure.from_file(str(cif_path))
                            # create an xyz string
                            xyz_str = structure.to(fmt="xyz")
                            view = py3Dmol.view(width=800, height=500)
                            view.addModel(xyz_str, "xyz")
                            view.setStyle({"stick": {}})
                            view.zoomTo()
                            view.show()
                            st.components.v1.html(view._make_html(), height=520, scrolling=True)
                        except Exception as e2:
                            st.error(f"py3Dmol fallback also failed: {e2}")
                    else:
                        st.error("py3Dmol not installed; please install py3Dmol or crystal-toolkit to visualize structures.")
            else:
                # Crystal Toolkit not available — use py3Dmol fallback
                if PY3DMOL_AVAILABLE:
                    try:
                        structure = Structure.from_file(str(cif_path))
                        xyz_str = structure.to(fmt="xyz")
                        view = py3Dmol.view(width=800, height=500)
                        view.addModel(xyz_str, "xyz")
                        view.setStyle({"stick": {}})
                        view.zoomTo()
                        view.show()
                        st.components.v1.html(view._make_html(), height=520, scrolling=True)
                    except Exception as e:
                        st.error(f"py3Dmol rendering failed: {e}")
                else:
                    st.error(
                        "Neither crystal-toolkit nor py3Dmol is installed in this environment. "
                        "Install `crystal-toolkit` for the primary viewer or `py3Dmol` as fallback."
                    )

st.divider()

# -------------------------
# References / footer
# -------------------------
st.header("References")
st.markdown(
    """
[1] Center for Basic Research on Materials, *MDR SuperCon Datasheet*, ver.240322 (2024).  
[2] K. M. Rabe et al., Phys. Rev. B **45**, 7650 (1992).  
[3] D. Davies et al., *J. Open Source Softw.* **4**, 1361 (2019).  
[4] V. Stanev et al., *npj Comput. Mater.* **4**, 28 (2018).  
"""
)

st.caption("Dashboard by Suhas Adiga — Theoretical Sciences Unit (TSU), JNCASR")
