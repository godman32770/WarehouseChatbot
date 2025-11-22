import type React from "react"
import { Navigation } from "./navigation"

interface AppLayoutProps {
  children: React.ReactNode
  showNavigation?: boolean
}

export function AppLayout({ children, showNavigation = true }: AppLayoutProps) {
  return (
    <div className="min-h-screen bg-gradient-to-b from-black to-red-900 text-white w-full">
      {showNavigation && <Navigation />}
      <main className="flex-1 w-full max-w-none">{children}</main>
    </div>
  )
}
