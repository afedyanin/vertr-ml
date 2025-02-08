-- Table: public.synthetic_candles

-- DROP TABLE IF EXISTS public.synthetic_candles;

CREATE TABLE IF NOT EXISTS public.synthetic_candles
(
    time_utc timestamp with time zone NOT NULL,
    "interval" integer NOT NULL,
    symbol text COLLATE pg_catalog."default" NOT NULL,
    open numeric,
    close numeric,
    high numeric,
    low numeric,
    volume numeric,
    is_completed boolean NOT NULL,
    candle_source integer NOT NULL,
    CONSTRAINT synthetic_candles_unique UNIQUE (time_utc, "interval", symbol)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.synthetic_candles
    OWNER to postgres;