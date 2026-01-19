import Image from 'next/image';
import type { Pet } from '@/lib/types';
import { PlaceHolderImages } from '@/lib/placeholder-images';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

type PetCardProps = {
  pet: Pet;
};

export default function PetCard({ pet }: PetCardProps) {
  const image = PlaceHolderImages.find(p => p.id === pet.image_id);

  return (
    <Card className="flex flex-col h-full overflow-hidden transition-all duration-300 hover:shadow-primary/20 hover:shadow-lg hover:-translate-y-1">
      <CardHeader className="p-0">
        <div className="relative aspect-[4/3] w-full">
            {image && (
                <Image
                    src={image.imageUrl}
                    alt={pet.name}
                    fill
                    className="object-cover"
                    sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                    data-ai-hint={image.imageHint}
                />
            )}
        </div>
      </CardHeader>
      <CardContent className="flex-grow p-4">
        <CardTitle className="text-xl font-body font-bold mb-2">{pet.name}</CardTitle>
        <p className="text-sm text-muted-foreground capitalize">{pet.breed || pet.type}</p>
        <div className="mt-2 flex flex-wrap gap-2">
            <Badge variant="outline" className="capitalize">{pet.type}</Badge>
            {pet.gender && <Badge variant="outline" className="capitalize">{pet.gender}</Badge>}
            {pet.age_months && <Badge variant="outline">{pet.age_months} months old</Badge>}
        </div>
      </CardContent>
      <CardFooter className="flex justify-between items-center p-4 pt-0">
        <p className="text-xl font-bold text-primary">${pet.price?.toFixed(2)}</p>
        <Button variant="secondary">Learn More</Button>
      </CardFooter>
    </Card>
  );
}
