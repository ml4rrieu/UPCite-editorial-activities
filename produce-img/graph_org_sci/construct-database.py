import pandas as pd, numpy as np
import sys
sys.path.append('../')
import my_functions


df_raw = pd.read_csv("../../2023-05-upcite-editorial-activities-data.csv")

## sel. du corpus
df_raw["reviewer_only"] = df_raw.apply(lambda row : my_functions.deduce_reviewer_only(row), axis = 1)

# selection des revues : en activité et où le reviewing n'est pas la seule activités éditoriales
mask = (df_raw["si inactif\ndate\ndernier \nnum"].isna()) & (~df_raw["reviewer_only"]) 
df = df_raw[mask].copy()

# réduction du corpus aux revues avec org. Sci. 

df = df[df["orga. \nscientifique"].notna()]

# ______0______ menage pour la colonne publisher 

# éclater la colonne publisher
df[["publisher_1", "publisher_2"]] = df["Publishers\n/Plateformes"].str.split(pat = ";", expand = True)
#retrait des espaces
df.loc[:, "publisher_1"]= df["publisher_1"].str.strip()
df.loc[:, "publisher_2"]= df["publisher_2"].str.strip()


# ______1______ menage pour les organisation scientifique 

# éclater la colonne orga scientifique qui contient une typologie avant le ":"
df[["org_type", "org_name"]] = df["orga. \nscientifique"].str.split(pat = ":", expand = True)
df.loc[:, "org_type"]= df["org_type"].str.strip()


"""
print(
    df["org_type"].value_counts()
    )

#association        54
laboratoire         27
institut            2
ecole doctorale     1
ministere           1
GIS                 1

"""


## ______2______ reduire typologie des modeles economiques

df.replace("Delayed OA", "Subscription", inplace = True)
df.replace("S2O", "Diamond", inplace = True)

print(
    df["publisher_1"].value_counts()
    )

# print(df.columns)

dfout = df[["main_subject", "nb \npersonne", "model_eco", "APC \nmontant\n€", "publisher_1", "org_type", "title host"]]
# print(dfout.columns)

dfout.to_csv("data-org-sci.csv", index = False)