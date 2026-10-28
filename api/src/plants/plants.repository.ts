import { Pool, QueryArrayResult } from "pg";
import { pool } from "../db/pool.js";

export class PlantRepository
{
    constructor(
        private readonly pool: Pool
    ) {}

    async getAll()
    {
        const query = "SELECT * FROM Plants WHERE True;"
        const result = await this.query(query);
        return result?.rows;
    }

    async getById(id: number)
    {
        const query = "SELECT * FROM Plants WHERE Id=$1;"
        const args = [id];
        const result = await this.query(query, args);
        if (result.rows.length)
            return result.rows[0];
        return [];
    }

    async add(name: string, imagePath: string)
    {
        const query = "INSERT INTO plants (name, image_path) VALUES ($1, $2) RETURNING Id;";
        const args = [name, imagePath];
        const result = await this.query(query, args);
        if (result.rows.length)
            return result.rows[0];
        return [];
    }

    async update(id: number, updatedValues: Partial<PlantEntry>)
    {
        const query = ";";
        const args = [...Object.keys(updatedValues), ...Object.values(updatedValues)];
        const result = await this.query(query, args);
        if (result.rows.length)
            return result.rows[0];
        return [];
    }

    async query(queryString: string, args: any[] = []): Promise<QueryArrayResult<any[]>>
    {
        const result = await this.pool.query(
            queryString,
            args
        );

        return result;
    }
}

type PlantEntry = {
    id: number,
    name: string,
    imagePath: string,
    createdAt: string,
    deletedAt: string
}

export const plantRepository = new PlantRepository(pool);