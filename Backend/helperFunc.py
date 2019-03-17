
def helper_get_discipline_multi_choice(disciplineNrs, disciplines):
    """
    functie om aangeduide disciplines terug te geven, vertrekkende vanuit een multiple choice select van een form
    :param disciplineNrs: nummers van de aangeduide opties, dit is een lijst van strings
    :param disciplines: lijst van alle mogelijke disciplines
    :return:
    """
    discipline = list()
    if ("0" in disciplineNrs):
        return None
    else:
        for iterSelected in disciplineNrs:
            discipline.append(disciplines[int(iterSelected) - 1])

    return discipline