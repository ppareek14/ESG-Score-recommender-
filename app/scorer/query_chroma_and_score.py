import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate
import json

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = openai_api_key  # for langchain

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
chroma_path = os.path.join(project_root, "app", "chroma_store")
print("Using Chroma DB path:", chroma_path)
collection_name = "esg-forced-labour"

# Initialize LangChain components
embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
vectorstore = Chroma(
    collection_name=collection_name,
    embedding_function=embedding,
    persist_directory=chroma_path
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

def extract_company_from_query(query_text):
    return query_text.strip()

def generate_prompt(document_chunk):
    instructions = (
        "You are an ESG analyst. Based on the company's sustainability disclosure provided below, "
        "assign a score to each risk factor related to forced labor and child labor based on disclosure quality.\n\n"
        "Scoring Rules:\n"
        "- Assign a score from 0 (full disclosure, low risk) to the listed maximum (10 or 15), where higher means greater disclosure risk.\n"
        "- Provide justification (1-2 sentences) for each score.\n"
        "- Return result in JSON format.\n\n"
        f"Disclosure Content:\n\n\"\"\"{document_chunk}\"\"\"\n\n"
        "Evaluate the following risk indicators:"
    )

    criteria = [
        ("Fails to mention forced labor or child labor", 15),
        ("Omits coverage of either workforce or supply chain", 15),
        ("Fails to identify high-risk regions or suppliers", 10),
        ("No clear due diligence process described", 15),
        ("No supplier audit or monitoring details", 10),
        ("No KPIs, data, or case examples provided", 10),
        ("Fails to reference GRI 408/409 or ILO standards", 15),
        ("No remediation or grievance mechanisms described", 10)
    ]

    for indicator, max_score in criteria:
        instructions += f"\n- {indicator} (Max: {max_score})"

    instructions += (
        "\n\nRespond using this JSON format:\n"
        "{\n"
        '  "Fails to mention forced labor or child labor": {"score": 0, "justification": "..."},\n'
        '  "Omits coverage of either workforce or supply chain": {"score": 0, "justification": "..."},\n'
        "  ...\n"
        "}"
    )
    return instructions

def get_vectorstore_for_company(company_name):
    company_db_path = os.path.join(project_root, "app", "chroma_store", company_name.lower())
    return Chroma(
        collection_name=collection_name,
        embedding_function=embedding,
        persist_directory=company_db_path
    )

def analyze_forced_labor_disclosure(company_name, search_query=None):
    vectorstore = get_vectorstore_for_company(company_name)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # Use provided search_query or fallback to default
    query_text = search_query or f"{company_name} forced labor and child labor disclosures"
    print(f"\n🔍 Using search query: '{query_text}'")

    retrieved_docs = retriever.get_relevant_documents(query_text)

    if not retrieved_docs:
        return {"error": f"No disclosure found for {company_name}"}

    # Concatenate context
    context = ""
    for doc in retrieved_docs:
        meta = doc.metadata
        source = meta.get("source", "Unknown")
        page = meta.get("page", "?")
        context += f"\n\n[Source: {source}, Page: {page}]\n{doc.page_content}"

    # Generate ESG scoring prompt
    prompt = generate_prompt(context)

    try:
        response = llm.invoke(prompt)
        parsed = json.loads(response.content)
    except Exception as e:
        return {"error": str(e)}

    total_score = sum(item["score"] for item in parsed.values())
    if total_score <= 25:
        risk_level = "Low Risk"
    elif total_score < 50:
        risk_level = "Medium"
    elif total_score < 75:
        risk_level = "High"
    else:
        risk_level = "Attention Required"

    return {
        "company": company_name,
        "total_score": round(total_score, 2),
        "risk_level": risk_level,
        "breakdown": parsed,
        "sources": [
            {"source": doc.metadata.get("source"), "page": doc.metadata.get("page")}
            for doc in retrieved_docs
        ]
    }

if __name__ == "__main__":
    user_query = input("🔍 Enter company name or question: ")
    company = extract_company_from_query(user_query)
    print(f"✨ Interpreted company name: {company}")
    result = analyze_forced_labor_disclosure(company)
    print("\n📊 RAG Evaluation Result:")
    print(json.dumps(result, indent=2))
