import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

import torch
from transformers import pipeline

class RagSearch:

    def __init__(self):
        self.corpus = ''
        self.collection = None
        self.chroma_client = chromadb.PersistentClient()
        self.sentence_transformer_ef = SentenceTransformerEmbeddingFunction(
            model_name="BAAI/bge-large-en-v1.5",
            device='cuda',
            normalize_embeddings=False
        )
        self.model_id = "meta-llama/Llama-3.2-1B-Instruct"
        self.pipe = pipeline(
            "text-generation", 
            model=self.model_id, 
            dtype=torch.bfloat16, 
            device_map="auto"
        )

    def set_records(self):
        corpus = []
        df = pd.read_csv('trials/matches.csv')
        df1 = pd.read_csv('trials/matches_25.csv')
        df2 = pd.read_csv('trials/match_data2.csv')

        print('1st Dataset(2008-2024) \n')
        for idx,row in df.iterrows():

            corpus.append(
                f"{row['team1']} vs {row['team2']} at {row['venue']}, {row['city']} on {row['date']} ({row['season']} IPL, {row['match_type']}). {row['toss_winner']} won the toss and chose to {row['toss_decision']}. {row['winner']} won by {row['result_margin']} {row['result']}, chasing a target of {row['target_runs']} in {row['target_overs']} overs. Player of the Match: {row['player_of_match']}. Umpires: {row['umpire1']} and {row['umpire2']}."
            )

        print('\n2nd Dataset(2025) \n')
        for idx,row in df1.iterrows():

            corpus.append(
                f"{row['stage']} match {row['team1']} vs {row['team2']} at {row['venue']} on {row['date']}. {row['match_winner']} won by margin of {row['margin']}. Player of the Match: {row['player_of_the_match']}."
            )

        print('\n3rd Dataset(2026) \n')
        for idx,row in df2.iterrows():

            corpus.append(
                f"{row['Match_no']} {row['Team1']} vs {row['Team2']} at {row['Venue']} on {row['Date']}. {row['Winning_team']} won. Player of the Match: {row['Player_of_match']} (impact score: {row['Player_of_match_total_impact']}). Top scorer: {row['Top_scorer']} with {row['Top_scorer_runs']} runs."
            )
        print()

        self.corpus = corpus

    def generate_vector_emd(self):

        collection = self.chroma_client.create_collection(
            name="ipl_matches_08_26",
            embedding_function=self.sentence_transformer_ef,
            get_or_create=True
        )

        collection.add(
            ids=[str(i) for i in range(len(self.corpus))],
            documents=self.corpus
        )

        self.collection = collection
    
    def load_vector_emd(self):
        self.collection = self.chroma_client.get_collection('ipl_matches_08_26', self.sentence_transformer_ef)

    def query(self):
        while True:
            query = input('(type e to end)Enter Query: ')
            if query == 'e':
                break
            res = self.collection.query(query_texts=[query])['documents']

            print(res)

            
    def run(self):
        while True:
            query = input('(type e to end)Enter Query: ')
            if query == 'e':
                break

            res = self.collection.query(query_texts=[query])['documents']

            messages = [
                {"role": "system", "content": "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, say that you don't know. Use three sentences maximum and keep the answer concise."},
                {"role": "user", "content": res},
            ]

            outputs = self.pipe(messages, max_new_tokens=256)

            print(outputs[0]["generated_text"][-1])


rag = RagSearch()
rag.set_records()
rag.load_vector_emd()
rag.query()
# rag.generate_vector_emd()
# rag.run()