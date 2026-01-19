import RecommendationForm from './recommendation-form';

export default function RecommendationsPage() {
  return (
    <div className="container mx-auto max-w-3xl px-4 py-12">
      <div className="text-center mb-12">
        <h1 className="text-5xl font-headline font-bold">AI Product Advisor</h1>
        <p className="text-lg text-muted-foreground mt-2">
          Get personalized product recommendations for your pet.
        </p>
      </div>
      <RecommendationForm />
    </div>
  );
}
