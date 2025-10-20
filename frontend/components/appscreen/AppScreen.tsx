import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";

interface AppScreenProps {
  appId: string;
}

export function AppScreen({ appId }: AppScreenProps) {
  // Panel 1 takes 40%, Panels 2+3 take 60% (vertically split)
  return (
    <div className="w-full max-w-[1440px] px-2">
      <ResizablePanelGroup
        direction="horizontal"
        className="rounded-xl border bg-zinc-900/80 shadow-xl min-h-[540px]"
      >
        <ResizablePanel defaultSize={45} minSize={20}>
          <div className="flex h-[500px] md:h-[600px] items-center justify-center p-6">
            <span className="font-semibold">App ID: {appId}</span>
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
