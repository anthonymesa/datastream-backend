FROM python:3.8

# This is the expected layout of the deployed apps folder
#
# /app
# ├── env
# │   └── (created by init_venv.py)
# ├── src
# │   └── (contents of your src folder)
# ├── scripts
# │   └── init_venv.py
# └── requirements.txt


COPY src /app/src
COPY scripts/init_venv.py /app/scripts/init_venv.py
COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN python scripts/init_venv.py

RUN pip install -r requirements.txt

CMD ["python", "src/webhook_server.py"]
