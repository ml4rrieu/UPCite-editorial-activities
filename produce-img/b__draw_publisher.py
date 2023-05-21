import pandas as pd, matplotlib, matplotlib.pyplot  as plt
import my_functions


df = my_functions.load_corpus()
print("columns", df.columns)

# ______0______ preparer les données

# eclatement de la colonne publisher
df[["pub_1", "pub_2"]] = df["Publieurs\n/Plateformes"].str.split(pat = ";", expand = True)
#retrait des espaces
df.loc[:, "pub_1"]= df["pub_1"].str.strip()
df.loc[:, "pub_2"]= df["pub_2"].str.strip()

# print(df["pub_1"].value_counts())
# print(len(df["pub_1"].value_counts()))


df_publisher = pd.crosstab(df["pub_1"], df["main_subject"])
# rename the index
df_publisher.index.rename("publisher", inplace = True)

# une colonne pour avoir le total des revues par publisher
df_publisher["sum"] = df_publisher["HSS"] + df_publisher["Health"] + df_publisher["ST"]

df_publisher.sort_values("sum", ascending = False, inplace = True)
print(df_publisher)


## ______0______ produire graphique
fig, (ax) = plt.subplots(figsize=(15, 11), dpi = 100, facecolor='w', edgecolor='k')

ax.bar(df_publisher.index, df_publisher.HSS, label = "Humanities & Social Sciences", color = "#47B39C")

ax.bar(df_publisher.index, df_publisher.Health , align='center', alpha = 1.0, color='#EC6B56', 
    bottom = df_publisher.HSS, ecolor='black', label="Health")

ax.bar(df_publisher.index, df_publisher.ST , align='center', alpha = 1.0, color='#FFC154', 
    bottom = [sum(x) for x in zip(df_publisher.HSS, df_publisher.Health)], ecolor='black', label="Science & Technology")


# ajout des noms des publishers en haut des histogrammes
for x, y in zip(df_publisher.index, df_publisher["sum"]) : 
    plt.annotate(
      x, 
      (x,y),
      textcoords="offset points", # how to position the text
      xytext=(0,2), # distance from text to points (x,y)
      ha='left', # horizontal alignment can be left, right or center
      va = 'bottom', 
      rotation= 30, 
      fontsize = 9
      )

# ______0______ configurer le rendu
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylabel("Amount of journals", labelpad = 10)
ax.set_xlabel("Publishers", labelpad = 10)

# remove xticks
plt.tick_params(
axis='x',          # changes apply to the x-axis
which='both',      # both major and minor ticks are affected
bottom=False,      # ticks along the bottom edge are off
top=False,         # ticks along the top edge are off
labelbottom=False) # labels along the bottom edge are off


#reorder labels
handles, labels = ax.get_legend_handles_labels()
order = [2, 1, 0]
plt.legend(
    [handles[idx] for idx in order], [labels[idx] for idx in order],
    frameon = True, markerscale = 1, fontsize = 12,  bbox_to_anchor=(0.65, 0.8) )


## titre
plt.title("Distribution of journals by publisher and domain", fontsize = 18, x = 0.5, y = 1.01, alpha = 0.6)
plt.suptitle("n = " + str(len(df)), x = 0.5, y = 0.87,  alpha = 0.6)
plt.savefig("hist-journals-by-publisher.png")
# plt.show()