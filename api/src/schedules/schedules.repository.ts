import { Pool, QueryArrayResult } from "pg";
import { pool } from "../db/pool.js";

interface UpdateScheduleInput {
  name?: string;
}

export class ScheduleRepository
{
    constructor(
        private readonly pool: Pool
    ) {}

    async getAll()
    {
        const query = "SELECT * FROM plant_task_schedules WHERE True;"
        const result = await this.query(query);
        return result?.rows;
    }

    async getById(id: number)
    {
        const query = "SELECT * FROM plant_task_schedules WHERE id=$1;"
        const args = [id];
        const result = await this.query(query, args);
        if (result.rows.length)
            return result.rows[0];
        return [];
    }

    async getDue()
    {
        // const query = "SELECT * FROM plant_task_schedules WHERE id=$1;"
        // const args = [id];
        // const result = await this.query(query, args);
        // if (result.rows.length)
        //     return result.rows[0];
        return [];
    }

    async add(name: string, plantId: number, taskId: number, frequencyDays: number)
    {
        const query = "INSERT INTO plant_task_schedules (name, plantId, taskId, frequencyDays) VALUES ($1, $2, $3, $4) RETURNING id;";
        const args = [name, plantId, taskId, frequencyDays];
        const result = await this.query(query, args);
        if (result.rows.length)
            return result.rows[0];
        return [];
    }

    async update(
        id: number,
        input: UpdateScheduleInput
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
            UPDATE plant_task_schedules
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
        const query = "DELETE * FROM plant_task_schedules WHERE id=$1;"
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

export const scheduleRepository = new ScheduleRepository(pool);