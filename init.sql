-- public.alerts definition

-- Drop table

-- DROP TABLE public.alerts;

CREATE TABLE alerts (
	id serial4 NOT NULL,
	description varchar NOT NULL,
	status varchar NOT NULL,
	"type" varchar NULL,
	value varchar NULL,
	created_at timestamp NULL,
	CONSTRAINT alerts_pkey PRIMARY KEY (id)
);

-- public.sensors definition

-- Drop table

-- DROP TABLE public.sensors;

CREATE TABLE sensors (
	id serial4 NOT NULL,
	"type" varchar NULL,
	value float8 NULL,
	created_at timestamp NULL,
	CONSTRAINT sensors_pkey PRIMARY KEY (id)
);

INSERT INTO sensors ("type", value, created_at) VALUES('temperature', 22.6, NULL);
INSERT INTO sensors ("type", value, created_at) VALUES('relative_humidity', 61.0, NULL);
INSERT INTO sensors ("type", value, created_at) VALUES('heat_index', 22.51, NULL);
INSERT INTO sensors ("type", value, created_at) VALUES('hl_sensor', 1023.0, NULL);
INSERT INTO sensors ("type", value, created_at) VALUES('auto_watering', 1.0, NULL);
