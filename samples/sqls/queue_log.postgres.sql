CREATE TABLE "queue_log" (
    "id" SERIAL,
    "time" TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL,
    "callid" character varying(50) NOT NULL DEFAULT '',
    "queuename" character varying(50) NOT NULL DEFAULT '',
    "agent" character varying(50) NOT NULL DEFAULT '',
    "event" character varying(20) NOT NULL DEFAULT '',
    "data" character varying(50) NOT NULL DEFAULT '',
    "data1" character varying(50) NOT NULL DEFAULT '',
    "data2" character varying(50) NOT NULL DEFAULT '',
    "data3" character varying(50) NOT NULL DEFAULT '',
    "data4" character varying(50) NOT NULL DEFAULT '',
    "data5" character varying(50) NOT NULL DEFAULT '',
    CONSTRAINT queue_log_pkey PRIMARY KEY (id)
) WITHOUT OIDS;
