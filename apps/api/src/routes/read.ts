import { FastifyInstance } from 'fastify';

export async function readRoutes(server: FastifyInstance) {

    // List Sessions
    server.get('/sessions', async (request, reply) => {
        const client = await server.pg.connect();
        try {
            const { rows } = await client.query(
                `SELECT * FROM sessions ORDER BY created_at DESC LIMIT 50`
            );
            return rows;
        } finally {
            client.release();
        }
    });

    // Get Session Detail
    server.get('/sessions/:id', async (request: any, reply) => {
        const { id } = request.params;
        const client = await server.pg.connect();
        try {
            const { rows } = await client.query(
                `SELECT * FROM sessions WHERE id = $1`, [id]
            );
            if (rows.length === 0) return reply.code(404).send({ error: "Not Found" });
            return rows[0];
        } finally {
            client.release();
        }
    });

    // Get Risk Timeline
    server.get('/sessions/:id/risk', async (request: any, reply) => {
        const { id } = request.params;
        const client = await server.pg.connect();
        try {
            const { rows } = await client.query(
                `SELECT * FROM risk_timeline WHERE session_id = $1 ORDER BY question_index ASC`, [id]
            );
            return rows;
        } finally {
            client.release();
        }
    });

    // Get Anchors
    server.get('/sessions/:id/anchors', async (request: any, reply) => {
        const { id } = request.params;
        const client = await server.pg.connect();
        try {
            const { rows } = await client.query(
                `SELECT * FROM anchors WHERE session_id = $1 ORDER BY created_at ASC`, [id]
            );
            return rows;
        } finally {
            client.release();
        }
    });
}
