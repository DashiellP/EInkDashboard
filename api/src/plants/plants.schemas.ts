export interface UpdatePlantBody {
  name?: string;
  imagePath?: string | null;
}

export interface PlantParams {
  id: string;
}

export const updatePlantSchema = {
  params: {
    type: "object",
    required: ["id"],
    properties: {
      id: {
        type: "string",
        pattern: "^[1-9][0-9]*$"
      }
    }
  },
  body: {
    type: "object",
    minProperties: 1,
    additionalProperties: false,
    properties: {
      name: {
        type: "string",
        minLength: 1,
        maxLength: 255
      },
      imagePath: {
        anyOf: [
          { type: "string", maxLength: 1024 },
          { type: "null" }
        ]
      }
    }
  }
} as const;
