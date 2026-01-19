// src/app/api/stats/route.ts - API route for database statistics
import { NextResponse } from 'next/server';
import * as db from '@/lib/db';

// GET /api/stats - Get database statistics
export async function GET() {
  try {
    const stats = await db.getDatabaseStats();
    return NextResponse.json({ stats });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch statistics' }, { status: 500 });
  }
}