echo "Creating database..."
createdb ohtu || exit 1

echo "Adding schema"
psql -d ohtu < sql/schema.sql
echo "Prepopulating"
psql -d ohtu < sql/populate.sql

echo "Installing dependencies"
poetry install || exit 1

echo "Running flask server"
poetry run flask --app src/app run --debug
