#!/bin/env python3
# Выполненное тестовое задание. Полагается, что скрипт нужно
# запускать в начале каждого дня или после добавления нового 
# файла в хранилище

import logging
import os
import datetime as dt
import shutil

from zipfile import ZipFile

def main():
    STORAGE_DIR = os.environ['STORAGE_DIR']
    ARCHIVE_DIR = os.environ['ARCHIVE_DIR']
    LOGFILE     = os.environ.get('LOGFILE', './logfile.txt')

    today = dt.date.today()

    f = open(LOGFILE, 'a')

    # по годам
    for year in os.listdir(STORAGE_DIR):
        year_path = os.path.join(STORAGE_DIR, year)
        
        # по месяцам
        for month in os.listdir(year_path):
            month_path = os.path.join(year_path, month)
            
            # по дням
            for day in os.listdir(month_path):
                file_date = dt.date(int(year), int(month), int(day))
                delta = today - file_date

                # есть ли достаточно места
                statvfs = os.statvfs(STORAGE_DIR)
                lack_of_space = statvfs.f_blocks * 0.1 > statvfs.f_bavail

                if delta.days > 90 or lack_of_space:
                    src_dir = os.path.join(month_path, day)
                    dest_dir = os.path.join(ARCHIVE_DIR, year, month, day)

                    if not os.path.isdir(dest_dir):
                        os.makedirs(dest_dir)

                    for filename in os.listdir(src_dir):
                        src_path = os.path.join(src_dir, filename)
                        dest_path = os.path.join(dest_dir, filename + '.zip')
                        f.write(f'Архивируется файл {src_path}\n')
                        with ZipFile(dest_path, 'w') as fz:
                            fz.write(src_path, filename)
                
                    f.write(f'Удаление каталога {src_dir}\n')
                    shutil.rmtree(src_dir)

            # удаляем каталог для месяца, если он пуст
            if not os.listdir(month_path):
                f.write(f'Удаление каталога {month_path}\n')
                shutil.rmtree(month_path)

        # удаляем каталог для года, если он пуст
        if not os.listdir(year_path):
            f.write(f'Удаление каталога {year_path}\n')
            shutil.rmtree(year_path)

        f.close()

if __name__ == '__main__':
    main()




            
            
