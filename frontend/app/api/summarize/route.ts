import { NextResponse } from "next/server";

const BACKEND_BASE_URL = process.env.BACKEND_BASE_URL
const DEMO_BACKEND_BASE_URL = process.env.DEMO_BACKEND_BASE_URL

export async function POST(req: Request) {
  try {
    const { appId, url, batchDuration = 10, idleGap = 5 } = await req.json();
    if (!appId || !url) {
      return NextResponse.json({ error: "Missing appId or url" }, { status: 400 });
    }
    // Append /stream to the log url before sending to backend
    const logUrlWithStream = url.endsWith('/') ? `${url}logs/stream` : `${url}/logs/stream`;
    const params = new URLSearchParams({
      log_url: logUrlWithStream,
      batch_duration: batchDuration.toString(),
      idle_gap: idleGap.toString(),
    });
    const backendUrl = `${BACKEND_BASE_URL}/continuous-summary/${appId}?${params.toString()}`;
    console.log(backendUrl)
    const backendRes = await fetch(backendUrl);
    // Stream the backend response directly to the client
    const readable = backendRes.body;
    if (!readable) {
      return NextResponse.json({ error: "No stream from backend" }, { status: 500 });
    }
    return new Response(readable, {
      status: backendRes.status,
      headers: {
        'Content-Type': backendRes.headers.get('content-type') || 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || "Internal error" }, { status: 500 });
  }
}

export async function DELETE(req: Request) {
  try {
    const { appId } = await req.json();
    if (!appId) {
      return NextResponse.json({ error: "Missing appId" }, { status: 400 });
    }
    const backendUrl = `${BACKEND_BASE_URL}/stop-process/${appId}`;
    const backendRes = await fetch(backendUrl, { method: 'POST' });
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
