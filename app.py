

# import os
import streamlit as st
from langchain_community.llms import OpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

# 1. Initialize Page Canvas
st.set_page_config(page_title="TRAIT TAC TOE", layout="wide", page_icon="🧬")

# 2. Inject Dark Teal and Pure White Input Bubble Container CSS
# (Original styling preserved; extended with interactive/professional effects
#  inspired by the referenced worldgenetics.app design language.)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {
        background: radial-gradient(circle at top left, #14404E 0%, #0F2D37 45%, #0B2229 100%) !important;
    }
    [data-testid="stSidebar"] {
        border-right: 1px solid #1A4452 !important;
    }
    [data-testid="stSidebar"] .stTextInput input {
        background-color: #163B48 !important;
        border: 1px solid #00D488 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        transition: box-shadow 0.25s ease, border-color 0.25s ease !important;
    }
    [data-testid="stSidebar"] .stTextInput input:focus {
        box-shadow: 0 0 0 3px rgba(0, 212, 136, 0.25) !important;
    }
    h1, h2, h3, p, label, span, li, td, th, div, .stMarkdown {
        color: #FFFFFF !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    }
    [data-testid="stMainViewContainer"] .stTextInput input,
    [data-testid="stMainViewContainer"] .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 2px solid #00D488 !important;
        color: #1A1A1A !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: box-shadow 0.25s ease, transform 0.15s ease !important;
    }
    [data-testid="stMainViewContainer"] .stTextInput input:focus {
        box-shadow: 0 0 0 4px rgba(0, 212, 136, 0.3) !important;
        transform: translateY(-1px);
    }
    [data-testid="stMainViewContainer"] .stTextInput input::placeholder {
        color: #718096 !important;
    }
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
        animation: fadeSlideIn 0.6s ease both !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #FF6B57 0%, #FF8A70 100%) !important;
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
        transform: translateY(-2px) scale(1.01) !important;
    }
    .stButton>button:active {
        transform: translateY(0px) scale(0.98) !important;
    }
    .content-block {
        background: linear-gradient(180deg, #133A46 0%, #102F3A 100%) !important;
        border: 1px solid #1A4452 !important;
        border-radius: 12px !important;
        padding: 30px !important;
        margin-top: 20px !important;
        min-height: 350px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25) !important;
        animation: fadeSlideIn 0.5s ease both !important;
    }
    .brand-ribbon {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 20px;
        border-bottom: 2px solid #FF6B57;
        margin-bottom: 35px;
        animation: fadeSlideIn 0.5s ease both;
    }
    .brand-title {
        font-size: 32px;
        font-weight: 800;
        letter-spacing: 3px;
        color: #FFFFFF;
        text-shadow: 0 0 14px rgba(0, 212, 136, 0.35);
    }
    .brand-title .dot {
        color: #00D488;
        animation: pulseDot 1.6s ease-in-out infinite;
    }
    .brand-tag {
        font-size: 12px;
        letter-spacing: 1.5px;
        color: #FF6B57;
        font-weight: 600;
        text-transform: uppercase;
    }
    .status-pill {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        background: rgba(0, 212, 136, 0.12);
        border: 1px solid #00D488;
        color: #00D488 !important;
        font-size: 12px;
        letter-spacing: 1px;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 14px;
    }
    .design-footer {
        border-top: 1px solid #1A4452;
        padding-top: 25px;
        margin-top: 60px;
        text-align: center;
        font-size: 14px;
        letter-spacing: 0.5px;
        color: #94A3B8;
        animation: fadeSlideIn 0.8s ease both;
    }
    .disclaimer-text {
        font-size: 11px;
        color: #64748B;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .hint-text {
        color: #94A3B8 !important;
        font-size: 14px;
        line-height: 1.6;
    }
    @keyframes fadeSlideIn {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseDot {
        0%, 100% { opacity: 1; }
        50%      { opacity: 0.35; }
    }
    </style>
""", unsafe_allow_html=True)

# 3. Top Section Brand Ribbon
st.markdown("""
<div class="brand-ribbon">
    <div class="brand-title"><span class="dot">●</span> TRAIT TAC TOE</div>
    <div class="brand-tag">
        WORLDGENETICS ARCHITECTURE ENGINE
    </div>
</div>
""", unsafe_allow_html=True)

# 4. Multi-Page Selection Matrix Setup
if 'current_pane' not in st.session_state:
    st.session_state.current_pane = "registry"

nav_col1, nav_col2, nav_col3 = st.columns(3)
with nav_col1:
    if st.button("1. Sequence Input Workspace", use_container_width=True, key="nav_registry"):
        st.session_state.current_pane = "registry"
with nav_col2:
    if st.button("2. Population Distance Matrix", use_container_width=True, key="nav_distance"):
        st.session_state.current_pane = "distance"
with nav_col3:
    if st.button("3. Clinical Profiler Hub", use_container_width=True, key="nav_profiler"):
        st.session_state.current_pane = "profiler"

# Live active-page indicator (interactive feedback)
_pane_labels = {
    "registry": "Active: Sequence Input Workspace",
    "distance": "Active: Population Distance Matrix",
    "profiler": "Active: Clinical Profiler Hub",
}
st.markdown(
    f"<div class='status-pill'>{_pane_labels.get(st.session_state.current_pane, '')}</div>",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# 5. Configurations Workspace
st.sidebar.markdown("### SYSTEM CONFIGURATION")
api_key = st.sidebar.text_input("NEBIUS OR OPENAI API KEY", type="password", value=os.getenv("CORE_API_KEY", ""))
tavily_key = st.sidebar.text_input("TAVILY API KEY", type="password", value=os.getenv("TAVILY_API_KEY", ""))

if api_key and tavily_key:
    st.sidebar.success("COMPUTATION ENGINE ONLINE")
else:
    st.sidebar.info("Enter both keys to bring the engine online.")

# Main Page Routing Engine logic
if st.session_state.current_pane == "registry":
    st.markdown("<div class='bubble-header'>Sequence Input Workspace</div>", unsafe_allow_html=True)
    st.markdown("<div class='content-block'>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.session_state.disease = st.text_input(
            "RARE GENETIC CONDITION",
            value=st.session_state.get('disease', ''),
            placeholder="e.g., Huntington's Disease",
        )
        st.session_state.variant = st.text_input(
            "SPECIFIC MUTATION / EXON DELETION",
            value=st.session_state.get('variant', ''),
            placeholder="e.g., Exon 1 Expansion",
        )
    with col_b:
        st.session_state.cyp_variant = st.selectbox(
            "CYP450 ENZYME METABOLIC STATUS",
            ["CYP2C19 Poor Metabolizer", "CYP2D6 Ultra-rapid Metabolizer", "CYP2C9 Intermediate Metabolizer", "Normal / Homozygous Wild-type"]
        )
        st.session_state.current_meds = st.text_input(
            "CONCOMITANT DAILY PRESCRIPTIONS",
            value=st.session_state.get('current_meds', ''),
            placeholder="e.g., Fluoxetine",
        )

    # Live profile completeness indicator
    _filled = sum(bool(st.session_state.get(k, '').strip()) if isinstance(st.session_state.get(k, ''), str) else False
                  for k in ('disease', 'variant', 'current_meds'))
    _progress_value = _filled / 3
    st.progress(_progress_value, text=f"Profile completeness: {int(_progress_value * 100)}%")

    st.markdown("<br><p class='hint-text'>Provide patient genomic profile string allocations above. Navigate to panels 2 or 3 using the workspace triggers to dynamically map alignment structures and flag active drug-gene interactions.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.current_pane == "distance" or st.session_state.current_pane == "profiler":
    st.markdown(f"<div class='bubble-header'>{st.session_state.current_pane.upper()} REPORT INTERFACE</div>", unsafe_allow_html=True)
    st.markdown("<div class='content-block'>", unsafe_allow_html=True)
    disease_input = st.session_state.get('disease', '')
    variant_input = st.session_state.get('variant', '')

    if not disease_input or not variant_input:
        st.warning("Awaiting profile configuration. Complete values inside Page 1: Sequence Input Workspace first.")
    elif not api_key or not tavily_key:
        st.error("Missing required credentials. Populate API elements inside sidebar configuration box.")
    else:
        os.environ["TAVILY_API_KEY"] = tavily_key

        with st.spinner("Processing real-time web mining stream via Tavily..."):
            tavily = TavilySearchResults(max_results=4)
            search_query = f"open clinical trials targeting {disease_input} mutation {variant_input} drug pathways"
            trial_data = tavily.invoke({"query": search_query})

        with st.spinner("Running language synthesis models..."):
            # If the user has a Nebius key (starts with something other than sk-), route to Nebius Token Factory
            if not api_key.startswith("sk-"):
                llm = OpenAI(
                    openai_api_key=api_key,
                    openai_api_base="https://nebius.ai",
                    model="nvidia/Llama-3.1-Nemotron-70B-Instruct"
                )
            else:
                # Fallback to OpenAI API for demonstration evaluation if blocked by card billing setup
                llm = OpenAI(
                    openai_api_key=api_key,
                    model="gpt-3.5-turbo-instruct"
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
    Used by 1,000+ users across the world including researchers in France, the United States, Germany, the United Kingdom, and Japan.
    <div class="disclaimer-text">Notice: For design presentation purposes only. Analytical assets represent statistical simulations.</div>
</div>
""", unsafe_allow_html=True)
