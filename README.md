
# ESG-Score-recommender

Forced Labour Risk ESG Assistant

A GenAI-powered tool to analyze, score, and explain the risk of forced labour practices in companies based on their ESG and sustainability reports. This helps investors make responsible and data-driven investment decisions.

---

📌 Project Overview

This project implements a Retrieval-Augmented Generation (RAG) pipeline combined with a forced labour risk scoring model to:

- Extract both native text and image-based text (OCR) from ESG and sustainability documents.
- Use semantic search and Large Language Model (LLM) reasoning to answer critical investment risk questions.
- Score companies based on global regulatory standards, including GRI 409 (Forced or Compulsory Labour), ESRS S2 (Value Chain Workers), and SFDR (Sustainable Finance Disclosure Regulation).
- Generate transparent investment recommendations with citations from original reports.
- Visualize forced labour risk across companies through an interactive Streamlit dashboard.

---

🚀 Key Features

✅ Comprehensive Document Parsing  
Parse complex ESG and sustainability reports, including scanned images and embedded tables.

✅ Context-Aware Semantic Search 
Leverage LLMs to retrieve contextually relevant disclosures and provide accurate, nuanced answers.

✅ Structured Risk Scoring  
Assign a forced labour risk score (scale 0–100) for each company, aligned with international ESG frameworks.

✅ Actionable Investment Recommendations  
Generate clear recommendations categorized as Invest, Watchlist, or Avoid.

✅ Transparent Justifications  
Provide audit-ready justifications with direct quotations and page-level citations from the original ESG documents.

✅ Interactive Visualization 
Visualize risk scores, key disclosures, and investment recommendations through an intuitive dashboard.

---

🛠️ How It Works

1️⃣ PDF Extraction  
Extract native digital text and use OCR for image-based sections.

2️⃣ Chunking and Embedding 
Split extracted content into manageable chunks and generate semantic embeddings for scalable retrieval.

3️⃣ Vector Database Storage 
Store document chunks in a vector database for fast and efficient search.

4️⃣ Prompted Retrieval 
Use structured prompts to retrieve relevant sections and answer questions, e.g.,  
"Does the company audit suppliers for forced labour risks?"

5️⃣ Risk Scoring  
Apply a structured scoring model aligned with global standards to evaluate the quality of disclosures.

6️⃣ Visualization & Reporting  
Generate interactive dashboards and downloadable, audit-ready risk reports.

---

Tech Stack

- Python, Streamlit – for the interactive dashboard and logic.
- LangChain – for semantic retrieval and prompt-driven reasoning.
- OpenAI API – for LLM-based contextual reasoning.
- Chroma DB – for storing and querying embeddings.
- PyMuPDF, Pytesseract – for PDF and OCR extraction.

---

📂 Folder Structure

```
app/
├── chroma_store/           # Vector databases organized by company
├── data/                   # Raw ESG reports (PDFs)
├── extracted_texts/        # Extracted JSONL text chunks (mirrors data/ structure)
├── outputs/                # Streamlit app and logs
├── scorer/                 # Core RAG + scoring logic
```

---

👥 Usage

1. Add PDF Reports to the `data/` directory, organized by company.
  
3. Run Extraction & Embedding scripts:
   python pdf_extraction.py
   python build_openai_chroma_embeddings.py
  
4. Start the Dashboard:
   streamlit run app/outputs/streamlit_app.py
   
5. Interact – select a company, choose a question, or use the recommended FAQ buttons for instant insights!

---

💡 Final Note

This tool is designed for responsible investment analysis. It ensures that insights are transparent, data-driven, and aligned with global ESG standards.

---
