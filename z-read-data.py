import pandas as pd

df_raw = pd.read_csv("2023-05-upcite-editorial-activities-data.csv")

df = my_functions.load_corpus()


print(df_raw.columns)

## integration liste colonne publisher
df_raw[["publisher_1", "publisher_2"]] = df_raw["Publieurs\n/Plateformes"].str.split(pat = ";", expand = True)

# retrait des espaces
df_raw[["org_type", "org_name"]] = df_raw["orga. \nscientifique"].str.split(pat = ":", expand = True)
df_raw.loc[:, "org_type"]= df_raw["org_type"].str.strip()


# print(
#     len(df_raw[df_raw["org_type"].notna()])
#     )

#print(" nb of journals", "")

# selection des revues : en activité et où le reviewing n'est pas la seule activités éditoriales
mask = (df_raw["si inactif\ndate\ndernier \nnum"].isna()) & (~df_raw["reviewer_only"]) 
df = df_raw[mask].copy()

df_excluded = df_raw[~mask]
df_excluded.to_csv("journals_excluded.csv")
exit()


# print(df_raw.columns)
print(f"nb of journals finded {len(df_raw)}")

exit()

publishers = df_raw["Publieurs\n/Plateformes"].value_counts()
print(f"nb publishers {len(publishers)}")


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
