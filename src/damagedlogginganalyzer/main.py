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
        "--calculate-most-dangerous-reasons",
        action="store_true",
        help="Calculates the most dangerous reasons for each specie.",
    )
    parser.add_argument(
        "--plot-reason-dependencies",
        action="store_true",
        help="Create combined plots for each specie and owner combinations for all reasons. Plots will be saved in: "
        "output-path/Specie/all_reasons/Owner/plot.png.",
    )
    parser.add_argument(
        "--plot-owner-dependencies",
        action="store_true",
        help="Create combined plots for each specie and reason combinations for all owners. Plots will be saved in: "
        "output-path/Specie/Reason/all_owners/plot.png.",
    )
    parser.add_argument(
        "--plot-temporal-dependencies-all",
        action="store_true",
        help="Create plots for temporal dependencies for each specie, reason and owner combination. "
        "Plots will be saved in: output-path/Specie/Reason/Owner/plot.png. Note: use --plot-owner-dependencies "
        "and --plot-reason-dependencies.",
    )
    parser.add_argument(
        "--predict",
        action="store_true",
        help="Estimates a death count function using Polynomial Regression with K-Fold Cross Validation to predict "
        "the numbers for the year 2024. "
        "Plots will be saved in: output-path/Prediction_2024/Specie/Reasons/Owner/plot.png.Note: will created a "
        "new model for every specie, reason and owner combination.",
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
        analyzer.analyze(
            plot_reason_dependencies=args.plot_reason_dependencies,
            plot_owner_dependencies=args.plot_owner_dependencies,
            plot_temporal_dependencies_all=args.plot_temporal_dependencies_all,
            predict_temporal_dependencies=args.predict,
            calculate_most_dangerous_reasons=args.calculate_most_dangerous_reasons,
        )


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
