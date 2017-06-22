# /bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import exceltool as et


def merge_excel(path, save_path=None, remove_duplicate=True):
    if not os.path.exists(path):
        print("Path dosen't exists")
        return None
    if os.path.splitext(path)[-1] in ['.xls', '.xlsx']:
        df = et.get_data_from_path(path)

    if os.path.isdir(path):
        files = et.get_file_names(path)
        df = list(map(et.get_data_from_path, files))
        df = pd.concat(df, axis=0)
        print("总数据长:", len(df))
        df = df.dropna(thresh=5)
        print("总数据长:", len(df))
        if remove_duplicate:
            df = df.drop_duplicates(df.columns[1])
        df.to_csv(os.path.join(path, "total.csv"), index=False)


if __name__ == '__main__':
    print(len(sys.argv))
    if len(sys.argv) == 2:
        target_path = sys.argv[1]
        merge_excel(target_path)
    if len(sys.argv) == 3:
        target_path, save_path = sys.argv[1:3]
        merge_excel(target_path, save_path)
