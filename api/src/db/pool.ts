import { Pool } from "pg";
import { loadConfig } from "../config.js";

const config = loadConfig();

export const pool = new Pool({
  connectionString: config.databaseUrl,
});
