import React, { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import {
    FileCode2,
    LogOut,
    LayoutDashboard,
    Upload,
} from "lucide-react";
import AuthModal from "../auth/AuthModal";

const Navbar = () => {
    const { currentUser, logout } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();
    const [showAuthModal, setShowAuthModal] = useState(false);
    const [authMode, setAuthMode] = useState("login");

    async function handleLogout() {
        try {
            await logout();
            navigate("/");
        } catch (err) {
            console.error("Failed to log out", err);
        }
    }

    const openAuthModal = (mode) => {
        setAuthMode(mode);
        setShowAuthModal(true);
    };

    return (
        <>
            {/* Premium Dark Navbar */}
            <nav className="bg-gray-50 dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50">

                <div className="max-w-7xl mx-auto px-6">
                    <div className="flex justify-between h-16 items-center">

                        {/* Logo */}
                        <Link to="/" className="flex items-center space-x-2">
                            <FileCode2 className="h-8 w-8 text-indigo-500" />
                            <span className="text-xl font-bold text-white tracking-tight">
                                DocGen
                            </span>
                        </Link>

                        {/* Right Side */}
                        <div className="flex items-center space-x-6">
                            {currentUser ? (
                                <>
                                    <span className="text-sm text-gray-400 hidden md:block">
                                        Welcome, {currentUser.displayName || currentUser.email}
                                    </span>

                                    <Link
                                        to="/dashboard"
                                        className={`px-3 py-2 rounded-md text-sm font-medium transition ${location.pathname === "/dashboard"
                                            ? "bg-gray-800 text-indigo-400"
                                            : "text-gray-400 hover:text-white hover:bg-gray-800"
                                            }`}
                                    >
                                        <div className="flex items-center">
                                            <LayoutDashboard className="h-4 w-4 mr-2" />
                                            Dashboard
                                        </div>
                                    </Link>

                                    <Link
                                        to="/upload"
                                        className={`px-3 py-2 rounded-md text-sm font-medium transition ${location.pathname === "/upload"
                                            ? "bg-gray-800 text-indigo-400"
                                            : "text-gray-400 hover:text-white hover:bg-gray-800"
                                            }`}
                                    >
                                        <div className="flex items-center">
                                            <Upload className="h-4 w-4 mr-2" />
                                            Upload
                                        </div>
                                    </Link>

                                    <button
                                        onClick={handleLogout}
                                        className="px-3 py-2 rounded-md text-sm font-medium text-gray-400 hover:text-white hover:bg-gray-800 transition"
                                    >
                                        <div className="flex items-center">
                                            <LogOut className="h-4 w-4 mr-2" />
                                            Logout
                                        </div>
                                    </button>
                                </>
                            ) : (
                                <>
                                    <button
                                        onClick={() => openAuthModal("login")}
                                        className="text-gray-400 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition"
                                    >
                                        Login
                                    </button>

                                    <button
                                        onClick={() => openAuthModal("signup")}
                                        className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium transition"
                                    >
                                        Get Started
                                    </button>
                                </>
                            )}
                        </div>
                    </div>
                </div>
            </nav>

            <AuthModal
                isOpen={showAuthModal}
                onClose={() => setShowAuthModal(false)}
                initialMode={authMode}
            />
        </>
    );
};

export default Navbar;
