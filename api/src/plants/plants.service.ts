import { PlantRepository, plantRepository } from "./plants.repository.js";

class PlantService {
  constructor(
    private readonly repository: PlantRepository
  ) {}

  async getPlant(id: number) 
  {
    return this.repository.getById(id);
  }

  async addPlant(name: string, imageData: string)
  {
    return this.repository.add(name, "")
  }
}

export const plantService = new PlantService(plantRepository);