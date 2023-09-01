#!/bin/bash

export PYTHONPATH=$PYTHONPATH:"/Users/ashfordhastings/PythonProjects/Practice Projects/prac-29-speed-api-1":"/Users/ashfordhastings/PythonProjects/Practice Projects/prac-29-speed-api-1/MetadataService"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source .venv/bin/activate

alembic downgrade base
echo "DB schema downgraded."


alembic upgrade head
echo "DB schema initialized."

python3 "$DIR/factory_boy/md/md_seed.py"
echo "Metadata seeded."

python3 "$DIR/factory_boy/auth/auth_seed.py"
echo "Auth seeded."


echo "Database has been reset to a known state."