# -*- coding: utf-8 -*-
"""helpers.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/188IthLpZmbBa9YKdqLXF_t5r7hfuFovn
"""

import pandas as pd
import numpy as np

#Function to convert height string to inches
def height_to_inches(height_str):
    """Convert height string like '6-3' to total inches (e.g., 75)."""
    try:
        if pd.isna(height_str) or not height_str:
            return np.nan
        height_str = str(height_str).strip()
        feet, inches = map(int, height_str.split('-'))
        return feet * 12 + inches
    except (ValueError, AttributeError):
        return np.nan