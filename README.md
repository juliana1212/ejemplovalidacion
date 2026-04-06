# CRUD Clientes

Proyecto ejemplo en Python para pruebas unitarias, cobertura y análisis con SonarQube.

## Crear entorno virtual
python -m venv .venv

## Activar entorno en Windows
.venv\Scripts\activate

## Instalar dependencias
pip install -r requirements.txt

## Ejecutar pruebas
pytest

## Ejecutar pruebas con cobertura
pytest --cov=src/clientes --cov-report=term-missing --cov-report=xml
