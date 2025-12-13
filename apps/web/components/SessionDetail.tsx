"use client";
import React, { useEffect, useState } from 'react';

// Simplified Risk Timeline visualization
export default function SessionDetail({ sessionId }: { sessionId: string }) {
    const [risks, setRisks] = useState<any[]>([]);

    useEffect(() => {
        fetch(`${process.env.NEXT_PUBLIC_API_URL}/v1/sessions/${sessionId}/risk`)
            .then(res => res.json())
            .then(data => setRisks(data))
            .catch(err => console.error(err));
    }, [sessionId]);

    return (
        <div className="mt-4 p-4 bg-gray-900 rounded">
            <h3 className="text-xl font-bold text-blue-400">Risk Timeline</h3>
            <div className="mt-4 space-y-2">
                {risks.length === 0 ? (
                    <p>No risk data calculated yet.</p>
                ) : (
                    risks.map((r, i) => (
                        <div key={i} className="flex justify-between border-b border-gray-800 pb-2">
                            <span>Q{r.question_index}</span>
                            <span className={r.r_t > 0.5 ? "text-red-500" : "text-green-500"}>
                                Score: {r.r_t.toFixed(2)} ({r.policy_band})
                            </span>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}
