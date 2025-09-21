# scripts/run_tests.sh
#!/bin/bash

# Roda pytest e coleta dados de cobertura, salvando no diretório mapeado
coverage run --source=src,tests -m pytest --maxfail=1 --disable-warnings
