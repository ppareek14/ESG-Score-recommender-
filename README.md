# ESG-Score-recommender-
Forced Labour Risk ESG Assistant
A GenAI-powered tool to analyze, score, and explain the risk of forced labour practices in companies based on their ESG and sustainability reports, helping investors make responsible and data-driven investment decisions.

Project Overview
This project implements a Retrieval-Augmented Generation (RAG) pipeline combined with a forced labour risk scoring model. It is designed to:

Extract both native text and image-based text (OCR) from ESG and sustainability documents.

Use semantic search and prompted Large Language Model (LLM) reasoning to answer critical investment risk questions.

Score companies based on global regulatory standards, including GRI 409 (Forced or Compulsory Labour), ESRS S2 (Value Chain Workers), and SFDR (Sustainable Finance Disclosure Regulation).

Generate transparent investment recommendations with citations from original reports.

Visualize forced labour risk across companies using interactive dashboards and risk reports.

Key Features
Parse and analyze complex ESG and sustainability reports, including both text and scanned images.

Leverage Large Language Models (LLMs) to retrieve contextually relevant disclosures from long documents.

Assign a forced labour risk score (scale of 0–100) for each company based on disclosure quality and risk mitigation.

Generate clear investment recommendations categorized as Invest, Watchlist, or Avoid.

Provide auditable justifications with direct quotations from official ESG documents.

Visualize risk scores, metrics, and flagged disclosures through a professional dashboard.

How It Works
1. PDF Extraction
Extracts both native digital text and applies Optical Character Recognition (OCR) to image-based sections of ESG and sustainability reports.

2. Chunking and Embedding
Splits extracted content into manageable chunks and generates semantic embeddings for efficient retrieval.

3. Vector Database Storage
Stores the document chunks in a vector database (e.g., FAISS) for scalable, high-performance semantic search.

4. Prompted Retrieval
Applies structured prompts to retrieve relevant sections and answer investment-related questions, such as:

"Does the company audit suppliers for forced labour risks?"

5. Risk Scoring
Applies a structured scoring model aligned with recognized ESG frameworks to evaluate the company's disclosures and practices.

Calculates an overall risk score and categorizes companies into investment recommendation tiers.

6. Visualization
Presents risk scores, key flagged disclosures, and investment recommendations through an interactive Streamlit dashboard.

Enables generation of downloadable, audit-ready risk reports.






