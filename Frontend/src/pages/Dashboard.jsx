
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/layout/Navbar';
import { Upload, FileCode, ArrowRight, Loader2, AlertCircle } from 'lucide-react';

const Dashboard = () => {
    const navigate = useNavigate();
    const [file, setFile] = useState(null);
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile && selectedFile.name.endsWith('.zip')) {
            setFile(selectedFile);
            setError(null);
        } else {
            setFile(null);
            setError('Please select a valid ZIP file.');
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setIsUploading(true);
        setError(null);

        const formData = new FormData();
        formData.append('zipFile', file);

        try {
            const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/upload-and-generate`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Upload failed');
            }

            const data = await response.json();
            // Navigate to documentation page with the result
            navigate('/documentation', { state: { documentation: data.documentation, metadata: data.metadata } });

        } catch (err) {
            console.error('Upload error:', err);
            setError(err.message || 'An error occurred during upload.');
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            <Navbar />

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-extrabold text-gray-900 dark:text-white sm:text-5xl sm:tracking-tight lg:text-6xl">
                        Document your code <span className="text-indigo-600 dark:text-indigo-400">in seconds</span>
                    </h1>
                    <p className="mt-5 max-w-xl mx-auto text-xl text-gray-500 dark:text-gray-400">
                        Upload your project zip file and let our AI generate comprehensive, beautiful documentation for you.
                    </p>
                </div>

                <div className="max-w-xl mx-auto">
                    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-xl overflow-hidden ring-1 ring-gray-900/5 dark:ring-white/10 p-8">
                        <div className="flex flex-col items-center justify-center border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-12 hover:border-indigo-500 dark:hover:border-indigo-400 transition-colors">
                            <Upload className="h-12 w-12 text-gray-400" />
                            <div className="mt-4 text-center">
                                <label htmlFor="file-upload" className="cursor-pointer">
                                    <span className="mt-2 block text-sm font-medium text-indigo-600 dark:text-indigo-400 hover:text-indigo-500">
                                        Upload a ZIP file
                                    </span>
                                    <input
                                        id="file-upload"
                                        name="file-upload"
                                        type="file"
                                        className="sr-only"
                                        accept=".zip"
                                        onChange={handleFileChange}
                                        disabled={isUploading}
                                    />
                                </label>
                                <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
                                    ZIP up to 50MB
                                </p>
                            </div>
                        </div>

                        {file && (
                            <div className="mt-6 flex items-center justify-between bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
                                <div className="flex items-center">
                                    <FileCode className="h-6 w-6 text-indigo-500" />
                                    <span className="ml-3 text-sm font-medium text-gray-900 dark:text-white truncate max-w-[200px]">
                                        {file.name}
                                    </span>
                                </div>
                                <span className="text-xs text-gray-500 dark:text-gray-400">
                                    {(file.size / 1024 / 1024).toFixed(2)} MB
                                </span>
                            </div>
                        )}

                        {error && (
                            <div className="mt-4 flex items-center p-4 bg-red-50 dark:bg-red-900/20 rounded-lg">
                                <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
                                <span className="text-sm text-red-600 dark:text-red-400">{error}</span>
                            </div>
                        )}

                        <button
                            onClick={handleUpload}
                            disabled={!file || isUploading}
                            className={`mt-6 w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white md:py-4 md:text-lg md:px-10 transition-colors ${!file || isUploading
                                ? 'bg-gray-400 cursor-not-allowed'
                                : 'bg-indigo-600 hover:bg-indigo-700 shadow-lg hover:shadow-xl'
                                }`}
                        >
                            {isUploading ? (
                                <>
                                    <Loader2 className="animate-spin -ml-1 mr-3 h-5 w-5" />
                                    Generating...
                                </>
                            ) : (
                                <>
                                    Generate Code Docs
                                    <ArrowRight className="ml-2 h-5 w-5" />
                                </>
                            )}
                        </button>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default Dashboard;
