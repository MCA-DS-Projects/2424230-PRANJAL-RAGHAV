# # backend/routes/food_routes.py
# from flask import Blueprint, request, jsonify, current_app
# from bson import ObjectId, errors as bson_errors
# from backend.db import db

# import os
# import re

# food_bp = Blueprint("foods", __name__, url_prefix="/api/foods")

# def _db():
#     return current_app.extensions["mongo"].db


# def _as_str_id(doc):
#     if doc and "_id" in doc:
#         doc["_id"] = str(doc["_id"])
#     return doc

# # Build Mongo filter from query params
# def _build_filter(args):
#     q = {}

#     # mealType / properties / region can be comma-separated; fields are arrays in docs
#     def parse_multi(name):
#         val = args.get(name)
#         if not val:
#             return None
#         items = [v.strip().lower() for v in val.split(",") if v.strip()]
#         return items or None

#     meal_types = parse_multi("mealType")
#     properties = parse_multi("properties")
#     regions = parse_multi("region")

#     if meal_types:
#         q["mealType"] = {"$in": meal_types}
#     if properties:
#         q["properties"] = {"$in": properties}
#     if regions:
#         q["region"] = {"$in": regions}

#     # search on name + description (case-insensitive)
#     search = args.get("search", "").strip()
#     if search:
#         rx = re.compile(re.escape(search), re.IGNORECASE)
#         q["$or"] = [{"name": rx}, {"description": rx}]

#     return q

# @food_bp.route("/", methods=["GET"])
# def list_foods():
#     db = _db()
#     page = max(int(request.args.get("page", 1)), 1)
#     limit = min(max(int(request.args.get("limit", 30)), 1), 100)  # cap at 100
#     q = _build_filter(request.args)

#     total = db.foods.count_documents(q)
#     cursor = (
#         db.foods
#         .find(q, {"_id": 1, "name": 1, "image": 1, "mealType": 1, "properties": 1,
#                   "region": 1, "description": 1, "prepTime": 1, "bodyTypeMsg": 1})
#         .sort([("name", 1)])
#         .skip((page - 1) * limit)
#         .limit(limit)
#     )
#     items = [_as_str_id(doc) for doc in cursor]
#     return jsonify({"items": items, "page": page, "limit": limit, "total": total}), 200

# # @food_bp.route("/<food_id>", methods=["GET"])
# # def get_food(food_id):
# #     db = _db()
# #     try:
# #         oid = ObjectId(food_id)
# #     except bson_errors.InvalidId:
# #         return jsonify({"error": "Invalid id"}), 400

# #     doc = db.foods.find_one({"._id": 1})  # safeguard no accidental projection
# #     doc = db.foods.find_one({"_id": oid})
# #     if not doc:
# #         return jsonify({"error": "Not found"}), 404
# #     return jsonify(_as_str_id(doc)), 200


# @food_bp.route("/<food_id>", methods=["GET"])
# def get_food(food_id):
#     db = _db()
#     try:
#         oid = ObjectId(food_id)
#     except bson_errors.InvalidId:
#         return jsonify({"error": "Invalid id"}), 400

#     doc = db.foods.find_one({"_id": oid})
#     if not doc:
#         return jsonify({"error": "Not found"}), 404
#     return jsonify(_as_str_id(doc)), 200


# # Admin create (optional)
# @food_bp.route("/", methods=["POST"])
# def create_food():
#     # Simple admin secret gate (optional)
#     admin_secret = os.getenv("ADMIN_SECRET")
#     if admin_secret and request.headers.get("X-ADMIN-SECRET") != admin_secret:
#         return jsonify({"error": "Unauthorized"}), 401

#     data = request.get_json(force=True)

#     # Normalize single vs multiple; store arrays
#     def ensure_array(val):
#         if val is None:
#             return []
#         if isinstance(val, list):
#             return [str(v).lower() for v in val]
#         return [str(val).lower()]

#     payload = {
#         "name": data.get("name", "").strip(),
#         "image": data.get("image", "").strip(),
#         "mealType": ensure_array(data.get("mealType")),      # e.g. ["breakfast","dinner"]
#         "properties": ensure_array(data.get("properties")),  # e.g. ["warming"]
#         "region": ensure_array(data.get("region")),          # e.g. ["indian"]
#         "description": data.get("description", "").strip(),
#         "prepTime": data.get("prepTime", "").strip(),
#         "bodyTypeMsg": data.get("bodyTypeMsg", "").strip(),
#         "benefits": data.get("benefits", []) or [],
#         "ingredients": data.get("ingredients", []) or []
#     }

#     if not payload["name"]:
#         return jsonify({"error": "name is required"}), 400

#     res = _db().foods.insert_one(payload)
#     return jsonify({"message": "food added", "id": str(res.inserted_id)}), 201

# @food_bp.route("/create-indexes", methods=["POST"])
# def create_indexes():
#     db = _db()
#     db.foods.create_index("name")
#     db.foods.create_index("description")
#     db.foods.create_index("mealType")
#     db.foods.create_index("properties")
#     db.foods.create_index("region")
#     return {"message": "indexes created"}
# backend/routes/food_routes.py
from flask import Blueprint, request, jsonify
from bson import ObjectId, errors as bson_errors
from backend.db import db
import os
import re

food_bp = Blueprint("foods", __name__, url_prefix="/api/foods")

def _db():
    return db

def _as_str_id(doc):
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

# # ===== CREATE INDEXES (run one time) =====
# @food_bp.route("/create-indexes", methods=["GET"])
# def create_indexes():
#     _db().foods.create_index("name")
#     _db().foods.create_index("description")
#     _db().foods.create_index("mealType")
#     _db().foods.create_index("properties")
#     _db().foods.create_index("region")
#     return {"message": "indexes created"}, 200


# ===== LIST FOODS =====
def _build_filter(args):
    q = {}

    def parse_multi(name):
        val = args.get(name)
        if not val:
            return None
        items = [v.strip().lower() for v in val.split(",") if v.strip()]
        return items or None

    meal_types = parse_multi("mealType")
    properties = parse_multi("properties")
    regions = parse_multi("region")

    if meal_types:
        q["mealType"] = {"$in": meal_types}
    if properties:
        q["properties"] = {"$in": properties}
    if regions:
        q["region"] = {"$in": regions}

    search = args.get("search", "").strip()
    if search:
        rx = re.compile(re.escape(search), re.IGNORECASE)
        q["$or"] = [{"name": rx}, {"description": rx}]

    return q


@food_bp.route("/", methods=["GET"])
def list_foods():
    page = max(int(request.args.get("page", 1)), 1)
    limit = min(max(int(request.args.get("limit", 30)), 1), 100)
    q = _build_filter(request.args)

    total = _db().foods.count_documents(q)
    cursor = (
        _db().foods
        .find(q, {"_id": 1, "name": 1, "image": 1, "mealType": 1, "properties": 1,
                  "region": 1, "description": 1, "prepTime": 1, "bodyTypeMsg": 1})
        .sort([("name", 1)])
        .skip((page - 1) * limit)
        .limit(limit)
    )
    items = [_as_str_id(doc) for doc in cursor]
    return jsonify({"items": items, "page": page, "limit": limit, "total": total}), 200


# ===== GET FOOD BY ID =====
@food_bp.route("/<food_id>", methods=["GET"])
def get_food(food_id):
    try:
        oid = ObjectId(food_id)
    except bson_errors.InvalidId:
        return jsonify({"error": "Invalid id"}), 400

    doc = _db().foods.find_one({"_id": oid})
    if not doc:
        return jsonify({"error": "Not found"}), 404
    return jsonify(_as_str_id(doc)), 200


# ===== ADMIN CREATE FOOD =====
@food_bp.route("/", methods=["POST"])
def create_food():
    admin_secret = os.getenv("ADMIN_SECRET")
    if admin_secret and request.headers.get("X-ADMIN-SECRET") != admin_secret:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(force=True)

    def ensure_array(val):
        if val is None:
            return []
        if isinstance(val, list):
            return [str(v).lower() for v in val]
        return [str(val).lower()]

    payload = {
        "name": data.get("name", "").strip(),
        "image": data.get("image", "").strip(),
        "mealType": ensure_array(data.get("mealType")),
        "properties": ensure_array(data.get("properties")),
        "region": ensure_array(data.get("region")),
        "description": data.get("description", "").strip(),
        "prepTime": data.get("prepTime", "").strip(),
        "bodyTypeMsg": data.get("bodyTypeMsg", "").strip(),
        "benefits": data.get("benefits", []) or [],
        "ingredients": data.get("ingredients", []) or []
    }

    if not payload["name"]:
        return jsonify({"error": "name is required"}), 400

    res = _db().foods.insert_one(payload)
    return jsonify({"message": "food added", "id": str(res.inserted_id)}), 201


# edit and delete 

@food_bp.route("/<food_id>", methods=["DELETE"])
def delete_food(food_id):
    from bson.objectid import ObjectId
    _db().foods.delete_one({"_id": ObjectId(food_id)})
    return jsonify({"message": "deleted"}), 200


@food_bp.route("/<food_id>", methods=["PUT"])
def update_food(food_id):
    from bson.objectid import ObjectId

    data = request.get_json(force=True)
    _db().foods.update_one({"_id": ObjectId(food_id)}, {"$set": data})
    return jsonify({"message": "updated"}), 200
