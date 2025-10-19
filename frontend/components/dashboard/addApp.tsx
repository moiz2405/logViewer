"use client";
import { useState } from "react";

type AddAppProps = {
  onAppRegistered: (app: {
    id: number;
    appName: string;
    description: string;
    logUrl: string;
  }) => void;
};

export default function AddApp({ onAppRegistered }: AddAppProps) {
  const [appName, setAppName] = useState("");
  const [description, setDescription] = useState("");
  const [logUrl, setLogUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!appName || !description || !logUrl) {
      alert("Please fill all fields including the log URL.");
      return;
    }

    const newApp = {
      id: Date.now(),
      appName,
      description,
      logUrl,
    };

    try {
      setLoading(true);
      // TODO: send to backend `/api/apps` with JSON
      onAppRegistered(newApp);

      setAppName("");
      setDescription("");
      setLogUrl("");
    } catch (err) {
      console.error(err);
      alert("Error registering app.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-xl mx-auto bg-zinc-900 shadow-lg rounded-2xl p-8">
      <h2 className="text-3xl font-bold text-center text-zinc-100 mb-6">
        Register Your App
      </h2>

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label className="block text-sm font-medium text-zinc-300 mb-1">
            App Name
          </label>
          <input
            type="text"
            value={appName}
            onChange={(e) => setAppName(e.target.value)}
            className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter app name"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-zinc-300 mb-1">
            Description
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Brief description"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-zinc-300 mb-1">
            Log URL
          </label>
          <input
            type="url"
            value={logUrl}
            onChange={(e) => setLogUrl(e.target.value)}
            className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="https://example.com/app.log"
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-700 text-zinc-100 py-2 rounded-lg hover:bg-blue-800 transition disabled:opacity-50"
        >
          {loading ? "Registering..." : "Register App"}
        </button>
      </form>
    </div>
  );
}
