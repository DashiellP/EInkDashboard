import type { FastifyPluginAsync } from "fastify";
import { plantImageService } from "./plant_images.service.js";
import { plantService } from "../plants/plants.service.js";

export const plantImageRoutes: FastifyPluginAsync =
  async (fastify) => {
    fastify.put<{ Params: { id: string } }>(
      "/:id/image",
      async (request, reply) => {
        const id = Number(request.params.id);

        if (!Number.isSafeInteger(id) || id <= 0) {
          return reply.code(400).send({
            error: "Invalid plant ID"
          });
        }

        const file = await request.file();

        if (!file) {
          return reply.code(400).send({
            error: "Image file is required"
          });
        }

        try
        {
          const imagePath = await plantImageService.addImage(id, file);
          plantService.updatePlant(id, undefined, imagePath);
          return reply.code(200).send({
            imagePath: imagePath
          });
        }
        catch (e)
        {
          reply.code(415).send({error: (e as Error).message});
        }
        
      }
    );
  };
