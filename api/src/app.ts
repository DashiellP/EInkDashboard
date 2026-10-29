import Fastify from "fastify";
import { plantRoutes } from "./plants/plants.routes.js";
import multipart from "@fastify/multipart";
import cors from "@fastify/cors";
import { plantImageRoutes } from "./plant_images/plant_images.routes.js";
import { taskRoutes } from "./tasks/tasks.routes.js";

export async function buildApp() {
  const app = Fastify({
    logger: true
  });

  await app.register(cors, {
    origin: "http://localhost:8080",
    methods: ["GET", "POST", "PATCH", "PUT", "DELETE"]
  });

  await app.register(multipart, {
    limits: {
      fileSize: 5 * 1024 * 1024, // 5 MB
      files: 1,
      fields: 0,
      parts: 1
    }
  });

  app.get("/health", async () => {
    return { status: "ok" };
  });

  app.register(plantRoutes, {
    prefix: "/v1/plants"
  });

  app.register(plantImageRoutes, {
    prefix: "/v1/plants"
  });

  app.register(taskRoutes, {
    prefix: "/v1/tasks"
  });

  return app;
}
