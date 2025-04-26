# ESG-Score-recommender-
Forced Labour Risk ESG Assistant
A GenAI-powered tool to analyze, score, and explain the risk of forced labour practices in companies based on their ESG and sustainability reports, helping investors make responsible and data-driven investment decisions.

Project Overview
This project builds a Retrieval-Augmented Generation (RAG) pipeline and a forced labour risk scoring model by:

Extracting both native text and image-based text (OCR) from ESG documents.

Using semantic search and prompted LLM reasoning to answer investment questions.

Scoring companies based on global standards (GRI 409, ESRS S2, SFDR).

Explaining recommendations with citations from original reports.

Visualizing forced labour risk using a dashboard and risk reports.

Key Features
Parse and understand complex ESG reports (text + scanned images)

Use LLMs (like GPT-4) to retrieve and reason over ESG disclosures

Assign a forced labour risk score (0–100) per company

Generate invest / watchlist / avoid recommendations

Provide transparent justifications with quotes from ESG reports

Visualize risk via charts, scorecards, and downloadable reports

How It Works
PDF Extraction:

Extract native text and OCR text from ESG reports.

Chunking & Embedding:

Split extracted text into chunks and create semantic embeddings.

Vector Database Storage:

Store document chunks for efficient retrieval using FAISS.

Prompted Retrieval:

Use RAG to answer investment-related queries like:
“Does the company audit suppliers for forced labour risks?”

Risk Scoring:

Apply a structured ESG metric framework to generate risk scores.

Visualization:

Use Streamlit to display risk levels, citations, and company comparisons.