# petstore/rbd/query.py
"""Unified query module for database operations"""

from typing import List, Dict, Any, Optional
from .database import ReferenceBaseDB
from .utils import format_record, sort_records

class QueryManager:
    """Manages database queries and provides a unified interface for data access"""
    
    def __init__(self, db_path: str):
        """
        Initialize the QueryManager with a database path.
        
        Args:
            db_path: Path to the database file
        """
        self.db = ReferenceBaseDB(db_path)
    
    def get_all_records(self, sort_by: str = "timestamp", reverse: bool = True) -> List[Dict[str, Any]]:
        """
        Retrieve all records from the database.
        
        Args:
            sort_by: Field to sort by (default: "timestamp")
            reverse: Whether to sort in descending order (newest first)
        
        Returns:
            List of all records with decoded data
        """
        return self.db.get_all_records(sort_by, reverse)
    
    def get_records_by_type(self, record_type: str, sort_by: str = "timestamp", reverse: bool = True) -> List[Dict[str, Any]]:
        """
        Retrieve all records of a specific type from the database.
        
        Args:
            record_type: Type of records to retrieve
            sort_by: Field to sort by (default: "timestamp")
            reverse: Whether to sort in descending order (newest first)
        
        Returns:
            List of records with the specified type
        """
        return self.db.get_records_by_type(record_type, sort_by, reverse)
    
    def get_record_by_ref(self, ref_hash: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific record by its reference hash.
        
        Args:
            ref_hash: The reference hash of the record to retrieve
            
        Returns:
            The formatted record or None if not found
        """
        if ref_hash in self.db.store:
            record = self.db.store[ref_hash]
            decoded_data = self.db._decode_data(record["data"])
            return format_record(ref_hash, record, decoded_data)
        return None
    
    def query_similar(self, text: str, threshold: float = 0.6) -> List[Dict[str, Any]]:
        """
        Query for similar records based on text similarity.
        
        Args:
            text: Text to search for similar records
            threshold: Similarity threshold (0.0 to 1.0)
            
        Returns:
            List of similar records with similarity scores
        """
        return self.db.query_similar(text, threshold)
    
    def get_chain(self, start_ref: str) -> List[Any]:
        """
        Get the chain of records starting from a reference.
        
        Args:
            start_ref: The starting reference hash
            
        Returns:
            List of decoded data in the chain
        """
        return self.db.get_chain(start_ref)
    
    def add_record(self, data: Any, text_hint: str = None, prev: str = None) -> str:
        """
        Add a new record to the database.
        
        Args:
            data: The data to store
            text_hint: Text hint for semantic search
            prev: Reference to previous record in chain
            
        Returns:
            The reference hash of the new record
        """
        return self.db.add(data, text_hint, prev)
    
    def get_record_types(self) -> Dict[str, int]:
        """
        Get a count of all record types in the database.
        
        Returns:
            Dictionary mapping record types to their counts
        """
        type_counts = {}
        for record in self.db.store.values():
            record_type = record.get("type", "unknown")
            type_counts[record_type] = type_counts.get(record_type, 0) + 1
        return type_counts

# Create a default query manager for the petstore database
default_query_manager = QueryManager("data/petstore_rbd.json")

# Convenience functions that use the default query manager
def get_all_records(sort_by: str = "timestamp", reverse: bool = True) -> List[Dict[str, Any]]:
    """Convenience function to get all records using the default query manager"""
    return default_query_manager.get_all_records(sort_by, reverse)

def get_records_by_type(record_type: str, sort_by: str = "timestamp", reverse: bool = True) -> List[Dict[str, Any]]:
    """Convenience function to get records by type using the default query manager"""
    return default_query_manager.get_records_by_type(record_type, sort_by, reverse)

def get_record_by_ref(ref_hash: str) -> Optional[Dict[str, Any]]:
    """Convenience function to get a record by reference using the default query manager"""
    return default_query_manager.get_record_by_ref(ref_hash)

def query_similar(text: str, threshold: float = 0.6) -> List[Dict[str, Any]]:
    """Convenience function to query similar records using the default query manager"""
    return default_query_manager.query_similar(text, threshold)

def get_chain(start_ref: str) -> List[Any]:
    """Convenience function to get a chain of records using the default query manager"""
    return default_query_manager.get_chain(start_ref)

def add_record(data: Any, text_hint: str = None, prev: str = None) -> str:
    """Convenience function to add a record using the default query manager"""
    return default_query_manager.add_record(data, text_hint, prev)

def get_record_types() -> Dict[str, int]:
    """Convenience function to get record types using the default query manager"""
    return default_query_manager.get_record_types()