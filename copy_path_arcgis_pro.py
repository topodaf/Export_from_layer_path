import os
from pathlib import Path, PurePath
from shutil import copy
import arcpy

import time

DEBUG = False

# Modify the field name containing the path. Here 'Tif'
FIELD_NAME_FOR_PATH = 'Tif'
PATH_SELECTION = arcpy.GetParameterAsText(0)
SORTIE = arcpy.GetParameterAsText(1)


def showPyMessage(message):
    arcpy.AddMessage(str(time.ctime()) + " - " + str(message))


def check_size(list_file):
    size = 0
    for file in list_file:
        try:
            size += os.path.getsize(file) / 1000000
        except FileNotFoundError:
           arcpy.AddWarning(f'!!!!! file missing from path: {file} !!!!!!!!!!')
    return size


count = arcpy.GetCount_management(PATH_SELECTION)
showPyMessage(f"The selection contains {count} elements to copy.")


def liste_copie():
    dir_tif = []
    dir_catalogues = []

    cursor = arcpy.da.SearchCursor(PATH_SELECTION, FIELD_NAME_FOR_PATH)
    for row in cursor:
        hyperlien = Path(row[0])
        dir_tif.append(hyperlien)
        dir_catalogues.append(hyperlien.parts[-2])

        if DEBUG:
            showPyMessage(hyperlien)
            showPyMessage(dir_catalogues[-1])
        else:
            pass

    size_tif = check_size(dir_tif)

    showPyMessage(f'size : {int(size_tif / 1000)} Gb')
    return dir_tif, dir_catalogues


def copie(dir_tif, dir_catalogues):
    for i, path in enumerate(dir_tif):
        total = len(dir_tif)
        pourcent = int((i+1)/total*100)
        showPyMessage(f'            {i+1} / {total} so {pourcent}%, path: {path}')
        created_path = SORTIE / Path(dir_catalogues[i])
        created_path.mkdir(parents=True, exist_ok=True)

        tif_out = SORTIE / PurePath(*path.parts[-2:])

        def copy_custom(in_file, out_file):
            if os.path.isfile(out_file):
                if os.path.getsize(in_file) == os.path.getsize(out_file):
                    showPyMessage(f'existing files {path}')
                else:
                    copy(in_file, out_file)
            else:
                try:
                    copy(in_file, out_file)
                except FileNotFoundError:
                    arcpy.AddWarning(f'not found files: {in_file}')

        copy_custom(path, tif_out)


def run_copy():
    try:
        dir_tif, dir_catalogue = liste_copie()
        copie(dir_tif, dir_catalogue)

    except Exception as e:
        showPyMessage("Error when copying")
        raise e


run_copy()
