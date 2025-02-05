-- Table: public.sb3_models

-- DROP TABLE IF EXISTS public.sb3_models;

CREATE TABLE IF NOT EXISTS public.sb3_models
(
    id uuid NOT NULL,
    time_utc timestamp with time zone NOT NULL,
    file_name text COLLATE pg_catalog."default" NOT NULL,
    algo text COLLATE pg_catalog."default" NOT NULL,
    version integer NOT NULL,
    description text COLLATE pg_catalog."default",
    content bytea NOT NULL,
    CONSTRAINT sb3_models_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.sb3_models
    OWNER to postgres;

