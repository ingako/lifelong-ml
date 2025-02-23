#!/usr/bin/env python3

import os
import sys
import math
import pandas as pd
import numpy as np

base_dir = os.getcwd()
generator = sys.argv[1]

cur_data_dir = f"{base_dir}/{generator}"
gain_report_path = f"{cur_data_dir}/gain-report.txt"

print(f"evaluating {generator}...")
params = [f for f in os.listdir(cur_data_dir) if os.path.isdir(os.path.join(cur_data_dir, f))]
print("evaluating params...")
print(params)

with open(gain_report_path, "w") as gain_report_out:
    gain_report_out.write("param,reuse-param,lossy-win,#instances,sarf-arf,parf-arf,parf-sarf\n")

    for param in params:

        cur_param_dir = f"{cur_data_dir}/{param}"

        arf_output  = f"{cur_data_dir}/result-0.csv"
        sarf_output = f"{cur_param_dir}/result-sarf-0.csv"

        reuse_params = [f for f in os.listdir(cur_param_dir) if os.path.isdir(os.path.join(cur_param_dir, f))]
        print(f"evaluating reuse params for {param}...")
        print(reuse_params)

        for reuse_param in reuse_params:

            cur_reuse_param = f"{cur_param_dir}/{reuse_param}"
            lossy_params = [f for f in os.listdir(cur_reuse_param) if os.path.isdir(os.path.join(cur_reuse_param, f))]

            for lossy_param in lossy_params:
                cur_lossy_param = f"{cur_reuse_param}/{lossy_param}"
                parf_output = f"{cur_lossy_param}/result-parf-0.csv"

                gain_output = f"{cur_lossy_param}/gain.csv"

                sarf_arf_gain = 0
                parf_arf_gain = 0
                parf_sarf_gain = 0

                with open(gain_output, "w") as out:

                    arf_df = pd.read_csv(arf_output)
                    arf_acc = arf_df["accuracy"]

                    sarf_df = pd.read_csv(sarf_output)
                    sarf_acc = sarf_df["accuracy"]

                    parf_df = pd.read_csv(parf_output)
                    parf_acc = parf_df["accuracy"]

                    num_instances = parf_df["count"]

                    out.write("#count,gain\n")

                    end = min(min(len(sarf_acc), len(parf_acc)), len(arf_acc))
                    # end = 500000
                    for i in range(0, end):
                        sarf_arf_gain += sarf_acc[i] - arf_acc[i]
                        parf_arf_gain += parf_acc[i] - arf_acc[i]
                        parf_sarf_gain += parf_acc[i] - sarf_acc[i]

                        if i == (end - 1):
                            gain_report_out.write(f"{param},{reuse_param},{lossy_param},{num_instances[i]},"
                                                  f"{sarf_arf_gain},"
                                                  f"{parf_arf_gain},"
                                                  f"{parf_sarf_gain}\n")

                        out.write(f"{num_instances[i]},"
                                  f"{sarf_arf_gain},"
                                  f"{parf_arf_gain},"
                                  f"{parf_sarf_gain}\n")

                        out.flush()
