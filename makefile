VENV = .venv

setup:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

test:
	$(VENV)/bin/python -m unittest discover -s tests -p "test_*.py" -v

perf:
	$(VENV)/bin/python -m scripts.minhash_perf
