import { Pool, QueryArrayResult } from "pg";
import { pool } from "../db/pool.js";

interface UpdatePlantInput {
  name?: string;
  imagePath?: string | null;
}

export class PlantRepository
{
    constructor(
        private readonly pool: Pool
    ) {}

    async getAll(): Promise<any[][]>
    {
        const query = "SELECT * FROM plants WHERE True;"
        const result = await this.query(query);
        if (result.rows.length)
            return result.rows;
        return [];
    }

    async getById(id: number): Promise<any[][]>
    {
        const query = "SELECT * FROM plants WHERE id=$1;"
        const args = [id];
        const result = await this.query(query, args);
        if (result.rows.length)
            return result.rows[0];
        return [];
    }

    async add(name: string): Promise<any[][]>
    {
        const query = "INSERT INTO plants (name) VALUES ($1) RETURNING id;";
        const args = [name];
        const result = await this.query(query, args);
        if (result.rows.length)
            return result.rows[0];
        return [];
    }

    async update(
        id: number,
        input: UpdatePlantInput
    )
    {
        const updates: string[] = [];
        const values: unknown[] = [];

        if (input.name !== undefined) {
            values.push(input.name);
            updates.push(`name = $${values.length}`);
        }

        if (input.imagePath !== undefined) {
            values.push(input.imagePath);
            updates.push(`image_path = $${values.length}`);
        }

        if (updates.length === 0) {
            throw new Error("No fields to update");
        }

        values.push(id);

        const result = await this.query(
            `
            UPDATE plants
            SET ${updates.join(", ")}
            WHERE id = $${values.length}
                AND deleted_at IS NULL
            RETURNING
                id,
                name,
                image_path AS "imagePath",
                created_at AS "createdAt"
            `,
            values
        );

        return result.rows[0] ?? null;
    }

    async delete(id: number)
    {
        const query = "DELETE * FROM Plants WHERE id=$1;"
        const args = [id];
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

export const plantRepository = new PlantRepository(pool);