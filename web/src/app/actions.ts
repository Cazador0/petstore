'use server';

import { getProductRecommendations, ProductRecommendationsInput } from '@/ai/flows/product-recommendations';
import { z } from 'zod';

const FormSchema = z.object({
  petType: z.string().min(1, 'Pet type is required.'),
  petBreed: z.string().optional(),
  purchaseHistory: z.array(z.string()),
});

type State = {
  recommendations?: {
    recommendedProducts: string[];
    reasoning: string;
  };
  error?: string;
  fieldErrors?: {
    [key: string]: string[];
  }
};

export async function handleGetRecommendations(
  prevState: State,
  formData: FormData
): Promise<State> {
  const validatedFields = FormSchema.safeParse({
    petType: formData.get('petType'),
    petBreed: formData.get('petBreed'),
    purchaseHistory: formData.getAll('purchaseHistory'),
  });

  if (!validatedFields.success) {
    return {
      error: 'Invalid form data.',
      fieldErrors: validatedFields.error.flatten().fieldErrors
    };
  }

  try {
    const recommendations = await getProductRecommendations(
      validatedFields.data as ProductRecommendationsInput
    );
    return { recommendations };
  } catch (error) {
    console.error(error);
    return {
      error: 'An unexpected error occurred while fetching recommendations.',
    };
  }
}
