from db.db import db
from workers.assessment.assessment_worker import *

assessment_worker = AssessmentWorker('assessment_worker_test')
assessment_worker.set_db(db)
