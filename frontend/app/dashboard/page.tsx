"use client";

import React, { useState } from "react";
import AddApp from "../components/dashboard/addApp";
import RegisteredApps from "../components/dashboard/dashboard";

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
    <div className="min-h-screen bg-gray-50 pt-24 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl w-full mx-auto">
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
