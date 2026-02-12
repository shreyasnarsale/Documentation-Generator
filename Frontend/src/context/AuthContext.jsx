import React, { createContext, useContext, useState, useEffect } from "react";
import { auth } from "../firebase";
import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signOut,
    onAuthStateChanged,
    updateProfile
} from "firebase/auth";

const AuthContext = createContext();

export function useAuth() {
    return useContext(AuthContext);
}

export function AuthProvider({ children }) {
    const [currentUser, setCurrentUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // ========================
    // SIGNUP FUNCTION
    // ========================
    async function signup(email, password, name) {
        try {
            const userCredential = await createUserWithEmailAndPassword(
                auth,
                email.trim(),
                password.trim()
            );

            if (name) {
                await updateProfile(userCredential.user, {
                    displayName: name
                });
            }

            return userCredential;

        } catch (error) {

            if (error.code === "auth/email-already-in-use") {
                throw new Error("This email is already registered.");
            }

            if (error.code === "auth/weak-password") {
                throw new Error("Password must be at least 6 characters.");
            }

            if (error.code === "auth/invalid-email") {
                throw new Error("Invalid email format.");
            }

            throw new Error("Signup failed. Please try again.");
        }
    }

    // ========================
    // LOGIN FUNCTION
    // ========================
    async function login(email, password) {
        try {
            return await signInWithEmailAndPassword(
                auth,
                email.trim(),
                password.trim()
            );

        } catch (error) {

            if (error.code === "auth/invalid-credential") {
                throw new Error("Account not found or incorrect password.");
            }

            if (error.code === "auth/invalid-email") {
                throw new Error("Invalid email format.");
            }

            if (error.code === "auth/too-many-requests") {
                throw new Error("Too many failed attempts. Please try again later.");
            }

            throw new Error("Login failed. Please try again.");
        }
    }

    // ========================
    // LOGOUT FUNCTION
    // ========================
    function logout() {
        return signOut(auth);
    }

    // ========================
    // AUTH STATE LISTENER
    // ========================
    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, (user) => {
            setCurrentUser(user);
            setLoading(false);
        });

        return unsubscribe;
    }, []);

    const value = {
        currentUser,
        signup,
        login,
        logout,
    };

    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
}
