from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Optional
import os


class VectorDatabase:
    def __init__(
        self,
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name="testing_col",
        # embedding_model_name: str = "BAAI/bge-small-en",  # Default model
    ):
        """
        Initialize the Qdrant client, FastEmbed, and collection.

        Args:
            host (str): Host address of the Qdrant server.
            port (int): Port of the Qdrant server.
            collection_name (str): Name of the collection to use or create.
            embedding_model_name (str): Name of the FastEmbed model to use.
        """
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection_name = collection_name

    def upsert_documents(self, texts: List[str]):
        # Insert into Qdrant
        self.client.add(
            collection_name=self.collection_name,
            documents=texts,
        )
        print(
            f"Inserted {len(texts)} documents into collection '{self.collection_name}'."
        )

    def search_similar(self, query_text: str):
        search_result = self.client.query(
            collection_name=self.collection_name,
            query_text=query_text,
            limit=1,
        )

        document = search_result[0].document

        return document

    def delete_collection(self):
        """
        Delete the Qdrant collection.
        """
        self.client.delete_collection(self.collection_name)
        print(f"Deleted collection: {self.collection_name}")

    def list_collections(self):
        """
        List all collections in the Qdrant database.

        Returns:
            List[str]: List of collection names.
        """
        collections = self.client.get_collections().collections
        return [collection.name for collection in collections]
