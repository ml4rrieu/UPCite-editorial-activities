import pandas as pd


df_raw = pd.read_csv("2022-02-upcite-editorial-activities-data.csv")
print(df_raw.columns)
print(f"nb of journals finded {len(df_raw)}")


print("\n\nnb of journals discontinued", 
    len( df_raw[ df_raw['si inactif\ndate\ndernier \nnum'].notna()] ) 
    )

df_raw[["org_type", "org_name"]] = df_raw["orga. \nscientifique"].str.split(pat = ":", expand = True)
df_raw["org_type"] = df_raw["org_type"].str.strip()


print("\n\nnb of journals managed by a sci. org.", 
    len( df_raw[ df_raw['orga. \nscientifique'].notna()] ) 
    )



print("\n\n\n\n",
    df_raw["org_type"].value_counts()
    )



print("\n\n\n\n",
    df_raw["model_eco"].value_counts()
    )
