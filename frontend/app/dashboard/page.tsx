"use client";

import React, { useState } from "react";
import AddApp from "../../components/dashboard/addApp";
import RegisteredApps from "../../components/dashboard/dashboard";

export default function Page() {
  const [apps, setApps] = useState<
    { id: number; appName: string; description: string }[]
  >([]);

  const handleAppRegistered = (app: {
    id: number;
    appName: string;
    description: string;
  }) => {
    setApps((prev) => [app, ...prev]);
  };

  return (
    <div className="min-h-screen px-4 pt-24 bg-zinc-900 text-zinc-100 sm:px-6 lg:px-8">
      <div className="w-full max-w-4xl mx-auto">
        {/* AddApp form */}
        <AddApp onAppRegistered={handleAppRegistered} />

        {/* Registered Apps */}
        <div className="mt-12">
          <RegisteredApps apps={apps} />
        </div>
      </div>
    </div>
  );
}
