"use client";

type App = {
  id: number;
  appName: string;
  description: string;
  logUrl: string;
};

type RegisteredAppsProps = {
  apps: App[];
};

export default function Dashboard({ apps }: RegisteredAppsProps) {
  return (
    <div className="max-w-5xl mx-auto mt-12 px-6 lg:px-8">
      <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">
        Registered Apps
      </h3>

      {apps.length === 0 ? (
        <p className="text-center text-gray-600">No apps registered yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {apps.map((app) => (
            <div
              key={app.id}
              className="bg-white shadow-md rounded-xl p-6 border border-gray-100 hover:shadow-lg transition"
            >
              <h4 className="text-lg font-semibold text-gray-800 mb-2">
                {app.appName}
              </h4>
              <p className="text-gray-600 text-sm mb-3">{app.description}</p>
              <a
                href={app.logUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 text-sm font-medium hover:underline"
              >
                View Logs
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
