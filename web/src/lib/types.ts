export interface Pet {
  id: string;
  type: 'dog' | 'cat' | 'bird' | string;
  breed?: string;
  name: string;
  age_months?: number;
  gender?: 'male' | 'female';
  price?: number;
  status: 'available' | 'sold' | 'in-care';
  tags: string[];
  created_at?: string;
  owner_id?: string;
  image_id: string;
}

export interface Product {
  id: string;
  name: string;
  category: 'food' | 'toy' | 'accessory' | 'health' | string;
  brand?: string;
  price: number;
  cost?: number;
  sku: string;
  in_stock: number;
  tags: string[];
  image_id: string;
}

export interface Customer {
  id: string;
  first_name: string;
  last_name: string;
  phone_number?: string;
  email_address?: string;
  transaction_ids: string[];
  created_at?: string;
  updated_at?: string;
}

export interface SaleItem {
  ref: string; // reference to product or pet
  type: 'product' | 'pet';
  price: number;
  quantity: number;
}

export interface Sale {
  id: string;
  customer_id: string;
  items: SaleItem[];
  total: number;
  tax?: number;
  payment_method: 'card' | 'cash' | 'online';
  timestamp: string;
}

export const ServiceType = {
  GROOMING: "grooming",
  VET_CHECKUP: "vet_checkup",
  TRAINING: "training",
  BOARDING: "boarding",
} as const;

export type ServiceTypeEnum = typeof ServiceType[keyof typeof ServiceType];

export interface Service {
  id: string;
  type: ServiceTypeEnum;
  name: string;
  description: string;
  price: number;
  duration_minutes: number;
  image_id: string;
}

// Sample data structure
export interface SampleDataSet {
  customers: Customer[];
  pets: Pet[];
  products: Product[];
  services: Service[];
  sales: Sale[];
}
