export FLASK_APP=event_planner
export FLASK_DEBUG=True
export PYTHONPATH=$(CURDIR)/src:$(CURDIR):/tests

.PHONY: run docs migrate purge test

run:
	flask run -h 0.0.0.0
docs:
	cd src && python3 -m pydoc -w ./
	cd src && mv -v *.html ../docs
migrate:
	flask migrate
purge:
	flask purge
test:
	echo $(PYTHONPATH)
	python3 -m unittest tests.unit
	python3 -m unittest tests.integration