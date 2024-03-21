import flask
from flask import Flask, jsonify, make_response, request
from . import db_session
from .jobs import Jobs


app = Flask(__name__)
blueprint = flask.Blueprint('news_api', __name__, template_folder='templates')


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(blueprint)
    app.run()


@blueprint.route('/api/jobs/<int:job_id>')
def get_jobs(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get({'id': job_id})
    if not jobs:
        return {"error": 'Not found'}
    return jsonify(
        {'news': [item.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', \
                                     'end_date', 'is_finished')) for item in jobs]}
    )


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {'news': [item.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', \
                                     'end_date', 'is_finished')) for item in jobs]}
    )


@blueprint.route('/api/jobs', methods=['POST'])
def add_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    jobs = Jobs(
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'id': jobs.id})


if __name__ == "__main__":
    main()