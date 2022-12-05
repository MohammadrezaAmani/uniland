import threading
from uniland import SESSION, search_engine
from uniland.db.tables import Submission
from uniland.db import user_methods as user_db
from uniland.utils.enums import UserLevel

"""
Submission Class Properties:
	- id: int
	- submission_data: datetime
	- is_confirmed: bool
	- faculty: str
	- search_text: str
	- description: str
	- correspondent_admin: int - -> fk user.user_id
	- owner: int - -> fk user.user_id
"""

SUBMISSION_INSERTION_LOCK = threading.RLock()

def increase_search_times(id: int):
	with SUBMISSION_INSERTION_LOCK:
		submission = SESSION.query(Submission).filter(Submission.id == id).first()
		if submission:
			submission.search_times += 1
			search_engine.increase_search_times(id)
			SESSION.commit()
		SESSION.close()

def get_submission(submission_id: int):
	return SESSION.query(Submission).filter(Submission.id == submission_id).first()
