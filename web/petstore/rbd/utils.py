# petstore/rbd/utils.py
"""Shared utilities for database operations and record formatting"""

from datetime import datetime
from typing import List, Dict, Any

def format_record(ref_hash: str, record: Dict[str, Any], decoded_data: Any = None) -> Dict[str, Any]:
    """
    Format a database record with standardized fields.
    
    Args:
        ref_hash: The reference hash of the record
        record: The raw record from the database
        decoded_data: Pre-decoded data (optional, will decode if not provided)
        
    Returns:
        Formatted record dictionary with standardized fields
    """
    from .database import ReferenceBaseDB  # Import here to avoid circular imports
    
    # Decode data if not provided
    if decoded_data is None:
        db = ReferenceBaseDB.__new__(ReferenceBaseDB)  # Create instance without __init__
        decoded_data = db._decode_data(record["data"])
    
    # Create formatted record
    formatted_record = {
        "ref": ref_hash,
        "data": decoded_data,
        "timestamp": record.get("ts", 0),
        "type": record.get("type", "unknown"),
        "prev": record.get("prev", None),
        "timestamp_iso": "Unknown"
    }
    
    # Convert timestamp to ISO format if available
    if formatted_record["timestamp"] > 0:
        try:
            formatted_record["timestamp_iso"] = datetime.fromtimestamp(
                formatted_record["timestamp"]
            ).isoformat()
        except (ValueError, OSError):
            # Handle invalid timestamps
            formatted_record["timestamp_iso"] = "Invalid timestamp"
    
    return formatted_record

def format_records_batch(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Format a batch of records.
    
    Args:
        records: List of (ref_hash, record, decoded_data) tuples
        
    Returns:
        List of formatted records
    """
    formatted_records = []
    for ref_hash, record, decoded_data in records:
        formatted_records.append(format_record(ref_hash, record, decoded_data))
    return formatted_records

def sort_records(records: List[Dict[str, Any]], sort_by: str = "timestamp", reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Sort records by a specified field.
    
    Args:
        records: List of formatted records
        sort_by: Field to sort by
        reverse: Whether to sort in descending order
        
    Returns:
        Sorted list of records
    """
    try:
        records.sort(key=lambda x: x.get(sort_by, 0), reverse=reverse)
    except Exception:
        # If sorting fails, sort by reference as fallback
        records.sort(key=lambda x: x.get("ref", ""), reverse=reverse)
    return records