// src/app/api/sales/route.ts - API routes for sales
import { NextResponse } from 'next/server';
import * as db from '@/lib/db';

// GET /api/sales - Get all sales
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const customerId = searchParams.get('customerId');
  
  try {
    if (customerId) {
      const sales = await db.getSalesByCustomerId(customerId);
      return NextResponse.json({ sales });
    } else {
      const sales = await db.getAllSales();
      return NextResponse.json({ sales });
    }
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch sales' }, { status: 500 });
  }
}

// POST /api/sales - Add a new sale
export async function POST(request: Request) {
  try {
    const saleData = await request.json();
    const newSale = await db.addSale(saleData);
    return NextResponse.json({ sale: newSale }, { status: 201 });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to add sale' }, { status: 500 });
  }
}