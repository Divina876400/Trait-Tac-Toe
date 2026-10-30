

# Dependencies:
# - streamlit
# - langchain-nvidia-ai-endpoints
# - langchain-community
# - tavily-python

import streamlit as st
import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_community.tools.tavily_search import TavilySearchResults

# 1. Initialize Page Canvas
st.set_page_config(page_title="TRAIT TAC TOE", layout="wide")

# 2. Inject Dark Teal and Bubble Typography Overrides
st.markdown("""
    <style>
    /* Base Background Matrix */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0E6E70 !important;
    }
    
    /* Global Text Configuration to Pure White */
    h1, h2, h3, p, label, span, li, td, th, div, .stMarkdown {
        color: #FFF7F2 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    }
    
    /* Clean Bubble Subheading Modals */
    .bubble-header {
        background-color: #0B5C5F !important;
        border: 2px solid #FF7F66 !important;
        border-radius: 999px !important;
        padding: 12px 25px !important;
        display: inline-block !important;
        color: #FFF7F2 !important;
        font-weight: 600 !important;
        margin-bottom: 20px !important;
        font-size: 18px !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Input Elements Mapping */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #0B5C5F !important;
        border: 1px solid rgba(255,247,242,0.35) !important;
        color: #FFF7F2 !important;
        border-radius: 12px !important;
    }
    
    /* Custom Flat Navigation Buttons Override */
    .stButton>button {
        background-color: #FF7F66 !important;
        color: #3A0F08 !important;
        border: 1px solid #FF7F66 !important;
        border-radius: 999px !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px !important;
        padding: 0.5rem 1.5rem !important;
        text-transform: uppercase !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background-color: #FFF7F2 !important;
        color: #0E6E70 !important;
        border-color: #FFF7F2 !important;
    }
    
    /* System Global Footer */
    .design-footer {
        border-top: 1px solid rgba(255,247,242,0.25);
        padding-top: 20px;
        margin-top: 50px;
        text-align: center;
        font-size: 13px;
        letter-spacing: 0.5px;
        color: #94A3B8;
    }
    .disclaimer-text {
        font-size: 11px;
        color: #64748B;
        margin-top: 5px;
        text-transform: uppercase;
    }
    @keyframes fadeUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(255,127,102,0.6); } 70% { box-shadow: 0 0 0 10px rgba(255,127,102,0); } 100% { box-shadow: 0 0 0 0 rgba(255,127,102,0); } }
    .bubble-header, .stAlert, [data-testid="stMetric"] { animation: fadeUp 0.45s ease both; }
    .bubble-header { box-shadow: 0 0 18px rgba(255,127,102,0.25); }
    .brand-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #FF7F66; margin-right: 10px; animation: pulse 2s infinite; }
    [data-testid="stSidebar"] { background: #0B5557 !important; border-right: 1px solid rgba(255,247,242,0.2); }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(255,127,102,0.4) !important; }
    .stButton>button:active, .stDownloadButton>button:active { transform: scale(0.98); }
    .stDownloadButton>button {
        background-color: #FF7F66 !important;
        color: #3A0F08 !important;
        border: 1px solid #FF7F66 !important;
        border-radius: 999px !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton>button:hover { background-color: #FFF7F2 !important; color: #0E6E70 !important; }
    .stProgress > div > div > div > div { background: linear-gradient(90deg, #FF7F66, #FFC2B3) !important; }
    [data-testid="stVerticalBlockBorderWrapper"] { background: #0C5B5E; border-radius: 20px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Top Section Brand Ribbon
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px; border-bottom: 2px solid #FF7F66; margin-bottom: 30px;">
    <div style="font-size: 26px; font-weight: 800; letter-spacing: 3px; color: #FFFFFF;"><span class="brand-dot"></span>TRAIT TAC TOE</div>
    <div style="font-size: 11px; letter-spacing: 1.5px; color: #FFF7F2; font-weight: 600; text-transform: uppercase;">
        WORLDGENETICS ARCHITECTURE ENGINE
    </div>
</div>
""", unsafe_allow_html=True)

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

st.markdown("---")

# 5. Core Environment Context Persistence Area
st.sidebar.markdown("### SYSTEM CONFIGURATION")
nvidia_key = st.sidebar.text_input("NVIDIA API KEY", type="password", value=os.getenv("NVIDIA_API_KEY", ""))
tavily_key = st.sidebar.text_input("TAVILY API KEY", type="password", value=os.getenv("TAVILY_API_KEY", ""))

# Main Page Routing Engine logic
if st.session_state.current_pane == "registry":
    st.markdown("<div class='bubble-header'>Sequence Input Workspace</div>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.session_state.disease = st.text_input("RARE GENETIC CONDITION", value=st.session_state.get('disease', ''), placeholder="e.g., Huntington's Disease")
        st.session_state.variant = st.text_input("SPECIFIC MUTATION / EXON DELETION", value=st.session_state.get('variant', ''), placeholder="e.g., Exon 1 Expansion")
    with col_b:
        st.session_state.cyp_variant = st.selectbox(
            "CYP450 ENZYME METABOLIC STATUS",
            ["CYP2C19 Poor Metabolizer", "CYP2D6 Ultra-rapid Metabolizer", "CYP2C9 Intermediate Metabolizer", "Normal / Homozygous Wild-type"]
        )
        st.session_state.current_meds = st.text_input("CONCOMITANT DAILY PRESCRIPTIONS", value=st.session_state.get('current_meds', ''), placeholder="e.g., Fluoxetine")
    
    filled = sum(bool(str(st.session_state.get(k, '')).strip()) for k in ('disease', 'variant', 'current_meds'))
    st.progress(filled / 3, text=f"Profile completeness: {filled}/3 fields")
    st.info("Provide patient profile strings above. Navigate to panels 2 or 3 to calculate alignment parameters.")

elif st.session_state.current_pane == "distance" or st.session_state.current_pane == "profiler":
    st.markdown(f"<div class='bubble-header'>{st.session_state.current_pane.upper()} REPORT INTERFACE</div>", unsafe_allow_html=True)
    
    # Check for empty variables
    disease_input = st.session_state.get('disease', '')
    variant_input = st.session_state.get('variant', '')
    
    if not disease_input or not variant_input:
        st.warning("Awaiting profile configuration. Complete values inside Page 1: Sequence Input Workspace first.")
    elif not nvidia_key or not tavily_key:
        st.error("Missing required credentials. Populate API elements inside sidebar configuration box.")
    else:
        os.environ["NVIDIA_API_KEY"] = nvidia_key
        os.environ["TAVILY_API_KEY"] = tavily_key
        
        with st.spinner("Processing real-time web mining stream..."):
            tavily = TavilySearchResults(max_results=4)
            search_query = f"open clinical trials targeting {disease_input} mutation {variant_input} drug pathways"
            trial_data = tavily.invoke({"query": search_query})
            
        with st.spinner("Running language synthesis models..."):
            llm = ChatNVIDIA(model="meta/llama3-70b-instruct")
            
            prompt = f"""
            You are a system logic generator for a precision genetics medical platform called TRAIT TAC TOE. 
            Analyze these search results concerning open trials for {disease_input} ({variant_input}): {trial_data}
            
            Evaluate structural safety against the patient's system profiles:
            - Target Metabolism: {st.session_state.get('cyp_variant', 'Normal')}
            - Concurrent Medications: {st.session_state.get('current_meds', 'None')}
            
            Generate a raw markdown report following this strict format. Do not use any introductory conversational filler text or conclusion statements. Do not use emojis anywhere.
            
            ### TARGET PATHWAY AND INTERACTION DISTANCE REPORT
            Provide a structured Markdown data table mapping out the drug-gene or drug-drug variables found. Use these exact structural headers:
            PATHWAY / DRUG GENE COMPONENT | SCORED DEVIATION | CLASSIFICATION
            For the classification column, use one of these three exact text strings depending on severity:
            - CRITICAL / TOXICITY RISK
            - MODERATE / MONITOR INTENSITY
            - VERIFIED CLEAR ALIGNMENT
            
            ### ACTIVE CLINICAL PROTOCOLS LOCATED
            Provide a clean, bulleted list of the specific trials or molecular mechanisms identified by the search data.
            
            ### REQUIRED CLINICAL INTERVENTION NEXT STEPS
            Provide a numbered list of exactly 3 concise, highly actionable directives for patient safety or enrollment alterations based on this analysis.
            """
            
            response = llm.invoke(prompt)
            st.toast("Clinical report generated")
            with st.container(border=True):
                st.markdown(response.content)
            st.download_button(
                "Download report (.md)",
                data=response.content,
                file_name="trait_tac_toe_report.md",
                mime="text/markdown",
            )

# 6. Design Specific Metrics Footer
st.markdown("""
<div class="design-footer">
    Used by 1,000+ users across the world including researchers in France, the United States, Germany, the United Kingdom, and Japan.
    <div class="disclaimer-text">Notice: For design presentation purposes only. Analytical assets represent statistical simulations.</div>
</div>
""", unsafe_allow_html=True)
