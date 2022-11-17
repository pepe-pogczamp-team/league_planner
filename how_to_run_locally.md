### 1. prerequisites:
* python
* postgres

### 2. setup db:

| **field** | **value**     |
|:----------|---------------|
| name      | league_planner |
| user      | postgres      |
| password  | postgres      |
| port      | 5432          |

### 3. install requirements from requirements.txt
    $ pip install --upgrade pip
    $ pip install -r requirements.txt

### 4. run migrations
    $ python manage.py migrate

### 5. run server
    $ python manage.py runserver 8000
