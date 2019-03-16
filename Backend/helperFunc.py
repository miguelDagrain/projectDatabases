def helper_sort_values_projects(projects, researchGroups):
    """
    functie om in de projects tab handig in een variabele de nodige informatie mee te geven
    :param projects: de projecten die bestaan
    :param researchGroups: de onderzoeksgroepen die bestaan
    :return:
    """
    neededValuesProject = []
    for project in projects:
        for group in researchGroups:
            if (group.ID == project.researchGroup):
                neededValuesProject.append([project.title, group.name, project.maxStudents])

    return neededValuesProject


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