export FLASK_APP=event_planner
export FLASK_DEBUG=True
export PYTHONPATH=$(CURDIR)/src

.PHONY: run docs migrate purge

run:
	flask run -h 0.0.0.0
docs:
	cd src && python3 -m pydoc -w ./
	cd src && mv -v *.html ../docs
migrate:
	flask migrate
purge:
	flask purge