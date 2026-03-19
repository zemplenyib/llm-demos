import os
import sys
# Add parent folder to sys.path so utils can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse
import utils
from ingest import Ingest
from chatbot import ChatBot

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
CHROMA_DIR = os.path.join(ROOT_DIR, "chroma_db")

parser = argparse.ArgumentParser(
                    prog="RagApp",
                    description="Experimenting with RAG")

parser.add_argument('--query', default = None)
parser.add_argument('--ingest', action='store_true', default=False)
parser.add_argument('--folder', default=CHROMA_DIR)
parser.add_argument('--HyDE', action='store_true', default=False)
parser.add_argument('--query_exp', action='store_true', default=False)
parser.add_argument('--keyw_extr', action='store_true', default=False)

args = parser.parse_args()

chatBot = ChatBot('all-MiniLM-L6-v2', 'chroma_db', args.HyDE, args.query_exp, args.keyw_extr)

if args.ingest:
    # Gather data
    ingest = Ingest(ROOT_DIR, chunk_size=800, overlap=150)
    chunks = ingest.process_folder("./data")

    embeddings = chatBot.add_data(chunks)

else:
    if args.query is not None:
        response = chatBot.query(args.query)
        print(response)
    else:
        while(True):
            input_text = input (">> ")
            if input_text == "exit":
                break

            response = chatBot.query(input_text)
            print(response)
