import { ScheduleRepository, scheduleRepository } from "./schedules.repository.js";

class ScheduleService {
  constructor(
    private readonly repository: ScheduleRepository
  ) {}

  async getSchedule(id: number) 
  {
    return this.repository.getById(id);
  }

  async getAllSchedules(): Promise<any[][]>
  {
    return this.repository.getAll();
  }

  async addSchedule(name: string, plantId: number, taskId: number, frequencyDays: number)
  {
    return this.repository.add(name, plantId, taskId, frequencyDays)
  }

  async updateSchedule(id: number, name?: string)
  {
    if (typeof name == "undefined")
    {
      throw new Error("No fields to update");
    }
    return this.repository.update(id, {name: name})
  }
}

export const scheduleService = new ScheduleService(scheduleRepository);