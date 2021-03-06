import pandas as pd
import numpy as np
import re

df = pd.read_csv('training/labelled_1000_inclprivate.csv')

# Correct incorrect dtypes
df.append(pd.DataFrame(columns=["Username"], dtype=str))
df.append(pd.DataFrame(columns=["Profile.URL"], dtype=str))

# add derivative features

# add has_number; check if username has a number
df["has_number"] = False
df.append(pd.DataFrame(columns=["has_number"], dtype=bool))
for i in range(len(df["Username"])):
    df["has_number"][i] = bool(re.search(r"\d", df["Username"][i]))

# add has_number_at_end; check if account has number at the end of its username
df["has_number_at_end"] = False
df.append(pd.DataFrame(columns=["has_number_at_end"], dtype=bool))
for i in range(len(df["Username"])):
    df["has_number_at_end"][i] = bool(re.search(r"\d$", df["Username"][i]))

# add alpha_numeric_ratio; ratio of alphabetic letters in username to total
df["alpha_numeric_ratio"] = 0.313
df.append(pd.DataFrame(columns=["alpha_numeric_ratio"], dtype=float))
for i in range(len(df["Username"])):
    df["alpha_numeric_ratio"][i] = round(len(re.findall(r"[a-z]", df["Username"][i])) / len(df["Username"][i]), 7)

# add following_followers_ratio
df["following_followers_ratio"] = 0.313
df.append(pd.DataFrame(columns=["following_followers_ratio"], dtype=float))
for i in range(len(df["Username"])):
    df["following_followers_ratio"][i] = round(df["Number.of.people.they.follow"][i] / df["Number.of.followers"][i], 7)

# add following_posts_ratio
df["following_posts_ratio"] = 0.313
df.append(pd.DataFrame(columns=["following_posts_ratio"], dtype=float))
for i in range(len(df["Username"])):
    df["following_posts_ratio"][i] = round(df["Number.of.people.they.follow"][i] / df["Number.of.posts"][i], 7)

# add followers_posts_ratio
df["followers_posts_ratio"] = 0.313
df.append(pd.DataFrame(columns=["followers_posts_ratio"], dtype=float))
for i in range(len(df["Username"])):
    df["followers_posts_ratio"][i] = round(df["Number.of.followers"][i] / df["Number.of.posts"][i], 7)

# Convert rating boolean values to int
# df["rating"] = df["rating"].astype(int)

# Imputation: replace infinite values with imputed values
# Replace infs with NaN
df = df.replace([np.inf, -np.inf], np.nan)
# Using imputation on ratio based columns
print(df["alpha_numeric_ratio"].mean())  # 0.9011392054358974
print(df["following_followers_ratio"].mean())  # 6.4194135501560865
print(df["followers_posts_ratio"].mean())  # 37.011870851559024
print(df["following_posts_ratio"].mean())  # 127.02637909977729
df["alpha_numeric_ratio"].fillna(df["alpha_numeric_ratio"].mean(), inplace=True)
df["following_followers_ratio"].fillna(df["following_followers_ratio"].mean(), inplace=True)
df["followers_posts_ratio"].fillna(df["followers_posts_ratio"].mean(), inplace=True)
df["following_posts_ratio"].fillna(df["following_posts_ratio"].mean(), inplace=True)

df.to_csv("training/output.csv", index=False)
