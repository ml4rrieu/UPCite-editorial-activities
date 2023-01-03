import pandas as pd, numpy as np
import matplotlib, matplotlib.pyplot  as plt
import my_functions

df_raw = pd.read_csv("../2023-01-upcite-editorial-activities-data.csv")


# ______0______ selection du corpus

df_raw["reviewer_only"] = df_raw.apply(lambda row : my_functions.deduce_reviewer_only(row), axis = 1)

# selection des revues : en activité et où le reviewing n'est pas la seule activités éditoriales
mask = (df_raw["si inactif\ndate\ndernier \nnum"].isna()) & (~df_raw["reviewer_only"]) 
df = df_raw[mask].copy()


## simplifier la classification des modèles : delayed OA = subscription
df.replace("Delayed OA", "Subscription (delayed OA)", inplace = True)
#df.replace("S2O", "Diamond", inplace = True)


df_fields = pd.crosstab(df["main_subject"], df["model_eco"])

print(df_fields, '\n\n\n')
## calculate percentage
df_fields = df_fields.T
df_fields = df_fields / df_fields.sum() * 100
df_fields = df_fields.T
#reordonner les rows

# reordonne les colonnes
df_fields = df_fields[["Subscription", "Subscription (delayed OA)", "Hybride", "Gold APC", "S2O", "Diamond" ]].copy()
# reordonne les rows
df_fields = df_fields.reindex( ["Health", "HSS", "ST"],  copy = False)

print(df_fields)


## ___0___do histogram      

ax = df_fields.plot(
    kind = "bar", 
    figsize = (12, 9),
    stacked = True,
    color = ["#023047", "#255770", "#0A9396", "#94D2BD", "#E9D8A6", "#EE9B00" ], 
    rot = -0,
    fontsize = 14
    )

#color = ["#9dd866", "#6f4e7c", "#0b84a5", "grey", "#ffa056", "#f6c85f"]

## _______ configurer l'afichage
# remove axis
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.ylabel("percentage", fontsize=10)
plt.xlabel(None)

#reorder labels
handles, labels = ax.get_legend_handles_labels()
order = [5, 4, 3, 2, 1, 0]
plt.legend(
    [handles[idx] for idx in order], [labels[idx] for idx in order],
    frameon = True, markerscale = 1, fontsize = 12,  bbox_to_anchor=(0.5, 0.6) )

plt.title("Journals adaptation to open access by domain", fontsize = 20, x = 0.5, y = 1.05, alpha = 0.6)
plt.savefig("hist-journal-oa-model-domain.png")