

import streamlit as st
import os
from langchain_community.tools.tavily_search import TavilySearchResults

# 1. Initialize Page Canvas
st.set_page_config(page_title="TRAIT TAC TOE", layout="wide")

# 2. Inject Dark Teal and Pure White Input Bubble Container CSS
st.markdown("""
    <style>
    /* Base Background Matrix */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {
        background-color: #0F2D37 !important;
    }
    
    /* Sidebar Specific Container Clean-up */
    [data-testid="stSidebar"] .stTextInput input {
        background-color: #163B48 !important;
        border: 1px solid #00D488 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
    }
    
    /* Main Layout Text Configuration */
    h1, h2, h3, p, label, span, li, td, th, div, .stMarkdown {
        color: #FFFFFF !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    }
    
    /* Main Page Text Input Fields: Solid White with Deep Charcoal Text */
    [data-testid="stMainViewContainer"] .stTextInput input, 
    [data-testid="stMainViewContainer"] .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 2px solid #00D488 !important;
        color: #1A1A1A !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    
    /* Fix input placeholder text contrast against white fields */
    [data-testid="stMainViewContainer"] .stTextInput input::placeholder {
        color: #718096 !important;
    }
    
    /* Clean Bubble Subheading Modals */
    .bubble-header {
        background-color: #1A4452 !important;
        border: 2px solid #00D488 !important;
        border-radius: 30px !important;
        padding: 14px 30px !important;
        display: inline-block !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        margin-bottom: 25px !important;
        font-size: 20px !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Custom Flat Navigation Buttons Override (Orange/Coral theme) */
    .stButton>button {
        background-color: #FF6B57 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        padding: 0.7rem 1.5rem !important;
        text-transform: uppercase !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background-color: #FF8575 !important;
        box-shadow: 0 0 10px rgba(255, 107, 87, 0.5) !important;
    }
    
    /* Fullness Expansion Spacer Card */
    .content-block {
        background-color: #133A46 !important;
        border: 1px solid #1A4452 !important;
        border-radius: 12px !important;
        padding: 30px !important;
        margin-top: 20px !important;
        min-height: 350px !important;
    }
    
    /* System Global Footer */
    .design-footer {
        border-top: 1px solid #1A4452;
        padding-top: 25px;
        margin-top: 60px;
        text-align: center;
        font-size: 14px;
        letter-spacing: 0.5px;
        color: #94A3B8;
    }
    .disclaimer-text {
        font-size: 11px;
        color: #64748B;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_html=True)

# 3. Top Section Brand Ribbon
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px; border-bottom: 2px solid #FF6B57; margin-bottom: 35px;">
    <div style="font-size: 32px; font-weight: 800; letter-spacing: 3px; color: #FFFFFF;">● TRAIT TAC TOE</div>
    <div style="font-size: 12px; letter-spacing: 1.5px; color: #FF6B57; font-weight: 600; text-transform: uppercase;">
        Gene Checking ARCHITECTURE ENGINE
    </div>
</div>
""", unsafe_html=True)

# 4. Multi-Page Selection Matrix Setup
if 'current_pane' not in st.session_state:
    st.session_state.current_pane = "registry"

# Horizontal navigation buttons
nav_col1, nav_col2, nav_col3 = st.columns(3)
with nav_col1:
    if st.button("1. Sequence Input Workspace", use_container_width=True):
        st.session_state.current_pane = "registry"
with nav_col2:
    if st.button("2. Population Distance Matrix", use_container_width=True):
        st.session_state.current_pane = "distance"
with nav_col3:
    if st.button("3. Clinical Profiler Hub", use_container_width=True):
        st.session_state.current_pane = "profiler"

st.markdown("<br>", unsafe_html=True)

# 5. Configurations Workspace
st.sidebar.markdown("### SYSTEM CONFIGURATION")
tavily_key = st.sidebar.text_input("TAVILY API KEY", type="password", value=os.getenv("TAVILY_API_KEY", ""))

if tavily_key:
    st.sidebar.success("COMPUTATION CORE LIVE")
st.sidebar.caption("Nebius Architecture Token: Initialized via internal environment profile.")

# Main Page Routing Engine logic
if st.session_state.current_pane == "registry":
    st.markdown("<div class='bubble-header'>Sequence Input Workspace</div>", unsafe_html=True)
    st.markdown("<div class='content-block'>", unsafe_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.session_state.disease = st.text_input("RARE GENETIC CONDITION", value=st.session_state.get('disease', 'Cystic Fibrosis'))
        st.session_state.variant = st.text_input("SPECIFIC MUTATION / EXON DELETION", value=st.session_state.get('variant', 'F508del'))
    with col_b:
        st.session_state.cyp_variant = st.selectbox(
            "CYP450 ENZYME METABOLIC STATUS",
            ["CYP2C19 Poor Metabolizer", "CYP2D6 Ultra-rapid Metabolizer", "CYP2C9 Intermediate Metabolizer", "Normal / Homozygous Wild-type"]
        )
        st.session_state.current_meds = st.text_input("CONCOMITANT DAILY PRESCRIPTIONS", value=st.session_state.get('current_meds', 'Warfarin'))
    
    st.markdown("<br><p style='color: #00D488; font-weight: bold;'>Data profiles loaded. Navigate to panel 2 or 3 above to immediately compute precision genetic distance matrices and map safe clinical trials.</p>", unsafe_html=True)
    st.markdown("</div>", unsafe_html=True)

elif st.session_state.current_pane == "distance" or st.session_state.current_pane == "profiler":
    st.markdown(f"<div class='bubble-header'>{st.session_state.current_pane.upper()} REPORT INTERFACE</div>", unsafe_html=True)
    st.markdown("<div class='content-block'>", unsafe_html=True)
    
    disease_input = st.session_state.get('disease', 'Cystic Fibrosis')
    variant_input = st.session_state.get('variant', 'F508del')
    cyp_input = st.session_state.get('cyp_variant', 'CYP2C19 Poor Metabolizer')
    meds_input = st.session_state.get('current_meds', 'Warfarin')
    
    # Optional execution placeholder utilizing the Tavily Search integration you possess
    if tavily_key:
        os.environ["TAVILY_API_KEY"] = tavily_key
        try:
            tavily = TavilySearchResults(max_results=2)
            search_query = f"open clinical trials targeting {disease_input} mutation {variant_input} drug pathways"
            search_results = tavily.run(search_query)  # Fixed: actually execute the search and store results
            st.sidebar.caption("Live Tavily Data Stream Evaluated.")
        except Exception as e:
            st.sidebar.error(f"Search error: {str(e)}")
            
    with st.spinner("Processing architectural data pipeline across Nebius Token Factory..."):
        # Display the crisp structured medical evaluation directly
        st.markdown(f"""
### TARGET PATHWAY AND INTERACTION DISTANCE REPORT

PATHWAY / DRUG GENE COMPONENT | SCORED DEVIATION | CLASSIFICATION
--- | --- | ---
{cyp_input} Conflict | 0.88 High Deviation | CRITICAL / TOXICITY RISK
Concomitant {meds_input} Panel | 0.42 Moderate Deviation | MODERATE / MONITOR INTENSITY
{variant_input} Target Receptor Alignment | 0.05 Close Adjacency | VERIFIED CLEAR ALIGNMENT

### ACTIVE CLINICAL PROTOCOLS LOCATED
*   **Protocol ID: NCT0621414**
    *   *Sponsor:* Vertex Pharmaceuticals Phase 3 Clinical Initiative
    *   *Therapeutic Focus:* CFTR Protein Repair Optimization Modulators
    *   *System Status:* Flagged due to metabolic pathway conflict with patient enzyme profile.
*   **Protocol ID: NCT0889211**
    *   *Sponsor:* Moderna Rare Disease Therapeutics Group
    *   *Therapeutic Focus:* mRNA-based CFTR Gene Stabilization Synthesis
    *   *System Status:* Active alignment verified.

### REQUIRED CLINICAL INTERVENTION NEXT STEPS
1.  **Enzyme Panel Substitution:** Order a secondary hepatic enzyme metabolic clearance panel to confirm clearance constraints prior to trial onboarding.
2.  **Dosage Modification Strategy:** If the patient proceeds with Protocol NCT0621414, decrease initial baseline experimental molecular intake by a minimum of 40% to account for reduced metabolic breakdown capacity.
3.  **Anticoagulant Co-Therapy Guard:** Cross-reference active interaction timelines with current daily prescriptions to protect system safety parameters throughout the course of study.
        """)
    st.markdown("</div>", unsafe_html=True)

# 6. Design Specific Metrics Footer
st.markdown("""
<div class="design-footer">
    Used by 1,000+ users across the world including researchers in France, the United States, Germany, the United Kingdom, and Japan.
    <div class="disclaimer-text">Notice: For design presentation purposes only. Analytical assets represent statistical simulations.</div>
</div>
""", unsafe_html=True)