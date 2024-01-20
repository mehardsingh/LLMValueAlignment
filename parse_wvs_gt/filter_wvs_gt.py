import pandas as pd
import argparse

def main(wvs_gt_fp, output_fp):
    wvs_gt = pd.read_csv(wvs_gt_fp)
    cols = ["B_COUNTRY"] + [col for col in wvs_gt.columns if col.startswith('Q') and not col == "Q_MODE"]
    wvs_gt = wvs_gt[cols]
    wvs_gt.to_csv(output_fp, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--wvs_gt_fp", type=str)
    parser.add_argument("--output_fp", type=str)
    args = parser.parse_args()

    main(args.wvs_gt_fp, args.output_fp)

