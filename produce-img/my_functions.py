

def deduce_reviewer_only(row) : 
    """
    repérer les revues où la _seule_ activité est le reviewing
    attentation pour ses revues il faut aussi s'assurer que ce n'est une "revue de laboratoire" dont nous sommes tutelle, celle-ci sont à conserver
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