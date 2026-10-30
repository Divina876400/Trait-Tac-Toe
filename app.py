

# Dependencies and imports:
# - streamlit
# - langchain-nvidia-ai-endpoints (provides ChatNVIDIA)
# - langchain-community (provides TavilySearchResults; also requires the tavily-python package)
# - Standard library: os
#
# Install with: pip install streamlit langchain-nvidia-ai-endpoints langchain-community tavily-python

import streamlit as st
import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_community.tools.tavily_search import TavilySearchResults

# 1. Initialize Page Canvas
st.set_page_config(page_title="TRAIT TAC TOE", layout="wide")

# 2. Inject Dark Teal and Pure White Input Bubble Container CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    /* Base Background Matrix */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {
        background: radial-gradient(1100px 550px at 8% -10%, rgba(0,212,136,0.13), transparent 60%), radial-gradient(900px 500px at 100% 0%, rgba(255,107,87,0.10), transparent 60%), #0B2530 !important;
    }
    
    /* Sidebar Specific Container Clean-up to remove white background box leaks */
    [data-testid="stSidebar"] .stTextInput input {
        background-color: #163B48 !important;
        border: 1px solid #00D488 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
    }
    
    /* Main Layout Text Configuration */
    h1, h2, h3, p, label, span, li, td, th, div, .stMarkdown {
        color: #FFFFFF !important;
        font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
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
        background: linear-gradient(135deg, #15404F 0%, #0E3240 100%) !important;
        border: 1px solid rgba(0,212,136,0.55) !important;
        border-radius: 999px !important;
        padding: 12px 26px !important;
        display: inline-block !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        margin-bottom: 22px !important;
        font-size: 18px !important;
        letter-spacing: 0.4px !important;
        box-shadow: 0 6px 24px rgba(0,0,0,0.25) !important;
    }
    .accent {
        color: #00D488 !important;
    }
    .hero-title {
        font-size: 40px;
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -0.5px;
        margin: 6px 0 10px 0;
    }
    .hero-sub {
        font-size: 17px;
        color: #B8C7D0 !important;
        max-width: 760px;
    }
    .chip-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 14px;
    }
    .chip {
        background: rgba(0,212,136,0.12);
        border: 1px solid rgba(0,212,136,0.4);
        border-radius: 999px;
        padding: 6px 14px;
        font-size: 13px;
    }
    .feature-card {
        background: #133A46;
        border: 1px solid #1A4452;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.2);
    }
    .feature-card h4 {
        margin: 8px 0 6px 0;
        font-size: 18px;
        font-weight: 700;
    }
    .feature-card p {
        font-size: 14px;
        color: #B8C7D0 !important;
        line-height: 1.55;
        margin: 0;
    }
    .feature-tag {
        color: #00D488 !important;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    /* Custom Flat Navigation Buttons Override (Orange/Coral theme from image) */
    .stButton>button {
        background: linear-gradient(135deg, #FF6B57, #FF8A5B) !important;
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
        background: linear-gradient(135deg, #FF8575, #FFA06B) !important;
        box-shadow: 0 6px 18px rgba(255, 107, 87, 0.45) !important;
        transform: translateY(-1px);
    }
    
    /* Fullness Expansion Spacer Card */
    .content-block {
        background-color: rgba(19,58,70,0.85) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 16px !important;
        padding: 30px !important;
        margin-top: 20px !important;
        min-height: 350px !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.25) !important;
    }
    
    /* System Global Footer */
    .design-footer {
        border-top: 1px solid #1A4452;
        padding-top: 25px;
        margin-top: 60px;
        text-align: center;
        font-size: 14px;
        letter-spacing: 0.5px;
        color: #94A3B8 !important;
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
<div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px; border-bottom: 2px solid #FF6B57; margin-bottom: 35px;">
    <div style="font-size: 32px; font-weight: 800; letter-spacing: 3px; color: #FFFFFF;">● TRAIT TAC TOE</div>
    <div style="font-size: 12px; letter-spacing: 1.5px; color: #FF6B57; font-weight: 600; text-transform: uppercase;">
        WORLDGENETICS ARCHITECTURE ENGINE
    </div>
</div>
""", unsafe_allow_html=True)

# Hero section and step cards, styled after the World Genetics landing page
st.markdown("""
<div class="hero-title">Discover the trials and drug interactions <span class="accent">closest to your profile.</span></div>
<div class="hero-sub">Enter a rare genetic condition and mutation, then generate a report that ranks open clinical trials and flags drug-gene risks.</div>
<div class="chip-row">
<span class="chip">Closest matches</span>
<span class="chip">Interaction breakdown</span>
<span class="chip">Live trial mining</span>
</div>
""", unsafe_allow_html=True)

feat1, feat2, feat3 = st.columns(3)
with feat1:
    st.markdown('<div class="feature-card"><div class="feature-tag">Step 1</div><h4>Sequence Input Workspace</h4><p>Describe the condition, the specific mutation or exon deletion, and any daily prescriptions.</p></div>', unsafe_allow_html=True)
with feat2:
    st.markdown('<div class="feature-card"><div class="feature-tag">Step 2</div><h4>Population Distance Matrix</h4><p>Mine open clinical trials and synthesize the results into a ranked interaction table.</p></div>', unsafe_allow_html=True)
with feat3:
    st.markdown('<div class="feature-card"><div class="feature-tag">Step 3</div><h4>Clinical Profiler Hub</h4><p>Review classified risks and three prioritized next steps for patient safety or enrollment.</p></div>', unsafe_allow_html=True)

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

st.markdown("<br>", unsafe_allow_html=True)

# 5. Core Environment Context Persistence Area
st.sidebar.markdown("### SYSTEM CONFIGURATION")
nvidia_key = st.sidebar.text_input("NVIDIA API KEY", type="password", value=os.getenv("NVIDIA_API_KEY", ""))
tavily_key = st.sidebar.text_input("TAVILY API KEY", type="password", value=os.getenv("TAVILY_API_KEY", ""))

# Main Page Routing Engine logic
if st.session_state.current_pane == "registry":
    st.markdown("<div class='bubble-header'>Sequence Input Workspace</div>", unsafe_allow_html=True)
    
    # Structural panel wrapper to add "fullness" to the display area
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
            st.markdown(response.content)
    st.markdown("</div>", unsafe_allow_html=True)

# 6. Design Specific Metrics Footer
st.markdown("""
<div class="design-footer">
    Used by 1,000+ users across the world including researchers in France, the United States, Germany, the United Kingdom, and Japan.
</div>
""", unsafe_allow_html=True)
