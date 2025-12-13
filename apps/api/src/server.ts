import Fastify from 'fastify';
import cors from '@fastify/cors';
import postgres from '@fastify/postgres';
import { ingestionRoutes } from './routes/ingestion';

const server = Fastify({
    logger: true
});

server.register(cors);

// Database connection
server.register(postgres, {
    connectionString: process.env.DATABASE_URL
});

// Routes
server.register(ingestionRoutes, { prefix: '/v1' });

const start = async () => {
    try {
        const port = parseInt(process.env.PORT || '3001');
        await server.listen({ port, host: '0.0.0.0' });
        console.log(`Server listening on ${port}`);
    } catch (err) {
        server.log.error(err);
        process.exit(1);
    }
};

start();
