import os
import json
import streamlit as st
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# Add the scorer folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scorer")))

from query_chroma_and_score import analyze_forced_labor_disclosure

# Page config
st.set_page_config(page_title="ESG Forced Labor Analyzer", page_icon="🌱", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>TEXpert.AI</h1>", unsafe_allow_html=True)


# Determine companies dynamically from chroma_store folder structure
chroma_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "chroma_store"))
companies = sorted([
    name for name in os.listdir(chroma_path)
    if os.path.isdir(os.path.join(chroma_path, name))
])

# Add an empty option at the top of the dropdown
companies.insert(0, "")

# Main interface
st.title("🌿 ESG Forced Labor & Child Labor Disclosure Analyzer")

company = st.selectbox("Select a company:", companies)

# Enter your question - starts empty
st.markdown("### 🔍 Enter your question below:")
question = st.text_input("", value="")

# Ask button - visually distinct
if st.button("🚀 Ask!", type="primary"):
    if not company or not question.strip():
        st.warning("Please select a company and enter your question.")
    else:
        enriched_query = f"{company} forced labor and child labor disclosures"
        result = analyze_forced_labor_disclosure(company, enriched_query)
        if "error" in result:
            st.error(result["error"])
        else:
            st.markdown("## 🌟 ESG Analysis Summary")
            st.markdown(f"**Company:** `{result['company']}`")
            st.markdown(f"**Total Score:** `{result['total_score']}`")
            st.markdown(f"**Risk Level:** :orange[{result['risk_level']}]")

            with st.expander("📊 Detailed Breakdown", expanded=True):
                for indicator, data in result["breakdown"].items():
                    st.markdown(f"#### {indicator}")
                    st.markdown(f"- **Score:** `{data['score']}`")
                    st.markdown(f"- **Justification:** {data['justification']}")
                    st.markdown("---")

            st.markdown("### 📚 Sources")
            if result.get("sources"):
                for idx, src in enumerate(result["sources"], 1):
                    st.markdown(f"- {idx}. **File:** `{src['source']}` | **Page:** `{src['page']}`")
            else:
                st.write("No sources available.")

            with st.expander("📝 Full JSON Output"):
                st.json(result)

# FAQ Section - clear separation
st.markdown("#### 💡 Frequently Asked Questions:")
faq_questions = [
    "What are the company's forced labor and child labor disclosures?",
    "What due diligence processes are mentioned in the company's sustainability reports?",
    "Does the company mention high-risk regions or suppliers for forced labor?",
    "Are there supplier audits or grievance mechanisms described in the disclosures?"
]

# Render FAQ buttons - smaller and organized in two columns
faq_cols = st.columns(2)
for idx, q in enumerate(faq_questions):
    col = faq_cols[idx % 2]
    if col.button(q, key=f"faq_{idx}"):
        if not company:
            st.warning("Please select a company first.")
        else:
            st.markdown(f"**Running analysis for:** `{q}`")
            enriched_query = f"{company} forced labor and child labor disclosures"
            result = analyze_forced_labor_disclosure(company, enriched_query)
            if "error" in result:
                st.error(result["error"])
            else:
                st.markdown("## 🌟 ESG Analysis Summary")
                st.markdown(f"**Company:** `{result['company']}`")
                st.markdown(f"**Total Score:** `{result['total_score']}`")
                st.markdown(f"**Risk Level:** :orange[{result['risk_level']}]")

                with st.expander("📊 Detailed Breakdown", expanded=True):
                    for indicator, data in result["breakdown"].items():
                        st.markdown(f"#### {indicator}")
                        st.markdown(f"- **Score:** `{data['score']}`")
                        st.markdown(f"- **Justification:** {data['justification']}")
                        st.markdown("---")

                st.markdown("### 📚 Sources")
                if result.get("sources"):
                    for idx, src in enumerate(result["sources"], 1):
                        st.markdown(f"- {idx}. **File:** `{src['source']}` | **Page:** `{src['page']}`")
                else:
                    st.write("No sources available.")

                with st.expander("📝 Full JSON Output"):
                    st.json(result)

# Sidebar logs/debug info
st.sidebar.header("Logs / Debug Info")
st.sidebar.write("Chroma DB path:")
st.sidebar.code(chroma_path)
