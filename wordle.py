import pandas as pd
import matplotlib.pyplot as plt

def load_df():
    df = pd.read_csv("matts_words.csv")
    df['first'] = df['words'].astype(str).str[0]
    df['second'] = df['words'].astype(str).str[1]
    df['third'] = df['words'].astype(str).str[2]
    df['fourth'] = df['words'].astype(str).str[3]
    df['fifth'] = df['words'].astype(str).str[4]

    letter_value = {'a':1 , 'b':3, 'c':3, 'd':2, 'e':1, 'f':4, 'g':2, 'h':4, 'i':1, 'j':8, 'k':5, 'l':1, 'm':3, 'n':1, 'o':1, 'p':3, 'q':10, 'r':1, 's':1, 't':1, 'u':1, 'v':8, 'w':4, 'x':8, 'y':4, 'z':10}
    
    df['first_score'] = df['first'].map(letter_value)
    df['second_score'] = df['second'].map(letter_value)
    df['third_score'] = df['third'].map(letter_value)
    df['fourth_score'] = df['fourth'].map(letter_value)
    df['fifth_score'] = df['fifth'].map(letter_value)

    df['score'] = df['first_score'] + df['second_score']+ df['third_score'] + df['fourth_score']+ df['fifth_score']
    df["duplicates"] = df.words.apply(lambda x: len(set(x)) == len(x))
    df.loc[df['duplicates']==False, 'score'] = df['score'] + 10
    return df

def filter_df(df, invalid_letters,invalid_position, letters):
    columns = {0: "first", 1: "second", 2: "third", 3: "fourth", 4: "fifth"}

    if len(invalid_letters) > 0:
        regex_string = "[" + "".join(invalid_letters) + "]"
        df = df.loc[~df.words.str.contains(regex_string, regex=True)]

    for items in letters:
        if items == {}:
            continue
        if items['position'] == '?':
            df =  df[df['words'].str.contains(items['letter'])]
            continue
        column = columns[items['position']]
        df = df.loc[df[column] == items['letter']]    

    for items in invalid_position:
        if items == {}:
            continue
        column = columns[items['position']]
        df = df.loc[df[column] != items['letter']]  
    
    return df

def check_word(guess):

    ret_list = []
    
    invalid_letters = []
    valid_index = []
    all_invalid_positions = []
    for i in range(0, 5):
        invalid_position = {}
        ret_dict = {}
        if guess[i] == hidden_word[i]:
            valid_index.append(i)
            ret_dict['letter'] = guess[i]
            ret_dict['position'] = i
            if guess[i] not in filled_position:
                filled_position.append(i)
            
        elif guess[i] in hidden_word and guess[i] not in ret_dict:
            ret_dict['letter'] = guess[i]
            ret_dict['position'] = "?"
            invalid_position['letter'] = guess[i]
            invalid_position['position'] = i
        else:
            invalid_letters.append(guess[i])
        all_invalid_positions.append(invalid_position.copy())
        ret_list.append(ret_dict.copy())

    return ret_list, invalid_letters, all_invalid_positions

def recommend_word(df, guesses, letters):
    if len(set(filled_position)) >= 3 and guesses <5:
        word = special_heuristic(letters)
        return word
    lowestscore = df.score.min()
    lowest_df = df.loc[df.score==lowestscore]
    word = lowest_df.sample(1).words.iat[0]
    return word

def special_heuristic(vacant_positions, chosen_letters):
    columns = {0: "first", 1: "second", 2: "third", 3: "fourth", 4: "fifth"}
    letter_value = {'a':1 , 'b':3, 'c':3, 'd':2, 'e':1, 'f':4, 'g':2, 'h':4, 'i':1, 'j':8, 'k':5, 'l':1, 'm':3, 'n':1, 'o':1, 'p':3, 'q':10, 'r':1, 's':1, 't':1, 'u':1, 'v':8, 'w':4, 'x':8, 'y':4, 'z':10}
    
    vacant_position = [x for x in vacant_positions if x not in filled_position]
    remaining_letters = []
    chosen_letters = [x['letter'] for x in chosen_letters if len(x) > 0]
    for pos in vacant_position:
        column = columns[pos]
        remaining_letters.extend(df[column].unique())

    for letter in remaining_letters:
        if letter not in chosen_letters:
            letter_value[letter] = -20
    df3['first_score'] = df3['first'].map(letter_value)
    df3['second_score'] = df3['second'].map(letter_value)
    df3['third_score'] = df3['third'].map(letter_value)
    df3['fourth_score'] = df3['fourth'].map(letter_value)
    df3['fifth_score'] = df3['fifth'].map(letter_value)

    df3['score'] = df3['first_score'] + df3['second_score']+ df3['third_score'] + df3['fourth_score']+ df3['fifth_score']
    df3["no_duplicates"] = df3.words.apply(lambda x: len(set(x)) == len(x))
    df3.loc[df3['no_duplicates']==False, 'score'] = df3['score'] +40
    df3.sort_values(by=['score'], inplace=True)
    word = df3.words.iat[0]
    return word
        

def visualise(df):
    df = df.loc[df.failed==False]
    df['attempts'] = df['attempts'] + 1
    df = df.groupby(by=["attempts"]).count()
    df = df.reset_index()
    df.rename(columns={'failed' : "num_of_words"},inplace=True)
    ax = df.plot.bar(x='attempts', y='num_of_words', rot=0)
    plt.show()

df = load_df()
df2 = df.copy()

if __name__ == "__main__":
    failed = True
    all_results = []
    result = {}

    for x in df2.iterrows():
        df3 = df.copy()
        vacant_positions= [0,1,2,3,4]
        filled_position = []
        hidden_word = x[1]["words"]
        # hidden_word = "water"
        letters=[]
        for i in range(0, 6):
            word = recommend_word(df,i, letters)
            #word = "utero"
            print("Guessing: " + word)
            if word == hidden_word:
                print("The word is: " + hidden_word)
                print("Took " + str(i+1) + " attempts")
                failed = False
                
                break
            letters,invalid_letters, invalid_position = check_word(word)
            df = filter_df(df, invalid_letters,invalid_position, letters)
        if failed:
            print("FAILURE")
        result["failed"] = failed
        result["attempts"] = i
        result["word"] = hidden_word
        all_results.append(result.copy())
        failed=True
        df = df2
    df = pd.DataFrame(all_results)
    visualise(df)