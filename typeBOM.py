import os


def list_directory(path):
    # type=0 - jeden plik pdf
    # type=1 - pliki pdf w jednym folderze
    # type=2 - pliki pdf w wielu folderach
    type = 0
    lista_plikow = []
    krotka_list = os.walk(path)
    count_folders = 0
    count_files = 0
    for _ in krotka_list:
        print(_)
        count_folders += 1
        # Unpacking tuple
        sciezka = _[0]
        lista_folderow = list(_[1])  # Convert generator to a list
        pliki = list(_[2])  # Convert generator to a list

        # Displaying content
        print("Ścieżka:", sciezka)
        print("Lista folderow:", lista_folderow)
        print("Lista plików:", lista_plikow)

        for el in pliki:
            if ".PDF" in el.upper():
                lista_plikow.append(sciezka+'/'+el)
                count_files += 1

    if count_files > 1 and count_folders > 2:
        type = 2
    elif count_files > 1 and count_folders == 2:
        type = 1
    elif count_files == 1:
        type = 0

    return lista_plikow, type
