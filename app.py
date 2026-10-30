Dependencies and imports:
- streamlit
- langchain-nvidia-ai-endpoints (provides ChatNVIDIA)
- langchain-community (provides TavilySearchResults)
- tavily-python (required at runtime by TavilySearchResults)
- Install with: pip install streamlit langchain-nvidia-ai-endpoints langchain-community tavily-python

import streamlit as st
import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_community.tools.tavily_search import TavilySearchResults

# 1. Force the World Genetics Minimalist Light Theme via CSS
st.set_page_config(page_title="GENMATCH RX", layout="wide")

st.markdown("""
    <style>
    /* Main Background and Typography */
    .stApp {
        background-color: #F8F9FA !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Global Text Colors to Deep Charcoal */
    h1, h2, h3, p, label, .stMarkdown {
        color: #1A1A1A !important;
    }
    
    /* Input Box Styles - Sharp Borders, Flat White Background */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 4px !important;
        color: #1A1A1A !important;
    }
    
    /* Flat Matte Blue Primary Button */
    .stButton>button {
        background-color: #1A2E40 !important;
        color: #FFFFFF !important;
        border-radius: 4px !important;
        border: none !important;
        width: 100% !important;
        font-weight: 500 !important;
        letter-spacing: 1px !important;
        padding: 0.6rem !important;
        text-transform: uppercase !important;
    }
    .stButton>button:hover {
        background-color: #2C4A66 !important;
        color: #FFFFFF !important;
    }
    
    /* Visual Matrix Tags */
    .tag-critical {
        background-color: #FDF2F2; color: #9B1C1C; 
        padding: 4px 8px; border-radius: 4px; font-weight: bold; border: 1px solid #F8B4B4;
    }
    .tag-monitor {
        background-color: #FDF8F2; color: #92400E; 
        padding: 4px 8px; border-radius: 4px; font-weight: bold; border: 1px solid #FCD34D;
    }
    .tag-verified {
        background-color: #F0FDF4; color: #166534; 
        padding: 4px 8px; border-radius: 4px; font-weight: bold; border: 1px solid #86EFAC;
    }
    </style>
""", unsafe_html=True)

# 2. Top Navigation Bar Layout
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px; border-bottom: 1px solid #E0E0E0; margin-bottom: 30px;">
    <div style="font-size: 24px; font-weight: 700; letter-spacing: 2px; color: #1A1A1A;">GENMATCH RX</div>
    <div style="font-size: 12px; letter-spacing: 1px; color: #6B7280; font-weight: 500;">
        UPLOAD GENOMIC SEQUENCE &nbsp; | &nbsp; CLINICAL PROFILER &nbsp; | &nbsp; POPULATION DRUG ANALYTICS
    </div>
</div>
""", unsafe_html=True)

# API Keys Configuration in Sidebar to keep main dashboard pristine
st.sidebar.markdown("### SYSTEM CONFIGULATION")
nvidia_key = st.sidebar.text_input("NVIDIA API KEY", type="password", value=os.getenv("NVIDIA_API_KEY", ""))
tavily_key = st.sidebar.text_input("TAVILY API KEY", type="password", value=os.getenv("TAVILY_API_KEY", ""))

if nvidia_key and tavily_key:
    st.sidebar.markdown("<span style='color: #166534; font-size: 12px; font-weight: bold;'>INTEGRATION ARCHITECTURE ONLINE</span>", unsafe_html=True)

# 3. Split-Pane Canvas Setup (35% Left Control Panel, 65% Right Visualizer Panel)
left_pane, right_pane = st.columns([35, 65])

with left_pane:
    st.markdown("<div style='font-size: 14px; font-weight: 600; letter-spacing: 1px; color: #4B5563; margin-bottom: 15px;'>REGISTRY DATA INPUT</div>", unsafe_html=True)
    
    disease = st.text_input("RARE GENETIC CONDITION", placeholder="e.g., Cystic Fibrosis")
    variant = st.text_input("SPECIFIC MUTATION / EXON DELETION", placeholder="e.g., F508del")
    
    cyp_variant = st.selectbox(
        "CYP450 ENZYME METABOLIC STATUS",
        ["CYP2C19 Poor Metabolizer", "CYP2D6 Ultra-rapid Metabolizer", "CYP2C9 Intermediate Metabolizer", "Normal / Homozygous Wild-type"]
    )
    
    current_meds = st.text_input("CONCOMITANT DAILY PRESCRIPTIONS", placeholder="e.g., Warfarin")
    
    st.markdown("<br>", unsafe_html=True)
    analyze_button = st.button("RUN GENOMIC ALIGNMENT")

with right_pane:
    # Initial state placeholder mimicking an unpopulated genetic mapping grid
    if not analyze_button:
        st.markdown("""
        <div style="border: 1px dashed #E0E0E0; border-radius: 4px; height: 400px; display: flex; align-items: center; justify-content: center; background-color: #FFFFFF;">
            <div style="color: #9CA3AF; font-size: 13px; letter-spacing: 1px; text-transform: uppercase;">Awaiting Clinical Registry Profile Submission</div>
        </div>
        """, unsafe_html=True)
        
    else:
        if not nvidia_key or not tavily_key:
            st.error("Missing required credentials. Populate API inputs inside configuration workspace.")
        elif not disease or not variant:
            st.warning("Primary Condition and Variant inputs are required to map sequences.")
        else:
            os.environ["NVIDIA_API_KEY"] = nvidia_key
            os.environ["TAVILY_API_KEY"] = tavily_key
            
            # Agent execution
            with st.spinner("Executing real-time registry query..."):
                tavily = TavilySearchResults(max_results=5)
                search_query = f"open clinical trials targeting {disease} mutation {variant} therapeutic drug molecules"
                trial_data = tavily.invoke({"query": search_query})

            with st.spinner("Computing enzymatic distance matrices..."):
                llm = ChatNVIDIA(model="meta/llama3-70b-instruct")
                
                prompt = f"""
                You are a system logic generator for a precision genetics medical platform. 
                Analyze these search results concerning open trials for {disease} ({variant}): {trial_data}
                
                Evaluate structural safety against the patient's system profiles:
                - Target Metabolism: {cyp_variant}
                - Concurrent Medications: {current_meds}
                
                Generate a raw markdown report following this strict format. Do not use any introductory conversational filler text or conclusion statements. Do not use emojis anywhere.
                
                ### TARGET PATHWAY AND INTERACTION DISTANCE REPORT
                Provide a structured Markdown data table mapping out the drug-gene or drug-drug variables found. Use these exact structural headers:
                PATHWAY / DRUG GENE COMPONENT | SCORED DEVIATION | CLASSIFICATION
                For the classification column, use one of these three exact text strings depending on severity:
                - CRITICAL / TOXICITY RISK
                - MODERATE / MONITOR INTENSITY
                - VERIFIED CLEAR ALIGNMENT
                
                ### ACTIVE CLINICAL PROTOCOLS LOCATED
                Provide a clean, bulleted list of the 2 or 3 specific trials or molecular mechanisms identified by the search data. Detail the registry identifier if visible, the trial sponsor, and target variant alignment parameters.
                
                ### REQUIRED CLINICAL INTERVENTION NEXT STEPS
                Provide a numbered list of exactly 3 concise, highly actionable directives for an attending clinical geneticist regarding patient safety or enrollment alterations based on this analysis.
                """
                
                response = llm.invoke(prompt)
            
            # Render the final clean structured output container
            st.markdown("<div style='font-size: 14px; font-weight: 600; letter-spacing: 1px; color: #4B5563; margin-bottom: 15px;'>GENETIC DISTANCE & TRIAL ALIGNMENT ANALYSIS</div>", unsafe_html=True)
            st.markdown(response.content)
