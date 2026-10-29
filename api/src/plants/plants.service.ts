import { PlantRepository, plantRepository } from "./plants.repository.js";

class PlantService {
  constructor(
    private readonly repository: PlantRepository
  ) {}

  async getPlant(id: number): Promise<any[][]>
  {
    return this.repository.getById(id);
  }
  
  async getAllPlants(): Promise<any[][]>
  {
    return this.repository.getAll();
  }

  async addPlant(name: string): Promise<any[][]>
  {
    return this.repository.add(name)
  }

  async updatePlant(id: number, name?: string, imagePath?: string)
  {
    if (typeof name == "undefined" && typeof imagePath == "undefined")
    {
      throw new Error("No fields to update");
    }
    return this.repository.update(id, {name: name, imagePath: imagePath})
  }
}

export const plantService = new PlantService(plantRepository);