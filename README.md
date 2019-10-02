# Table of Contents

<!-- MarkdownTOC autolink="true" autoanchor="true" levels="1,2,3" -->

- [User API Documentation](#user-api-documentation)
  - [Get telephone bill](#get-telephone-bill)
  - [Save telephone call detail records](#save-telephone-call-detail-records)

<!-- /MarkdownTOC -->


<a id="user-api-documentation"></a>
## User API Documentation

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
**Content:** `{"number": "number must be a string of 10 or 11 digits"}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"period": "period must be in the format: MM/YYYY"}`

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
**Content:** `{"call_id": "call_id must be an integer"}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"timestamp": "timestamp must be a string"}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"source": "source must be a string"}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"destination": "destination must be a string"}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"type": "type must be a string with value 'start' or 'end'."}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"timestamp": "timestamp must be in the format: 'YYYY-MM-DDThh:mm:ssZ'."}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"source": "source must be a string of 10 or 11 digits"}`

**Code:** 400 BAD REQUEST <br />
**Content:** `{"destination": "destination must be a string of 10 or 11 digits"}`


<a id="notes"></a>
#### Notes

- Each Record Start and End must always be sent in separated requests.
- You application should check for 204 code status to verify the record was saved correctly. 
