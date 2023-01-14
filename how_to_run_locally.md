# How to run server locally:

1. prerequisites:
   >python 3.10
   
   >postgres 15.1

2. setup db:

    | **field** | **value**     |
    |:----------|---------------|
    | name      | league_planner |
    | user      | postgres      |
    | password  | postgres      |
    | port      | 5432          |

3. create league_planner/.env file with all necessary variables e.g.
   * DJANGO_SECRET_KEY=<your_key>
   * WEATHER_API_SECRET_KEY=<your_key>
   * DB_NAME=league_planner
   * DB_USER=postgres
   * DB_PASSWORD=postgres
   * DB_HOST=127.0.0.1
   * DB_PORT=5432

4. install requirements from requirements.txt
   >$ pip install --upgrade pip
    
   >$ pip install -r requirements.txt

5. run migrations 
   >$ python manage.py migrate

6. run server
   >$ python manage.py runserver 8000
