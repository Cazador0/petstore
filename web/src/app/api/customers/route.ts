// src/app/api/customers/route.ts - API routes for customers
import { NextResponse } from 'next/server';
import * as db from '@/lib/db';

// GET /api/customers - Get all customers
export async function GET() {
  try {
    const customers = await db.getAllCustomers();
    return NextResponse.json({ customers });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch customers' }, { status: 500 });
  }
}

// POST /api/customers - Add a new customer
export async function POST(request: Request) {
  try {
    const customerData = await request.json();
    const newCustomer = await db.addCustomer(customerData);
    return NextResponse.json({ customer: newCustomer }, { status: 201 });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to add customer' }, { status: 500 });
  }
}