// src/ai/flows/product-recommendations.ts - AI flow for product recommendations
'use server';

/**
 * @fileOverview This file defines a Genkit flow for providing personalized product recommendations based on pet type, breed, and customer purchase history.
 *
 * - getProductRecommendations - A function that retrieves personalized product recommendations.
 * - ProductRecommendationsInput - The input type for the getProductRecommendations function.
 * - ProductRecommendationsOutput - The return type for the getProductRecommendations function.
 */

import {ai} from '../genkit';
import {z} from 'genkit';

const ProductRecommendationsInputSchema = z.object({
  petType: z.string().describe('The type of pet (e.g., dog, cat, bird).'),
  petBreed: z.string().optional().describe('The breed of the pet (optional).'),
  purchaseHistory: z.array(z.string()).describe('List of product IDs representing the customer\'s past purchases.'),
});
export type ProductRecommendationsInput = z.infer<typeof ProductRecommendationsInputSchema>;

const ProductRecommendationsOutputSchema = z.object({
  recommendedProducts: z.array(z.string()).describe('List of product IDs recommended for the pet.'),
  reasoning: z.string().describe('Explanation of why these products were recommended.'),
});
export type ProductRecommendationsOutput = z.infer<typeof ProductRecommendationsOutputSchema>;

export async function getProductRecommendations(input: ProductRecommendationsInput): Promise<ProductRecommendationsOutput> {
  return productRecommendationsFlow(input);
}

const productRecommendationsPrompt = ai.definePrompt({
  name: 'productRecommendationsPrompt',
  input: {schema: ProductRecommendationsInputSchema},
  output: {schema: ProductRecommendationsOutputSchema},
  prompt: `You are an expert pet product recommendation engine. Based on the pet's type, breed, and the customer's purchase history, you will recommend relevant products.

Pet Type: {{{petType}}}
{{#if petBreed}}Pet Breed: {{{petBreed}}}{{/if}}
Purchase History: {{#each purchaseHistory}}{{{this}}}, {{/each}}

Recommend products that are relevant to the pet and their needs, and explain why these products are recommended in the reasoning field. Only return product IDs.`,
});

const productRecommendationsFlow = ai.defineFlow(
  {
    name: 'productRecommendationsFlow',
    inputSchema: ProductRecommendationsInputSchema,
    outputSchema: ProductRecommendationsOutputSchema,
  },
  async input => {
    const {output} = await productRecommendationsPrompt(input);
    return output!;
  }
);
