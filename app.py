from flask import Flask, jsonify, abort, make_response, request
from models import bibliotekus

app = Flask(__name__)
app.config["SECRET_KEY"] = "rampampam"


@app.route("/biblioteku/<int:bibi_id>", methods=["GET"])
def get_todo(bibi_id):
    biblioteku = bibliotekus.get(bibi_id)
    if not biblioteku:
        abort(404)
    return jsonify({"ksiazka": biblioteku})

@app.route("/biblioteku/<int:bibi_id>", methods=["POST"])
def create_todo():
    if not request.json or not 'tytuł' in request.json:
        abort(400)
    biblioteku = {
        'id': biblioteku.all()[-1]['id'] + 1,
        'tytul': request.json['tytul'],
        'gatunek': request.json.get('gatunek', ""),
        'strony': request.json['strony'],
        'done': False
    }
    biblioteku.create(biblioteku)
    return jsonify({'ksiazka': biblioteku}), 201

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.route("/biblioteku/<int:bibi_id>", methods=['DELETE'])
def delete_todo(bibi_id):
    result = bibliotekus.delete(bibi_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/biblioteku/<int:bibi_id>", methods=["PUT"])
def update_todo(bibi_id):
    biblioteku = biblioteku.get(bibi_id)
    if not biblioteku:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'tytul' in data and not isinstance(data.get('tytul'), str),
        'gatunek' in data and not isinstance(data.get('gatunek'), str),
        'strony' in data and not isinstance(data.get('strony'), str),
        'obejrzane' in data and not isinstance(data.get('obejrzane'), bool)
    ]):
        abort(400)
    biblioteku = {
        'tytul': data.get('tytul', biblioteku['tytul']),
        'gatunek': data.get('gatunek', biblioteku['gatunek']),
        'strony': data.get('strony', biblioteku['strony']),
        'obejrzane': data.get('obejrzane', biblioteku['obejrzane'])
    }
    biblioteku.update(bibi_id, biblioteku)
    return jsonify({'ksiazka': biblioteku})


if __name__ == "__main__":
    app.run(debug=True)