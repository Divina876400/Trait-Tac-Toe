

import streamlit as st
import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_community.tools.tavily_search import TavilySearchResults

# Native Page Configuration
st.set_page_config(page_title="TRAIT TAC TOE", layout="wide")

# Constants
MAX_INPUT_LENGTH = 200
CYP_OPTIONS = [
    "CYP2C19 Poor Metabolizer",
    "CYP2D6 Ultra-rapid Metabolizer",
    "CYP2C9 Intermediate Metabolizer",
    "Normal / Homozygous Wild-type",
]
DISCLAIMER = (
    "Research decision-support output only. This is not medical advice and not a clinical recommendation. "
    "All results must be reviewed by a licensed clinical geneticist or pharmacist before any action is taken."
)


def input_too_long(*values):
    return any(len(value) > MAX_INPUT_LENGTH for value in values)


# Pure Typography Navigation Header
st.title("TRAIT TAC TOE")
st.caption("UPLOAD GENOMIC SEQUENCE  |  CLINICAL PROFILER  |  POPULATION DRUG ANALYTICS")
st.warning(DISCLAIMER)
st.markdown("---")

# System Configurations Area in Sidebar
st.sidebar.markdown("### SYSTEM CONFIGURATION")
nvidia_key = st.sidebar.text_input("NVIDIA API KEY", type="password", value=os.getenv("NVIDIA_API_KEY", ""))
tavily_key = st.sidebar.text_input("TAVILY API KEY", type="password", value=os.getenv("TAVILY_API_KEY", ""))

if nvidia_key and tavily_key:
    st.sidebar.success("INTEGRATION ARCHITECTURE ONLINE")

# Split-Pane Canvas Setup (35% Left Control Panel, 65% Right Visualizer Panel)
left_pane, right_pane = st.columns(2)

with left_pane:
    st.markdown("### REGISTRY DATA INPUT")

    disease = st.text_input("RARE GENETIC CONDITION", placeholder="e.g., Cystic Fibrosis")
    variant = st.text_input("SPECIFIC MUTATION / EXON DELETION", placeholder="e.g., F508del")

    cyp_variant = st.selectbox(
        "CYP450 ENZYME METABOLIC STATUS",
        CYP_OPTIONS
    )

    current_meds = st.text_input("CONCOMITANT DAILY PRESCRIPTIONS", placeholder="e.g., Warfarin")

    acknowledged = st.checkbox(
        "I understand this output is not clinical advice and requires expert review"
    )

    analyze_button = st.button("RUN GENOMIC ALIGNMENT", use_container_width=True)

with right_pane:
    if not analyze_button:
        st.info("Awaiting Clinical Registry Profile Submission")
    elif not acknowledged:
        st.error("Acknowledge the clinical disclaimer in the registry panel before running the analysis.")
    elif not nvidia_key or not tavily_key:
        st.error("Missing required credentials. Populate API inputs inside configuration workspace.")
    else:
        disease = disease.strip()
        variant = variant.strip()
        current_meds = current_meds.strip()

        if not disease or not variant:
            st.warning("Primary Condition and Variant inputs are required to map sequences.")
        elif input_too_long(disease, variant, current_meds):
            st.warning(f"Each input must be {MAX_INPUT_LENGTH} characters or fewer.")
        elif cyp_variant not in CYP_OPTIONS:
            st.error("Unrecognized CYP450 enzyme metabolic status. Select an option from the list.")
        else:
            os.environ["NVIDIA_API_KEY"] = nvidia_key
            os.environ["TAVILY_API_KEY"] = tavily_key

            with st.spinner("Executing real-time registry query..."):
                try:
                    tavily = TavilySearchResults(max_results=5)
                    search_query = f"open clinical trials targeting {disease} mutation {variant} therapeutic drug molecules"
                    trial_data = tavily.invoke({"query": search_query})
                except Exception as exc:
                    st.error(
                        f"Registry search failed: {exc}. "
                        "Check the Tavily API key and network connection, then try again."
                    )
                    st.stop()

            if not trial_data:
                st.warning("The registry search returned no results, so no analysis was generated.")
                st.stop()

            with st.spinner("Computing enzymatic distance matrices..."):
                try:
                    llm = ChatNVIDIA(model="meta/llama3-70b-instruct")

                    prompt = f"""
                You are a system logic generator for a precision genetics medical platform called TRAIT TAC TOE. 
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
                except Exception as exc:
                    st.error(
                        f"Analysis model request failed: {exc}. "
                        "Check the NVIDIA API key, rate limits, and network connection, then try again."
                    )
                    st.stop()

            report = (response.content or "").strip()
            if not report:
                st.warning("The model returned an empty report. Try running the analysis again.")
                st.stop()

            st.markdown("### GENETIC DISTANCE & TRIAL ALIGNMENT ANALYSIS")
            st.warning(DISCLAIMER)
            st.markdown(report)