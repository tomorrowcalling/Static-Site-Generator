from textnode import TextNode, TextType
from splitdelimiter import split_nodes_delimiter

def run_experiment(description, old_nodes, delimiter, text_type):
    print(f"---Experiment: {description} ---")
    print(f"Input nodes: {old_nodes}")
    print(f"Delimiter:  {delimiter}")
    print(f"Expected text type: {text_type}")

    try:
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        print("Output nodes:")
        for node in new_nodes:
            print(node)
    except Exception as e:
        print(f"An error occurred: {e}")

    print("-" * 30)


node1 = TextNode("This is text with a **bold** word", TextType.NORMAL_TEXT)
run_experiment("Simple Bold", [node1], "**", TextType.BOLD)

node2 = TextNode("Another node with 'code' here", TextType.NORMAL_TEXT)
run_experiment("No delimiter", [node2], None, TextType.CODE)
