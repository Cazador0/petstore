# Morty Pet Store - Web Application

This is a fully functional web application for the Morty Pet Store, built with Next.js, TypeScript, and Deno.

## Features

- Browse pets available for adoption
- Shop for pet products
- Book premium services
- Get AI-powered product recommendations
- RESTful API for all data entities
- Database integration with in-memory storage

## Prerequisites

- Deno 1.40 or higher
- Node.js (for development tools)

## Getting Started

1. **Install dependencies:**
   ```bash
   deno install --unstable-byonm
   ```

2. **Initialize the database:**
   ```bash
   deno task init-db
   ```

3. **Run the development server:**
   ```bash
   deno task dev
   ```

4. **Build for production:**
   ```bash
   deno task build
   ```

5. **Start the production server:**
   ```bash
   deno task start
   ```

6. **Run the standalone server:**
   ```bash
   deno task server
   ```

## API Endpoints

- `GET /api/pets` - Get all pets
- `GET /api/pets?type=dog` - Get pets by type
- `POST /api/pets` - Add a new pet
- `GET /api/products` - Get all products
- `GET /api/products?category=food` - Get products by category
- `POST /api/products` - Add a new product
- `GET /api/customers` - Get all customers
- `POST /api/customers` - Add a new customer
- `GET /api/sales` - Get all sales
- `GET /api/sales?customerId=cust:001` - Get sales by customer
- `POST /api/sales` - Add a new sale
- `GET /api/services` - Get all services
- `GET /api/services?type=grooming` - Get services by type
- `POST /api/services` - Add a new service
- `GET /api/stats` - Get database statistics

## Testing

Run the API tests:
```bash
deno task test-api
```

## Project Structure

```
src/
├── app/                 # Next.js app router pages
│   ├── api/             # API routes
│   ├── pets/            # Pets page
│   ├── products/        # Products page
│   ├── services/        # Services page
│   ├── recommendations/ # AI recommendations page
│   └── page.tsx         # Home page
├── components/          # React components
├── lib/                 # Utility functions and types
└── ai/                  # AI integration
```

## Technologies Used

- Next.js 15 with App Router
- TypeScript
- Tailwind CSS
- Lucide React Icons
- Genkit AI Framework
- Deno (for package management and tasks)
- Zod (validation)

## Development

The application uses Deno for package management and task running, but Next.js for the actual web framework. This allows us to leverage the Deno ecosystem while still using Next.js for its excellent React development experience.
