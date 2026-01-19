// src/app/api/products/route.ts - API routes for products
import { NextResponse } from 'next/server';
import * as db from '@/lib/db';

// GET /api/products - Get all products
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const category = searchParams.get('category');
  
  try {
    if (category) {
      const products = await db.getProductsByCategory(category);
      return NextResponse.json({ products });
    } else {
      const products = await db.getAllProducts();
      return NextResponse.json({ products });
    }
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch products' }, { status: 500 });
  }
}

// POST /api/products - Add a new product
export async function POST(request: Request) {
  try {
    const productData = await request.json();
    const newProduct = await db.addProduct(productData);
    return NextResponse.json({ product: newProduct }, { status: 201 });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to add product' }, { status: 500 });
  }
}