import { TaskRepository, taskRepository } from "./tasks.repository.js";

class TaskService {
  constructor(
    private readonly repository: TaskRepository
  ) {}

  async getTask(id: number) 
  {
    return this.repository.getById(id);
  }

  async getAllTasks(): Promise<any[][]>
  {
    return this.repository.getAll();
  }

  async addTask(name: string)
  {
    return this.repository.add(name)
  }

  async updateTask(id: number, name?: string)
  {
    if (typeof name == "undefined")
    {
      throw new Error("No fields to update");
    }
    return this.repository.update(id, {name: name})
  }
}

export const taskService = new TaskService(taskRepository);