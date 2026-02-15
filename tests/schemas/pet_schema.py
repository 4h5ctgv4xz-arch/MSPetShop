PET_SCHEMA = {
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
    },
    "name": {
      "type": "string",
    },
    "category": {
      "type": "object",
      "properties": {
        "id": {
          "type": "integer",
        },
        "name": {
          "type": "string",
        }
      },
      "required": ["id", "name"],
      "additionalProperties": False
    },
    "photoUrls": {
      "type": "array",
      "items": {
        "type": "string",
        "format": "uri"
      },
      "minItems": 0
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "integer",
            "minimum": 0
          },
          "name": {
            "type": "string",
            "minLength": 1
          }
        },
        "required": ["id", "name"],
        "additionalProperties": False
      },
      "minItems": 0
    },
    "status": {
      "type": "string",
      "enum": ["available", "pending", "sold"]
    }
  },
  "required": ["id", "name", "status"],
  "additionalProperties": False
}