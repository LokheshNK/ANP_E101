import pandas as pd
import numpy as np

def process_metrics(raw_data):
    """
    Performs Z-Score normalization to identify outliers (Silent Architects).
    """
    df = pd.DataFrame(raw_data)

    # 1. Calculate Visibility (Log-scaled)
    # We use log1p (log(1+x)) to penalize 'spammers' and avoid skewed results
    df['visibility_raw'] = df['comm_score'] + (df['meetings'] * 1.5)
    df['visibility_log'] = np.log1p(df['visibility_raw'])

    # 2. Calculate Technical Impact (Entropy-weighted)
    df['impact_score'] = df['commits'] * df['entropy']

    # 3. Z-Score Normalization (Relative to Team Performance)
    # This detects how many standard deviations a user is away from the mean
    df['vis_z'] = (df['visibility_log'] - df['visibility_log'].mean()) / df['visibility_log'].std()
    df['imp_z'] = (df['impact_score'] - df['impact_score'].mean()) / df['impact_score'].std()

    # Handle cases with zero variance (avoid NaN)
    df = df.fillna(0)

    return df.to_dict(orient='records')