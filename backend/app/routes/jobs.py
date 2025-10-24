from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.job import Job
from flask_jwt_extended import jwt_required

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

# GET all jobs (with pagination)
@jobs_bp.route('/', methods=['GET'])
def get_jobs():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    jobs = Job.query.paginate(page=page, per_page=per_page)
    return jsonify({
        "jobs": [job.to_dict() for job in jobs.items],
        "total": jobs.total,
        "pages": jobs.pages,
    }), 200

# GET a single job by ID
@jobs_bp.route('/<int:id>', methods=['GET'])
def get_job(id):
    job = Job.query.get_or_404(id)
    return jsonify(job.to_dict()), 200

# CREATE a job
@jobs_bp.route('/', methods=['POST'])
@jwt_required()
def create_job():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title or not description:
        return jsonify({"error": "Title and description required"}), 400

    job = Job(title=title, description=description)
    db.session.add(job)
    db.session.commit()
    return jsonify(job.to_dict()), 201

# UPDATE a job
@jobs_bp.route('/<int:id>', methods=['PATCH'])
@jwt_required()
def update_job(id):
    job = Job.query.get_or_404(id)
    data = request.get_json()
    job.title = data.get('title', job.title)
    job.description = data.get('description', job.description)
    db.session.commit()
    return jsonify(job.to_dict()), 200

# DELETE a job
@jobs_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_job(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    return jsonify({"message": "Job deleted"}), 200
