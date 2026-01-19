import Image from 'next/image';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import ProductCard from '@/components/product-card';
import ServiceCard from '@/components/service-card';
import PetCard from '@/components/pet-card';
import { ArrowRight, Sparkles } from 'lucide-react';
import { PlaceHolderImages } from '@/lib/placeholder-images';
import type { Product, Service, Pet } from '@/lib/types';

// Fetch data from our API
async function getFeaturedData() {
  try {
    // Fetch products
    const productsRes = await fetch('http://localhost:9002/api/products');
    const productsData = await productsRes.json();
    const products = productsData.products || [];
    
    // Fetch services
    const servicesRes = await fetch('http://localhost:9002/api/services');
    const servicesData = await servicesRes.json();
    const services = servicesData.services || [];
    
    // Fetch pets
    const petsRes = await fetch('http://localhost:9002/api/pets');
    const petsData = await petsRes.json();
    const pets = petsData.pets || [];
    
    return {
      products: products.slice(0, 4),
      services: services.slice(0, 3),
      pets: pets.filter((p: Pet) => p.status === 'available').slice(0, 4)
    };
  } catch (error) {
    console.error('Failed to fetch featured data:', error);
    return {
      products: [],
      services: [],
      pets: []
    };
  }
}

export default async function Home() {
  const { products, services, pets } = await getFeaturedData();
  const heroImage = PlaceHolderImages.find(p => p.id === 'hero');

  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="relative w-full h-[60vh] text-white flex items-center justify-center text-center">
        {heroImage && (
             <Image
                src={heroImage.imageUrl}
                alt={heroImage.description}
                fill
                className="object-cover"
                priority
                data-ai-hint={heroImage.imageHint}
              />
        )}
        <div className="absolute inset-0 bg-black/60" />
        <div className="relative z-10 max-w-4xl px-4">
          <h1 className="text-5xl md:text-7xl font-headline font-bold text-white mb-4 drop-shadow-lg">
            Luxury &amp; Love for Your Loyal Companion
          </h1>
          <p className="text-lg md:text-xl mb-8 text-gray-200 drop-shadow-md">
            Discover exclusive supplies and premium services at Royal Paws Boutique.
          </p>
          <div className="flex gap-4 justify-center">
            <Button asChild size="lg" className="font-bold">
              <Link href="/products">Shop All Products</Link>
            </Button>
            <Button asChild size="lg" variant="secondary" className="font-bold">
              <Link href="/services">Explore Services</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="py-16 md:py-24 bg-background">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-headline text-center mb-12">Featured Products</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {products.slice(0, 4).map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
          <div className="text-center mt-12">
            <Button asChild variant="link" className="text-accent-foreground text-lg">
              <Link href="/products">View All Products <ArrowRight className="ml-2 h-5 w-5" /></Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Our Services */}
      <section className="py-16 md:py-24 bg-card">
         <div className="container mx-auto px-4">
          <h2 className="text-4xl font-headline text-center mb-12">Our Services</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {services.slice(0, 3).map((service) => (
              <ServiceCard key={service.id} service={service} />
            ))}
          </div>
           <div className="text-center mt-12">
            <Button asChild variant="link" className="text-accent-foreground text-lg">
              <Link href="/services">Discover All Services <ArrowRight className="ml-2 h-5 w-5" /></Link>
            </Button>
          </div>
        </div>
      </section>
      
      {/* AI Recommendations */}
      <section className="py-16 md:py-24 bg-background">
        <div className="container mx-auto px-4 text-center">
            <Sparkles className="mx-auto h-12 w-12 text-primary mb-4" />
            <h2 className="text-4xl font-headline mb-4">Personalized For Your Pet</h2>
            <p className="max-w-2xl mx-auto text-muted-foreground mb-8">
              Let our AI assistant help you find the perfect products for your pet's unique needs. Get tailored recommendations based on their breed, age, and preferences.
            </p>
            <Button asChild size="lg" className="font-bold">
              <Link href="/recommendations">Get AI Recommendations <Sparkles className="ml-2 h-4 w-4" /></Link>
            </Button>
        </div>
      </section>

      {/* Meet Our Pets */}
      <section className="py-16 md:py-24 bg-card">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-headline text-center mb-12">Meet Our Pets</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {pets.filter(p => p.status === 'available').slice(0, 4).map((pet) => (
              <PetCard key={pet.id} pet={pet} />
            ))}
          </div>
          <div className="text-center mt-12">
            <Button asChild variant="link" className="text-accent-foreground text-lg">
              <Link href="/pets">Find Your New Best Friend <ArrowRight className="ml-2 h-5 w-5" /></Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
