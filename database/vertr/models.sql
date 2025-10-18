-- Table: public.models

-- DROP TABLE IF EXISTS public.models;

CREATE TABLE IF NOT EXISTS public.models
(
    id uuid NOT NULL,
    time_utc timestamp with time zone NOT NULL,
    version integer NOT NULL,
    model_type text COLLATE pg_catalog."default" NOT NULL,
    file_name text COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    content bytea NOT NULL,
    CONSTRAINT models_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.models
    OWNER to postgres;

