import PetCard from "@/components/pet-card";
import type { Pet } from "@/lib/types";

// Fetch available pets from our API
async function getAvailablePets() {
  try {
    const res = await fetch('http://localhost:9002/api/pets');
    const data = await res.json();
    const pets = data.pets || [];
    return pets.filter((p: Pet) => p.status === 'available');
  } catch (error) {
    console.error('Failed to fetch pets:', error);
    return [];
  }
}

export default async function PetsPage() {
  const availablePets = await getAvailablePets();

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="text-center mb-12">
        <h1 className="text-5xl font-headline font-bold">Find a New Friend</h1>
        <p className="text-lg text-muted-foreground mt-2">Meet the adorable pets waiting for a loving home.</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
        {availablePets.map((pet: Pet) => (
          <PetCard key={pet.id} pet={pet} />
        ))}
      </div>
    </div>
  );
}
