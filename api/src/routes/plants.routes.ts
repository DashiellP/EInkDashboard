import type { FastifyPluginAsync, FastifyRequest } from "fastify";
import { randomUUID } from "node:crypto";
import { waitForDebugger } from "node:inspector";
import { pool } from "../db/pool.js"

export const plantRoutes: FastifyPluginAsync =
    async (fastify) => {

        fastify.get("/", async (request, reply) => {
            const result = await pool.query("SELECT * FROM plants WHERE True;");
            return reply.code(201).send(result.rows);
        });

        fastify.get<{ Params: { id: number } }>("/:id", async (request, reply) => {
            const result = await pool.query("SELECT * FROM plants WHERE id=$1;", [request.params.id]);
            return reply.code(201).send(result.rows);
        });

        fastify.post<{ Body: { name: string } }>(
            "/",
            {
                schema: {
                    body: {
                        type: "object",
                        required: ["name"],
                        additionalProperties: false,
                        properties: {
                            name: {
                                type: "string",
                                minLength: 1,
                                maxLength: 255
                            }
                        }
                    }
                }
            },
            async (request, reply) => {

                const result = await pool.query(
                    "INSERT INTO plants (name) VALUES ($1) RETURNING *;",
                    [request.body.name]
                );

                return reply.code(201).send(result.rows[0]);
            }
        );
    };