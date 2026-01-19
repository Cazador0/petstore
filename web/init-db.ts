// init-db.ts - Initialize the database with sample data
import { export_sample_dataset } from './src/lib/data';
import * as db from './src/lib/db';

async function initializeDatabase() {
  console.log('Initializing database with sample data...');
  
  try {
    // Get the sample dataset
    const dataset = export_sample_dataset();
    
    // Add all pets to the database
    console.log('Adding pets to database...');
    for (const pet of dataset.pets) {
      await db.addPet(pet);
    }
    
    // Add all products to the database
    console.log('Adding products to database...');
    for (const product of dataset.products) {
      await db.addProduct(product);
    }
    
    // Add all customers to the database
    console.log('Adding customers to database...');
    for (const customer of dataset.customers) {
      await db.addCustomer(customer);
    }
    
    // Add all services to the database
    console.log('Adding services to database...');
    for (const service of dataset.services) {
      await db.addService(service);
    }
    
    // Add all sales to the database
    console.log('Adding sales to database...');
    for (const sale of dataset.sales) {
      await db.addSale(sale);
    }
    
    // Get database statistics
    const stats = await db.getDatabaseStats();
    console.log('Database initialized successfully!');
    console.log('Database statistics:', stats);
  } catch (error) {
    console.error('Failed to initialize database:', error);
  }
}

// Run the initialization
if (import.meta.main) {
  await initializeDatabase();
}