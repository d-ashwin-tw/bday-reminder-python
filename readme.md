
# Birthday Reminder

Inhouse Project to remind the admin regarding any upcoming Birthday's


[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/) ![Website](https://img.shields.io/website?url=https%3A%2F%2Fd-ashwin.github.io%2F)
## Authors

- [@d-ashwin-tw](https://github.com/d-ashwin-tw)



## Installation

Clone the project

```bash
  git clone https://github.com/d-ashwin-tw/bday-reminder-python.git
```

Go to the project directory

```bash
  cd bday-reminder-python
```

Install dependencies

```bash
  pip install -r requirements.tx
```

Install Fixtures

```bash
  python manage.py dumpdata gateway --indent 4 > email_gateway/fixtures/email_template.json
  python manage.py loaddata apps/gateway/fixtures/email_template.json
```

Start the server

```bash
  python manage.py runserver
```


## Running Tests

To run tests, run the following command

```bash
  python manage.py test
```



## Documentation

[Documentation](https://linktodocumentation)


