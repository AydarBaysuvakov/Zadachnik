from flask import *
from . import db_session
from .problems import Problems

blueprint = Blueprint(
    'problems_api',
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/problems')
def get_problems():
    db_sess = db_session.create_session()
    problems = db_sess.query(Problems).all()
    return jsonify(
        {
            'problems':
                [item.to_dict(only=('title', 'author.username', 'difficult', 'post_date'))
                 for item in problems]
        }
    )

@blueprint.route('/api/problems/<int:problem_id>', methods=['GET'])
def get_one_problem(problem_id):
    db_sess = db_session.create_session()
    problem = db_sess.query(Problems).get(problem_id)
    if not problem:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'problem': problem.to_dict(only=(
                'title', 'author_id', 'author.username', 'description',
                'input_description', 'output_description', 'difficult',
                'example_count', 'test_count', 'post_date'))
        }
    )

@blueprint.route('/api/problems', methods=['POST'])
def add_problem():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'description', 'author_id', 'input_description', 'output_description', 'difficult',
                  'time_needed', 'memory_needed', 'example_count', 'test_count']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    problem = Problems(
        title=request.json['title'],
        description=request.json['description'],
        author_id=request.json['author_id'],
        input_description=request.json['input_description'],
        output_description=request.json['output_description'],
        difficult=request.json['difficult'],
        time_needed=request.json['time_needed'],
        memory_needed=request.json['memory_needed'],
        example_count=request.json['example_count'],
        test_count=request.json['test_count']
    )
    db_sess.add(problem)
    db_sess.commit()
    return jsonify({'success': 'OK'})

@blueprint.route('/api/problems/<int:problem_id>', methods=['DELETE'])
def delete_problem(problem_id):
    db_sess = db_session.create_session()
    problem = db_sess.query(Problems).get(problem_id)
    if not problem:
        return jsonify({'error': 'Not found'})
    db_sess.delete(problem)
    db_sess.commit()
    return jsonify({'success': 'OK'})

@blueprint.route('/api/problems/<int:problem_id>', methods=['PUT'])
def edit_problem(problem_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    db_sess = db_session.create_session()
    problem = db_sess.query(Problems).filter(Problems.id == problem_id).first()
    if not problem:
        return jsonify({'error': 'Id doesnt exists'})
    if 'title' in request.json:
        problem.title = request.json['title']
    if 'description' in request.json:
        problem.description = request.json['description']
    if 'author_id' in request.json:
        problem.author_id = request.json['author_id']
    if 'input_description' in request.json:
        problem.input_description = request.json['input_description']
    if 'output_description' in request.json:
        problem.output_description = request.json['output_description']
    if 'difficult' in request.json:
        problem.difficult = request.json['difficult']
    if 'time_needed' in request.json:
        problem.time_needed = request.json['time_needed']
    if 'memory_needed' in request.json:
        problem.memory_needed = request.json['memory_needed']
    if 'example_count' in request.json:
        problem.example_count = request.json['example_count']
    if 'test_count' in request.json:
        problem.test_count = request.json['test_count']
    db_sess.commit()
    return jsonify({'success': 'OK'})