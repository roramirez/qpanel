CREATE TABLE "queue_log" (
    "id" SERIAL,
    "time" TIMESTAMP WITHOUT TIME ZONE DEFAULT now() NOT NULL,
    "callid" character varying(50) NOT NULL,
    "queuename" character varying(50) NOT NULL,
    "agent" character varying(50) NOT NULL,
    "event" character varying(20) NOT NULL,
    "data" character varying(50) NOT NULL,
    "data1" character varying(50) NOT NULL,
    "data2" character varying(50) NOT NULL,
    "data3" character varying(50) NOT NULL,
    "data4" character varying(50) NOT NULL,
    "data5" character varying(50) NOT NULL,
    CONSTRAINT queue_log_pkey PRIMARY KEY (id)
) WITHOUT OIDS;
