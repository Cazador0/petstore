import type { Pet, Product, Customer, Sale, SaleItem, Service, SampleDataSet, ServiceTypeEnum } from './types';
import { ServiceType } from './types';

// Simple counter for ID generation to mimic the Python example
const COUNTER = { pet: 0, product: 0, customer: 0, sale: 0, service: 0 };
function generate_id(prefix: keyof typeof COUNTER): string {
  COUNTER[prefix]++;
  return `${prefix}:${String(COUNTER[prefix]).padStart(3, '0')}`;
}

// Factory Methods for Sample Data
function create_sample_pet(
  name: string,
  animal_type: 'dog' | 'cat' | 'bird',
  image_id: string,
  breed?: string,
  price: number = 0.0,
  age_months?: number,
  gender?: 'male' | 'female',
): Pet {
  return {
    id: generate_id("pet"),
    type: animal_type,
    breed,
    name,
    price,
    status: "available",
    created_at: new Date().toISOString(),
    tags: [animal_type, breed || ''].filter(Boolean),
    image_id,
    age_months,
    gender,
  };
}

function create_sample_product(
  name: string,
  category: 'food' | 'toy' | 'accessory' | 'health',
  price: number,
  in_stock: number,
  image_id: string,
  sku?: string,
  brand?: string,
): Product {
  if (!sku) {
    const prefix = (brand || category).substring(0,4).toUpperCase();
    sku = `${prefix}-${String(COUNTER['product']+1).padStart(4, '0')}`;
  }
  return {
    id: generate_id("product"),
    name,
    category,
    price,
    in_stock,
    sku,
    brand,
    tags: [category, brand || ''].filter(Boolean),
    image_id,
  };
}

function create_sample_customer(
  first_name: string,
  last_name: string,
  phone_number?: string,
  email_address?: string
): Customer {
  return {
    id: generate_id("customer"),
    first_name,
    last_name,
    phone_number,
    email_address,
    transaction_ids: [],
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };
}

function create_sale(customer: Customer, items: SaleItem[], payment_method: 'card' | 'cash' | 'online' = 'card'): Sale {
  const total = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  return {
    id: generate_id("sale"),
    customer_id: customer.id,
    items,
    total,
    payment_method,
    timestamp: new Date().toISOString(),
  };
}

function create_service(
    type: ServiceTypeEnum,
    name: string,
    description: string,
    price: number,
    duration_minutes: number,
    image_id: string
): Service {
    return {
        id: generate_id('service'),
        type,
        name,
        description,
        price,
        duration_minutes,
        image_id
    }
}

// Data Export
function export_sample_dataset(): SampleDataSet {
  // Create customers
  const john = create_sample_customer("John", "Smith", "+1-555-123-4567", "john.smith@email.com");
  const sarah = create_sample_customer("Sarah", "Johnson", "+1-555-987-6543", "sarah.j@email.com");

  // Create pets
  const buddy = create_sample_pet("Buddy", "dog", "golden-retriever", "Golden Retriever", 800.00, 5, 'male');
  const whiskers = create_sample_pet("Whiskers", "cat", "siamese-cat", "Siamese", 300.00, 12, 'female');
  const sunny = create_sample_pet("Sunny", "bird", "parrot", "Sun Conure", 450.00, 24, 'male');
  const roscoe = create_sample_pet("Roscoe", "dog", "labrador", "Labrador", 750.00, 6, 'male');
  const mittens = create_sample_pet("Mittens", "cat", "persian-cat", "Persian", 500.00, 36, 'female');
  mittens.status = 'sold';
  mittens.owner_id = sarah.id;

  // Create products
  const dog_food = create_sample_product("Premium Dog Food", "food", 45.99, 50, "dog-food", "DF-PREM-20", "Royal Canin");
  const cat_toy = create_sample_product("Laser Pointer", "toy", 9.99, 100, "cat-toy", undefined, "PetSafe");
  const dog_leash = create_sample_product("Leather Leash", "accessory", 25.50, 75, "dog-leash", "DL-LTHR-01", "Gentle Leader");
  const cat_tree = create_sample_product("Cat Tree", "accessory", 120.00, 20, "cat-tree", "CT-DLX-05", "Go Pet Club");
  const fish_oil = create_sample_product("Fish Oil Supplement", "health", 19.99, 60, "dog-food", undefined, "Nordic Naturals");

  // Create services
  const grooming = create_service(ServiceType.GROOMING, "Full Groom Package", "Includes bath, haircut, nail trim, and ear cleaning.", 75.00, 120, "grooming");
  const vet_checkup = create_service(ServiceType.VET_CHECKUP, "Annual Wellness Exam", "Comprehensive health check-up with our certified veterinarian.", 150.00, 45, "vet-checkup");
  const training = create_service(ServiceType.TRAINING, "Puppy Obedience Class", "6-week course covering basic commands and socialization.", 250.00, 60, "training");
  const boarding = create_service(ServiceType.BOARDING, "Luxury Pet Boarding", "Overnight stay in a comfortable, safe environment. Price per night.", 50.00, 1440, "boarding");
  
  // Create sales
  const john_purchase = create_sale(john, [
    { ref: buddy.id, type: "pet", price: buddy.price!, quantity: 1 },
    { ref: dog_food.id, type: "product", price: dog_food.price, quantity: 2 }
  ]);
  john.transaction_ids.push(john_purchase.id);
  buddy.status = "sold";
  buddy.owner_id = john.id;

  const sarah_purchase = create_sale(sarah, [
    { ref: cat_tree.id, type: "product", price: cat_tree.price, quantity: 1 },
    { ref: cat_toy.id, type: "product", price: cat_toy.price, quantity: 3 }
  ]);
  sarah.transaction_ids.push(sarah_purchase.id);

  return {
    customers: [john, sarah],
    pets: [buddy, whiskers, sunny, roscoe, mittens],
    products: [dog_food, cat_toy, dog_leash, cat_tree, fish_oil],
    services: [grooming, vet_checkup, training, boarding],
    sales: [john_purchase, sarah_purchase]
  };
}

const data = export_sample_dataset();

export const customers = data.customers;
export const pets = data.pets;
export const products = data.products;
export const services = data.services;
export const sales = data.sales;

// Export the function itself
export { export_sample_dataset };
