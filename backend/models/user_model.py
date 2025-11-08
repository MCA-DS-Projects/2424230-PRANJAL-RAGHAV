from bson import ObjectId

# Utility function to clean Mongo user data before returning JSON
def serialize_user(user):
    return {
        "id": str(user["_id"]),
        "fullName": user.get("fullName"),
        "email": user.get("email"),
        "phone": user.get("phone", ""),
        "healthGoals": user.get("healthGoals", []),
    }
