# Qpanel API

 Qpanel have a API where you can consume data related of queue. This data is returned in
  JSON format



**Show Queue**
----
  Returns json data about a particular queue

* **URL**

  /queue/:name.json

* **Method:**

  `GET`

*  **URL Params**

   **Required:**

   `name=[text]`


* **Success Response:**

  * **Code:** 200

  * **Content:**

   ```json
          {"data": {

                "Abandoned": "0",
                "Calls": "0",
                "Completed": "0",
                "Holdtime": "0",
                "Max": "0",
                "ServiceLevel": "60",
                "ServicelevelPerf": "0.0",
                "Strategy": "linear",
                "TalkTime": "0",
                "Weight": "0",
                "entries": { },
                "members":{

                        "SIP/1001": {
                            "CallsTaken": "0",
                            "LastCall": "0",
                            "LastCallAgo": "0 segundos",
                            "Membership": "static",
                            "Name": "John Smith",
                            "Paused": "0",
                            "Penalty": "0",
                            "StateInterface": "SIP/1001",
                            "Status": "1"
                        }
                }
     },
    "name": "support"
    }
    ```

* **Error Response:**

  * **Code:** 404 NOT FOUND
  * **Content:** `{ error : "User doesn't exist" }`

  OR

  * **Code:** 401 UNAUTHORIZED
  * **Content:** `{ error : "You are unauthorized to make this request." }`

* **Sample Call:**

  ```javascript
    $.ajax({
      url: "/queue/support.json",
      dataType: "json",
      type : "GET",
      success : function(r) {
        console.log(r);
      }
    });
  ```




**Show Queues**
----
  Returns json data about of all queues

* **URL**

  /queues

* **Method:**

  `GET`

*  **URL Params**

   `None`


* **Success Response:**

  * **Code:** 200

  * **Content:**

   ```json

      { "data": {
          "a1": {
            "Abandoned": "0",
            "Calls": "0",
            "Completed": "0",
            "Holdtime": "0",
            "Max": "0",
            "ServiceLevel": "0",
            "ServicelevelPerf": "0.0",
            "Strategy": "ringall",
            "TalkTime": "0",
            "Weight": "0",
            "entries": { },
            "members": { }

          },
          "sales": {
              "Abandoned": "0",
              "Calls": "0",
              "Completed": "0",
              "Holdtime": "0",
              "Max": "0",
              "ServiceLevel": "60",
              "ServicelevelPerf": "0.0",
              "Strategy": "ringall",
              "TalkTime": "0",
              "Weight": "0",
              "entries": { },
              "members": {
                "SIP/1000": {

                      "CallsTaken": "0",
                      "LastCall": "0",
                      "LastCallAgo": "0 segundos",
                      "Membership": "static",
                      "Name": "John Smith",
                      "Paused": "0",
                      "Penalty": "0",
                      "StateInterface": "SIP/1000",
                      "Status": "5"

                  },
                "SIP/1001": {
                     "CallsTaken": "0",
                     "LastCall": "0",
                     "LastCallAgo": "0 segundos",
                     "Membership": "static",
                     "Name": "John Smith",
                     "Paused": "0",
                     "Penalty": "0",
                     "StateInterface": "SIP/1001",
                     "Status": "1"
                 }
              }
        },
          "support": {

              "Abandoned": "0",
              "Calls": "0",
              "Completed": "0",
              "Holdtime": "0",
              "Max": "0",
              "ServiceLevel": "60",
              "ServicelevelPerf": "0.0",
              "Strategy": "linear",
              "TalkTime": "0",
              "Weight": "0",
              "entries": { },
              "members": {

                "SIP/1001": {
                      "CallsTaken": "0",
                      "LastCall": "0",
                      "LastCallAgo": "0 segundos",
                      "Membership": "static",
                      "Name": "John Smith",
                      "Paused": "0",
                      "Penalty": "0",
                      "StateInterface": "SIP/1001",
                      "Status": "1"
                  }
              }

          },
          "z1":

                  {
                      "Abandoned": "0",
                      "Calls": "0",
                      "Completed": "0",
                      "Holdtime": "0",
                      "Max": "0",
                      "ServiceLevel": "0",
                      "ServicelevelPerf": "0.0",
                      "Strategy": "ringall",
                      "TalkTime": "0",
                      "Weight": "0",
                      "entries": { },
                      "members": { }
                  }
              }

          }

    ```

* **Error Response:**

  * **Code:** 404 NOT FOUND
  * **Content:** `{ error : "404 Not Found" }`

  OR

  * **Code:** 401 UNAUTHORIZED
  * **Content:** `{ error : "You are unauthorized to make this request." }`

* **Sample Call:**

  ```javascript
    $.ajax({
      url: "/queues",
      dataType: "json",
      type : "GET",
      success : function(r) {
        console.log(r);
      }
    });
  ```
