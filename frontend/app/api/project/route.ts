import { supabase } from '@/lib/db/supabaseClient';

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const user_id = searchParams.get('user_id');
  if (!user_id) return new Response(JSON.stringify({ error: 'Missing user_id' }), { status: 400 });
  const { data, error } = await supabase.from('apps').select('*').eq('user_id', user_id);
  if (error) return new Response(JSON.stringify({ error }), { status: 500 });
  return new Response(JSON.stringify(data), { status: 200 });
}

export async function POST(req: Request) {
  const body = await req.json();
  const { user_id, name, description, url } = body;
  if (!user_id || !name) return new Response(JSON.stringify({ error: 'Missing required fields' }), { status: 400 });
  const { data, error } = await supabase.from('apps').insert([{ user_id, name, description, url }]).select();
  if (error) return new Response(JSON.stringify({ error }), { status: 500 });
  return new Response(JSON.stringify(data[0]), { status: 201 });
}

export async function DELETE(req: Request) {
  const body = await req.json();
  const { app_id } = body;
  if (!app_id) return new Response(JSON.stringify({ error: 'Missing app_id' }), { status: 400 });
  const { error } = await supabase.from('apps').delete().eq('id', app_id);
  if (error) return new Response(JSON.stringify({ error }), { status: 500 });
  return new Response(JSON.stringify({ success: true }), { status: 200 });
}

// Usage
// const userId = "USER_ID_HERE";
// const res = await fetch(`/api/project?user_id=${userId}`);
// const apps = await res.json();

// const res = await fetch('/api/project', {
//   method: 'POST',
//   headers: { 'Content-Type': 'application/json' },
//   body: JSON.stringify({
//     user_id: "USER_ID_HERE",
//     name: "App Name",
//     description: "App Description",
//     url: "https://yourapp.com"
//   })
// });

// const newApp = await res.json();
// const res = await fetch('/api/project', {
//   method: 'DELETE',
//   headers: { 'Content-Type': 'application/json' },
//   body: JSON.stringify({ app_id: "APP_ID_HERE" })
// });
// const result = await res.json();