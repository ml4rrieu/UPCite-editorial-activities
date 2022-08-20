import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd, numpy as np
import my_functions

sns.set_theme(style = "ticks", color_codes = True)

tips = sns.load_dataset("tips")
#print(type(sns))

df_raw = pd.read_csv("2022-02-carto-activite-editoriale-univ-paris-cite-data.csv")


# ______0______ selection du corpus

df_raw["reviewer_only"] = df_raw.apply(lambda row : my_functions.deduce_reviewer_only(row), axis = 1)

# selection des revues : en activité et où le reviewing n'est pas la seule activités éditoriales
mask = (df_raw["si inactif\ndate\ndernier \nnum"].isna()) & (~df_raw["reviewer_only"]) 
df = df_raw[mask].copy()



# retrait des valeurs de modele_co Diamond & Subscription
df.replace("Subscription", np.nan, inplace = True)
df.replace("Diamond", np.nan, inplace = True)
df.replace("S2O", np.nan, inplace = True)

## a voir si l'on retire Delayed OA
df.replace("Delayed OA", np.nan, inplace = True)


## ___0____  graph

rel = sns.catplot(x = "main_subject", 
    y = "APC \nmontant\n€", 
    hue="model_eco",
    height = 7,
    data = df, 
    legend = False,
    palette = sns.color_palette(['#94D2BD', '#255770'])
    )
    # color = ["#94D2BD", ""])


## modifier les noms des axes
plt.ylabel("Amount of APCs in €uros")
plt.xlabel("")

# param pour la légende
plt.gca().legend().set_title('') # retirer le titre de la légende
plt.legend(loc='upper center')

rel.fig.subplots_adjust(top=0.9)
rel.fig.suptitle("Amount of the Article Processing Charges by domain", fontsize = 20, alpha = 0.6)

#plt.show()
plt.savefig("apc.png")


