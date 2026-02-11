import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/layout/Navbar';
import { Upload as UploadIcon, FileArchive, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const Upload = () => {
    const [file, setFile] = useState(null);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [progress, setProgress] = useState(0);
    const fileInputRef = useRef(null);
    const navigate = useNavigate();
    const { currentUser } = useAuth();

    const handleDragOver = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            const droppedFile = e.dataTransfer.files[0];
            validateAndSetFile(droppedFile);
        }
    };

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            validateAndSetFile(e.target.files[0]);
        }
    };

    const validateAndSetFile = (selectedFile) => {
        setError('');

        if (!selectedFile.name.endsWith('.zip')) {
            setError('Please upload a ZIP file.');
            return;
        }

        // Max size 50MB
        if (selectedFile.size > 50 * 1024 * 1024) {
            setError('File size exceeds 50MB limit.');
            return;
        }

        setFile(selectedFile);
    };

    const handleUpload = async () => {
        if (!file) return;
        if (!currentUser) {
            setError('You must be logged in to upload files.');
            return;
        }

        setLoading(true);
        setError('');
        setProgress(10); // Start progress

        const formData = new FormData();
        formData.append('zipFile', file);
        formData.append('userId', currentUser.uid);

        try {
            // Emulate progress for better UX since Axios progress can be fast
            const progressInterval = setInterval(() => {
                setProgress(prev => {
                    if (prev >= 90) {
                        clearInterval(progressInterval);
                        return 90;
                    }
                    return prev + 10;
                });
            }, 500);

            const response = await axios.post(
                `${import.meta.env.VITE_API_BASE_URL}/api/upload-and-generate`,
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                }
            );

            clearInterval(progressInterval);
            setProgress(100);

            // Navigate to documentation with the result
            navigate('/documentation', {
                state: {
                    documentation: response.data.documentation,
                    metadata: response.data.metadata,
                    sessionId: response.data.sessionId
                }
            });

        } catch (err) {
            console.error(err);
            setError(err.response?.data?.detail || 'An error occurred during upload or generation.');
            setLoading(false);
            setProgress(0);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            <Navbar />

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="max-w-3xl mx-auto">
                    <div className="text-center mb-12">
                        <h1 className="text-3xl font-extrabold text-gray-900 dark:text-white sm:text-4xl">
                            Upload your codebase
                        </h1>
                        <p className="mt-4 text-xl text-gray-500 dark:text-gray-300">
                            Upload a ZIP file of your project. We'll analyze it and generate comprehensive documentation.
                        </p>
                    </div>

                    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
                        {/* Upload Area */}
                        <div
                            className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors cursor-pointer
                                ${file
                                    ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/10'
                                    : 'border-gray-300 dark:border-gray-600 hover:border-indigo-400 dark:hover:border-indigo-500'
                                }`}
                            onDragOver={handleDragOver}
                            onDrop={handleDrop}
                            onClick={() => !loading && fileInputRef.current?.click()}
                        >
                            <input
                                type="file"
                                ref={fileInputRef}
                                className="hidden"
                                accept=".zip"
                                onChange={handleFileChange}
                                disabled={loading}
                            />

                            {file ? (
                                <div className="space-y-4">
                                    <FileArchive className="h-16 w-16 mx-auto text-indigo-600 dark:text-indigo-400" />
                                    <div>
                                        <p className="text-lg font-medium text-gray-900 dark:text-white">
                                            {file.name}
                                        </p>
                                        <p className="text-sm text-gray-500 dark:text-gray-400">
                                            {(file.size / (1024 * 1024)).toFixed(2)} MB
                                        </p>
                                    </div>
                                    {!loading && (
                                        <button
                                            className="text-sm text-red-500 hover:text-red-700 font-medium"
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                setFile(null);
                                            }}
                                        >
                                            Remove file
                                        </button>
                                    )}
                                </div>
                            ) : (
                                <div className="space-y-4">
                                    <UploadIcon className="h-16 w-16 mx-auto text-gray-400" />
                                    <div>
                                        <p className="text-lg font-medium text-gray-900 dark:text-white">
                                            Click or drag file to upload
                                        </p>
                                        <p className="text-sm text-gray-500 dark:text-gray-400">
                                            Only .zip files allowed (Max 50MB)
                                        </p>
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Error Message */}
                        {error && (
                            <div className="mt-6 bg-red-50 dark:bg-red-900/20 p-4 rounded-md flex items-start">
                                <AlertCircle className="h-5 w-5 text-red-400 mt-0.5 mr-2" />
                                <div className="flex-1">
                                    <h3 className="text-sm font-medium text-red-800 dark:text-red-200">Upload Error</h3>
                                    <div className="mt-1 text-sm text-red-700 dark:text-red-300">{error}</div>
                                </div>
                            </div>
                        )}

                        {/* Processing State */}
                        {loading && (
                            <div className="mt-8 space-y-4">
                                <div className="flex justify-between text-sm font-medium text-gray-900 dark:text-white">
                                    <span>Processing...</span>
                                    <span>{progress}%</span>
                                </div>
                                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                                    <div
                                        className="bg-indigo-600 h-2.5 rounded-full transition-all duration-500"
                                        style={{ width: `${progress}%` }}
                                    ></div>
                                </div>
                                <p className="text-sm text-center text-gray-500 dark:text-gray-400 animate-pulse">
                                    Analyzing codebase and generating documentation... This may take a minute.
                                </p>
                            </div>
                        )}

                        {/* Action Buttons */}
                        <div className="mt-8 flex justify-center">
                            <button
                                onClick={handleUpload}
                                disabled={!file || loading}
                                className={`
                                    flex items-center justify-center px-8 py-3 border border-transparent 
                                    text-base font-medium rounded-md text-white shadow-sm
                                    ${!file || loading
                                        ? 'bg-indigo-400 cursor-not-allowed'
                                        : 'bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
                                    }
                                `}
                            >
                                {loading && <Loader2 className="animate-spin -ml-1 mr-3 h-5 w-5" />}
                                {loading ? 'Generating Documentation...' : 'Generate Documentation'}
                            </button>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default Upload;
