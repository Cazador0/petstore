import os
from petstore import export_sample_dataset
from rbd.database import ReferenceBaseDB
from rbd.query import QueryManager

def load_sample_data():
    print("🚀 Initializing pet store database with sample data...")
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Create query manager for unified data access
    query_manager = QueryManager("data/petstore_rbd.json")
    
    # Get the complete sample dataset
    dataset = export_sample_dataset()
    
    # Load each entity type
    total_added = 0
    for entity_type, entities in dataset.items():
        print(f"📦 Adding {len(entities)} {entity_type}...")
        for entity in entities:
            try:
                # Use the entity's name or description as text hint
                name = entity.get('name') or entity.get('id') or entity_type
                text_hint = f"Sample {entity_type}: {name}"
                
                ref = query_manager.add_record(entity, text_hint=text_hint)
                total_added += 1
                print(f"  ✅ Added: {entity_type} {entity['id']} ({ref})")
                
            except Exception as e:
                print(f"  ❌ Failed to add {entity_type} {entity.get('id', 'unknown')}: {e}")
                import traceback
                traceback.print_exc()
    
    print(f"🎉 Successfully added {total_added} records to the database!")
    print(f"💾 Database saved at: data/petstore_rbd.json")
    
    # Show summary of loaded data
    print("\n📊 Database Summary:")
    records = query_manager.get_all_records()
    print(f"   Total records: {len(records)}")
    
    # Group by type
    type_counts = query_manager.get_record_types()
    
    for record_type, count in type_counts.items():
        print(f"   {record_type}: {count}")

if __name__ == "__main__":
    load_sample_data()