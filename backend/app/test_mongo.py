from bson import ObjectId

# Replace with an actual file_id from MongoDB
test_id = "67b66fc0789aeef1566dd76b"

try:
    converted_id = ObjectId(test_id)
    print("Valid ObjectId:", converted_id)
except Exception as e:
    print("Invalid ObjectId:", e)
