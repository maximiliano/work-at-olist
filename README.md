# Table of Contents

<!-- MarkdownTOC autolink="true" autoanchor="true" levels="1,2,3" -->

- [User API Documentation](#user-api-documentation)
  - [Get telephone bill](#get-telephone-bill)
  - [Save telephone call detail records](#save-telephone-call-detail-records)
- [App Documentation](#app-documentation)
  - [Requirements](#requirements)
  - [Install Instructions](#install-instructions)
  - [Heroku Deploy](#heroku-deploy)
  - [Work environment used](#work-environment-used)

<!-- /MarkdownTOC -->


<a id="user-api-documentation"></a>
## User API Documentation
This application can be used to save call detail records and get the bills associated with them by your convenience. It calculates monthly bills for a given telephone number.

<a id="get-telephone-bill"></a>
### Get telephone bill

Returns calls records for a single number and period of month/year.
The telephone bill itself is composed by subscriber and period
attributes and a list of all call records of the period.

<a id="url"></a>
#### URL

*/calls/*

<a id="method"></a>
#### Method

`GET`

<a id="url-params"></a>
#### URL Params

| param      | required | type/values     | description |
|:-----------|:---------|:----------------|:------------|
| `number`   | Yes      | `string` (format: 10 or 11 digits)   | The phone number of the subscriber that origined the calls. Format is 2 digits for area code plus 8 or 9 for the phone number. |
| `period`   | No       | `string` (format: `"MM/YYYY"`)     | The month/year that the searched calls ended. If the param is not informed the system will consider the last closed period, aka the previous month. |


<a id="data-params"></a>
#### Data Params

None

<a id="sample-call"></a>
#### Sample Call:

  `curl --request GET 'http://127.0.0.1:8000/calls/?number=9912345678'`

  `curl --request GET 'http://127.0.0.1:8000/calls/?number=9912345678&period=09/2019'`

<a id="success-response"></a>
#### Success Response

**Code:** 200 OK <br />
**Content:**

  ```json
  {
    "number": "Number that originated the calls",
    "period": "Closed period of month/year for the calls",
    "call_records": [{
        "destination": "Number that received the call",
        "call_start_date": "Date the call started in YYYY-MM-DD format",
        "call_start_time": "Time the call started in hh-mm-dd format",
        "call_duration": "Total call duration",
        "call_price": "Total charged for the call"
    }, {
        "..."
    }]
  }
  ```

**Content Sample:**

  ```json
  {
    "number": "9912345678",
    "period": "09/2019",
    "call_records": [{
        "destination": "8812345678",
        "call_start_date": "2019-09-13",
        "call_start_time": "08:30:15",
        "call_duration": "0h9m45s",
        "call_price": "R$ 1,17"
    }, {
        "destination": "8812345678",
        "call_start_date": "2019-09-13",
        "call_start_time": "21:57:13",
        "call_duration": "0h20m40s",
        "call_price": "R$ 0,54"
    }]
  }
  ```

<a id="error-response"></a>
#### Error Response:

**Code:** 400 BAD REQUEST <br />
**Content:** `{"number": "This field is required."}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"number": "number must be a string of 10 or 11 digits."}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"period": "period must be in the format: MM/YYYY."}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"period": "period must be of a closed (previous) month."}`

<a id="notes"></a>
#### Notes

- If the reference period is not informed the system will consider the last closed period, aka the previous month. 
- It's only possible to get a telephone bill after the reference period has ended.
- A call record belongs to the period in which the call has ended (eg. A call that started on January 31st and finished in February 1st belongs to February
period).

<a id="save-telephone-call-detail-records"></a>
### Save telephone call detail records

Saves call details from sent call records. There are two call detailed record types: Call Start Record and Call End Record. To save all information of a telephone call you should send the records pair.

<a id="url"></a>
#### URL

*/calls/*

<a id="method"></a>
#### Method

`POST`

<a id="url-params"></a>
#### URL Params

None

<a id="data-params"></a>
#### Data Params

| param | used in call type | type/values | description |
|:------|:------------------|:------------|:------------|
| `type`        | `"start"` and `"end"` | `string` (`"start"` or `"end"`) | Indicate if it's a call start or end record |
| `timestamp`   | `"start"` and `"end"` | `string` (format: `"YYYY-MM-DDThh:mm:ssZ"`) | The timestamp of when the event occured |
| `call_id`     | `"start"` and `"end"` | `integer`     | Unique for each call record pair |
| `source`      | `"start"` only        | `string` (format: 10 or 11 digits) | The subscriber phone number that originated the call. Format is 2 digits for area code plus 8 or 9 for the phone number.|
| `destination` | `"start"` only        | `string` (format: 10 or 11 digits) | The phone number receiving the call. Format is 2 digits for area code plus 8 or 9 for the phone number. |

<a id="sample-call"></a>
#### Sample Call:

  Send Call Start Record:

  ```bash
  curl --request POST http://127.0.0.1:8000/calls/ \
    --header "Content-Type: application/json" \
    --data '
        {
          "call_id": 123,
          "type": "start",
          "source": "2212345678",
          "destination": "33987654321",
          "timestamp": "2019-09-30T08:36:21Z"
        }
    '
  ```

  Send Call End Record:

  ```bash
  curl --request POST http://127.0.0.1:8000/calls/ \
    --header "Content-Type: application/json" \
    --data '
        {
          "call_id": 123,
          "type": "end",
          "timestamp": "2019-09-30T08:40:00Z"
        }
    '
  ```

<a id="success-response"></a>
#### Success Response

**Code:** 204 NO CONTENT <br />
**Content:** None

<a id="error-response"></a>
#### Error Response:

**Code:** 400 BAD REQUEST <br />
**Content:** `{"call_id": "This field is required."}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"type": "This field is required."}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"timestamp": "This field is required."}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"source": "This field is required if call type is start."}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"destination": "This field is required if call type is start."}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"call_id": "call_id must be an integer."}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"timestamp": "timestamp must be a string."}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"source": "source must be a string."}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"destination": "destination must be a string."}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"type": "type must be a string with value 'start' or 'end'."}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"timestamp": "timestamp must be in the format: 'YYYY-MM-DDThh:mm:ssZ'."}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"source": "source must be a string of 10 or 11 digits"}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"destination": "destination must be a string of 10 or 11 digits."}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"timestamp": "Start Record Call timestamp cannot be after End Record Call timestamp."}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"timestamp": "End Record Call timestamp cannot be before Start Record Call timestamp."}`

<a id="notes"></a>
#### Notes

- Each Record Start and End must always be sent in separated requests.
- You application should check for 204 code status to verify the record was saved correctly. 
- You MUST send the timestamp in UTC timezone, do any convertion timezone conversion needed in your end.

<a id="app-documentation"></a>
## App Documentation
If you're a developer trying to understand better this app or modify it, use this section to learn more.

This is a Python application using the Django framework and Django Rest Framework. It can be used as is or modified as you wish.

<a id="requirements"></a>
### Requirements
- Python3

<a id="install-instructions"></a>
### Install Instructions
Bellow you will find instructions to install and run the app locally as well as deploying in Heroku. It's convenient to use a virtual environment to install Python modules, if you're not familiar with it, read about it here: [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html).

1. Enter in your workspace directory
2. Create a virtual env directory: `$ mkdir venvs`
3. Create the virtual env: `$ python3 -m venv python/venvs/calldetail`
4. Activate the virtual env: `$ source venvs/calldetail/bin/activate`
5. Clone the repository: `$ git clone https://github.com/maximiliano/work-at-olist`
6. `$ cd work-at-olist`
7. Install dependencies: `$ pip install -r requirements.txt`
8. Define a secret key by assigning the `CD_SECRET_KEY` enviroment variable, either via export command or or adding them to your shell initialization file, you can generate a random string like this: ``$ export CD_SECRET_KEY=`openssl rand -base64 12` ``
9. Configure your database:
  - If you're going to use sqlite you can just run the migrations:  `$ python manage.py migrate`
  - Else, you will need a few extra steps:
  - Create the data base in your choosen database: `> CREATE DATABASE calldetails;` (or another name you choose)
  - Assign these enviroment variables, either via export command or or adding them to your shell initialization file:
  - `$ export CD_DB_ENGINE=<your engine, like mysql or postgres>`
  - `$ export CD_DB_NAME=calldetails`
  - `$ export CD_DB_USER=<your db user>`
  - `$ export CD_DB_PASSWORD=<your user password>`
  - `$ export CD_DB_HOST=<localhost or other host>`
  - `$ export CD_DB_PORT=<your db port>`
  - To know more about django database configuration see this: [Dabatase Settings](https://docs.djangoproject.com/en/2.2/ref/settings/#databases)
  - Run migrations: `$ python manage.py migrate`
10. Run the local server to test: `$ python manage.py runserver`
11. If you see the message "Starting development server at http://127.0.0.1:8000/" means everything is working!


#### Debug Mode

If you want to see the app in DEBUG mode you have to assign the `CD_DEBUG` enviroment variable to `true`: `$ export CD_DEBUG=true` (Don't need to put quotes, it still is a string value).

Run the export command before running the server or add it to your shell initialization file, commonly named `~/.bash_profile`, `~/.profile` or `~/.bashrc`.

#### Testing
You can run the test suit with the command: `$ python -m pytest -vv`

<a id="heroku-deploy"></a>
### Heroku Deploy

If you want to deploy in Heroku, the app is all set up, you just need to run a few commands.

1. Log in your Heroku account: `$ heroku login`
2. Create your Heroku application: `$ heroku create`
3. Disable uneeded stuff: `$ heroku config:set DISABLE_COLLECTSTATIC=1`
4. Define a secret key by assigning the `CD_SECRET_KEY` enviroment variable, you can generate a random string like this: ``$ heroku config:set CD_SECRET_KEY=`openssl rand -base64 12` ``
5. Make sure you have only one dyno running: `$ heroku ps:scale web=1`
6. Send your code to heroku: `$ git push heroku master`
7. Run the migrations in Heroku, it will run in a PostgreSQL database, everything is already set up: `$ heroku run python manage.py migrate`
8. All done! Your app is running in Heroku

#### Debug Mode

If you want to see the app in DEBUG mode you have to assign the `CD_DEBUG` enviroment variable to `true`: `$ heroku config:set CD_DEBUG=true` (Don't need to put quotes, it still is a string value).

#### Checking Logs

You can check logs of running app with the commmand: `$ heroku logs --tail`

If the heroku deploy isn't working, refer to Heroku Docs on Python to learn more: [Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python) and [Deploying Python and Django Apps on Heroku](https://devcenter.heroku.com/articles/deploying-python).

<a id="work-environment-used"></a>
### Work environment used

- Computer:
  + MacBook Air (13-inch, Early 2014)
  + Processor: 1,4 GHz Intel Core i5
  + Memory: 4 GB 1600 MHz DDR3
- Operating System
  + macOS Mojave
  + Version: 10.14.6
- Software:
  + Text Editor: Sublime Text 3 (with PEP8 linters)
  + Terminal: iTerm
  + Databases: sqlite3 and MySQL
  + Libraries: Django, Django Rest Framework, Pytest, Freezegun
  + API tests: curl, Postman
  + Browsers: Safari and Chrome
