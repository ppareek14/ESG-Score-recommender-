# --- tests/test_embeddings.py ---

import unittest
from pathlib import Path
from chromadb import PersistentClient
from chromadb.config import Settings
from dotenv import load_dotenv
load_dotenv()

class TestChromaEmbeddings(unittest.TestCase):

    def setUp(self):
        project_root = Path(__file__).resolve().parents[1]
        chroma_path = project_root / "chroma_store"
        self.client = PersistentClient(path=str(chroma_path), settings=Settings())
        self.collection_name = "esg-forced-labour"
        self.collection = self.client.get_collection(self.collection_name)

    def test_collection_exists(self):
        self.assertIsNotNone(self.collection, "Collection not found.")

    def test_chunk_count_nonzero(self):
        count = self.collection.count()
        self.assertGreater(count, 0, "Collection is empty — no chunks uploaded.")

    def test_peek_chunks_and_show_sample(self):
        results = self.collection.peek(3)
        self.assertEqual(len(results["documents"]), 3)
        print("\n===== SAMPLE DOCUMENT CHUNKS =====")
        for i, doc in enumerate(results["documents"]):
            print(f"\n--- Chunk {i+1} ---\n{doc[:300]}...\n")
            self.assertTrue(len(doc.strip()) > 0, "Empty document chunk found.")

    def test_metadata_fields_present(self):
        results = self.collection.peek(5)
        for i, meta in enumerate(results["metadatas"]):
            print(f"\n[Meta {i+1}] → company: {meta.get('company')}, source: {meta.get('source')}, page: {meta.get('page')}")
            self.assertIn("company", meta, "Missing 'company' in metadata.")
            self.assertIn("source", meta, "Missing 'source' in metadata.")
            self.assertIn("page", meta, "Missing 'page' number in metadata.")
            self.assertIsInstance(meta["page"], int, "'page' should be an integer.")
            self.assertGreater(meta["page"], 0, "Page number should be > 0.")

if __name__ == "__main__":
    unittest.main()
