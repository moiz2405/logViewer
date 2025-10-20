"use client"

import { useSession } from "next-auth/react"
import React, { useState } from "react"
import { IconCirclePlusFilled } from "@tabler/icons-react"
import { Button } from "@/components/ui/button"
import {
  Field,
  FieldGroup,
  FieldLabel,
  FieldSet,
  FieldLegend,
  FieldDescription,
  FieldSeparator,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { toast } from "sonner"
import {
  Item,
  ItemContent,
  ItemMedia,
  ItemTitle,
} from "@/components/ui/item"
import { Spinner } from "@/components/ui/spinner"

export function AddAppContent() {
  const { data: session } = useSession()
  const [name, setName] = useState("")
  const [description, setDescription] = useState("")
  const [url, setUrl] = useState("")
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState("")

  const isUrlValid =
    url.trim().startsWith("http://localhost") || url.trim().startsWith("https://")
  const isFormValid = name.trim() !== "" && url.trim() !== "" && isUrlValid

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError("")
    setSuccess(false)
    try {
      // Check for duplicate app URL for this user
      let duplicate = false
      let checked = false
      try {
        const checkRes = await fetch(`/api/project?user_id=${session?.user?.id}`)
        if (checkRes.ok) {
          const existingApps = await checkRes.json()
          duplicate = existingApps.some((app: any) => (app.url?.trim().toLowerCase() === url.trim().toLowerCase()))
          checked = true
        }
      } catch {
        toast.error("Could not check for duplicates. Please try again.")
        setLoading(false)
        return
      }
      if (checked && duplicate) {
        toast.error("Project already exists")
        setLoading(false)
        return
      }
      const appUrl = url.trim() === "" ? "user's app" : url
      const res = await fetch("/api/project", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: session?.user?.id,
          name,
          description,
          url: appUrl,
        }),
      })
      if (!res.ok) throw new Error((await res.json()).error || "Failed to add app")
      setSuccess(true)
      setName("")
      setDescription("")
      setUrl("")
      toast.success("App registered successfully!")
    } catch (err: any) {
      setError(err.message)
      toast.error(`${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center flex-1 px-6 py-10 bg-gradient-to-b from-black via-zinc-950 to-black">
      <div
        className="w-full max-w-2xl p-8 rounded-2xl border border-zinc-800/60 
        bg-gradient-to-t from-primary/5 to-zinc-900/80 
        shadow-[0_0_20px_-4px_rgba(0,0,0,0.4)] backdrop-blur-xl
        transition-all duration-300 hover:shadow-[0_0_35px_-8px_rgba(59,130,246,0.3)]"
      >
        <div className="flex flex-col items-center gap-3 mb-6 text-center">
          <h2 className="text-3xl font-bold tracking-tight text-zinc-100">
            Register Your App
          </h2>
        </div>
        {loading ? (
          <div className="flex flex-col w-full max-w-xs gap-4 mx-auto">
            <Item variant="muted">
              <ItemMedia>
                <Spinner />
              </ItemMedia>
              <ItemContent>
                <ItemTitle className="line-clamp-1">Registering app...</ItemTitle>
              </ItemContent>
            </Item>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-8">
            <FieldGroup>
              <FieldSet>
                <FieldLegend className="text-lg font-semibold text-zinc-200">
                  Application Details
                </FieldLegend>
                <FieldDescription className="mb-4 text-sm text-zinc-400">
                  Provide information about your app and its logging endpoint.
                </FieldDescription>

                <FieldGroup className="space-y-5">
                  <Field>
                    <FieldLabel htmlFor="app-name">App Name</FieldLabel>
                    <Input
                      id="app-name"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      placeholder="Enter app name"
                      required
                      autoComplete="off"
                      className="transition-all bg-zinc-800/70 text-zinc-100 border-zinc-700 placeholder-zinc-500 focus-visible:ring-2 focus-visible:ring-primary/40 rounded-xl"
                    />
                  </Field>

                  <Field>
                    <FieldLabel htmlFor="app-url">App URL</FieldLabel>
                    <Input
                      id="app-url"
                      type="url"
                      value={url}
                      onChange={(e) => setUrl(e.target.value)}
                      placeholder="https://example.com/app"
                      autoComplete="off"
                      required
                      className="transition-all bg-zinc-800/70 text-zinc-100 border-zinc-700 placeholder-zinc-500 focus-visible:ring-2 focus-visible:ring-primary/40 rounded-xl"
                    />
                  </Field>

                  <Field>
                    <FieldLabel htmlFor="app-desc">Description (optional)</FieldLabel>
                    <Textarea
                      id="app-desc"
                      value={description}
                      onChange={(e) => setDescription(e.target.value)}
                      placeholder="Brief description"
                      className="transition-all resize-none bg-zinc-800/70 text-zinc-100 border-zinc-700 placeholder-zinc-500 focus-visible:ring-2 focus-visible:ring-primary/40 rounded-xl"
                      rows={3}
                    />
                  </Field>
                </FieldGroup>
              </FieldSet>

              <FieldSeparator />

              <Field className="flex-row items-center gap-4 mt-4">
                <Button
                  type="submit"
                  disabled={!isFormValid || loading}
                  className={`w-full py-2 rounded-xl bg-primary text-primary-foreground font-semibold transition-all duration-200 hover:shadow-lg hover:scale-[1.02] disabled:opacity-50 focus-visible:ring-2 focus-visible:ring-primary/40 ${isFormValid ? '' : 'pointer-events-none'}`}
                >
                  {loading ? "Registering..." : "Register App"}
                </Button>
              </Field>
            </FieldGroup>
          </form>
        )}
      </div>
    </div>
  )
}
