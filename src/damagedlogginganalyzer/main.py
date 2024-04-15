import argparse
import sys
import pandas as pd

from pathlib import Path

from damagedlogginganalyzer import __version__

__author__ = "HokageM"
__copyright__ = "HokageM"
__license__ = "Unliscened"

def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Just a Fibonacci demonstration")
    parser.add_argument(
        "--version",
        action="version",
        version=f"DamagedLoggingAnalyzer {__version__}",
    )
    parser.add_argument(
        "csv",
        metavar="CSV",
        type=str,
        help="Path to the CSV containing the statistic."
    )
    return parser.parse_args(args)

def main(args):
    args = parse_args(args)
    print(f"DamagedLoggingAnalyzer! Pow Pow")

    statistic_csv = Path(args.csv)
    if not statistic_csv.exists():
        raise FileExistsError(f"{statistic_csv} does not exists!. Please enter correct Path to your CSV file!")

    # Read the CSV file into a DataFrame
    df = pd.read_csv(statistic_csv)

    # Display the DataFrame
    print(df[7:]) # The first rows are meta data.


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
