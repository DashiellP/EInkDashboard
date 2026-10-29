import { Pool, QueryArrayResult } from "pg";
import { pool } from "../db/pool.js";
import { MultipartFile } from "@fastify/multipart";
import { unlink } from "node:fs/promises";
import { pipeline } from "node:stream/promises";
import { createWriteStream } from "node:fs";
import { mkdir } from "node:fs/promises";
import path from "node:path";

export class PlantImageRepository
{
    uploadDir = "uploads/plants";

    constructor(
        private readonly pool: Pool
    ) {}

    async add(plantId: number, filename: string, file: MultipartFile)
    {
        const destination = path.join(this.uploadDir, plantId + "", filename);
        await mkdir(path.join(this.uploadDir, plantId + ""), { recursive: true });
        await pipeline(
            file.file,
            createWriteStream(destination, {
                flags: "wx"
            })
        );

        if (file.file.truncated) {
            throw "Image exceeds 5 MB";
        }
        return destination;
    }

    async delete(path: string)
    {
        await unlink(path).catch(() => {});
    }
}

export const plantImageRepository = new PlantImageRepository(pool);