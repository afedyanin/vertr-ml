-- Table: public.trading_signals

DROP TABLE IF EXISTS public.trading_signals;

CREATE TABLE IF NOT EXISTS public.trading_signals
(
    id uuid NOT NULL,
    time_utc timestamp with time zone NOT NULL,
    symbol text COLLATE pg_catalog."default" NOT NULL,
    "action" integer NOT NULL,
    "interval" int NOT NULL,
    predictor text COLLATE pg_catalog."default" NOT NULL,
    algo text COLLATE pg_catalog."default" NOT NULL,
    candles_source text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT trading_signals_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.trading_signals
    OWNER to postgres;