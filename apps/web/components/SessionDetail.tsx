"use client";
import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { AlertTriangle, Download, ArrowLeft } from 'lucide-react';
import Link from 'next/link';

export default function SessionDetail({ sessionId }: { sessionId: string }) {
    const [timeline, setTimeline] = useState<any[]>([]);
    const [anchors, setAnchors] = useState<any[]>([]);

    useEffect(() => {
        const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

        fetch(`${api}/v1/sessions/${sessionId}/risk`)
            .then(res => res.json())
            .then(data => setTimeline(data))
            .catch(err => console.error(err));

        fetch(`${api}/v1/sessions/${sessionId}/anchors`)
            .then(res => res.json())
            .then(data => setAnchors(data))
            .catch(err => console.error(err));
    }, [sessionId]);

    return (
        <div className="w-full">
            <Link href="/" className="inline-flex items-center text-gray-400 hover:text-white mb-6">
                <ArrowLeft size={16} className="mr-2" /> Back to Dashboard
            </Link>

            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold">Session Analysis <span className="text-gray-500 text-lg font-mono ml-2">#{sessionId.slice(0, 8)}</span></h1>
                <button className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-sm font-semibold transition">
                    <Download size={16} /> Export Bundle
                </button>
            </div>

            {/* Risk Chart */}
            <div className="glass p-6 rounded-xl mb-6">
                <h2 className="text-xl font-semibold mb-4">Risk Velocity</h2>
                <div className="h-64 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={timeline}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                            <XAxis dataKey="question_index" stroke="#666" label={{ value: 'Question Index', position: 'insideBottom', offset: -5 }} />
                            <YAxis stroke="#666" domain={[0, 1]} />
                            <Tooltip
                                contentStyle={{ backgroundColor: '#111', border: '1px solid #333' }}
                                itemStyle={{ color: '#fff' }}
                            />
                            <ReferenceLine y={0.8} stroke="red" strokeDasharray="3 3" label="Enforce" />
                            <ReferenceLine y={0.6} stroke="orange" strokeDasharray="3 3" label="Anchors" />
                            <Line type="monotone" dataKey="r_t" stroke="#3b82f6" strokeWidth={2} dot={false} />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </div>

            {/* Anchors Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="glass p-6 rounded-xl">
                    <h2 className="text-xl font-semibold mb-4">Intervention History</h2>
                    <div className="space-y-4">
                        {anchors.length === 0 ? <p className="text-gray-500">No interventions triggered.</p> : anchors.map((a, i) => (
                            <div key={i} className={`p-4 rounded border ${a.passed ? 'border-green-500/30 bg-green-500/10' : 'border-red-500/30 bg-red-500/10'}`}>
                                <div className="flex justify-between items-start mb-2">
                                    <span className="font-bold text-sm uppercase">{a.anchor_type}</span>
                                    <span className={`text-xs px-2 py-1 rounded ${a.passed ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                                        {a.passed ? 'PASSED' : 'FAILED'}
                                    </span>
                                </div>
                                <p className="text-sm text-gray-300 mb-2">{a.trigger_reason}</p>
                                <div className="text-xs text-gray-500 mt-2 font-mono">
                                    Resp: {a.response_text ? a.response_text.slice(0, 50) + "..." : "N/A"}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="glass p-6 rounded-xl">
                    <h2 className="text-xl font-semibold mb-4">Evidence Bundle</h2>
                    <div className="p-4 bg-black/50 rounded font-mono text-xs text-green-400 h-64 overflow-y-auto">
                        <p>{`{`}</p>
                        <p className="ml-4">{`"session_id": "${sessionId}",`}</p>
                        <p className="ml-4">{`"risk_score": ${timeline.length > 0 ? timeline[timeline.length - 1].r_t.toFixed(4) : 0},`}</p>
                        <p className="ml-4">{`"integrity_sealed": true,`}</p>
                        <p className="ml-4">{`"timestamp": "${new Date().toISOString()}"`}</p>
                        <p>{`}`}</p>
                        {/* Placeholder for real JSON bundle content */}
                    </div>
                </div>
            </div>
        </div>
    );
}
