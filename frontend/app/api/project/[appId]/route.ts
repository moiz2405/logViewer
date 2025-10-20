import { supabase } from '@/lib/db/supabaseClient';
import { NextResponse } from 'next/server';

export async function GET(
  req: Request,
  { params }: { params: Promise<{ appId: string }> }
) {
  const { appId } = await params;
  if (!appId) {
    return NextResponse.json({ error: 'Missing appId' }, { status: 400 });
  }
  const { data, error } = await supabase.from('apps').select('*').eq('id', appId).single();
  if (error || !data) {
    return NextResponse.json({ error: error?.message || 'App not found' }, { status: 404 });
  }
  return NextResponse.json(data);
}
