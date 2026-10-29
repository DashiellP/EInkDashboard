import { MultipartFile } from "@fastify/multipart";
import { PlantImageRepository, plantImageRepository } from "./plant_images.repository.js";
import { randomUUID } from "node:crypto";

class PlantImageService {
  constructor(
    private readonly repository: PlantImageRepository
  ) {}
  
  allowedTypes: Record<string, string> = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp"
  };

  async addImage(plantId: number, file: MultipartFile)
  {
    const extension = this.allowedTypes[file.mimetype];
    if (!extension) {
        file.file.resume();
        throw "Unsupported image type";
    }
    const filename = `${randomUUID()}${extension}`;

    try {
        const imagePath = await this.repository.add(plantId, filename, file)
        return imagePath;
    } catch (error) {
        throw error;
    }
  }
}

export const plantImageService = new PlantImageService(plantImageRepository);