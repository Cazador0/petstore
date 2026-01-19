// test-api.ts - Test the API endpoints
async function testAPI() {
  console.log('Testing API endpoints...');
  
  try {
    // Test pets endpoint
    console.log('\nTesting /api/pets endpoint...');
    const petsRes = await fetch('http://localhost:9002/api/pets');
    const petsData = await petsRes.json();
    console.log(`Found ${petsData.pets?.length || 0} pets`);
    
    // Test products endpoint
    console.log('\nTesting /api/products endpoint...');
    const productsRes = await fetch('http://localhost:9002/api/products');
    const productsData = await productsRes.json();
    console.log(`Found ${productsData.products?.length || 0} products`);
    
    // Test customers endpoint
    console.log('\nTesting /api/customers endpoint...');
    const customersRes = await fetch('http://localhost:9002/api/customers');
    const customersData = await customersRes.json();
    console.log(`Found ${customersData.customers?.length || 0} customers`);
    
    // Test services endpoint
    console.log('\nTesting /api/services endpoint...');
    const servicesRes = await fetch('http://localhost:9002/api/services');
    const servicesData = await servicesRes.json();
    console.log(`Found ${servicesData.services?.length || 0} services`);
    
    // Test stats endpoint
    console.log('\nTesting /api/stats endpoint...');
    const statsRes = await fetch('http://localhost:9002/api/stats');
    const statsData = await statsRes.json();
    console.log('Database statistics:', statsData.stats);
    
    console.log('\nAll API tests completed successfully!');
  } catch (error) {
    console.error('API test failed:', error);
  }
}

// Run the tests
if (import.meta.main) {
  await testAPI();
}