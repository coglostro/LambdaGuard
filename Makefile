install:
	python3 setup.py install

test:
	python3 -m pytest -W ignore

dev:
	python3 -m venv dev
	echo "\nNow run: \n\n. dev/bin/activate\n"

install-dev:
	python3 setup.py develop
	pip3 install pytest

clean:
	set -e
	find . -iname "dist" -exec rm -rf {} \;
	find . -iname "build" -exec rm -rf {} \;
	find . -iname "dev" -exec rm -rf {} \;
	find . -iname "*.DS_Store*" -exec rm -rf {} \;
	find . -iname "*__pycache__*" -exec rm -rf {} \;
	find . -iname "*.pytest_cache*" -exec rm -rf {} \;
	find . -iname "lambdaguard.egg-info" -exec rm -rf {} \;
	find . -iname "lambdaguard_output" -exec rm -rf {} \;
	python3 setup.py clean
	sudo pip3 uninstall lambdaguard

dist:
	rm -rf dist
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*

test-pip:
	python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps lambdaguard

sonarqube:
	docker build -t sonarqube -f SonarQube.Dockerfile .
	docker run -d -p 9000:9000 sonarqube
	python3 sonarqube-setup.py

.PHONY: clean dist