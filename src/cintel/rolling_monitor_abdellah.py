"""
rolling_monitor_case.py - Project script (example).

Author: Denise Case
Date: 2026-03

Time-Series System Metrics Data

- Data is taken from a system that records operational metrics over time.
- Each row represents one observation at a specific timestamp.
- The CSV file includes these columns:
  - timestamp: when the observation occurred
  - requests: number of requests handled
  - errors: number of failed requests
  - total_latency_ms: total response time in milliseconds

Purpose

- Read time-series system metrics from a CSV file.
- Demonstrate rolling monitoring using a moving window.
- Compute rolling averages to smooth short-term variation.
- Save the resulting monitoring signals as a CSV artifact.
- Log the pipeline process to assist with debugging and transparency.

OBS:
  Original example preserved. Modified version created by Abdellah Boudlal.
"""

# === DECLARE IMPORTS ===

import logging
from pathlib import Path
from typing import Final

import polars as pl
from datafun_toolkit.logger import get_logger, log_header, log_path

# === CONFIGURE LOGGER ===

LOG: logging.Logger = get_logger("P5", level="DEBUG")

# === DEFINE GLOBAL PATHS ===

ROOT_DIR: Final[Path] = Path.cwd()
DATA_DIR: Final[Path] = ROOT_DIR / "data"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"

DATA_FILE: Final[Path] = DATA_DIR / "system_metrics_timeseries_case.csv"
OUTPUT_FILE: Final[Path] = ARTIFACTS_DIR / "rolling_metrics_abdellah.csv"

# === DEFINE THE MAIN FUNCTION ===


def main() -> None:
    log_header(LOG, "CINTEL")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    log_path(LOG, "ROOT_DIR", ROOT_DIR)
    log_path(LOG, "DATA_FILE", DATA_FILE)
    log_path(LOG, "OUTPUT_FILE", OUTPUT_FILE)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    log_path(LOG, "ARTIFACTS_DIR", ARTIFACTS_DIR)

    # STEP 1: READ DATA
    df = pl.read_csv(DATA_FILE)
    LOG.info(f"Loaded {df.height} time-series records")

    # STEP 2: SORT BY TIME
    df = df.sort("timestamp")
    LOG.info("Sorted records by timestamp")

    # STEP 3: WINDOW SIZE
    WINDOW_SIZE: int = 3

    # STEP 4: ORIGINAL + CUSTOM SIGNALS
    df_custom = df.with_columns(
        [
            pl.col("requests").rolling_mean(WINDOW_SIZE).alias("requests_rolling_mean"),
            pl.col("errors").rolling_mean(WINDOW_SIZE).alias("errors_rolling_mean"),
            pl.col("total_latency_ms")
            .rolling_mean(WINDOW_SIZE)
            .alias("latency_rolling_mean"),
            # NEW SIGNALS
            (pl.col("errors") / pl.col("requests")).alias("error_rate"),
            pl.col("total_latency_ms")
            .rolling_max(WINDOW_SIZE)
            .alias("latency_rolling_max"),
        ]
    ).with_columns(
        [
            pl.when(pl.col("error_rate") > 0.08)
            .then(1)
            .otherwise(0)
            .alias("high_error_flag")
        ]
    )

    LOG.info("Computed rolling mean + custom signals")

    # STEP 5: SAVE
    df_custom.write_csv(OUTPUT_FILE)
    LOG.info(f"Wrote monitoring file: {OUTPUT_FILE}")

    LOG.info("========================")
    LOG.info("Pipeline executed successfully!")
    LOG.info("========================")
    LOG.info("END main()")


if __name__ == "__main__":
    main()
