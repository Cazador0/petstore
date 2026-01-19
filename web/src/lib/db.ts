// db.ts - Database integration for the web application
import { customers, pets, products, services, sales } from './data.ts';
import type { Pet, Product, Customer, Sale, Service } from './types.ts';

// In-memory database (simulating the RBD database)
let db: {
  pets: Pet[];
  products: Product[];
  customers: Customer[];
  sales: Sale[];
  services: Service[];
} = {
  pets: [...pets],
  products: [...products],
  customers: [...customers],
  sales: [...sales],
  services: [...services]
};

// Database operations
export async function getAllPets(): Promise<Pet[]> {
  return db.pets;
}

export async function getPetById(id: string): Promise<Pet | undefined> {
  return db.pets.find(pet => pet.id === id);
}

export async function getPetsByType(type: string): Promise<Pet[]> {
  return db.pets.filter(pet => pet.type === type);
}

export async function getAllProducts(): Promise<Product[]> {
  return db.products;
}

export async function getProductById(id: string): Promise<Product | undefined> {
  return db.products.find(product => product.id === id);
}

export async function getProductsByCategory(category: string): Promise<Product[]> {
  return db.products.filter(product => product.category === category);
}

export async function getAllCustomers(): Promise<Customer[]> {
  return db.customers;
}

export async function getCustomerById(id: string): Promise<Customer | undefined> {
  return db.customers.find(customer => customer.id === id);
}

export async function getAllSales(): Promise<Sale[]> {
  return db.sales;
}

export async function getSaleById(id: string): Promise<Sale | undefined> {
  return db.sales.find(sale => sale.id === id);
}

export async function getSalesByCustomerId(customerId: string): Promise<Sale[]> {
  return db.sales.filter(sale => sale.customer_id === customerId);
}

export async function getAllServices(): Promise<Service[]> {
  return db.services;
}

export async function getServiceById(id: string): Promise<Service | undefined> {
  return db.services.find(service => service.id === id);
}

export async function getServicesByType(type: string): Promise<Service[]> {
  return db.services.filter(service => service.type === type);
}

// Add a new pet to the database
export async function addPet(pet: Omit<Pet, 'id'>): Promise<Pet> {
  const newPet: Pet = {
    ...pet,
    id: `pet:${String(db.pets.length + 1).padStart(3, '0')}`
  };
  db.pets.push(newPet);
  return newPet;
}

// Add a new product to the database
export async function addProduct(product: Omit<Product, 'id'>): Promise<Product> {
  const newProduct: Product = {
    ...product,
    id: `prod:${String(db.products.length + 1).padStart(3, '0')}`
  };
  db.products.push(newProduct);
  return newProduct;
}

// Add a new customer to the database
export async function addCustomer(customer: Omit<Customer, 'id' | 'transaction_ids' | 'created_at' | 'updated_at'>): Promise<Customer> {
  const newCustomer: Customer = {
    ...customer,
    id: `cust:${String(db.customers.length + 1).padStart(3, '0')}`,
    transaction_ids: [],
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };
  db.customers.push(newCustomer);
  return newCustomer;
}

// Add a new sale to the database
export async function addSale(sale: Omit<Sale, 'id' | 'timestamp'>): Promise<Sale> {
  const newSale: Sale = {
    ...sale,
    id: `sale:${String(db.sales.length + 1).padStart(3, '0')}`,
    timestamp: new Date().toISOString()
  };
  db.sales.push(newSale);
  
  // Update customer's transaction history
  const customer = db.customers.find(c => c.id === sale.customer_id);
  if (customer) {
    customer.transaction_ids.push(newSale.id);
    customer.updated_at = new Date().toISOString();
  }
  
  return newSale;
}

// Add a new service to the database
export async function addService(service: Omit<Service, 'id'>): Promise<Service> {
  const newService: Service = {
    ...service,
    id: `serv:${String(db.services.length + 1).padStart(3, '0')}`
  };
  db.services.push(newService);
  return newService;
}

// Update a pet's status (e.g., when sold)
export async function updatePetStatus(petId: string, status: Pet['status'], ownerId?: string): Promise<Pet | undefined> {
  const pet = db.pets.find(p => p.id === petId);
  if (pet) {
    pet.status = status;
    if (ownerId) {
      pet.owner_id = ownerId;
    }
    return pet;
  }
  return undefined;
}

// Get database statistics
export async function getDatabaseStats() {
  return {
    totalPets: db.pets.length,
    totalProducts: db.products.length,
    totalCustomers: db.customers.length,
    totalSales: db.sales.length,
    totalServices: db.services.length,
    availablePets: db.pets.filter(pet => pet.status === 'available').length,
    soldPets: db.pets.filter(pet => pet.status === 'sold').length,
  };
}