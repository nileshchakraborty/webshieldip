import SessionDetail from '@/components/SessionDetail';

export default function SessionPage({ params }: { params: { id: string } }) {
    return (
        <main className="min-h-screen p-6 max-w-6xl mx-auto">
            <SessionDetail sessionId={params.id} />
        </main>
    )
}
