import Image from 'next/image';
import type { Service } from '@/lib/types';
import { PlaceHolderImages } from '@/lib/placeholder-images';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Clock } from 'lucide-react';

type ServiceCardProps = {
  service: Service;
};

export default function ServiceCard({ service }: ServiceCardProps) {
  const image = PlaceHolderImages.find(p => p.id === service.image_id);

  return (
    <Card className="flex flex-col h-full overflow-hidden transition-all duration-300 hover:shadow-primary/20 hover:shadow-lg hover:-translate-y-1">
      <CardHeader className="p-0">
        <div className="relative aspect-[4/3] w-full">
            {image && (
                <Image
                    src={image.imageUrl}
                    alt={service.name}
                    fill
                    className="object-cover"
                    sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                    data-ai-hint={image.imageHint}
                />
            )}
        </div>
      </CardHeader>
      <CardContent className="flex-grow p-4">
        <Badge variant="secondary" className="mb-2 capitalize">{service.type.replace('_', ' ')}</Badge>
        <CardTitle className="text-xl font-body font-bold mb-2">{service.name}</CardTitle>
        <p className="text-sm text-muted-foreground h-20">{service.description}</p>
        <div className="flex items-center text-sm text-muted-foreground mt-4">
            <Clock className="h-4 w-4 mr-2" />
            <span>{service.duration_minutes} minutes</span>
        </div>
      </CardContent>
      <CardFooter className="flex justify-between items-center p-4 pt-0">
        <p className="text-xl font-bold text-primary">${service.price.toFixed(2)}</p>
        <Button>Book Now</Button>
      </CardFooter>
    </Card>
  );
}
