import pandas as pd
import logging

import settings

# Configure Logging
logger = logging.getLogger(__name__)

"""LOAD DATA FROM CSV"""
try:
    df = pd.read_csv(settings.DATA_PATH)
    # This ensures lookups are robust (strip spaces, strings)
    product_lookup = df.set_index(df['StockCode'].astype(str).str.strip())['Description'].to_dict()
except Exception as e:
    logger.warning(f"Could not load data from {settings.DATA_PATH}: {e}")
    product_lookup = {}