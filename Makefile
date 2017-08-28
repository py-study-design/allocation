.PHONY: docs test

help:
	@echo "  env         create a development environment using virtualenv"
	@echo "  deps        install dependencies using pip"
	@echo "  lint        check style with flake8"
	@echo "  test        run all your tests using py.test"

env:
	sudo easy_install pip && \
	pip install virtualenv && \
	virtualenv env && \
	. env/bin/activate && \
	make deps

deps:
	pip install -r requirements.txt

lint:
	flake8 --exclude=env .

test:
	py.test allocation