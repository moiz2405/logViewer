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
import { ServiceHealthCards } from "@/components/appscreen/ServiceHealthCards";
import { LogRatiosPopover } from "@/components/appscreen/LogRatiosPopover";
import { TerminalLog } from "@/components/appscreen/TerminalLog";
import { ChartAreaInteractive } from "@/components/dashboard/chart-area-interactive";
import { ResponsiveChartWrapper } from "./chartWrapper";
import { Separator } from "@/components/ui/separator";
import { ServiceDetailsPanel } from "@/components/appscreen/ServiceDetailsPanel";
import { Empty, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle } from "@/components/ui/empty";
import { IconFolderCode } from "@tabler/icons-react";

// ...inside your render, where summary is available:

export function AppScreen({ appId }: AppScreenProps) {
  const [appData, setAppData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState<any>(null);
  const [summarizing, setSummarizing] = useState(false);
  const [error, setError] = useState("");
  const [errorRates, setErrorRates] = useState<number[]>([]);
  const [avgErrorRate, setAvgErrorRate] = useState<number>(0);
  const [selectedService, setSelectedService] = useState<string | null>(null);

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
    setErrorRates([]); // Reset error rates on new monitoring
    setAvgErrorRate(0);
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
       const decoder = new TextDecoder();

        let buffer = "";
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split(/\r?\n/);
          buffer = lines.pop() || "";
          for (const line of lines) {
            if (line.trim().startsWith("data:")) {
              try {
                const jsonStr = line.replace(/^data:/, "").trim();
                const batch = JSON.parse(jsonStr);
                setSummary(batch); // Only keep the latest batch
                if (Array.isArray(batch.errors_per_10_logs)) {
                  setErrorRates((prev) => [...prev, ...batch.errors_per_10_logs]);
                }
                if (typeof batch.avg_errors_per_10_logs === "number") {
                  setAvgErrorRate(batch.avg_errors_per_10_logs);
                }
              } catch {}
            }
          }
        }
        if (buffer.trim().startsWith("data:")) {
          try {
            const jsonStr = buffer.replace(/^data:/, "").trim();
            const batch = JSON.parse(jsonStr);
            setSummary(batch);
            if (Array.isArray(batch.errors_per_10_logs)) {
              setErrorRates((prev) => [...prev, ...batch.errors_per_10_logs]);
            }
            if (typeof batch.avg_errors_per_10_logs === "number") {
              setAvgErrorRate(batch.avg_errors_per_10_logs);
            }
          } catch {}
        }
      } else {
        // Fallback: if not a stream, just set the single summary
        const data = await res.json();
        setSummary(data);
        if (Array.isArray(data.errors_per_10_logs)) {
          setErrorRates(data.errors_per_10_logs);
        }
        if (typeof data.avg_errors_per_10_logs === "number") {
          setAvgErrorRate(data.avg_errors_per_10_logs);
        }
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
        className="rounded-xl border bg-[oklch(0.205_0_0)] shadow-xl min-h-[540px]"
      >
        <ResizablePanel defaultSize={45} minSize={20}>
          <div className="relative flex flex-col h-[600px] md:h-[705px] items-start justify-start p-6 gap-4">
            {/* Always show header and button */}
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
            <h2 className="w-full text-3xl font-semibold tracking-tight text-left scroll-m-20 first:mt-0">
              Active Microservices
            </h2>
            <Separator className="my-2" />
            {/* Main content area */}
            <div className="w-full">
              <div className="flex items-center justify-end mb-2">
                {/* Show popover only when summarizing (running) */}
                {summarizing && <LogRatiosPopover />}
              </div>
              {selectedService ? (
                <div className="w-full h-full">
                  <ServiceDetailsPanel
                    service={selectedService}
                    summary={summary}
                    onBack={() => setSelectedService(null)}
                  />
                </div>
              ) : (
                <div className="flex items-center justify-center flex-1 w-full">
                  {!summarizing && !summary ? (
                    <Empty>
                      <EmptyHeader>
                        <EmptyMedia variant="icon">
                          <IconFolderCode />
                        </EmptyMedia>
                        <EmptyTitle>Start monitoring your microservices</EmptyTitle>
                        <EmptyDescription>
                          Click the button above to begin monitoring and view your microservice health and logs.
                        </EmptyDescription>
                      </EmptyHeader>
                    </Empty>
                  ) : (
                    summarizing && !summary ? (
                      <ServiceHealthCards
                        services={[]}
                        serviceHealth={{}}
                        loading={true}
                      />
                    ) : (
                      Array.isArray(summary?.services) ? (
                        <ServiceHealthCards
                          services={summary.services}
                          serviceHealth={summary.service_health}
                          onServiceClick={setSelectedService}
                        />
                      ) : null
                    )
                  )}
                </div>
              )}
            </div>
          </div>
        </ResizablePanel>
        <ResizableHandle />
        <ResizablePanel defaultSize={55} minSize={20}>
          <ResizablePanelGroup direction="vertical" className="h-full">
            <ResizablePanel defaultSize={50} minSize={10}>
              <div className="flex items-center justify-center w-full h-full p-0">
                {appData?.url && <TerminalLog url={appData.url} />}
              </div>
            </ResizablePanel>
            <ResizableHandle />
            <ResizablePanel defaultSize={50} minSize={10}>
              <div className="flex items-stretch justify-center flex-1 w-full h-full p-2">
                <ResponsiveChartWrapper>
                  <ChartAreaInteractive
                    errorRates={summary?.errors_per_10_logs || []}
                    avgErrorRate={summary?.avg_errors_per_10_logs || 0}
                  />
                </ResponsiveChartWrapper>
              </div>
            </ResizablePanel>
          </ResizablePanelGroup>
        </ResizablePanel>
      </ResizablePanelGroup>
    </div>
  );
}
