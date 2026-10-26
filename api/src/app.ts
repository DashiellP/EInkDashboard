import Fastify from "fastify";
import { plantRoutes } from "./routes/plants.routes.js";

export function buildApp() {
  const app = Fastify({
    logger: true
  });

  app.get("/health", async () => {
    return { status: "ok" };
  });

  app.register(plantRoutes, {
    prefix: "/v1/plants"
  });

  return app;
}
