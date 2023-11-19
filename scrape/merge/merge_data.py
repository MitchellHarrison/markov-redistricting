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
df4 = pd.read_csv("scrape/merge/ethnicity.csv")

# merge by county name
df12 = pd.merge(df1, df2, on="County")
df123 = pd.merge(df12, df3, on="County")
full_df = pd.merge(df123, df4, on="County")
full_df.to_csv("scrape/data_by_county.csv", index=False)
