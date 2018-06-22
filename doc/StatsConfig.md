# Stats, Realtime and other things.

Now you can have more information from QPanel through QueueLog

Into config.init-dist you can find a sample of configuration about configuration of database to get information for stattics.


The sample configuration it's like:


```
[queue_log]
database = asterisk
table = queue_log
host = localhost
user = user
password = changeme
port = 5432
adapter = postgres

```


Before you configure the database conection, is really neccesary set configuration for queue_log logger into the database. If you dont want the realtime can too parse to queue_log file.


## How config queue_log Realtime

Into file /etc/asterisk/logger.conf set the follow configs

```
  queue_log_to_file  = yes
  queue_adaptive_realtime = yes

```

For /etc/asterisk/extconfig.conf set the follow configs 


```
queue_log => odbc,general,queue_log (e.g. Adapter,Database,Table)

```

odbc is your driver and general the section where set config respective file 


| Driver | File Configs           |
|--------|------------------------|
| odbc   | res_config_odbc.conf   |
| sqlite | res_config_sqlite.conf |
| pgsql  | res_pgsql.conf         |
| curl   | res_config_curl.conf   |
| ldap   | res_config_ldap.conf   |



## Not realtime?

If you dont want to work in realtime, you can parse the queue_log with parser_queuelog.py

Into the  samples/sqls directory there are samples of DDL for MySQL and PostgreSQL database.

