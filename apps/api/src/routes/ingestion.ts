import { FastifyInstance } from 'fastify';
import { Event } from '@webshield/shared';
// import { randomUUID } from 'crypto'; // Node 20+

export async function ingestionRoutes(fastify: FastifyInstance) {

    fastify.post<{ Body: any }>('/sessions', async (request, reply) => {
        const { id, deviceId, userId, assessmentId } = request.body;

        // Using simple hashing via SQL for demo, or assume pre-hashed by client?
        // Spec says "user_hash", "device_hash". 
        // We'll store directly for now, assume API/Client contract handles hashing or we do it here.

        const client = await fastify.pg.connect();
        try {
            const { rows } = await client.query(
                `INSERT INTO sessions (id, assessment_id, user_hash, device_hash, status) 
             VALUES ($1, $2, $3, $4, 'active') RETURNING id`,
                [id || crypto.randomUUID(), assessmentId, userId, deviceId]
            );
            reply.code(201).send({ sessionId: rows[0].id });
        } catch (e) {
            request.log.error(e);
            reply.code(500).send({ error: 'Database error' });
        } finally {
            client.release();
        }
    });

    fastify.post<{ Body: Event, Params: { id: string } }>('/sessions/:id/events', async (request, reply) => {
        const { id } = request.params;
        const event = request.body;

        const client = await fastify.pg.connect();
        try {
            // Validation: Ensure ts_ms is present
            if (!event.ts_ms) {
                event.ts_ms = Date.now();
            }

            await client.query(
                `INSERT INTO event_history 
             (id, session_id, question_id, event_type, payload, ts_ms) 
             VALUES ($1, $2, $3, $4, $5, $6)`,
                [
                    event.id || crypto.randomUUID(),
                    id,
                    event.question_id || event.payload?.question_id, // extraction fallback
                    event.event_type,
                    event.payload,
                    event.ts_ms
                ]
            );
            reply.code(201).send({ status: 'received' });
        } catch (e) {
            request.log.error(e);
            reply.code(500).send({ error: 'Database error' });
        } finally {
            client.release();
        }
    });

    // Read-only endpoints for Frontend
    fastify.get<{ Params: { id: string } }>('/sessions/:id/risk', async (request, reply) => {
        const { id } = request.params;
        const client = await fastify.pg.connect();
        try {
            const { rows } = await client.query(
                `SELECT * FROM risk_timeline WHERE session_id = $1 ORDER BY question_index ASC`,
                [id]
            );
            reply.send(rows);
        } finally {
            client.release();
        }
    });
}
