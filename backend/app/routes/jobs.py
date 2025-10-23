from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models.job import Job

jobs_bp = Blueprint("jobs", __name__)

#  Create a new job
@jobs_bp.route("/", methods=["POST"])
def create_job():
    data = request.get_json()
    required_fields = ["title", "company", "location", "description"]

    # Validation
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    job = Job(
        title=data["title"],
        company=data["company"],
        location=data["location"],
        description=data["description"],
        salary=data.get("salary"),
    )
    db.session.add(job)
    db.session.commit()
    return jsonify(job.to_dict()), 201


#  Read (List all jobs with pagination)
@jobs_bp.route("/", methods=["GET"])
def get_jobs():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))
    jobs = Job.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "jobs": [job.to_dict() for job in jobs.items],
        "total": jobs.total,
        "pages": jobs.pages,
        "current_page": jobs.page
    })


#  Get a single job
@jobs_bp.route("/<int:id>", methods=["GET"])
def get_job(id):
    job = Job.query.get_or_404(id)
    return jsonify(job.to_dict())


#  Update a job
@jobs_bp.route("/<int:id>", methods=["PUT"])
def update_job(id):
    job = Job.query.get_or_404(id)
    data = request.get_json()

    for field in ["title", "company", "location", "description", "salary"]:
        if field in data:
            setattr(job, field, data[field])

    db.session.commit()
    return jsonify(job.to_dict())


#  Delete a job
@jobs_bp.route("/<int:id>", methods=["DELETE"])
def delete_job(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    return jsonify({"message": "Job deleted successfully"})
