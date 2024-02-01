To run this project locally

Step 1: git clone git@github.com:olartbaraq/chathome.git (if using ssh) and activate a new python environment

Step 2: install redis server - ubuntu - sudo apt install redis-server && sudo systemctl restart redis.service - windows - use docker compose file with docker GUI app - macOS - brew install redis && brew services start redis

Step 3: cd into the cloned directory and run <b>(pip install -r requirements.txt)</b>

Step 4: run python manage.py makemigrations

Step 5: run python manage.py migrate

Step 6: run python manage.py runserver

Proceed to run the Frontend repo after this
