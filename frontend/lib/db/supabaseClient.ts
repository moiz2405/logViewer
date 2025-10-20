import { createClient } from '@supabase/supabase-js'

// TODO: Replace with your actual Supabase project URL and anon key
const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || '<YOUR_SUPABASE_URL>'
const SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '<YOUR_SUPABASE_ANON_KEY>'

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)
