"use client";

import React, { useState } from "react";
import AddApp from "../components/dashboard/addApp";
import RegisteredApps from "../components/dashboard/dashboard";

export default function Page() {
  const [apps, setApps] = useState<{ id: number; appName: string; description: string }[]>([]);

  const handleAppRegistered = (app: { id: number; appName: string; description: string }) => {
    setApps((prev) => [app, ...prev]);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-10 px-6 lg:px-8">
      {/* Pass callback to AddApp so it can push new apps */}
      <AddApp onAppRegistered={handleAppRegistered} />

      {/* Pass registered apps down to dashboard */}
      <RegisteredApps apps={apps} />
    </div>
  );
}
