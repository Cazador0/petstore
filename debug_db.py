# debug_db.py
"""Debug script to see what's actually in the database"""

from rbd.database import ReferenceBaseDB
import json

def debug_database():
    print("🔍 Debugging database contents...")
    
    # Load the database
    db = ReferenceBaseDB("data/petstore_rbd.json")
    
    print(f"📊 Total records: {len(db.store)}")
    
    # Print each record with its structure
    for i, (ref_hash, record) in enumerate(db.store.items(), 1):
        print(f"\n{i}. 🔗 Reference: {ref_hash}")
        print(f"   📄 Record keys: {list(record.keys())}")
        
        # Check if timestamp exists
        if "ts" in record:
            print(f"   ⏱️  Timestamp: {record['ts']}")
        else:
            print(f"   ⏱️  Timestamp: MISSING")
        
        # Check if type exists
        if "type" in record:
            print(f"   🧩 Type: {record['type']}")
        else:
            print(f"   🧩 Type: MISSING")
        
        # Check if prev exists
        if "prev" in record:
            print(f"   🔗 Previous: {record['prev']}")
        
        # Show data preview
        data_preview = str(record.get("data", "MISSING"))[:100]
        print(f"   📝 Data: {data_preview}...")

if __name__ == "__main__":
    debug_database()