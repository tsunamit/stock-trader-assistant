default: assistant

init:
	pip3 install -r requirements.txt

assistant:
	clear
	python3 assistant.py

scrape:
	python3 assistant.py > out
  

