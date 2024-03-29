#!/bin/bash
echo "Flushing the manage.py command"
while ! python manage.py flush --no-input 2>&1; do
    sleep 3
done

echo "Migrating the DB"
while ! python manage.py migrate 2>&1; do
    sleep 4
done

echo "Adding the ingredients to DB"
while ! python manage.py add_ingredients 2>&1; do
    sleep 10
done

echo "Adding the admin group to DB"
while ! python manage.py add_admin_group 2>&1; do
    sleep 3
done

echo "Adding users to DB"
while ! python manage.py add_users 2>&1; do
    sleep 3
done

echo "Adding recipes to DB"
while ! python manage.py add_recipes 2>&1; do
    sleep 3
done

echo "Adding static files"
while ! python manage.py collectstatic --noinput 2>&1; do
    sleep 3
done

exec "$@"