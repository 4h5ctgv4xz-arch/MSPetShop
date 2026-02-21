INVENTORY_SCHEMA = {
    "type": "object",
    "properties": {
        "approved": {
            "type": "integer",
            "minimum": 0,
        },
        "placed": {
            "type": "integer",
            "minimum": 0,
        },
        "available": {
            "type": "integer",
            "minimum": 0,
        },
    }
}