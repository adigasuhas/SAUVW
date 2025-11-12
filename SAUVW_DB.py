"""
Author: Suhas Adiga  
Affiliation: Theoretical Sciences Unit (TSU), JNCASR  
Date: May 13, 2025 (Re-verified)  
Description: This Python code creates a dashboard of predicted compounds supporting the poster presented at Aapali PSI-K.

!! Disclaimer !!
This code was converted to PEP 8 guidelines using autopep8.
"""

# Importing necessary libraries
import streamlit as st
import pandas as pd

# Loading all data
data_literature = pd.read_csv('SC_Literature.csv')
# data_mp = pd.read_csv('SC_MP.csv')
# data_us1 = pd.read_csv('SC_L_SMACT.csv')
# data_us2 = pd.read_csv('SC_SMACT_New.csv') 

with st.container():
    st.title("🚀 Accelerating Search for Superconductors Using Machine Learning")
    
    st.markdown(
        "Suhas Adiga<sup>1,2</sup> and Umesh V. Waghmare<sup>1</sup>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<sub>"
        "[1] Theoretical Sciences Unit, School of Advanced Materials (SAMat), Jawaharlal Nehru Centre for Advanced Scientific Research, Jakkur, Bengaluru 560064<br>"
        "[2] Chemistry and Physics of Materials Unit, Jawaharlal Nehru Centre for Advanced Scientific Research, Jakkur, Bengaluru 560064"
        "</sub>",
        unsafe_allow_html=True
    )

st.divider()

st.markdown(
    "The website is still under deployment!! Appreciate your interest. Suhas will soon be updating once he is awake 😴"
)
st.divider()

# --- Add a GIF from an online source ---
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://tenor.com/view/fall-asleep-falling-asleep-sleepy-doze-off-dozing-off-gif-10742301" width="400">
    </div>
    """,
    unsafe_allow_html=True
)

# Display results

# with st.container():
#     st.header("📚 Superconductors from Literature")
#     st.write("We selected approximately 28 compounds reported as superconductors in the literature since 2016. None of these materials are present in 'SuperCon-MTG'. All 28 compounds have been identified as superconductors by our model, and their predicted Tc values are reasonably close to the experimental values.")
#     st.dataframe(data_literature, use_container_width=True)

# st.divider()

# with st.container():
#     st.header("🧪 Superconductors from Materials Project")
#     st.write("Using our model, we searched for potential superconducting materials in the Materials Project database. We selected materials with a bandgap of 0eV, non-magnetic behavior, and experimental validation in either the ICSD or Pauling Files databases.")
#     st.write("We list the top 10 materials with the highest predicted Tc, none of which are in 'SuperCon-MTG'.")
#     st.dataframe(data_mp, use_container_width=True)


# st.divider()

# with st.container():
#     st.header("🌌 Unexplored Space of Materials")
#     st.write("Using our model, we search for potential superconducting materials composed of one transition element and one main group element. The compositions were generated using the SMACT [3] library in Python. To reduce the search space, we selected compounds only if their probability of existence was greater than 0. Some compounds that turned out to be already reported in the literature for superconductivity are listed below.")
#     st.subheader("✅ Experimentally Verified for Superconductivity")
#     st.dataframe(data_us1, use_container_width=True)
#     st.write("Below, we list the generated compounds that could be potential superconductors but require experimental validation.")
#     st.subheader("🧾 Compounds Reported for Superconductivity")
#     st.dataframe(data_us2)

# st.divider()

# with st.container():
# 	st.header("Acknowledgements")
# 	st.write('S.A. acknowledges JNCASR for the research fellowship. The authors thank Prof. Ram Seshadri, Prof. A. Sundaresan and Prof. Ricardo Grau-Crespo for valuable discussions and insights.')

# st.divider()    

with st.container():
	st.header("References")
	st.markdown("""
[1] Center for Basic Research on Materials, *MDR SuperCon Datasheet*, ver.240322 (2024).

[2] K. M. Rabe, J. C. Phillips, P. Villars, and I. D. Brown, Phys. Rev. B **45**, 7650 (1992).

[3] D. Davies, K. Butler, A. Jackson, J. Skelton, K. Morita, and A. Walsh, *J. Open Source Softw.* **4**, 1361 (2019).

[4] V. Stanev, C. Oses, A. G. Kusne, E. Rodriguez, J. Paglione, S. Curtarolo, and I. Takeuchi, *npj Comput. Mater.* **4**, 28 (2018).

""")
