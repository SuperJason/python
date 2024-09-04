# -*- coding: utf-8 -*-
"""
Created on Sun Sep 1 11:13:47 2024

Scan a dedicated folder and genterates sqlite database with information about
the files, including their sha256sum. If it unexceptedly breaks while
calculating the sha256sum, restarting it will allow you to countinue the
previous work.

@auther: Jason Fu
"""

import argparse
import os
import sys
import sqlite3
import hashlib
import time

class DBase():
    FILE_TAB_NAME = 'FILES'
    DIR_TAB_NAME = 'FOLDERS'
    SHA256_TAB_NAME = 'SHA256SUM'

    def __init__(self, filename='tmp.db', path='/volume1'):
        self.to_scan_path = path
        self.scan_finished = False
        self.db_file_name = filename

        if os.path.exists(filename):
            print(f"{filename} is exist.")
            # Check if SHA256SUM table is exist.
            conn = sqlite3.connect(filename)
            cursor = conn.cursor()
            cursor.execute("SELECT NAME FROM SQLITE_MASTER WHERE TYPE='table'")
            rows = cursor.fetchall()
            table_name_list = [row[0] for row in rows]
            indent = " " * 4
            #print(f"{indent}{table_name_list = }")
            if self.SHA256_TAB_NAME in table_name_list:
                print(f"{indent}scanning has finished!")
                self.scan_finished = True
            else:
                # SHA256SUM table is not exist.
                print(f"{indent}scanning hasn't finished, remove it!")
                os.remove(filename)
                self.scan_finished = False
            conn.close()

        self.conn = sqlite3.connect(filename)
        #print('%s open succeed'%(filename))
        self.cursor = self.conn.cursor()

    def create_file_table(self):
        table_name = self.FILE_TAB_NAME
        self.cursor.execute(f'''CREATE TABLE {table_name}
            (NAME      TEXT PRIMARY KEY NOT NULL,
             SIZE      INT              NOT NULL,
             MTIME     INT              NOT NULL,
             INDEX_    INT              NOT NULL);''')
        #print(f"db: Table {table_name} create succeed")

    def create_folder_table(self):
        table_name = self.DIR_TAB_NAME
        self.cursor.execute(f'''CREATE TABLE {table_name}
            (NAME      TEXT PRIMARY KEY NOT NULL,
             SIZE      INT              NOT NULL,
             MTIME     INT              NOT NULL,
             INDEX_    INT              NOT NULL);''')
        #print(f"db: Table {table_name} create succeed")

    def create_sha256_table(self):
        table_name = self.SHA256_TAB_NAME
        self.cursor.execute(f'''CREATE TABLE {table_name}
            (INDEX_    INT  PRIMARY KEY NOT NULL,
             SHA256SUM TEXT);''')
        #print(f"db: Table {table_name} create succeed")

    def cursor_execute(self, cmd):
        try:
            return self.cursor.execute(cmd)
        except Exception as e:
            print(f"{cmd = }")
            raise e

    def insert_file(self, fn, size, mtime, index):
        table_name = self.FILE_TAB_NAME
        db_cmd = f'''INSERT INTO {table_name} (NAME,SIZE,MTIME,INDEX_)
            VALUES ('{fn}', {size}, {mtime}, {index})'''
        self.cursor_execute(db_cmd)

    def insert_folder(self, fn, size, mtime, index):
        table_name = self.DIR_TAB_NAME
        db_cmd = f'''INSERT INTO {table_name} (NAME,SIZE,MTIME,INDEX_)
            VALUES ('{fn}', {size}, {mtime}, {index})'''
        self.cursor_execute(db_cmd)

    def insert_sha256sum(self, index, sha256sum):
        table_name = self.SHA256_TAB_NAME
        db_cmd = f'''INSERT INTO {table_name} (INDEX_,SHA256SUM)
            VALUES ({index}, '{sha256sum}')'''
        self.cursor_execute(db_cmd)

    def get_max_index_of_sha256sum_table(self):
        table_name = self.SHA256_TAB_NAME
        db_cmd = f"SELECT MAX(INDEX_) FROM {table_name}"
        ret = self.cursor_execute(db_cmd)
        item_list = ret.fetchall()
        index, = item_list[0]
        if index == None:
            return 0
        else:
            return index

    def close(self):
        self.conn.close()
        time_suffix = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        final_db_filename = f"data_{time_suffix:s}.db"
        os.rename(self.db_file_name, final_db_filename)
        print(f"\n{final_db_filename} has been generated!")

class Main():
    def __init__(self):
        self.file_total_size = 0
        self.file_count = 0
        self.calculated_file_count = 0
        self.folder_count = 0
        self.original_calculated_size = 0
        self.calculated_size = 0
        self.rest_size = 0
        self.process_start_time = 0
        self.process_old_pct = 0
        self.sync_count = 0
        self.bar_len = 0

    def init_state(self, file_list, max_idx):
        for name, size, index in file_list:
            if index <= max_idx:
                self.original_calculated_size += size
                self.calculated_file_count += 1
            self.file_total_size += size
            self.file_count += 1
        self.rest_size = self.file_total_size - self.original_calculated_size

    def acc_calc_count(self):
        self.calculated_file_count += 1

    def acc_calc_size(self, size):
        self.rest_size -= size
        self.calculated_size += size

    def init_process_bar(self):
        self.process_start_time = time.perf_counter()

    def readable_duration(self, seconds):
        parts_with_units = [
            (60 * 60 * 24 * 365, "y"),
            (60 * 60 * 24 * 30, "M"),
            (60 * 60 * 24, "d"),
            (60 * 60, "h"),
            (60, "m"),
            (1, "s")
        ]

        fmt = ""
        remaining = abs(seconds)
        for time_part, unit in parts_with_units:
            partial_amount = int(remaining // time_part)
            if unit == "s":
                sec = seconds - ((seconds // 60) * 60)
                fmt = "".join([fmt, f"{sec:.1f}{unit}"])
            elif partial_amount:
                fmt = "".join([fmt, f"{partial_amount}{unit}"])
            remaining %= time_part
        return fmt

    def update_process_bar(self):
        file_cnt = self.calculated_file_count
        file_cnt_pct = (self.calculated_file_count / self.file_count) * 100
        size_pct = ((self.original_calculated_size+self.calculated_size)
                    / self.file_total_size) * 100
        finished = "#" * (round(size_pct)//2)
        need2do = "-" * (50 - round(size_pct)//2)
        dur = time.perf_counter() - self.process_start_time
        escaped_fmt_time = self.readable_duration(dur)
        rest_time = dur * self.rest_size / self.calculated_size 
        rest_fmt_time = self.readable_duration(rest_time)

        # clean bar print space
        if self.bar_len > 0:
            bar = "".join(["\r", " " * self.bar_len])
            print(bar, end="")

        bar = ""
        bar = "".join([bar, "\r"])
        bar = "".join([bar, f"cnt:{file_cnt:d}({file_cnt_pct:.0f}%)"])
        calc_size = self.original_calculated_size + self.calculated_size
        fmt_size = self.readable_size(calc_size)
        bar = "".join([bar, f", size:{fmt_size}({size_pct:.0f}%)"])
        bar = "".join([bar, f"[{finished}>>{need2do}]"])
        bar = "".join([bar, f" taken:{escaped_fmt_time}"])
        bar = "".join([bar, f", rest:{rest_fmt_time}"])
        print(bar, end="")
        self.bar_len = len(bar)

    def if_sync_db(self):
        process_pct = ((self.original_calculated_size+self.calculated_size)
                       / self.file_total_size) * 100
        if process_pct - self.process_old_pct > 1:
            self.process_old_pct = process_pct
            return True
        return False

    def readable_size(self, size):
        for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]:
            if size < 1024.0 or unit == "PB":
                break
            size /= 1024.0
        return f"{size:.2f}{unit}"

def main(path):
    if not os.path.exists(path):
        print(f"{path} is not exist.")
        return

    db = DBase()
    m = Main()

    if db.scan_finished == False:
        db.create_file_table()
        db.create_folder_table()
        # scan folder
        time_start = time.perf_counter()
        print(f"scanning {path} starts ...")
        for dirpath,dirnames,filenames in os.walk(path):
            stat_info = os.stat(dirpath)
            m.folder_count += 1
            # replace ' to '', due to ' is SQL's special character.
            if '\'' in dirpath:
                dirpath = dirpath.replace('\'', '\'\'')
            db.insert_folder(dirpath, stat_info.st_size, stat_info.st_mtime,
                             m.folder_count)
            for filename in filenames:
                full_filename = os.path.join(dirpath,filename)
                if os.path.isfile(full_filename):
                    stat_info = os.stat(full_filename)
                    if '\'' in full_filename:
                        full_filename = full_filename.replace('\'', '\'\'')
                    m.file_count += 1
                    m.file_total_size += stat_info.st_size
                    db.insert_file(full_filename, stat_info.st_size,
                                   stat_info.st_mtime, m.file_count)
        m.rest_size = m.file_total_size
        time_end = time.perf_counter()
        # file_count = 10558160
        print(f"total folder/file count: {m.folder_count}/{m.file_count}")
        # time_end - time_start = 1489.692s
        print(f"{time_end - time_start = :.3f}s")
        db.create_sha256_table()
        db.conn.commit()

    # start from scrach or continue to calculate sha256sum
    max_index = db.get_max_index_of_sha256sum_table()
    print(f"  {max_index = }")

    if db.scan_finished == True:
        # initialize calaulated state
        table_name = db.FILE_TAB_NAME
        db_cmd = f"SELECT NAME,SIZE,INDEX_ FROM %s"%(table_name)
        ret = db.cursor_execute(db_cmd)
        file_list = ret.fetchall()
        m.init_state(file_list, max_index)

    table_name = db.FILE_TAB_NAME
    db_cmd = f"SELECT NAME,SIZE,INDEX_ FROM %s WHERE INDEX_ > %d"%(table_name, max_index)
    ret = db.cursor_execute(db_cmd)
    continue_file_table_list = ret.fetchall()
    print(f"  total file count: {m.file_count}")
    print(f"   rest file count: {len(continue_file_table_list)}")
    print(f"  total size: {m.file_total_size}"
          f"({m.readable_size(m.file_total_size)})")
    print(f"   rest size: {m.rest_size}({m.readable_size(m.rest_size)})")

    print("calculating sha265sum starts ...")
    m.init_process_bar()
    for name, size, index in continue_file_table_list:
        sha256sum = ''
        if os.access(name, os.R_OK):
            # Calculate sha256sum value
            hash_sha256 = hashlib.new('sha256')
            try:
                with open(name, 'rb') as f:
                    for chunk in iter(lambda: f.read(512 * 1024), b''):
                        hash_sha256.update(chunk)
                    sha256sum = hash_sha256.hexdigest()
            except Exception as e:
                print(e)
                sha256sum = str(e)
        else:
            sha256sum = '[Permission denied]'

        db.insert_sha256sum(index, sha256sum)
        m.acc_calc_size(size)
        m.acc_calc_count()
        m.update_process_bar()
        if m.if_sync_db():
            m.sync_count += 1
            db.conn.commit()

    db.conn.commit()
    db.close()
    #print(f"{m.sync_count = }")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Scan a folder and genterates sqlite database")
    parser.add_argument("-p", "--path", nargs="+", default=[],
        help="specify the folder to be scan")
    arg_setting, unknown_args = parser.parse_known_args(sys.argv[1:])

    if arg_setting.path:
        to_scan_path = arg_setting.path[0]
    else:
        #to_scan_path = '/volume1'
        to_scan_path = "/home/jason/codes/"

    print('path: %s'%(to_scan_path))
    main(to_scan_path)
