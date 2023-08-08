FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Copier le modèle catboost.pkl dans l'image
# COPY model/catboost.pkl /app/catboost.pkl

# Copier les fichiers de dépendances et le code de l'application

COPY ./app /app/
# COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt



