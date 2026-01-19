# view_records_safe.py
"""Safe view of all records in the pet store database"""

from rbd.database import ReferenceBaseDB
from rbd.query import QueryManager
import json

def view_all_records():
    print("📋 Viewing all records in the pet store database...")
    
    # Create query manager for unified data access
    query_manager = QueryManager("data/petstore_rbd.json")
    
    # Get raw records first to inspect structure
    db = query_manager.db  # Access the underlying database for raw data
    print(f"\n🔍 Database contains {len(db.store)} records")
    
    # Check the first record to see its structure
    for i, (ref_hash, record) in enumerate(db.store.items()):
        if i >= 1:  # Just check first record
            break
        print(f"\n📄 First record structure:")
        print(json.dumps(record, indent=2, default=str))
    
    # Try to get all records with error handling
    try:
        records = query_manager.get_all_records()
        print(f"\n📊 Successfully retrieved {len(records)} records:")
        
        for i, record in enumerate(records, 1):
            data = record['data']
            name_or_id = data.get('name') or data.get('id') or 'N/A'
            
            print(f"\n{i}. 🔗 Ref: {record['ref']}")
            print(f"   ⏱️  Time: {record.get('timestamp_iso', 'Unknown')}")
            print(f"   🧩 Type: {record.get('type', 'unknown')}")
            if record.get('prev'):
                print(f"   🔗 Prev: {record['prev']}")
            print(f"   📄 {name_or_id}")
            
    except Exception as e:
        print(f"\n❌ Error retrieving records: {e}")
        print("\n📂 Raw database content:")
        print(json.dumps(db.store, indent=2, default=str))

def view_records_by_type(record_type: str):
    """View records of a specific type"""
    print(f"📋 Viewing all {record_type} records in the pet store database...")
    
    # Create query manager for unified data access
    query_manager = QueryManager("data/petstore_rbd.json")
    
    try:
        records = query_manager.get_records_by_type(record_type)
        print(f"\n📊 Successfully retrieved {len(records)} {record_type} records:")
        
        for i, record in enumerate(records, 1):
            data = record['data']
            name_or_id = data.get('name') or data.get('id') or 'N/A'
            
            print(f"\n{i}. 🔗 Ref: {record['ref']}")
            print(f"   ⏱️  Time: {record.get('timestamp_iso', 'Unknown')}")
            if record.get('prev'):
                print(f"   🔗 Prev: {record['prev']}")
            print(f"   📄 {name_or_id}")
            
    except Exception as e:
        print(f"\n❌ Error retrieving {record_type} records: {e}")

if __name__ == "__main__":
    view_all_records()
    
    # Also show records by type
    print("\n" + "="*50)
    query_manager = QueryManager("data/petstore_rbd.json")
    type_counts = query_manager.get_record_types()
    
    print("\n📊 Records by Type:")
    for record_type, count in type_counts.items():
        print(f"   {record_type}: {count}")
        # Show first few records of each type
        view_records_by_type(record_type)
        print()