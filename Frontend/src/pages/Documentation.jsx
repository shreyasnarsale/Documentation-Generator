import React, { useState } from 'react';
import { useLocation, Navigate } from 'react-router-dom';
import Navbar from '../components/layout/Navbar';
import DocumentationViewer from '../components/documentation/DocumentationViewer';
import TableOfContents from '../components/documentation/TableOfContents';
import ExportButton from '../components/common/ExportButton';
import ChatInterface from '../components/chat/ChatInterface';
import { MessageSquare, X } from 'lucide-react';

const Documentation = () => {
    const location = useLocation();
    const { documentation, metadata } = location.state || {};
    const [showChat, setShowChat] = useState(false);

    if (!documentation) {
        return <Navigate to="/" replace />;
    }

    return (
        <div className="min-h-screen bg-gray-100">

            <Navbar />

            <main className="max-w-7xl mx-auto px-6 py-12">
                <div className="flex flex-col lg:flex-row gap-10">

                    {/* Main Content */}
                    <div className="lg:w-3/4 flex-grow">

                        <div className="bg-white rounded-2xl shadow-xl p-12 border border-gray-200">

                            {/* Metadata */}
                            {metadata && (
                                <div className="mb-12 p-6 bg-indigo-50 rounded-xl border border-indigo-200">
                                    <h2 className="text-xs font-semibold text-indigo-700 uppercase tracking-widest mb-4">
                                        Project Stats
                                    </h2>

                                    <div className="grid grid-cols-2 md:grid-cols-3 gap-8">
                                        <div>
                                            <p className="text-gray-500 text-sm">Files</p>
                                            <p className="text-3xl font-bold text-gray-900">
                                                {metadata.totalFiles}
                                            </p>
                                        </div>

                                        <div>
                                            <p className="text-gray-500 text-sm">Languages</p>
                                            <p className="text-3xl font-bold text-gray-900">
                                                {metadata.languages?.join(', ')}
                                            </p>
                                        </div>

                                        <div>
                                            <p className="text-gray-500 text-sm">Processing</p>
                                            <p className="text-3xl font-bold text-gray-900">
                                                {metadata.processingTime}s
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* Actions */}
                            <div className="flex justify-end mb-10 space-x-4">
                                <button
                                    onClick={() => setShowChat(!showChat)}
                                    className={`inline-flex items-center px-5 py-2.5 rounded-lg text-sm font-medium shadow-md transition ${
                                        showChat
                                            ? 'bg-gray-700 hover:bg-gray-800 text-white'
                                            : 'bg-indigo-600 hover:bg-indigo-700 text-white'
                                    }`}
                                >
                                    {showChat ? (
                                        <X className="mr-2 h-5 w-5" />
                                    ) : (
                                        <MessageSquare className="mr-2 h-5 w-5" />
                                    )}
                                    {showChat ? 'Close Chat' : 'Chat with Docs'}
                                </button>

                                <ExportButton documentation={documentation} />
                            </div>

                            {/* Content */}
                            {showChat ? (
                                <div className="h-[650px] mb-8 border rounded-xl overflow-hidden shadow-inner">
                                    <ChatInterface
                                        documentation={documentation}
                                        onClose={() => setShowChat(false)}
                                    />
                                </div>
                            ) : (
                                <div className="prose prose-lg max-w-none text-gray-800">
                                    <DocumentationViewer markdown={documentation} />
                                </div>
                            )}

                        </div>
                    </div>

                    {/* Sidebar */}
                    <aside className="lg:w-1/4 hidden lg:block">
                        <div className="sticky top-28">
                            <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-200">
                                <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-widest mb-4">
                                    Table of Contents
                                </h3>
                                <TableOfContents markdown={documentation} />
                            </div>
                        </div>
                    </aside>

                </div>
            </main>
        </div>
    );
};

export default Documentation;
