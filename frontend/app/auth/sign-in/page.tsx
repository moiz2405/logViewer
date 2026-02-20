"use client";

import { useSearchParams } from "next/navigation";
import { LoginForm } from "@/components/auth/login-form";

export default function LoginPage() {
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get("callbackUrl") || "/";

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-zinc-900 via-zinc-800 to-zinc-900 text-zinc-100">
      <div className="w-full max-w-lg">
        <LoginForm callbackUrl={callbackUrl} />
      </div>
    </div>
  );
}
