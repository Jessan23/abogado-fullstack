rm -R -f ./migrations &&
pipenv run init &&
dropdb -h localhost -U postgres abogado-web || true &&
createdb -h localhost -U postgres abogado-web || true &&
psql -h localhost abogado-web -U postgres -c 'CREATE EXTENSION unaccent;' || true &&
pipenv run migrate &&
pipenv run upgrade
