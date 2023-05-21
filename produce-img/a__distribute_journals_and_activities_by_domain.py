import pandas as pd, numpy as np
import matplotlib, matplotlib.pyplot  as plt
import my_functions


df = my_functions.load_corpus()
# print("columns", df.columns)


print( df["Autres liens\navec UPC"].value_counts())


## ________1___________ graph pie nb journals by domain

# répartir les revues par domaines, renommer la colonne de sortie "amount"
df_pie = df["main_subject"].value_counts().to_frame('amount')
print(df_pie)

def pct_n_val(x):
    """
    affiche les pourcentages correspondant pour le graphique pie
    """
    return '{:.0f}%\n({:.0f})'.format(x, df_pie.amount.sum() * x / 100)

fig1, ax1 = plt.subplots(figsize=(10, 7)) 
_, _, autopcts = ax1.pie(
    df_pie.amount,
    labels = df_pie.index,
    explode = (0.02, 0.02, 0.02), 
    autopct = pct_n_val,
    shadow = False,
    startangle=40, 
    colors = ['#47B39C', '#EC6B56', '#FFC154'],
    textprops={'fontsize': 14},
    labeldistance = 1.2
    )

## redefinition des autopct afin de modifier indépendamment leur font et celle des labels
plt.setp(autopcts, **{'color':'black', 'fontsize':10})


plt.title('Amount of journals by domain', fontsize = 20, x = 0.5, y = 1.08, alpha = 0.6)
plt.suptitle("n = " + str(df_pie.amount.sum()), x = 0.5, y = 0.94,  alpha = 0.6)
plt.savefig("pie-journals-by-domain.png")



### ______2.1_____________  hist des activités EiC et Editorial board by domain
"""
faire un graph qui répartie les activités par disciplines, où EiC prévault sur les autres
objectif : voir si les EiC varient pas discipline
"""
print("nb revue avec EiC", len(df[df["editor\nin\nchief"] == True]))

df_hist = pd.DataFrame( df.groupby(["main_subject"])
[["editor\nin\nchief"]].agg(["count", "sum"])).reset_index()

## le goupeby effectue une répartition sur deux niveaux, re nommer les colonnes après traitement pour plus de lisibilité
df_hist.columns = ["main_subject", "nb_journal", "eic"]

df_hist["no_eic"] = df_hist["nb_journal"] - df_hist["eic"]


print(df_hist)

##_____________2.2____________ faire graphique


fig, (ax) = plt.subplots(figsize=(10, 7), dpi=100, facecolor='w', edgecolor='k')

ax.bar(df_hist.main_subject, df_hist.eic , align='center', alpha = 1.0, color='#2272b4', 
    ecolor='black', label="Editor-in-Chief")

ax.bar(df_hist.main_subject, df_hist.no_eic , align='center', alpha = 1.0, color='#bcd4e8', 
    bottom = df_hist.eic, ecolor='black', label="other activities")

# ____n____ configurer l'affichage
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
#ax.spines['left'].set_visible(False)
# retirer l'origine sur Y
#yticks = ax.yaxis.get_major_ticks()
#yticks[0].label1.set_visible(False)

ax.yaxis.grid(ls='--', alpha=0.3)
ax.set_yticks([5, 15, 30, 100, 150 ])
ax.set_ylabel("Number of journals")
ax.set_xticks(np.arange(len(df_hist["main_subject"]))) # just to remove an mess error UserWarning: FixedFormatter should only be used together with FixedLocator
ax.set_xticklabels(df_hist.main_subject.tolist(), fontsize = 16)


# legende
ax.legend(loc = "upper left", bbox_to_anchor=(0.65, 0.95),  fontsize = 15, borderaxespad =1.7)
plt.title("Distribution of editorial activities by type and domain", fontsize = 20, x = 0.5, y = 1.05, alpha = 0.6)
plt.suptitle("n = " + str(df_hist.nb_journal.sum()), x = 0.5, y = 0.92,  alpha = 0.6)
plt.savefig("hist-activities.png")
# plt.show()


