'use client'

import { useState } from 'react'

export default function Navbar() {
    const [isOpen, setIsOpen] = useState(false)

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 backdrop-blur-md bg-white/80 border-b border-white/20 shadow-lg">
            <div className="max-w-6xl mx-auto px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    {/* Logo */}
                    <div className="flex-shrink-0">
                        <h1 className="text-xl font-bold text-gray-900 hover:text-blue-600 transition-colors duration-200 cursor-pointer">
                            LogViewer
                        </h1>
                    </div>

                    {/* Desktop Navigation */}
                    <div className="hidden md:block">
                        <div className="ml-10 flex items-baseline space-x-8">
                            <a
                                href="#"
                                className="relative px-4 py-2 text-gray-700 hover:text-blue-600 font-medium transition-all duration-300 group"
                            >
                                Home
                                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-blue-600 transition-all duration-300 group-hover:w-full"></span>
                            </a>
                            
                            <a
                                href="#"
                                className="relative px-4 py-2 text-gray-700 hover:text-blue-600 font-medium transition-all duration-300 group"
                            >
                                Dashboard
                                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-blue-600 transition-all duration-300 group-hover:w-full"></span>
                            </a>

                            {/* CTA Button */}
                            <button className="ml-4 bg-blue-600/90 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-lg transition-all duration-300 hover:shadow-lg hover:scale-105 backdrop-blur-sm">
                                Analyze Logs
                            </button>
                        </div>
                    </div>

                    {/* Mobile menu button */}
                    <div className="md:hidden">
                        <button
                            onClick={() => setIsOpen(!isOpen)}
                            className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-blue-600 hover:bg-white/20 transition-all duration-200"
                        >
                            <svg
                                className={`${isOpen ? 'hidden' : 'block'} h-6 w-6 transition-transform duration-200`}
                                stroke="currentColor"
                                fill="none"
                                viewBox="0 0 24 24"
                            >
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                            </svg>
                            <svg
                                className={`${isOpen ? 'block' : 'hidden'} h-6 w-6 transition-transform duration-200`}
                                stroke="currentColor"
                                fill="none"
                                viewBox="0 0 24 24"
                            >
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>
                </div>

                {/* Mobile Navigation Menu */}
                <div className={`md:hidden transition-all duration-300 ease-in-out ${isOpen ? 'max-h-48 opacity-100' : 'max-h-0 opacity-0'} overflow-hidden`}>
                    <div className="px-2 pt-2 pb-3 space-y-1 backdrop-blur-md bg-white/70 rounded-lg mt-2 border border-white/30">
                        <a
                            href="#"
                            className="block px-4 py-3 text-gray-700 hover:text-blue-600 hover:bg-white/40 rounded-md font-medium transition-all duration-200"
                        >
                            Home
                        </a>
                        
                        <a
                            href="#"
                            className="block px-4 py-3 text-gray-700 hover:text-blue-600 hover:bg-white/40 rounded-md font-medium transition-all duration-200"
                        >
                            Dashboard
                        </a>

                        <div className="px-4 pt-2">
                            <button className="w-full bg-blue-600/90 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-lg transition-all duration-300 hover:shadow-lg backdrop-blur-sm">
                                Analyze Logs
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    )
}