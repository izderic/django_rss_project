======
README
======


Setup instructions
------------------

1. Create and activate virtual environment ``virtualenv -p python3 rss_env`` ``source rss_env/bin/activate``

2. Clone the repository ``git clone https://github.com/izderic/django_rss_project.git``

3. Move to project directory ``cd django_rss_project``

4. Install the requirements ``pip install -r requirements.txt``

5. Create the database with ``python manage.py migrate``

6. Run the server ``python manage.py runserver``

7. Navigate to ``http://127.0.0.1:8000/``


About
-----

This app fetches RSS feed data from configured addresses. Each word is stored in db with the number of occurences, by feed and total. Data is fetched only for active feeds. Status is configured in the feed list page.


Management command for saving to database
-----------------------------------------

    ``python manage.py save_feed_data`
