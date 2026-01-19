from database import ReferenceBaseDB
from queries import print_all_records

db = ReferenceBaseDB("data/petstore_rbd.json")
records = print_all_records(db)