# petstore.py - Pet Store Data Model
import json
from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, EmailStr, validator
from pathlib import Path

# -------------------------------
# Pydantic Models for Validation
# -------------------------------

class Pet(BaseModel):
    id: str
    type: str  # e.g., dog, cat, bird
    breed: Optional[str] = None
    name: str
    age_months: Optional[int] = None
    gender: Optional[str] = None  # male, female
    price: Optional[float] = None
    status: str = "available"  # available, sold, in-care
    tags: List[str] = []
    created_at: Optional[str] = None
    owner_id: Optional[str] = None  # reference to customer

class Product(BaseModel):
    id: str
    name: str
    category: str  # food, toy, accessory, health
    brand: Optional[str] = None
    price: float
    cost: Optional[float] = None
    sku: str
    in_stock: int
    tags: List[str] = []

class Customer(BaseModel):
    id: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    email_address: Optional[EmailStr] = None
    transaction_ids: List[str] = []  # references to sale IDs
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    @validator('phone_number')
    def validate_phone(cls, v):
        if v is None:
            return v
        # Remove all non-digit characters
        digits = ''.join(filter(str.isdigit, v))
        if len(digits) < 10:
            raise ValueError('Phone number must have at least 10 digits')
        return v
    
    def full_name(self) -> str:
        """Return the customer's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def display_contact(self) -> str:
        """Return a formatted contact string"""
        contacts = []
        if self.email_address:
            contacts.append(self.email_address)
        if self.phone_number:
            contacts.append(self.phone_number)
        return " | ".join(contacts) if contacts else "No contact info"

class SaleItem(BaseModel):
    ref: str  # reference to product or pet
    type: str  # "product" or "pet"
    price: float
    quantity: int = 1

class Sale(BaseModel):
    id: str
    customer_id: str
    items: List[SaleItem]
    total: float
    tax: Optional[float] = None
    payment_method: str  # card, cash, online
    timestamp: str

class ServiceType:
    GROOMING = "grooming"
    VET_CHECKUP = "vet_checkup"
    TRAINING = "training"
    BOARDING = "boarding"

class Service(BaseModel):
    id: str
    pet_id: str
    type: str  # e.g., ServiceType.GROOMING
    description: str
    price: float
    scheduled_for: str  # ISO 8601 datetime
    status: str = "scheduled"  # scheduled, in-progress, completed, canceled
    notes: Optional[str] = None

# -------------------------------
# ID Generation Utilities
# -------------------------------

def generate_id(prefix: str, counter: int) -> str:
    """Generate a unique ID with prefix and counter"""
    return f"{prefix}:{str(counter).zfill(3)}"

class Counter:
    """Simple persistent counter for ID generation"""
    def __init__(self, counter_path: str = "data/petstore_counters.json"):
        self.path = Path(counter_path)
        self.counters = {"pet": 0, "product": 0, "customer": 0, "sale": 0, "service": 0}
        self.load()
        
    def load(self):
        if self.path.exists():
            try:
                self.counters = json.loads(self.path.read_text())
            except:
                self.counters = {"pet": 0, "product": 0, "customer": 0, "sale": 0, "service": 0}
    
    def save(self):
        # Ensure data directory exists
        self.path.parent.mkdir(exist_ok=True)
        self.path.write_text(json.dumps(self.counters, indent=2))
    
    def next(self, entity: str) -> int:
        self.counters[entity] += 1
        self.save()
        return self.counters[entity]

# Global counter instance
COUNTER = Counter()

# -------------------------------
# Factory Methods for Sample Data
# -------------------------------

def create_sample_pet(
    name: str,
    animal_type: str,
    breed: Optional[str] = None,
    price: float = 0.0
) -> Pet:
    """Create a pet with automatically generated ID"""
    return Pet(
        id=generate_id("pet", COUNTER.next("pet")),
        type=animal_type,
        breed=breed,
        name=name,
        price=price,
        created_at=datetime.utcnow().isoformat() + "Z"
    )

def create_sample_product(
    name: str,
    category: str,
    price: float,
    in_stock: int,
    sku: Optional[str] = None
) -> Product:
    """Create a product with automatically generated ID"""
    if not sku:
        sku = f"PROD-{str(COUNTER.next('product')).zfill(4)}"
    
    return Product(
        id=generate_id("prod", COUNTER.next("product")),
        name=name,
        category=category,
        price=price,
        in_stock=in_stock,
        sku=sku
    )

def create_sample_customer(
    first_name: str,
    last_name: str,
    phone_number: Optional[str] = None,
    email_address: Optional[str] = None
) -> Customer:
    """Create a customer with automatically generated ID"""
    return Customer(
        id=generate_id("cust", COUNTER.next("customer")),
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        email_address=email_address,
        created_at=datetime.utcnow().isoformat() + "Z",
        updated_at=datetime.utcnow().isoformat() + "Z"
    )

# -------------------------------
# Pet Store Helper Functions
# -------------------------------

def link_customer_to_sale(customer_id: str, sale_id: str, db: any) -> None:
    """Helper function to establish customer-sale relationship"""
    # In a real implementation, we'd update both customer and sale records
    print(f"Linking customer {customer_id} to sale {sale_id}")

def create_sale(customer: Customer, items: List[SaleItem]) -> Sale:
    """Create a sale transaction"""
    total = sum(item.price * item.quantity for item in items)
    
    return Sale(
        id=generate_id("sale", COUNTER.next("sale")),
        customer_id=customer.id,
        items=items,
        total=total,
        payment_method="card",
        timestamp=datetime.utcnow().isoformat() + "Z"
    )

def create_service(
    pet_id: str,
    service_type: str,
    description: str,
    price: float,
    scheduled_time: datetime
) -> Service:
    return Service(
        id=generate_id("serv", COUNTER.next("service")),
        pet_id=pet_id,
        type=service_type,
        description=description,
        price=price,
        scheduled_for=scheduled_time.isoformat() + "Z"
    )

# -------------------------------
# Data Export Utilities
# -------------------------------

def export_sample_dataset() -> Dict[str, list]:
    """Export a complete sample dataset"""
    # Create customers with proper fields
    john = create_sample_customer(
        first_name="John",
        last_name="Smith",
        phone_number="+1-555-123-4567",
        email_address="john.smith@email.com"
    )
    
    sarah = create_sample_customer(
        first_name="Sarah",
        last_name="Johnson",
        phone_number="+1-555-987-6543",
        email_address="sarah.johnson@email.com"
    )
    
    # Create pets
    buddy = create_sample_pet("Buddy", "dog", "Golden Retriever", 800)
    whiskers = create_sample_pet("Whiskers", "cat", "Siamese", 300)
    
    # Create products
    dog_food = create_sample_product(
        "Premium Dog Food", "food", 45.99, 50, "DF-PREM-20"
    )
    cat_toy = create_sample_product(
        "Laser Pointer", "toy", 9.99, 100
    )
    
    # Create services
    grooming = create_service(
        buddy.id,
        ServiceType.GROOMING,
        "Full groom package",
        75.00,
        datetime.utcnow()
    )
    
    # Create sales
    john_purchase = create_sale(john, [
        SaleItem(ref=buddy.id, type="pet", price=buddy.price),
        SaleItem(ref=dog_food.id, type="product", price=dog_food.price)
    ])
    
    # Link sale to customer
    john.transaction_ids.append(john_purchase.id)
    
    return {
        "customers": [john.dict(), sarah.dict()],
        "pets": [buddy.dict(), whiskers.dict()],
        "products": [dog_food.dict(), cat_toy.dict()],
        "services": [grooming.dict()],
        "sales": [john_purchase.dict()]
    }

if __name__ == "__main__":
    # Generate and print a sample dataset
    dataset = export_sample_dataset()
    print("✅ Pet Store Sample Dataset:")
    print(json.dumps(dataset, indent=2))