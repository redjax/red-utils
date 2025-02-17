# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "msgpack",
#     "red-utils[msgpack]",
# ]
#
# [tool.uv.sources]
# red-utils = { path = "../../" }
# ///


from red_utils.ext import msgpack_utils


if __name__ == "__main__":
    serialized = msgpack_utils.msgpack_serialize({"hello": "world"})
    print(f"Serialized:\n{serialized}")
    deserialized = msgpack_utils.msgpack_deserialize(serialized.detail)
    print(f"Deserialized:\n{deserialized}")
