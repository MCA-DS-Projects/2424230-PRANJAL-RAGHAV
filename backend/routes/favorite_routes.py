# backend/routes/favorite_routes.py
from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId, errors as bson_errors

favorites_bp = Blueprint("favorites", __name__, url_prefix="/api/users")

def _db():
    return current_app.extensions["pymongo"].db

def _oid(s):
    return ObjectId(s)

@favorites_bp.route("/<user_id>/favorites", methods=["GET"])
def get_favorites(user_id):
    db = _db()
    try:
        uoid = _oid(user_id)
    except bson_errors.InvalidId:
        return jsonify({"error": "Invalid user id"}), 400

    user = db.users.find_one({"_id": uoid}, {"favorites": 1})
    if not user:
        return jsonify({"error": "User not found"}), 404

    fav_ids = user.get("favorites", [])
    expand = request.args.get("expand", "false").lower() == "true"
    if not expand:
        return jsonify({"favorites": fav_ids}), 200

    # Expand foods
    oids = []
    for fid in fav_ids:
        try:
            oids.append(_oid(fid))
        except Exception:
            continue

    foods = list(db.foods.find({"_id": {"$in": oids}}))
    for f in foods:
        f["_id"] = str(f["_id"])
    return jsonify({"items": foods}), 200

@favorites_bp.route("/<user_id>/favorites", methods=["POST"])
def add_favorite(user_id):
    db = _db()
    body = request.get_json(force=True)
    food_id = body.get("foodId")
    if not food_id:
        return jsonify({"error": "foodId required"}), 400

    try:
        uoid = _oid(user_id)
        _ = _oid(food_id)  # validate
    except bson_errors.InvalidId:
        return jsonify({"error": "Invalid id"}), 400

    # Upsert user if not present; add to set
    db.users.update_one(
        {"_id": uoid},
        {"$addToSet": {"favorites": food_id}},
        upsert=True
    )
    return jsonify({"message": "added"}), 200

@favorites_bp.route("/<user_id>/favorites/<food_id>", methods=["DELETE"])
def remove_favorite(user_id, food_id):
    db = _db()
    try:
        uoid = _oid(user_id)
        _ = _oid(food_id)
    except bson_errors.InvalidId:
        return jsonify({"error": "Invalid id"}), 400

    db.users.update_one({"_id": uoid}, {"$pull": {"favorites": food_id}})
    return jsonify({"message": "removed"}), 200
