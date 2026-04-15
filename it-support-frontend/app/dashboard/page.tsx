"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import Navbar from "@/components/Navbar";
import type { User } from "@/types";

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.replace("/login");
      return;
    }

    api
      .get<User>("/auth/me/")
      .then((res) => {
        setUser(res.data);
      })
      .catch(() => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        router.replace("/login");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-gray-500">Loading…</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-4xl mx-auto px-6 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600 mb-8">Welcome to the IT Support System.</p>

        {user && (
          <div className="bg-white rounded-2xl shadow p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">
              Your Profile
            </h2>
            <dl className="space-y-2 text-sm text-gray-700">
              <div className="flex gap-2">
                <dt className="font-medium w-28">Username:</dt>
                <dd>{user.username}</dd>
              </div>
              {user.full_name && (
                <div className="flex gap-2">
                  <dt className="font-medium w-28">Full name:</dt>
                  <dd>{user.full_name}</dd>
                </div>
              )}
              {user.email && (
                <div className="flex gap-2">
                  <dt className="font-medium w-28">Email:</dt>
                  <dd>{user.email}</dd>
                </div>
              )}
              <div className="flex gap-2">
                <dt className="font-medium w-28">Role:</dt>
                <dd className="capitalize">{user.role.replace(/_/g, " ")}</dd>
              </div>
              {user.department && (
                <div className="flex gap-2">
                  <dt className="font-medium w-28">Department:</dt>
                  <dd>{user.department}</dd>
                </div>
              )}
            </dl>
          </div>
        )}
      </main>
    </div>
  );
}
