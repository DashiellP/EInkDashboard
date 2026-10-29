
import { buildApp } from "./app.js";
import { loadConfig } from "./config.js"
import { pool } from "./db/pool.js"

const config = loadConfig();
const app = await buildApp();

app.addHook("onClose", async () => {
  await pool.end();
});

try {
  await app.listen({
    port: config.port,
    host: config.host
  });
} catch (error) {
  app.log.error(error);
  process.exit(1);
}