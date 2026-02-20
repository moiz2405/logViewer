import { NextResponse } from "next/server";

const BACKEND_BASE_URL = process.env.BACKEND_BASE_URL || "http://localhost:8001";
const DEMO_BACKEND_BASE_URL = process.env.DEMO_BACKEND_BASE_URL || "http://localhost:8000";

export async function GET(req: Request) {
  try {
    const { searchParams } = new URL(req.url);
    const appId = searchParams.get("appId");
    if (!appId) {
      return NextResponse.json({ error: "Missing appId" }, { status: 400 });
    }
    const backendUrl = `${BACKEND_BASE_URL}/summary/${appId}`;
    const backendRes = await fetch(backendUrl);
    const data = await backendRes.json();
    return NextResponse.json(data, { status: backendRes.status });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || "Internal error" }, { status: 500 });
  }
}

export async function PUT(req: Request) {
  try {
    const { api, auth, inventory, notification, payment } = await req.json();
    if ([api, auth, inventory, notification, payment].some(v => v === undefined)) {
      return NextResponse.json({ error: "Missing one or more required fields" }, { status: 400 });
    }
    const backendUrl = `${DEMO_BACKEND_BASE_URL}/logs/ratios`;
    const backendRes = await fetch(backendUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ api, auth, inventory, notification, payment })
    });
    const data = await backendRes.json();
    return NextResponse.json(data, { status: backendRes.status });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || "Internal error" }, { status: 500 });
  }
}
