from flask_restful import reqparse, abort, Api, Resource
from flask import *
from . import db_session
from .problems import Problems

def abort_if_problems_not_found(problems_id):
    session = db_session.create_session()
    problems = session.query(Problems).get(problems_id)
    if not problems:
        abort(404, message=f"News {problems_id} not found")

class ProblemResource(Resource):
    def get(self, problem_id):
        abort_if_problems_not_found(problem_id)
        session = db_session.create_session()
        problem = session.query(Problems).get(problem_id)
        return jsonify({'problem': problem.to_dict(
            only=('title', 'author_id', 'author.username', 'description',
                'input_description', 'output_description', 'difficult',
                'example_count', 'test_count', 'post_date'))})

    def delete(self, problem_id):
        abort_if_problems_not_found(problem_id)
        session = db_session.create_session()
        problem = session.query(Problems).get(problem_id)
        session.delete(problem)
        session.commit()
        return jsonify({'success': 'OK'})

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('description', required=True)
parser.add_argument('author_id', required=True, type=int)
parser.add_argument('input_description', required=True)
parser.add_argument('output_description', required=True)
parser.add_argument('difficult', required=True, type=int)
parser.add_argument('time_needed', required=True, type=int)
parser.add_argument('memory_needed', required=True, type=int)
parser.add_argument('example_count', required=True, type=int)
parser.add_argument('test_count', required=True, type=int)

class ProblemListResource(Resource):
    def get(self):
        session = db_session.create_session()
        problems = session.query(Problems).all()
        return jsonify({'problems': [item.to_dict(
            only=('title', 'author.username', 'difficult', 'post_date')) for item in problems]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
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
        session.add(problem)
        session.commit()
        return jsonify({'success': 'OK'})