import argparse
from Code.graph import Tree
from Code.decision_tree_adapter import DecisionTreeAdapter

command_setting = {
    "infoGain": False,
    "minInfoGain": 0.0,
    "file": "komputery.csv"
}


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gainRatio', action="store_false", help='Using GainRatio (default using InfoGain).')
    parser.add_argument('--minInfoGain', type=float, default=0.0, required=False, help='Minimal information gain.')
    parser.add_argument('file', type=str, help='File with data.')
    args = parser.parse_args()

    command_setting["infoGain"] = args.gainRatio
    command_setting["minInfoGain"] = args.minInfoGain
    command_setting["file"] = args.file


def main():
    parse_arguments()
    decision_tree = DecisionTreeAdapter(command_setting)
    decision_tree.run()
    graph = Tree(decision_tree.root)
    graph.draw_graph()


main()
