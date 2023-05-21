import pandas as pd

data_file_name = "../2023-05-upcite-editorial-activities-data.csv"


def load_corpus() : 
    """
    chargement des données et selection du corpus : 
    retient uniquement les revues actives et où le reviewing n'est pas la seule activité
    """

    df_raw = pd.read_csv(data_file_name)
    
    print("nb of lines first load", len(df_raw))

    #identifier les revues où seul le reviewing est exercé
    df_raw["reviewer_only"] = df_raw.apply(lambda row : deduce_reviewer_only(row), axis = 1)

    # selection du corpus : en activité et où reviewing n'est pas la seule activités éditoriales
    mask = (df_raw["si inactif\ndate\ndernier \nnum"].isna()) & (~df_raw["reviewer_only"]) 
    
    df = df_raw[mask]
    print("\nnb of lines after selection", len(df))
    return df




def deduce_reviewer_only(row) : 
    """
    Identifier les revues où la _seule_ activité est le reviewing
    """

    # si EiC du perimetre alors on conserve
    if row["editor\nin\nchief"] : 
        return False

    # séparer les autres activités
    other_activities = str(row["Autres liens\navec UPC"]).lower().split(";") 
    
    # identifier les revues où la seule activitée est reviewer
    if other_activities : 
        if len(other_activities) == 1 : 
            ## verifie si le premier item est egal à reviewer
            if other_activities[0] == "reviewer" : 
                return True 

    return False