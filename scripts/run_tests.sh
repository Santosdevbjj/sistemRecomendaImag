#!/bin/bash

# Roda pytest e coleta dados de cobertura
coverage run --source=src,tests -m pytest --maxfail=1 --disable-warnings

# Gera relatório de cobertura em formato XML
coverage xml -o /app/coverage.xml
