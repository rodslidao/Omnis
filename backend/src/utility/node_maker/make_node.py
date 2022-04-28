from os.path import exists
from os import makedirs

import argparse

parser = argparse.ArgumentParser(description="Make a node from a template.")

parser.add_argument(
    "--node_name",
    action="store",
    dest="node_name",
    default=None,
    required=True,
    help="Node da pasta, Classe e nome do node",
)
parser.add_argument(
    "--node_type",
    action="store",
    dest="node_type",
    default=None,
    required=False,
    help="Tipo do node",
)
parser.add_argument(
    "--description",
    action="store",
    dest="node_description",
    default="insert_node_description_here",
    required=False,
    help="Descrição do node",
)
parser.add_argument(
    "--path",
    action="store",
    dest="path",
    default="../../nodes/",
    required=False,
    help="Caminho para o node",
)
parser.add_argument(
    "--class_name",
    action="store",
    dest="class_name",
    default=None,
    required=False,
    help="Nome da classe",
)
arguments = parser.parse_args()
if arguments.class_name is None:
    arguments.class_name = (
        arguments.node_name[0].upper() + arguments.node_name[1:] + "Node"
    )

if arguments.node_type is None:
    arguments.node_type = arguments.node_name.upper()
else:
    arguments.node_type = arguments.node_type.upper()

_path = f"{arguments.path}{arguments.node_name}"

if not exists(_path):
    print((f"{_path} not found, creating..."))
    makedirs(_path)
else:
    print("Path already exists. Want to overwrite? (y/n)")
    answer = input().lower()
    if answer == "y":
        print("Overwriting...")
    else:
        print("Aborting...")
        exit()

with open("template.py", "r", encoding="utf8") as firstfile, open(
    f"{_path}/{arguments.node_name}_node.py", "w", encoding="utf8"
) as secondfile:
    for line in firstfile:
        for k, v in arguments.__dict__.items():
            line = line.replace(k, v)
        secondfile.write(line)
