'use client'

import { useState } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import Link from 'next/link'

export default function Navbar() {
  const router = useRouter()
  const pathname = usePathname()

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 backdrop-blur-md bg-white/80 border-b border-white/20 shadow-lg">
      <div className="max-w-6xl mx-auto px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex-shrink-0">
            <button
              onClick={() => router.push('/')}
              className="text-xl font-bold text-gray-900 hover:text-blue-600 transition-colors duration-200 cursor-pointer"
            >
              LogViewer
            </button>
          </div>

          {/* Desktop Navigation */}
          <div>
            <div className="ml-10 flex items-baseline space-x-8">
              {/* Show Home only if NOT on "/" */}
              {pathname !== '/' && (
                <Link
                  href="/"
                  className="relative px-4 py-2 text-gray-700 hover:text-blue-600 font-medium transition-all duration-300 group"
                >
                  Home
                  <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-blue-600 transition-all duration-300 group-hover:w-full"></span>
                </Link>
              )}

              {/* Show Dashboard only if NOT on "/dashboard" */}
              {pathname !== '/dashboard' && (
                <Link
                  href="/dashboard"
                  className="relative px-4 py-2 text-gray-700 hover:text-blue-600 font-medium transition-all duration-300 group"
                >
                  Dashboard
                  <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-blue-600 transition-all duration-300 group-hover:w-full"></span>
                </Link>
              )}

              {/* CTA Button */}
              <button
                onClick={() => router.push('/register')}
                className="ml-4 bg-blue-600/90 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-lg transition-all duration-300 hover:shadow-lg hover:scale-105 backdrop-blur-sm"
              >
                Register
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}
