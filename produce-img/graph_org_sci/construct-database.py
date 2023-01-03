import pandas as pd, numpy as np


df_raw = pd.read_csv("../../2023-01-upcite-editorial-activities-data.csv")


# ______0______ selection du corpus

def deduce_reviewer_only(row) : 
    """
    repérer les revues où la _seule_ activité est le reviewing
    """

    # si EiC du perimetre alors on conserve
    if row["editor\nin\nchief"] : 
        return False

    # séparer les autres activités
    other_activities = str(row["Autres liens\navec UPC"]).split(";") 
    
    # retirer les revues où la seule activitée est reviewer
    if other_activities : 
        if len(other_activities) == 1 : 
            if other_activities[0] == "reviewer" : 
                return True 

    return False

df_raw["reviewer_only"] = df_raw.apply(lambda row : deduce_reviewer_only(row), axis = 1)

# selection des revues : en activité et où le reviewing n'est pas la seule activités éditoriales
mask = (df_raw["si inactif\ndate\ndernier \nnum"].isna()) & (~df_raw["reviewer_only"]) 
df = df_raw[mask].copy()


df = df[df["orga. \nscientifique"].notna()]



# ___0___ menage pour la colonne publisher 

df[["publisher_1", "publisher_2"]] = df["Publieurs\n/Plateformes"].str.split(pat = ";", expand = True)
#retrait des espaces
df.loc[:, "publisher_1"]= df["publisher_1"].str.strip()
df.loc[:, "publisher_2"]= df["publisher_2"].str.strip()



# ___0___ menage pour les organisation scientifique 

# éclatement  la colonne orga scientifique qui contient une typologie avant le ":""
df[["org_type", "org_name"]] = df["orga. \nscientifique"].str.split(pat = ":", expand = True)
df["org_type"] = df["org_type"].str.strip()

# reduire la typologie des organisation sci. 
# df["org_type"].replace(
#     {"institut" : "other",
#      "ministere" : "other",
#       "GIS" : "other",
#        "ecole doctorale" : "other",
#         "organisation" : "other"},
#         inplace = True
#         ) 


## ___0___ reduire typologie des modeles economiques

df.replace("Delayed OA", "Subscription", inplace = True)
df.replace("S2O", "Diamond", inplace = True)

print(
    df["publisher_1"].value_counts()
    )

print(df.columns)

dfout = df[["editor\nin\nchief", "main_subject", "nb \npersonne", "model_eco", "APC \nmontant\n€", "publisher_1", "org_type", "title host"]]
print(dfout.columns)

dfout.to_csv("data-org-sci.csv", index = False)