import { PawPrint } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-border/40 bg-background/95">
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col md:flex-row justify-between items-center text-center md:text-left">
          <div className="flex items-center gap-2 mb-4 md:mb-0">
             <PawPrint className="h-5 w-5 text-primary" />
             <p className="text-sm text-muted-foreground">&copy; {new Date().getFullYear()} Royal Paws Boutique. All rights reserved.</p>
          </div>
          <p className="text-sm text-muted-foreground">Crafted with love for the finest pets.</p>
        </div>
      </div>
    </footer>
  );
}
