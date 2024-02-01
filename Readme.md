python -m venv venv
venv\Scripts\activate

pip install fastapi
pip install "uvicorn[standard]"

run
uvicorn main:app --reload
