ORDER_SCHEMA = {
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "format": "int64",
      "example": 10
    },
    "petId": {
      "type": "integer",
      "format": "int64",
      "example": 198772
    },
    "quantity": {
      "type": "integer",
      "format": "int32",
      "example": 7
    },
    "shipDate": {
      "type": "string",
      "format": "date-time"
    },
    "status": {
      "type": "string",
      "description": "Order Status",
      "enum": ["placed", "approved", "delivered"],
      "example": "approved"
    },
    "complete": {
      "type": "boolean"
    }
  },
  "required": ["id", "petId", "quantity", "status", "complete"],
  "additionalProperties": False,
  "xml": {
    "name": "order"
  }
}