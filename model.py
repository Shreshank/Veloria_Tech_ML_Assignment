import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

class Model:

    def __init__(self, df):
        """ This Class is a warpper around LogisticRegression model fitted on matches data of ipl
            (2008-2024), the features used in datasets are, venue, main_team, opposing_team, toss_decision, main_team_won_toss.
            with main_team_won as a target column. you can accesss dataset using self.df and model using self.model, and also
            save or load the already built model. make sure to call clean dataset when using pre-built model.
        """
        self.df = df
        self.model = None

    def correct_team_name(self, tn):
        if tn == 'Royal Challengers Bengaluru':
            return 'Royal Challengers Bangalore'
        
        if tn == 'Rising Pune Supergiants':
            return 'Rising Pune Supergiant'
        
        if tn == 'Kings XI Punjab':
            return 'Punjab Kings'
        
        if tn == 'Delhi Daredevils':
            return 'Delhi Capitals'
        
        if tn == 'Deccan Chargers':
            return 'Sunrisers Hyderabad'
        # 4 defunct (keep in training data): Pune Warriors, Gujarat Lions, Rising Pune Supergiant, Kochi Tuskers Kerala
        return tn
    
    def clean_data(self):
        print('cleaning dataset...')
        self.df = self.df.drop(columns=['id', 'season', 'city', 'date', 'match_type', 'player_of_match', 'method', 'umpire1', 'umpire2', 'result_margin', 'target_overs', 'super_over', 'result'])

        self.df = self.df[~self.df['winner'].isna()]

        self.df['venue'] = self.df['venue'].str.split(',').apply(lambda x: x[0]).str.strip()

        self.df['team1'] = self.df['team1'].apply(self.correct_team_name)
        self.df['team2'] = self.df['team2'].apply(self.correct_team_name)
        self.df['toss_winner'] = self.df['toss_winner'].apply(self.correct_team_name)
        self.df['winner'] = self.df['winner'].apply(self.correct_team_name)

        self.df[['venue', 'team1', 'team2', 'toss_winner', 'toss_decision', 'winner']] = self.df.drop(columns=['target_runs']).apply(lambda x: x.str.lower())

        self.df = self.df.rename(columns={'team1':'main_team', 'team2':'opposing_team'})

        self.df['main_team_won_toss'] = (self.df['toss_winner'] == self.df['main_team']).astype(int)

        self.df['main_team_won'] = (self.df['winner'] == self.df['main_team']).astype(int)

        self.df = self.df.drop(columns=['toss_winner', 'winner'])
    
    def build_model(self):
        self.clean_data()
        print('building model...')

        X = self.df.iloc[:,:-1]
        y = self.df.iloc[:,-1].values
        params = {'C': 0.5, 'l1_ratio': 0, 'solver': 'liblinear'}

        pipe = Pipeline([
            ('OrdinalEncoder', OrdinalEncoder()),
            ('StandardScaler', StandardScaler()),
            ('LogisticRegression', LogisticRegression(**params))
        ])

        pipe.fit(X, y)

        self.model = pipe

        print('model built. checking metrics')
        self.display_metrics()
    
    def display_metrics(self):
        X = self.df.iloc[:,:-1]
        y = self.df.iloc[:,-1].values

        y_pred = self.model.predict(X)

        print(accuracy_score(y, y_pred))
        print(confusion_matrix(y, y_pred))
        print(classification_report(y, y_pred))

    def save_model(self, name='model.pkl'):
        with open(name, 'wb') as handle:
            pickle.dump(self.model, handle)

    def load_model(self, name='model.pkl'):
        with open(name, 'rb') as handle:
            self.model = pickle.load(handle)


df = pd.read_csv('trials/matches.csv')
m = Model(df)

# m.build_model()
# m.save_model()

m.load_model()
m.clean_data()
m.display_metrics()

# X = m.df.iloc[:,:-1]
# y = m.df.iloc[:,-1].values
# print(accuracy_score(y, m.model.predict(X)))