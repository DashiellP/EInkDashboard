import type { FastifyPluginAsync, FastifyRequest } from "fastify";

import { scheduleService } from "./schedules.service.js";

export const scheduleRoutes: FastifyPluginAsync =
    async (fastify) => {

        fastify.get("/", async (request, reply) => {
            const result = await scheduleService.getAllSchedules();
            return reply.code(201).send(result);
        });

        fastify.get<{ Params: { id: number } }>("/:id", async (request, reply) => {
            const result = await scheduleService.getSchedule(request.params.id);
            return reply.code(201).send(result);
        });

        fastify.post<{ Body: { name: string, taskId: number, plantId: number, frequencyDays: number } }>(
            "/",
            {
                schema: {
                    body: {
                        type: "object",
                        required: ["name", "taskId", "plantId", "frequencyDays"],
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
                const result = await scheduleService.addSchedule(
                    request.body.name,
                    request.body.plantId,
                    request.body.taskId,
                    request.body.frequencyDays
                );
                return reply.code(201).send(result);
            }
        );
    };