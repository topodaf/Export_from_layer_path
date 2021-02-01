# coding: utf8
import os
from shutil import copy
import arcpy

import time

DEBUG = True

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
            size += os.path.getsize(file) / 1000000.0
        except FileNotFoundError:
           arcpy.AddWarning('!!!!! file not found: {} !!!!!!!!!!'.format(file))
    return size


count = arcpy.GetCount_management(PATH_SELECTION)
showPyMessage("The layer contains {} elements to copy.".format(count))


def liste_copie():
    dir_tif = []
    dir_catalogues = []

    cursor = arcpy.da.SearchCursor(PATH_SELECTION, 'Tif')
    for row in cursor:
        hyperlien = row[0]
        dir_tif.append(hyperlien)
        chemin_1 = os.path.dirname(hyperlien)
        dir_catalogues.append(os.path.basename(chemin_1))

        if DEBUG:
            showPyMessage(hyperlien)
            showPyMessage(dir_catalogues[-1])
        else:
            pass

    size_tif = check_size(dir_tif)

    showPyMessage('size : {} Gb'.format(int(size_tif / 1000)))
    return dir_tif, dir_catalogues


def copie(dir_tif, dir_catalogues):
    total = len(dir_tif)
    for i, path in enumerate(dir_tif):
        showPyMessage('{} / {} so {}%, path: {}'.format(i+1, total, int(float(i+1)/total*100), path))
        created_path = SORTIE + '\\' + dir_catalogues[i]

        if DEBUG:
            showPyMessage(created_path)
        else:
            pass
        try:
            os.mkdir(created_path)
        except WindowsError:
            pass

        tif_out = SORTIE + '\\' + dir_catalogues[i] + '\\' + os.path.basename(path)

        def copy_custom(in_file, out_file):
            if os.path.isfile(out_file):
                if os.path.getsize(in_file) == os.path.getsize(out_file):
                    showPyMessage('existing file {}'.format(path))
                else:
                    copy(in_file, out_file)
            else:
                try:
                    copy(in_file, out_file)
                except:
                    arcpy.AddWarning('Files not found: {}'.format(in_file))

        copy_custom(path, tif_out)


def run_copy():
    try:
        dir_tif, dir_catalogue = liste_copie()
        copie(dir_tif, dir_catalogue)

    except Exception as e:
        showPyMessage(in_file)
   


run_copy()
