# test_refactored.py
"""Test script to verify the refactored code works correctly"""

import sys
import os

# Add the web directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'web'))

# Import directly from the rbd module
from petstore.rbd.query import QueryManager
from petstore.rbd.database import ReferenceBaseDB

# Import export_sample_dataset from the root petstore.py file
sys.path.insert(0, os.path.dirname(__file__))
from petstore import export_sample_dataset

def test_refactored_code():
    print("🧪 Testing refactored code...")
    
    # Create a test database
    db_path = "data/test_rbd.json"
    query_manager = QueryManager(db_path)
    
    # Add some test data
    test_data = {
        "name": "Test Pet",
        "type": "dog",
        "breed": "Labrador",
        "age_months": 24
    }
    
    ref = query_manager.add_record(test_data, text_hint="Test pet data")
    print(f"✅ Added test record with ref: {ref}")
    
    # Retrieve all records
    records = query_manager.get_all_records()
    print(f"✅ Retrieved {len(records)} records")
    
    # Retrieve records by type
    j_records = query_manager.get_records_by_type("j")
    print(f"✅ Retrieved {len(j_records)} JSON records")
    
    # Get record types
    type_counts = query_manager.get_record_types()
    print(f"✅ Record types: {type_counts}")
    
    # Test querying similar records
    similar = query_manager.query_similar("pet")
    print(f"✅ Found {len(similar)} similar records")
    
    # Test getting a record by reference
    record = query_manager.get_record_by_ref(ref)
    if record:
        print(f"✅ Retrieved record by ref: {record['ref']}")
    else:
        print("❌ Failed to retrieve record by ref")
    
    print("🎉 All tests passed!")

if __name__ == "__main__":
    test_refactored_code()