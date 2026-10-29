import type { FastifyPluginAsync, FastifyRequest } from "fastify";

import { taskService } from "./tasks.service.js";

export const taskRoutes: FastifyPluginAsync =
    async (fastify) => {

        fastify.get("/", async (request, reply) => {
            const result = await taskService.getAllTasks();
            return reply.code(201).send(result);
        });

        fastify.get<{ Params: { id: number } }>("/:id", async (request, reply) => {
            const result = await taskService.getTask(request.params.id);
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
                const result = await taskService.addTask(request.body.name);
                return reply.code(201).send(result);
            }
        );
    };