run: 
	python main.py

install:
	pip install -r requirements.txt

init_db:
	python database.py

test:
	python test.py