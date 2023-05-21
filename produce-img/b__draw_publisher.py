import pandas as pd, matplotlib, matplotlib.pyplot  as plt
import my_functions


df = my_functions.load_corpus()
# print("columns", df.columns)

# ______0______ preparer les données

# eclatement de la colonne publisher
df[["pub_1", "pub_2"]] = df["Publieurs\n/Plateformes"].str.split(pat = ";", expand = True)
#retrait des espaces
df.loc[:, "pub_1"]= df["pub_1"].str.strip()
df.loc[:, "pub_2"]= df["pub_2"].str.strip()

# print(df["pub_1"].value_counts())
# print(len(df["pub_1"].value_counts()))

# calcul nb de revues par publisher
df_publisher = df["pub_1"].value_counts().rename_axis('publishers').reset_index(name='counts')


## ______0______ produire graphique
fig, (ax) = plt.subplots(figsize=(15, 11), dpi = 100, facecolor='w', edgecolor='k')

ax.bar(df_publisher.publishers, df_publisher.counts, color = "#2272b4")


# ajout des noms des publishers en haut des histogrammes
for x, y in zip(df_publisher.publishers, df_publisher.counts) : 
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
ax.set_ylabel("Amont of journals/series", labelpad = 10)
ax.set_xlabel("Publishers", labelpad = 10)

# remove xticks
plt.tick_params(
axis='x',          # changes apply to the x-axis
which='both',      # both major and minor ticks are affected
bottom=False,      # ticks along the bottom edge are off
top=False,         # ticks along the top edge are off
labelbottom=False) # labels along the bottom edge are off


## titre
plt.title("Amount of journals by publisher", fontsize = 18, x = 0.5, y = 1.01, alpha = 0.6)
plt.suptitle("n = " + str(len(df)), x = 0.5, y = 0.87,  alpha = 0.6)
plt.savefig("hist-journals-by-publisher.png")