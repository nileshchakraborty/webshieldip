"use client";
import React, { useEffect, useState } from 'react';
import { Activity, Shield, AlertTriangle, CheckCircle } from 'lucide-react';
import Link from 'next/link';

export default function Dashboard() {
    const [sessions, setSessions] = useState<any[]>([]);
    const [stats, setStats] = useState({ active: 0, flagged: 0 });

    useEffect(() => {
        fetch(`${process.env.NEXT_PUBLIC_API_URL}/v1/sessions`)
            .then(res => res.json())
            .then(data => {
                setSessions(data);
                // Simple stats aggregation
                const flagged = data.filter((s: any) => s.status === 'flagged' || s.status === 'enforce').length;
                setStats({ active: data.length, flagged });
            })
            .catch(err => console.error(err));
    }, []);

    return (
        <div className="w-full max-w-6xl mx-auto p-6">
            <h1 className="text-3xl font-bold mb-8 flex items-center gap-2">
                <Shield className="text-blue-500" /> WebShield Supervisor
            </h1>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="glass p-6 rounded-xl flex items-center gap-4">
                    <div className="p-3 bg-blue-500/20 rounded-lg text-blue-400">
                        <Activity size={24} />
                    </div>
                    <div>
                        <p className="text-sm text-gray-400">Total Sessions</p>
                        <p className="text-2xl font-bold">{stats.active}</p>
                    </div>
                </div>
                <div className="glass p-6 rounded-xl flex items-center gap-4">
                    <div className="p-3 bg-red-500/20 rounded-lg text-red-400">
                        <AlertTriangle size={24} />
                    </div>
                    <div>
                        <p className="text-sm text-gray-400">Flagged / Enforced</p>
                        <p className="text-2xl font-bold">{stats.flagged}</p>
                    </div>
                </div>
                <div className="glass p-6 rounded-xl flex items-center gap-4">
                    <div className="p-3 bg-green-500/20 rounded-lg text-green-400">
                        <CheckCircle size={24} />
                    </div>
                    <div>
                        <p className="text-sm text-gray-400">System Health</p>
                        <p className="text-2xl font-bold text-green-400">Optimal</p>
                    </div>
                </div>
            </div>

            {/* Session List */}
            <div className="glass rounded-xl p-6">
                <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead>
                            <tr className="border-b border-gray-700 text-gray-400">
                                <th className="py-3 px-4">Session ID</th>
                                <th className="py-3 px-4">Status</th>
                                <th className="py-3 px-4">Time</th>
                                <th className="py-3 px-4">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {sessions.map(session => (
                                <tr key={session.id} className="border-b border-gray-800 hover:bg-white/5 transition">
                                    <td className="py-3 px-4 font-mono text-sm text-blue-300">
                                        {session.id.slice(0, 8)}...
                                    </td>
                                    <td className="py-3 px-4">
                                        <span className={`px-2 py-1 rounded text-xs ${session.status === 'enforce' ? 'bg-red-500/20 text-red-400' :
                                                session.status === 'active' ? 'bg-green-500/20 text-green-400' :
                                                    'bg-yellow-500/20 text-yellow-400'
                                            }`}>
                                            {session.status.toUpperCase()}
                                        </span>
                                    </td>
                                    <td className="py-3 px-4 text-gray-400 text-sm">
                                        {new Date(session.created_at).toLocaleString()}
                                    </td>
                                    <td className="py-3 px-4">
                                        <Link href={`/session/${session.id}`} className="text-blue-400 hover:underline text-sm">
                                            View Details
                                        </Link>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}
