

# Dependencies (install before running):
#     pip install streamlit langchain-community tavily-python openai
#
# Environment variables (optional, pre-fill the sidebar fields):
#     NEBIUS_API_KEY
#     TAVILY_API_KEY
#
# Run with:
#     streamlit run app.py

import streamlit as st
import os
from langchain_community.llms import OpenAI  # Using the clean, standard base connector
from langchain_community.tools.tavily_search import TavilySearchResults

# 1. Initialize Page Canvas
st.set_page_config(page_title="TRAIT TAC TOE", layout="wide")

# 2. Inject Dark Teal and Pure White Input Bubble Container CSS
st.markdown("""
    <style>
    /* Animation Keyframes */
    @keyframes ttt-fade-up {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes ttt-pulse {
        0%   { box-shadow: 0 0 0 0 rgba(0, 212, 136, 0.6); }
        70%  { box-shadow: 0 0 0 10px rgba(0, 212, 136, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 212, 136, 0); }
    }

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
        transition: box-shadow 0.2s ease, border-color 0.2s ease !important;
    }
    [data-testid="stSidebar"] .stTextInput input:focus {
        border-color: #FF6B57 !important;
        box-shadow: 0 0 0 3px rgba(0, 212, 136, 0.35) !important;
        outline: none !important;
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
        transition: box-shadow 0.2s ease, transform 0.2s ease !important;
    }
    [data-testid="stMainViewContainer"] .stTextInput input:focus {
        box-shadow: 0 0 0 4px rgba(0, 212, 136, 0.35) !important;
        outline: none !important;
    }
    [data-testid="stMainViewContainer"] .stTextInput input:hover {
        transform: translateY(-1px);
    }

    /* Fix input placeholder text contrast against white fields */
    [data-testid="stMainViewContainer"] .stTextInput input::placeholder {
        color: #718096 !important;
    }

    /* Clean Bubble Subheading Modals */
    .bubble-header {
        background: linear-gradient(135deg, #1A4452 0%, #163B48 100%) !important;
        border: 2px solid #00D488 !important;
        border-radius: 30px !important;
        padding: 14px 30px !important;
        display: inline-block !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        margin-bottom: 25px !important;
        font-size: 20px !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 18px rgba(0, 212, 136, 0.15) !important;
        animation: ttt-fade-up 0.45s ease both !important;
    }

    /* Step Progress Indicator */
    .step-bar {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 18px;
        font-size: 12px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #94A3B8 !important;
        font-weight: 600;
    }
    .step-track {
        flex: 1;
        height: 4px;
        border-radius: 4px;
        background: #1A4452;
        overflow: hidden;
    }
    .step-fill {
        height: 100%;
        background: linear-gradient(90deg, #00D488, #FF6B57);
        border-radius: 4px;
        transition: width 0.4s ease;
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
        transform: translateY(-2px) !important;
    }
    .stButton>button:active {
        transform: translateY(1px) scale(0.98) !important;
    }

    /* Fullness Expansion Spacer Card */
    .content-block {
        background: linear-gradient(180deg, #133A46 0%, #0F2D37 100%) !important;
        border: 1px solid #1A4452 !important;
        border-radius: 12px !important;
        padding: 30px !important;
        margin-top: 20px !important;
        min-height: 350px !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25) !important;
        animation: ttt-fade-up 0.5s ease both !important;
    }

    /* Brand Ribbon Live Status Dot */
    .live-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #00D488;
        margin-right: 12px;
        vertical-align: middle;
        animation: ttt-pulse 2s infinite;
    }

    /* Smooth Scrolling Track */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #0F2D37; }
    ::-webkit-scrollbar-thumb { background: #1A4452; border-radius: 8px; }
    ::-webkit-scrollbar-thumb:hover { background: #00D488; }

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
""", unsafe_allow_html=True)

# 3. Top Section Brand Ribbon
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px; border-bottom: 2px solid #FF6B57; margin-bottom: 35px; animation: ttt-fade-up 0.4s ease both;">
    <div style="font-size: 32px; font-weight: 800; letter-spacing: 3px; color: #FFFFFF;">● TRAIT TAC TOE</div>
    <div style="font-size: 12px; letter-spacing: 1.5px; color: #FF6B57; font-weight: 600; text-transform: uppercase;">
        <span class="live-dot"></span>WORLDGENETICS ARCHITECTURE ENGINE
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

# Step progress indicator (reflects the active panel)
step_index = {"registry": 1, "distance": 2, "profiler": 3}.get(st.session_state.current_pane, 1)
st.markdown(
    f"""
    <div class="step-bar">
        <span>Step {step_index} of 3</span>
        <div class="step-track"><div class="step-fill" style="width: {step_index / 3 * 100:.0f}%;"></div></div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# 5. Configurations Workspace targeting Nebius Token Factory
st.sidebar.markdown("### SYSTEM CONFIGURATION")
nebius_key = st.sidebar.text_input("NEBIUS API KEY", type="password", value=os.getenv("NEBIUS_API_KEY", ""))
tavily_key = st.sidebar.text_input("TAVILY API KEY", type="password", value=os.getenv("TAVILY_API_KEY", ""))

if nebius_key and tavily_key:
    st.sidebar.success("NEBIUS INFRASTRUCTURE ONLINE")

# Main Page Routing Engine logic
if st.session_state.current_pane == "registry":
    st.markdown("<div class='bubble-header'>Sequence Input Workspace</div>", unsafe_allow_html=True)

    st.markdown("<div class='content-block'>", unsafe_allow_html=True)
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

    st.markdown("<br><p style='color: #94A3B8; font-size: 14px;'>Provide patient genomic profile string allocations above. Navigate to panels 2 or 3 using the workspace triggers to dynamically map alignment structures and flag active drug-gene interactions.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.current_pane == "distance" or st.session_state.current_pane == "profiler":
    st.markdown(f"<div class='bubble-header'>{st.session_state.current_pane.upper()} REPORT INTERFACE</div>", unsafe_allow_html=True)

    st.markdown("<div class='content-block'>", unsafe_allow_html=True)
    disease_input = st.session_state.get('disease', '')
    variant_input = st.session_state.get('variant', '')

    if not disease_input or not variant_input:
        st.warning("Awaiting profile configuration. Complete values inside Page 1: Sequence Input Workspace first.")
    elif not nebius_key or not tavily_key:
        st.error("Missing required credentials. Populate API elements inside sidebar configuration box.")
    else:
        os.environ["TAVILY_API_KEY"] = tavily_key

        with st.spinner("Processing real-time web mining stream via Tavily..."):
            tavily = TavilySearchResults(max_results=4)
            search_query = f"open clinical trials targeting {disease_input} mutation {variant_input} drug pathways"
            trial_data = tavily.invoke({"query": search_query})

        with st.spinner("Running language synthesis models via Nebius Token Factory..."):
            # Direct base endpoint execution wrapper passing standard parameters natively
            llm = OpenAI(
                openai_api_key=nebius_key,
                openai_api_base="https://nebius.ai",
                model="nvidia/Llama-3.1-Nemotron-70B-Instruct"
            )

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
            st.markdown(response)
    st.markdown("</div>", unsafe_allow_html=True)

# 6. Design Specific Metrics Footer
st.markdown("""
<div class="design-footer">
    <div>TRAIT TAC TOE | WORLDGENETICS ARCHITECTURE ENGINE</div>
    <div class="disclaimer-text">Research and decision-support use only. Not a substitute for clinical judgment.</div>
</div>
""", unsafe_allow_html=True)
