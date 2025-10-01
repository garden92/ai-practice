# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jupyter notebook-based data analysis project focused on marketing analytics. The project runs in a Docker container using the `jupyter/datascience-notebook` image with Korean font support for matplotlib visualizations.

## Development Environment

### Docker Setup
- Start Jupyter notebook: `docker-compose up`
- Access notebook at: http://localhost:8888 (token: `mytoken`)
- Work directory is mounted at `/home/jovyan/work` inside the container

### Container Configuration
- Base image: `jupyter/datascience-notebook`
- Korean fonts installed: Nanum fonts and Noto CJK
- Matplotlib cache is cleared on build to ensure Korean fonts work properly

## Code Architecture

### Data Generation Module (`work/create_data.py`)

The `create_data` class generates synthetic marketing campaign data with realistic patterns:

**Key Methods:**
- `catdata()`: Generates categorical campaign response data (600 records)
- `tmsdata()`: Generates detailed time-series marketing metrics with seasonality and trends

**Data Dimensions:**
- Channels: Email, SMS, Push, Ads, Search
- Segments: New, Returning customers
- Devices: Mobile, Desktop
- Regions: Seoul, Busan, Incheon, Daegu, Daejeon, Gwangju

**Time Series Features:**
- `weekly_seasonality()`: Models day-of-week effects (weekends show ~8-10% decrease)
- `monthly_seasonality()`: Models monthly variations (Jan: 0.95 → Jun: 1.10)
- `linear_trend()`: Adds 15% growth trend over the period

**Generated Metrics:**
- Raw: impressions, clicks, cost, conversions, revenue
- Calculated: CTR, CVR, CPC, CAC, ROAS

### Analysis Notebook (`work/create_data.ipynb`)

Main workflow demonstrates:
1. Data generation using `create_data` class
2. Daily aggregation and margin calculation
3. Moving average (7-day) for revenue smoothing
4. Time series visualization with matplotlib

## Working with This Codebase

- All data analysis work happens in the `work/` directory
- Notebook outputs are saved as PNG files in the work directory
- Data CSVs are generated with `output.csv` as default filename
- Korean text rendering is supported in matplotlib charts

## Language Preference

- **IMPORTANT**: Always respond in Korean (한글) to the user
