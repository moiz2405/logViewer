'use client'

import { useRouter } from 'next/navigation'

export default function Hero() {
    const router = useRouter()
    return (
        <div className="min-h-screen flex items-center px-2 ">
            <div className="max-w-4xl mx-auto text-center">
                {/* Main heading */}
                <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
                    LogViewer
                </h1>
                
                {/* Subtitle */}
                <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
                    Intelligent Log Analysis & Classification System
                </p>
                
                {/* Description */}
                <p className="text-lg text-gray-500 mb-12 max-w-2xl mx-auto leading-relaxed">
                    Transform raw system logs into structured insights. Automatically detect anomalies, 
                    classify errors, and get actionable summaries for faster debugging.
                </p>
                
                {/* CTA Buttons */}
                <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                    <button 
                    onClick={()=>router.push("/dashboard")}
                    className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200 shadow-lg hover:shadow-xl">
                        Register Your App
                    </button>
                </div>
                
                {/* Feature highlights */}
                <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-3xl mx-auto">
                    <div className="text-center">
                        <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                            <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                            </svg>
                        </div>
                        <h3 className="font-semibold text-gray-900 mb-2">Smart Classification</h3>
                        <p className="text-gray-600 text-sm">Automatically categorize errors by service, type, and severity</p>
                    </div>
                    
                    <div className="text-center">
                        <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                            <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                            </svg>
                        </div>
                        <h3 className="font-semibold text-gray-900 mb-2">Fast Processing</h3>
                        <p className="text-gray-600 text-sm">Process large log files in seconds with intelligent filtering</p>
                    </div>
                    
                    <div className="text-center">
                        <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                            <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <h3 className="font-semibold text-gray-900 mb-2">Structured Output</h3>
                        <p className="text-gray-600 text-sm">Get clean JSON summaries ready for analysis and visualization</p>
                    </div>
                </div>
            </div>
        </div>
    )
}