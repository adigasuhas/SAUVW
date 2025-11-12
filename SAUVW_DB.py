"""
Author: Suhas Adiga  
Affiliation: Theoretical Sciences Unit (TSU), JNCASR  
Date: May 13, 2025 (Re-verified)  
Description: Streamlit dashboard for the Text Mined Crystal Structure Database of Superconductors.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Text Mined Crystal Structure Database of Superconductors",
    layout="wide",
)

# --- Try loading logo if exists ---
logo_path = None
for name in ["LOGO.png", "LOGO.jpg", "LOGO.jpeg", "logo.png", "LOGO"]:
    if Path(name).exists():
        logo_path = name
        break

# Header section
col1, col2 = st.columns([1, 6])

with col1:
    if logo_path:
        st.image(logo_path, use_column_width=True, caption="Project Logo")

with col2:
    st.title("🚀 Text Mined Crystal Structure Database of Superconductors")
    st.markdown(
        "Suhas Adiga<sup>1,2</sup> and Umesh V. Waghmare<sup>1</sup>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<sub>"
        "[1] Theoretical Sciences Unit, School of Advanced Materials (SAMat), JNCASR, Bengaluru 560064<br>"
        "[2] Chemistry and Physics of Materials Unit, JNCASR, Bengaluru 560064"
        "</sub>",
        unsafe_allow_html=True
    )

st.divider()

# --- Description block ---
st.markdown(
    """
The dataset is generated through text mining and benchmarking of **60 research articles**.

A total of **461 compositions** along with their Tc values were extracted.

- **97** have full crystal structure information  
- **54** have CIF files  
- **77** contain partial information  
- **287** have no crystal structure data  

Below are the two datasets used in this project.
"""
)

st.divider()

# --- Load data ---
try:
    data_cs_f = pd.read_csv("SAUVW_full_crysdata.csv")
    st.header("📘 Full Crystal Data – SAUVW_full_crysdata.csv")
    st.dataframe(data_cs_f, use_container_width=True)
except Exception as e:
    st.error(f"Could not load SAUVW_full_crysdata.csv: {e}")

st.divider()

try:
    data_benchmark = pd.read_csv("SAUVW_Benchmark.csv")
    st.header("📗 Benchmark Results – SAUVW_Benchmark.csv")
    st.dataframe(data_benchmark, use_container_width=True)
except Exception as e:
    st.error(f"Could not load SAUVW_Benchmark.csv: {e}")

st.divider()

# --- References ---
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
