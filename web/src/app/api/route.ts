// src/app/api/route.ts - API routes for the pet store
import { NextResponse } from 'next/server';
import * as db from '@/lib/db';

// GET /api/pets - Get all pets
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const type = searchParams.get('type');
  
  try {
    if (type) {
      const pets = await db.getPetsByType(type);
      return NextResponse.json({ pets });
    } else {
      const pets = await db.getAllPets();
      return NextResponse.json({ pets });
    }
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch pets' }, { status: 500 });
  }
}

// POST /api/pets - Add a new pet
export async function POST(request: Request) {
  try {
    const petData = await request.json();
    const newPet = await db.addPet(petData);
    return NextResponse.json({ pet: newPet }, { status: 201 });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to add pet' }, { status: 500 });
  }
}