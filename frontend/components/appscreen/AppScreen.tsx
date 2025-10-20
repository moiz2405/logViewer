"use client";
import React, { useEffect, useState } from "react";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";

interface AppScreenProps {
  appId: string;
}

export function AppScreen({ appId }: AppScreenProps) {
  const [appData, setAppData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState<any>(null);
  const [summarizing, setSummarizing] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    setError("");
    fetch(`/api/project/${appId}`)
      .then((res) => res.json())
      .then((data) => setAppData(data))
      .catch((err) => setError("Failed to fetch app details"))
      .finally(() => setLoading(false));
  }, [appId]);

  async function handleSummarize() {
    if (!appData?.url) return;
    setSummarizing(true);
    setError("");
    setSummary(null); // Clear previous summary
    try {
      const res = await fetch("/api/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          appId,
          url: appData.url,
          batchDuration: 10,
          idleGap: 5,
        }),
      });
      if (!res.ok) throw new Error("Failed to summarize");
      const reader = res.body?.getReader();
      if (reader) {
        let decoder = new TextDecoder();
        let buffer = "";
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });
          let lines = buffer.split(/\r?\n/);
          buffer = lines.pop() || "";
          for (const line of lines) {
            if (line.trim().startsWith("data:")) {
              try {
                const jsonStr = line.replace(/^data:/, "").trim();
                const batch = JSON.parse(jsonStr);
                setSummary(batch); // Only keep the latest batch
              } catch {}
            }
          }
        }
        if (buffer.trim().startsWith("data:")) {
          try {
            const jsonStr = buffer.replace(/^data:/, "").trim();
            const batch = JSON.parse(jsonStr);
            setSummary(batch);
          } catch {}
        }
      } else {
        // Fallback: if not a stream, just set the single summary
        const data = await res.json();
        setSummary(data);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSummarizing(false);
    }
  }

  return (
    <div className="w-full max-w-[1440px] px-2">
      <ResizablePanelGroup
        direction="horizontal"
        className="rounded-xl border bg-zinc-900/80 shadow-xl min-h-[540px]"
      >
        <ResizablePanel defaultSize={45} minSize={20}>
          <div className="relative flex flex-col h-[500px] md:h-[600px] items-center justify-center p-6 gap-4">
            {!summarizing ? (
              <button
                className="absolute z-10 px-4 py-2 font-semibold transition shadow top-6 right-6 rounded-xl bg-primary text-primary-foreground hover:scale-105 disabled:opacity-50"
                onClick={handleSummarize}
                disabled={summarizing}
              >
                Start Monitoring
              </button>
            ) : (
              <button
                className="absolute z-10 px-4 py-2 font-semibold text-white transition bg-red-600 shadow top-6 right-6 rounded-xl hover:scale-105 disabled:opacity-50"
                onClick={async () => {
                  try {
                    await fetch("/api/summarize", {
                      method: "DELETE",
                      headers: { "Content-Type": "application/json" },
                      body: JSON.stringify({ appId }),
                    });
                    setSummarizing(false);
                  } catch (err: any) {
                    setError("Failed to stop monitoring");
                  }
                }}
                disabled={!summarizing}
              >
                Stop Monitoring
              </button>
            )}
            {loading ? (
              <span className="text-zinc-400">Loading app details...</span>
            ) : error ? (
              <span className="text-red-500">{error}</span>
            ) : appData ? (
              <>
                <span className="font-semibold">App Name: {appData.name}</span>
                <span className="font-mono text-xs text-zinc-400">
                  App ID: {appId}
                </span>
                <span className="text-zinc-400">URL: {appData.url}</span>
                {summary && (
                  <div className="w-full p-2 mt-4 overflow-auto text-xs text-left rounded max-h-80 bg-zinc-900/60">
                    <pre className="break-words whitespace-pre-wrap">
                      {JSON.stringify(summary, null, 2)}
                    </pre>
                  </div>
                )}
              </>
            ) : null}
          </div>
        </ResizablePanel>
        <ResizableHandle />
        <ResizablePanel defaultSize={55} minSize={20}>
          <ResizablePanelGroup direction="vertical" className="h-full">
            <ResizablePanel defaultSize={50} minSize={10}>
              <div className="flex items-center justify-center h-full p-6">
                <span className="font-semibold">Panel Two</span>
              </div>
            </ResizablePanel>
            <ResizableHandle />
            <ResizablePanel defaultSize={50} minSize={10}>
              <div className="flex items-center justify-center h-full p-6">
                <span className="font-semibold">Panel Three</span>
              </div>
            </ResizablePanel>
          </ResizablePanelGroup>
        </ResizablePanel>
      </ResizablePanelGroup>
    </div>
  );
}
