import type { FastifyPluginAsync, FastifyRequest } from "fastify";
import { randomUUID } from "node:crypto";
import { waitForDebugger } from "node:inspector";

const plants = new Map<string, {
    id: string,
    name: string,
    wateringFrequencyDays: number,
    lastWateredTimestamp: number,
    imgPath: string
}>();

export const plantRoutes: FastifyPluginAsync =
    async (fastify) => {

        fastify.get("/", async () => {
            return {
                plants: plants
            };
        });

        fastify.get<{ Params: { id: string } }>(
            "/:id",
            async (request) => {
                return {
                    id: request.params.id,
                    username: "TestPlayer"
                };
            }
        );

        fastify.post<{ Params: { name: string, wateringFrequencyDays: number, imgData: string } }>(
            "/create",
            {
                schema: {
                    body: {
                        type: "object",
                        required: ["name", "wateringFrequency", "imgData"],
                        additionalProperties: true,
                        properties: {
                            name: {
                                type: "string",
                                minLength: 3,
                                maxLength: 128
                            },
                            wateringFrequency: {
                                type: "number"
                            },
                            imgData: {
                                type: "string" // TODO: Replace with file upload
                            }
                        }
                    }
                }
            },
            async (request, reply) => {
                const plant = {
                    id: randomUUID(),
                    name: request.params.name,
                    wateringFrequencyDays: request.params.wateringFrequencyDays,
                    lastWateredTimestamp: 0,
                    imgPath: ""
                };

                plants.set(plant.id, plant);

                return reply.code(201).send(plant);
            }
        );
    };