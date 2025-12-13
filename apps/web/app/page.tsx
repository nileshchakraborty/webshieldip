import SessionDetail from '../components/SessionDetail';

export default function Home() {
    return (
        <main className="flex min-h-screen flex-col items-center justify-between p-24">
            <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
                <h1 className="text-4xl font-bold mb-8">WebShield Dashboard</h1>
                <p>System Status: Active</p>
            </div>

            <div className="w-full">
                <h2 className="text-2xl mb-4">Recent Sessions</h2>
                {/* Placeholder for list of sessions */}
                <div className="border border-gray-700 p-4 rounded bg-gray-800">
                    <p>Session ID: demo-session-123</p>
                    <SessionDetail sessionId="demo-session-123" />
                </div>
            </div>
        </main>
    )
}
