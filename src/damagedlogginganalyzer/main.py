import argparse
import sys

from damagedlogginganalyzer.DamagedLoggingAnalyzer import DamagedLoggingAnalyzer
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
    parser = argparse.ArgumentParser(description="Analyzes the data about damaged wood from the CSV file.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"DamagedLoggingAnalyzer {__version__}",
    )
    parser.add_argument("csv", metavar="CSV", type=str, help="Path to the CSV containing the statistic.")
    parser.add_argument(
        "--temporal-dependencies",
        action="store_true",
        help="Create plots for temporal dependencies.",
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        help="Output directory for the plots.",
        default="plots",
    )
    return parser.parse_args(args)


def main(args):
    args = parse_args(args)
    print("DamagedLoggingAnalyzer! Pow Pow")

    with DamagedLoggingAnalyzer(args.out_dir) as analyzer:
        analyzer.read_in_csv(args.csv)
        analyzer.analyze(args.temporal_dependencies)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
