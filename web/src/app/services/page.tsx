import ServiceCard from "@/components/service-card";
import type { Service } from "@/lib/types";

// Fetch services from our API
async function getServices() {
  try {
    const res = await fetch('http://localhost:9002/api/services');
    const data = await res.json();
    return data.services || [];
  } catch (error) {
    console.error('Failed to fetch services:', error);
    return [];
  }
}

export default async function ServicesPage() {
  const services = await getServices();

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="text-center mb-12">
        <h1 className="text-5xl font-headline font-bold">Premium Services</h1>
        <p className="text-lg text-muted-foreground mt-2">Expert care for your cherished pet.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {services.map((service: Service) => (
          <ServiceCard key={service.id} service={service} />
        ))}
      </div>
    </div>
  );
}
