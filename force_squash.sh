#! /bin/bash

rm ./test_deploy/orbach.sqlite3

./manage.py makemigrations
last_migration=$(ls -1 orbach/core/migrations/0*.py | tail -n1)
./manage.py squashmigrations --noinput core $(basename $last_migration .py)

rm orbach/core/migrations/0001_initial.py
mv orbach/core/migrations/0001* orbach/core/migrations/0001_initial.bk
rm orbach/core/migrations/000*.py
mv orbach/core/migrations/0001_initial.{bk,py}

sed -i -e '/replaces = .*/ { N; d; }' orbach/core/migrations/0001_initial.py

./manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" |  ./manage.py shell

