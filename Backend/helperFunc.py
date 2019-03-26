def helper_get_selected_multi_choice(selectedNrs, options):
    """
    functie om aangeduide disciplines terug te geven, vertrekkende vanuit een multiple choice select van een form
    :param selectedNrs: nummers van de aangeduide opties, dit is een lijst van strings
    :param options: lijst van alle mogelijke disciplines
    :return:
    """
    selected = list()
    if "0" in selectedNrs:
        return None
    else:
        for iterSelected in selectedNrs:
            selected.append(options[int(iterSelected) - 1])

    return selected
