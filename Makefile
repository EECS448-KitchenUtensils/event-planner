export FLASK_APP=event_planner
export FLASK_DEBUG=True
export PYTHONPATH=$(CURDIR)/src:$(CURDIR):/tests

.PHONY: run docs migrate purge test clean

run:
	EV_CONFIG=$(CURDIR)/src/event_planner/defaults.conf flask run -h 0.0.0.0
docs:
	cd documentation && pdoc --html event_planner --overwrite
migrate:
	EV_CONFIG=$(CURDIR)/src/event_planner/defaults.conf flask migrate
purge:
	EV_CONFIG=$(CURDIR)/src/event_planner/defaults.conf flask purge-db
test:
	echo $(PYTHONPATH)
	python3 -m unittest tests.unit
	python3 -m unittest tests.integration
clean:
	find . -name \*.pyc -delete
