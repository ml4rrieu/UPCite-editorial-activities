import pandas as pd, numpy as np
import matplotlib, matplotlib.pyplot  as plt
import my_functions

df_raw = pd.read_csv("2022-02-carto-activite-editoriale-univ-paris-cite-data.csv")
print(df_raw.columns, df_raw.shape)

print("\n\n\n", df_raw["Autres liens\navec UPC"].value_counts())


# ______0______ selection du corpus

df_raw["reviewer_only"] = df_raw.apply(lambda row : my_functions.deduce_reviewer_only(row), axis = 1)

# selection des revues : en activité et où le reviewing n'est pas la seule activités éditoriales
mask = (df_raw["si inactif\ndate\ndernier \nnum"].isna()) & (~df_raw["reviewer_only"]) 
df = df_raw[mask].copy()

print(
    "\n\napres traitement\n\n", 
    df["Autres liens\navec UPC"].value_counts(), "\n\n",df.shape
)


### ______1_____________ agréger les colonnes pour le graph main activities

df_activities = df[["main_subject", "editor\nin\nchief", "Autres liens\navec UPC"]].copy()

# isoler l'activité editorial board
df_activities["editorial_board"] = df_activities["Autres liens\navec UPC"].str.contains("editorial board")
# remplacer les champs vides par False
df_activities["editorial_board"].fillna(False, inplace = True)

# df_activities["reviewer"] = df_activities["Autres liens\navec UPC"].str.contains("reviewer")
# #remplace les champs vides par False
# df_activities["reviewer"].fillna(False, inplace = True)


# faire la répartition des acitvitiés par domaines
df3 = pd.DataFrame( df_activities.groupby(["main_subject"])
[["editor\nin\nchief", "editorial_board"]].agg(["count", "sum"])).reset_index()

df3.columns = ["main_subject", "nb_journal", "eic", "nb_journal2", "editorial_board"]

#print(df3[["nb_journal", "eic", "editorial_board", "reviewer"]])

## trier par EiC
df3.sort_values("eic", ascending=False, inplace = True)

## calculer nb activité
nb_activities = df3.eic.sum() + df3.editorial_board.sum() 


## ________0___________ graph pie nb journals by field

def pct_n_val(x):
     return '{:.0f}%\n({:.0f})'.format(x, df3.nb_journal.sum() * x / 100)



fig1, ax1 = plt.subplots(figsize=(10, 7)) 
_, _, autopcts = ax1.pie(
    df3.nb_journal,
    labels = df3.main_subject,
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
plt.suptitle("n = " + str(df3.nb_journal.sum()), x = 0.5, y = 0.94,  alpha = 0.6)
plt.savefig("pie-journals-by-domain.png")

# exit()



## ________4___________ grahph hist editorials activities by field

fig, (ax) = plt.subplots(figsize=(10, 7), dpi=100, facecolor='w', edgecolor='k')

ax.bar(df3.main_subject, df3.eic , align='center', alpha = 1.0, color='#2272b4', 
    ecolor='black', label="Editor in Chief")

ax.bar(df3.main_subject, df3.editorial_board , align='center', alpha = 1.0, color='#bcd4e8', 
    bottom = df3.eic, ecolor='black', label="Editorial board")

# ax.bar(df3.main_subject, df3.reviewer , align='center', alpha = 1.0, color='#e8f0f7', 
#     bottom = [sum(x) for x in zip(df3.eic, df3.editorial_board)], ecolor='black', label="Reviewer")


# ____n____ configurer l'affichage
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
#ax.spines['left'].set_visible(False)
# retirer l'origine sur Y
#yticks = ax.yaxis.get_major_ticks()
#yticks[0].label1.set_visible(False)

ax.yaxis.grid(ls='--', alpha=0.3)
ax.set_yticks([5, 13, 25, 100, 150 ])
ax.set_ylabel("Number of occurrences")
ax.set_xticks(np.arange(len(df3["main_subject"]))) # just to remove an mess error UserWarning: FixedFormatter should only be used together with FixedLocator
ax.set_xticklabels(df3.main_subject.tolist(), fontsize = 16)


# legende
ax.legend(loc = "upper left", bbox_to_anchor=(0.65, 0.95),  fontsize = 15, borderaxespad =1.7)
plt.title("Main editorial activities by domain", fontsize = 20, x = 0.5, y = 1.05, alpha = 0.6)
plt.suptitle("n = " + str(nb_activities), x = 0.5, y = 0.92,  alpha = 0.6)
plt.savefig("hist-activities.png")
#plt.show()