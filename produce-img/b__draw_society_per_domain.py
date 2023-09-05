import pandas as pd, numpy as np
import matplotlib, matplotlib.pyplot  as plt
import my_functions


df = my_functions.load_corpus()


## ________________1____________ preparer les données
# menage dans la colonne orga scientifique qui contient une typologie avant le ":""
df[["org_type", "org_name"]] = df["orga. \nscientifique"].str.split(pat = ":", expand = True)
df["org_type"] = df["org_type"].str.strip() 

print(df.org_type.value_counts())

# reduire la typologie
df["org_type"].replace(
    {"institut" : "other",
     "ministere" : "other",
      "GIS" : "other",
       "ecole doctorale" : "other",
        "organisation" : "other"},
        inplace = True
        )

# print(df.org_type.value_counts())

## les publishers des revues avec org type
# print(
#     df["Publieurs\n/Plateformes"][ df["org_type"].notna()].value_counts()
#     )

# pour avoir la répartition par domaine sans pourcentage 
dfgraph = pd.crosstab(df["main_subject"], df["org_type"])
print("\n\n", dfgraph.index)

fig, (ax) = plt.subplots(figsize=(10, 7), dpi=100, facecolor='w', edgecolor='k')


ax.bar(dfgraph.index, dfgraph.association , align='center', alpha = 1.0, color='#2272b4', 
    ecolor='black', label="Association")

ax.bar(dfgraph.index, dfgraph.laboratoire , align='center', alpha = 1.0, color='#bcd4e8', 
    bottom = dfgraph.association, ecolor='black', label="Laboratory")


ax.bar(dfgraph.index, dfgraph.other , align='center', alpha = 1.0, color='#e8f0f7', 
    bottom = [sum(x) for x in zip(dfgraph.association, dfgraph.laboratoire)], ecolor='black', label="Other")


# ____n____ configurer l'affichage
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
#ax.spines['left'].set_visible(False)
# retirer l'origine sur Y
ax.set_xticks(np.arange(len(dfgraph.index))) # just to remove an mess error UserWarning: FixedFormatter should only be used together with FixedLocator
yticks = ax.yaxis.get_major_ticks()
ax.set_xticklabels(dfgraph.index, fontsize = 16)


# legende
plt.ylabel("Number of scientific organisation")
ax.legend(loc = "upper left", bbox_to_anchor=(0.65, 0.95),  fontsize = 15, borderaxespad =1.7)
plt.title("Scientific organisations by domain", fontsize = 18, x = 0.5, y = 1.05, alpha = 0.6)
plt.suptitle("n = " + str(df.org_type.notna().sum()) + "  (~" + str(round(df.org_type.notna().sum()/len(df)*100)) + " %)",
 x = 0.5, y = 0.92,  alpha = 0.6)
plt.savefig("hist-scientific-organisation-by-domain.png")
#plt.show()
