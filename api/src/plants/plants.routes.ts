import type { FastifyPluginAsync, FastifyRequest } from "fastify";
import { randomUUID } from "node:crypto";
import { waitForDebugger } from "node:inspector";
import { pool } from "../db/pool.js";

import { plantService } from "./plants.service.js";

export const plantRoutes: FastifyPluginAsync =
    async (fastify) => {

        fastify.get("/", async (request, reply) => {
            const result = await pool.query("SELECT * FROM plants WHERE True;");
            return reply.code(201).send(result.rows);
        });

        fastify.get<{ Params: { id: number } }>("/:id", async (request, reply) => {
            const result = await plantService.getPlant(request.params.id);
            return reply.code(201).send(result);
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

                const result = await plantService.addPlant(request.body.name, "");

                return reply.code(201).send(result);
            }
        );
    };