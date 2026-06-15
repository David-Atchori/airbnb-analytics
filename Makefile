.PHONY: install run-bronze run-silver run-gold run-all test docs app

install:
	pip install -r requirements.txt

run-bronze:
	dbt run --select bronze

run-silver:
	dbt run --select silver

run-gold:
	dbt run --select gold

run-all:
	dbt run

test:
	dbt test

docs:
	dbt docs generate && dbt docs serve

app:
	streamlit run streamlit/app.py
