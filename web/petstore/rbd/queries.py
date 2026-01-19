# queries.py
from datetime import datetime

def get_all_records(db):
    """Get all records from the RBD database"""
    records = []
    
    for ref_hash, record in db.store.items():
        decoded_data = db._decode_data(record["data"])
        
        records.append({
            "ref": ref_hash,
            "data": decoded_data,
            "timestamp": record["ts"],
            "timestamp_iso": datetime.fromtimestamp(record["ts"]).isoformat(),
            "type": record["type"],
            "prev": record["prev"]
        })
    
    # Sort by timestamp, newest first
    records.sort(key=lambda x: x["timestamp"], reverse=True)
    return records

def get_records_by_type(db, record_type: str):
    """Get all records of a specific type"""
    return [r for r in get_all_records(db) if r["type"] == record_type]

def get_records_after(db, timestamp: int):
    """Get all records after a specific timestamp"""
    return [r for r in get_all_records(db) if r["timestamp"] > timestamp]

def print_all_records(db):
    """Print all records in a readable format"""
    records = get_all_records(db)
    
    print(f"\n📋 ALL RECORDS ({len(records)} total)")
    print("=" * 80)
    
    for i, record in enumerate(records, 1):
        print(f"\n{i}. 🔗 Ref: {record['ref']}")
        print(f"   ⏱️  Time: {record['timestamp_iso']}")
        print(f"   🧩 Type: {record['type']}")
        if record['prev']:
            print(f"   🔗 Prev: {record['prev']}")
        
        print(f"   📄 Data: {json.dumps(record['data'], indent=2, default=str)}")
    
    return records