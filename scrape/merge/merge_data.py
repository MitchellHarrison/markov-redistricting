import pandas as pd

"""
Merge three separate datasets together based on county name.
1. PVI by County (Partisan Lean)
2. Population by County
3. Voter Registration by County (#Democrats, #Republicans)
"""

# load each dataset
df1 = pd.read_csv("scrape/merge/partisan_lean.csv")
df2 = pd.read_csv("scrape/merge/population.csv")
df3 = pd.read_csv("scrape/merge/registered.csv")

# merge by county name
df1_and_df2 = pd.merge(df1, df2, on="County")
full_df = pd.merge(df1_and_df2, df3, on="County")
full_df.to_csv("scrape/data_by_county.csv", index=False)
