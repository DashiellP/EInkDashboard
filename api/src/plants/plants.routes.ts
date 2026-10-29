import type { FastifyPluginAsync, FastifyRequest } from "fastify";

import { plantService } from "./plants.service.js";

export const plantRoutes: FastifyPluginAsync =
    async (fastify) => {

        fastify.get("/", async (request, reply) => {
            const result = await plantService.getAllPlants();
            return reply.code(201).send(result);
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
                const result = await plantService.addPlant(request.body.name);
                return reply.code(201).send(result);
            }
        );
    };