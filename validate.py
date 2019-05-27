import json
import sys
import os
from jsonschema import validate

if len(sys.argv) != 2:
    print("The script expects an argument which is the path to the dataset file")
    sys.exit(1)
elif not os.path.exists(sys.argv[1]):
    print("The file doesn't exist")
    sys.exit(1)


try:
    with open(sys.argv[1]) as f:
        dataset = json.load(f)
except:
    print("The file doesn't have the JSON format")

if not isinstance(dataset, list):
    print("The json should contain a list of entries at the root")
    sys.exit(1)




schema = {
    "type": "object",
    "properties" : {
        "replies" : {
            "type": "array",
            "maxItems": 4,
            "minItems": 3,
            "items": {
                "type": "array",
                "items" : {
                    "type": "object",
                    "properties" : {
                        "pos": {"type": "string"}, #"pattern": r"^(\$|:|#|\.|[A-Z]{2,3}\$?)$"},
                        "word": {"type": "string"},# "pattern": r"^(\w+|<w+>)$"},
                        "lemma": {"type": "string"},# "pattern": r"^(\w+|<w+>)$"},
                        "synonyms": {"type": "array", "items": { "type": "string" } }
                    },
                    "additionalProperties": {
                        "best_syn": {"type": "string", "pattern": r"^(\w+|<w+>)$"}
                    }
                }
            }
        },
        "emotion": {
            "type": "string",
            "pattern": r"^(sad|happy|others|angry)$"
        },
        "sentiments": {
            "type": "array",
            "maxItems": 4,
            "minItems": 3,
            "items": {"type":"string", "pattern": "^(neg|pos|neutral|unknown)$"}
        },
        "capslock": {"type": "boolean"},
        "topics": {"type": "string"}
    }
}

for i in range(0, len(dataset)):
    try:
        validate(instance=dataset[i], schema=schema)
    except Exception as err:
        print("Error at entry {}:".format(str(i)))
        raise err

print("The dataset is valid")

