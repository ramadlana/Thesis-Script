python -m venv venv
venv\Scripts\activate

pip install fastapi
pip install "uvicorn[standard]"

## To Run Simulation thesis Script

1. Run Command to run uvicorn as Web Server
   `uvicorn main:app --reload`
2. then run python `python .\ping_check.py`
3. Adjust `ARRAY_LENGTH` in ping_check.py to fine tune array
