import { Pool, QueryArrayResult } from "pg";
import { pool } from "../db/pool.js";

interface UpdateTaskInput {
  name?: string;
}

export class TaskRepository
{
    constructor(
        private readonly pool: Pool
    ) {}

    async getAll()
    {
        const query = "SELECT * FROM plant_tasks WHERE True;"
        const result = await this.query(query);
        return result?.rows;
    }

    async getById(id: number)
    {
        const query = "SELECT * FROM plant_tasks WHERE id=$1;"
        const args = [id];
        const result = await this.query(query, args);
        if (result.rows.length)
            return result.rows[0];
        return [];
    }

    async add(name: string)
    {
        const query = "INSERT INTO plant_tasks (name) VALUES ($1) RETURNING id;";
        const args = [name];
        const result = await this.query(query, args);
        if (result.rows.length)
            return result.rows[0];
        return [];
    }

    async update(
        id: number,
        input: UpdateTaskInput
    )
    {
        const updates: string[] = [];
        const values: unknown[] = [];

        if (input.name !== undefined) {
            values.push(input.name);
            updates.push(`name = $${values.length}`);
        }

        if (updates.length === 0) {
            throw new Error("No fields to update");
        }

        values.push(id);

        const result = await this.query(
            `
            UPDATE plant_tasks
            SET ${updates.join(", ")}
            WHERE id = $${values.length}
            RETURNING
                id,
                name
            `,
            values
        );

        return result.rows[0] ?? null;
    }

    async delete(id: number)
    {
        const query = "DELETE * FROM plant_tasks WHERE id=$1;"
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

export const taskRepository = new TaskRepository(pool);