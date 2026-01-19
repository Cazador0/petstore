import ProductCard from "@/components/product-card";
import type { Product } from "@/lib/types";

// Fetch products from our API
async function getProducts() {
  try {
    const res = await fetch('http://localhost:9002/api/products');
    const data = await res.json();
    return data.products || [];
  } catch (error) {
    console.error('Failed to fetch products:', error);
    return [];
  }
}

export default async function ProductsPage() {
  const products = await getProducts();

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="text-center mb-12">
        <h1 className="text-5xl font-headline font-bold">Our Products</h1>
        <p className="text-lg text-muted-foreground mt-2">Everything your royal companion desires.</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
        {products.map((product: Product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
}
