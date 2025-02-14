import pandas as pd
#from zone import plot_strike_zone
from zone2 import plot_strike_zone

class BASEAPI:


    def load_base(self, filename):
        self.df = pd.read_csv(filename)

    def get_pitcher(self):
        return list(self.df["player_name"].unique())
    
    def separate_balls_strikes(self, df, query):

        if query == "Balls":
            query = "B"
        else:
            query = "S"
        balls_df = df[df['s_or_b'] == query]
        strikes_df = df[df['s_or_b'] == query]
        if query == "B":
            return balls_df
        else:
            return strikes_df       

    def seperate_batter_stand(self, df, query):

        if query == "Right":
            query = "R"
        else:
            query = "L"
        right_df = df[df['stand'] == query]
        left_df = df[df['stand'] == query]
        if query == "R":
            return right_df
        else:
            return left_df    
        
    def get_stats(self, name, date):

        temp = self.df[self.df["player_name"] == name]
        temp = temp[temp["game_date"] == date]
        return temp
        
    #def get_summary(self, n)

def main():

    # Initialize the API
    base = BASEAPI()
    base.load_base("player_data.csv")
    df = base.get_stats("Gray, Sonny", "2024-09-18")
    plot_strike_zone(df)

if __name__ == '__main__':
    main()