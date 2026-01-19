'use client';

import { useFormState, useFormStatus } from 'react-dom';
import { handleGetRecommendations } from '@/app/actions';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import ProductCard from '@/components/product-card';
import { Checkbox } from '@/components/ui/checkbox';
import { Sparkles, Bot } from 'lucide-react';
import type { Product } from '@/lib/types';

// Fetch products from our API
async function fetchProducts() {
  try {
    const res = await fetch('http://localhost:9002/api/products');
    const data = await res.json();
    return data.products || [];
  } catch (error) {
    console.error('Failed to fetch products:', error);
    return [];
  }
}

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <Button type="submit" className="w-full" disabled={pending}>
      {pending ? 'Thinking...' : <> <Sparkles className="mr-2 h-4 w-4" /> Get Recommendations</>}
    </Button>
  );
}

export default async function RecommendationForm() {
  // Fetch products for the purchase history section
  const products = await fetchProducts();
  
  const initialState = {};
  const [state, dispatch] = useFormState(handleGetRecommendations, initialState);

  const recommendedProducts =
    state?.recommendations?.recommendedProducts.map((id: string) =>
      products.find((p: Product) => p.id === id)
    ).filter(Boolean) || [];

  return (
    <div>
      <Card>
        <form action={dispatch}>
          <CardHeader>
            <CardTitle>Pet Details</CardTitle>
            <CardDescription>
              Tell us about your pet to get the best recommendations.
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-6">
            <div className="grid md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="petType">Pet Type</Label>
                <Select name="petType" required>
                  <SelectTrigger id="petType">
                    <SelectValue placeholder="Select pet type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="dog">Dog</SelectItem>
                    <SelectItem value="cat">Cat</SelectItem>
                    <SelectItem value="bird">Bird</SelectItem>
                  </SelectContent>
                </Select>
                 {state?.fieldErrors?.petType && <p className="text-sm text-destructive">{state.fieldErrors.petType.join(', ')}</p>}
              </div>
              <div className="space-y-2">
                <Label htmlFor="petBreed">Pet Breed (optional)</Label>
                <Input
                  id="petBreed"
                  name="petBreed"
                  placeholder="e.g., Golden Retriever"
                />
              </div>
            </div>
            <div className="space-y-2">
              <Label>Purchase History (optional)</Label>
              <Card className="p-4 bg-background">
                <div className="grid grid-cols-2 gap-4">
                {products.slice(0, 4).map((product: Product) => (
                    <div key={product.id} className="flex items-center space-x-2">
                    <Checkbox
                        id={`purchase-${product.id}`}
                        name="purchaseHistory"
                        value={product.id}
                    />
                    <Label
                        htmlFor={`purchase-${product.id}`}
                        className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                    >
                        {product.name}
                    </Label>
                    </div>
                ))}
                </div>
              </Card>
            </div>
          </CardContent>
          <CardFooter className="flex flex-col">
            {state?.error && <p className="text-sm text-destructive mb-4">{state.error}</p>}
            <SubmitButton />
          </CardFooter>
        </form>
      </Card>

      {state?.recommendations && (
        <div className="mt-12">
            <h2 className="text-3xl font-headline text-center mb-8">Our Recommendations</h2>
            <Card className="bg-primary/10 border-primary/30 mb-8">
                <CardHeader className="flex-row items-start gap-4">
                    <div className="bg-primary/20 p-2 rounded-full">
                        <Bot className="h-6 w-6 text-primary" />
                    </div>
                    <div>
                        <CardTitle className="mb-1 text-primary">AI Reasoning</CardTitle>
                        <CardDescription className="text-foreground/80">{state.recommendations.reasoning}</CardDescription>
                    </div>
                </CardHeader>
            </Card>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
                {recommendedProducts.map(product => product && (
                    <ProductCard key={product.id} product={product} />
                ))}
            </div>
        </div>
      )}
    </div>
  );
}
