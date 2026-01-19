// src/app/api/services/route.ts - API routes for services
import { NextResponse } from 'next/server';
import * as db from '@/lib/db';

// GET /api/services - Get all services
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const type = searchParams.get('type');
  
  try {
    if (type) {
      const services = await db.getServicesByType(type);
      return NextResponse.json({ services });
    } else {
      const services = await db.getAllServices();
      return NextResponse.json({ services });
    }
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch services' }, { status: 500 });
  }
}

// POST /api/services - Add a new service
export async function POST(request: Request) {
  try {
    const serviceData = await request.json();
    const newService = await db.addService(serviceData);
    return NextResponse.json({ service: newService }, { status: 201 });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to add service' }, { status: 500 });
  }
}