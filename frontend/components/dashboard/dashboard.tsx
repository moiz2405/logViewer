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
      <h3 className="text-2xl font-bold text-zinc-100 mb-6 text-center">
        Registered Apps
      </h3>

      {apps.length === 0 ? (
        <p className="text-center text-zinc-400">No apps registered yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {apps.map((app) => (
            <div
              key={app.id}
              className="bg-zinc-900 shadow-md rounded-xl p-6 border border-zinc-800 hover:shadow-lg transition"
            >
              <h4 className="text-lg font-semibold text-zinc-200 mb-2">
                {app.appName}
              </h4>
              <p className="text-zinc-400 text-sm mb-3">{app.description}</p>
              <a
                href={app.logUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 text-sm font-medium hover:underline"
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
