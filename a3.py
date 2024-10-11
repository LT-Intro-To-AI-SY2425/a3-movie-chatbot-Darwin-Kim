# Important variables:
#     movie_db: list of 4-tuples (imported from movies.py)
#     pa_list: list of pattern-action pairs (queries)
#       pattern - strings with % and _ (not consecutive)
#       action  - return list of strings

# THINGS TO ASK THE MOVIE CHAT BOT:
# what movies were made in _ (must be date, because we don't have location)
# what movies were made between _ and _
# what movies were made before _
# what movies were made after _
# who directed %
# who was the director of %
# what movies were directed by %
# who acted in %
# when was % made
# in what movies did % appear
# bye

#  Include the movie database, named movie_db
from movies import movie_db
from match import match
from typing import List, Tuple, Callable, Any

# The projection functions, that give us access to certain parts of a "movie" (a tuple)
def get_title(movie: Tuple[str, str, int, List[str]]) -> str:
    return movie[0]


def get_director(movie: Tuple[str, str, int, List[str]]) -> str:
    return movie[1]


def get_year(movie: Tuple[str, str, int, List[str]]) -> int:
    return movie[2]


def get_actors(movie: Tuple[str, str, int, List[str]]) -> List[str]:
    return movie[3]




def title_by_year(matches: List[str]) -> List[str]:
    ans=[]
    for i in range(len(movie_db)):
        if get_year(movie_db[i])==int(matches[0]): ans.append(get_title(movie_db[i]))
    return ans
    pass


def title_by_year_range(matches: List[str]) -> List[str]:
    YStart=int(matches[0])
    YEnd=int(matches[1])
    result=[]

    for i in range(len(movie_db)):
        if YStart<get_year(movie_db[i])<YEnd+1: result.append(get_title(movie_db[i]))
    return(result)
    pass


def title_before_year(matches: List[str]) -> List[str]:
    MaxYear=int(matches[0])
    result=[]
    for i in range(len(movie_db)):
        if get_year(movie_db[i])<MaxYear: result.append(get_title(movie_db[i]))
    return result
    pass


def title_after_year(matches: List[str]) -> List[str]:
    MinYear=int(matches[0])
    result=[]
    for i in range(len(movie_db)):
        if get_year(movie_db[i])>MinYear: result.append(get_title(movie_db[i]))
    return result
    pass


def director_by_title(matches: List[str]) -> List[str]:
    Ans=[]
    for i in range(len(movie_db)):
        if get_title(movie_db[i])==matches[0]: Ans.append(get_director(movie_db[i]))
    return Ans
    pass


def title_by_director(matches: List[str]) -> List[str]:
    Ans=[]
    for i in range(len(movie_db)):
        if get_director(movie_db[i])==matches[0]: Ans.append(get_title(movie_db[i]))
    return Ans
    pass


def actors_by_title(matches: List[str]) -> List[str]:
    for i in range(len(movie_db)):
        if get_title(movie_db[i])==matches[0]:
            return get_actors(movie_db[i])
    pass


def year_by_title(matches: List[str]) -> List[int]:
    Ans=[]
    for i in range(len(movie_db)):
        if get_title(movie_db[i])==matches[0]: Ans.append(get_year(movie_db[i]))
    return Ans
    pass


def title_by_actor(matches: List[str]) -> List[str]:
    Ans=[]
    for i in range(len(movie_db)):
        for indx in range(len(get_actors(movie_db[i]))):
            if get_actors(movie_db[i])[indx]==matches[0]: Ans.append(get_title(movie_db[i]))
    return Ans
    pass


# dummy argument is ignored and doesn't matter
def bye_action(dummy: List[str]) -> None:
    raise KeyboardInterrupt


# The pattern-action list for the natural language query system A list of tuples of
# pattern and action It must be declared here, after all of the function definitions
pa_list: List[Tuple[List[str], Callable[[List[str]], List[Any]]]] = [
    (str.split("what movies were made in _"), title_by_year),
    (str.split("what movies were made between _ and _"), title_by_year_range),
    (str.split("what movies were made before _"), title_before_year),
    (str.split("what movies were made after _"), title_after_year),
    # note there are two valid patterns here two different ways to ask for the director
    # of a movie
    (str.split("who directed %"), director_by_title),
    (str.split("who was the director of %"), director_by_title),
    (str.split("what movies were directed by %"), title_by_director),
    (str.split("who acted in %"), actors_by_title),
    (str.split("when was % made"), year_by_title),
    (str.split("in what movies did % appear"), title_by_actor),
    (["bye"], bye_action),
]


def search_pa_list(src: List[str]) -> List[str]:
    
    #VARIABLES
    matches=[]
    CurrentListMatches=0
    HighestMatches=0
    BestMatch=0
    ans=[]

    # FIGURING OUT WHAT TUPLE TO USE

    # Creating a list(matches[]) of the number of matches between each value of src[] 
    # and the corresponding value of each of the 8 patterns
    for i in range(len(pa_list)):
        for i2 in range(len(pa_list[i][0])):
            if i2<len(src):
                if src[i2]==pa_list[i][0][i2]:
                    CurrentListMatches+=1
        matches.append(CurrentListMatches)
        CurrentListMatches=0

    # Figuring out which tuple has the highest match between its pattern and the given source using matches[] 
    for i in range(len(matches)):
        if matches[i]>HighestMatches:
            BestMatch=pa_list[i]
            HighestMatches=matches[i]

    # CALLING THE APPROPRIATE FUNCTION

    # Telling this block of code to run only if there is a match (if there are no matches, skip to line 193)
    if BestMatch!=0:

        # VARIABLES
        Diff=len(src)-len(BestMatch[0])
        val=[]
        
        # Checking for every item in the string of the matched tuple for %s and _s, then utilizing those symbols to determine 
        # what to send into the function
        for i3 in range(len(BestMatch[0])):
            if BestMatch[0][i3]=="%": 
                for i2 in range(Diff+1): val.append(src[i3+i2])
            if BestMatch[0][i3]=="_": val.append(src[i3])

        # Calling the function of said tuple once the loop has ended and the list of inputs is therefore complete,
        # and setting ans equal to the output of that function
        ans=BestMatch[1](val)

    # Telling the function what to do if there are no matches(if statement) 
    # or if the function of said match returns blank list(elif statement)
    if BestMatch==0: ans=["I don't understand"]
    elif ans==[]: ans=["No answers"]


    return ans
            
        
    pass


def query_loop() -> None:
    print("Welcome to the movie database!\n")
    while True:
        try:
            print()
            query = input("Your query? ").replace("?", "").lower().split()
            answers = search_pa_list(query)
            for ans in answers:
                print(ans)

        except (KeyboardInterrupt, EOFError):
            break

    print("\nSo long!\n")

query_loop()

if __name__ == "__main__":
    assert isinstance(title_by_year(["1974"]), list), "title_by_year not returning a list"
    assert isinstance(title_by_year_range(["1970", "1972"]), list), "title_by_year_range not returning a list"
    assert isinstance(title_before_year(["1950"]), list), "title_before_year not returning a list"
    assert isinstance(title_after_year(["1990"]), list), "title_after_year not returning a list"
    assert isinstance(director_by_title(["jaws"]), list), "director_by_title not returning a list"
    assert isinstance(title_by_director(["steven spielberg"]), list), "title_by_director not returning a list"
    assert isinstance(actors_by_title(["jaws"]), list), "actors_by_title not returning a list"
    assert isinstance(year_by_title(["jaws"]), list), "year_by_title not returning a list"
    assert isinstance(title_by_actor(["orson welles"]), list), "title_by_actor not returning a list"
    
    assert sorted(title_by_year(["1974"])) == sorted(
        ["amarcord", "chinatown"]
    ), "failed title_by_year test"
    assert sorted(title_by_year_range(["1970", "1972"])) == sorted(
        ["the godfather", "johnny got his gun"]
    ), "failed title_by_year_range test"
    assert sorted(title_before_year(["1950"])) == sorted(
        ["casablanca", "citizen kane", "gone with the wind", "metropolis"]
    ), "failed title_before_year test"
    assert sorted(title_after_year(["1990"])) == sorted(
        ["boyz n the hood", "dead again", "the crying game", "flirting", "malcolm x"]
    ), "failed title_after_year test"
    assert sorted(director_by_title(["jaws"])) == sorted(
        ["steven spielberg"]
    ), "failed director_by_title test"
    assert sorted(title_by_director(["steven spielberg"])) == sorted(
        ["jaws"]
    ), "failed title_by_director test"
    assert sorted(actors_by_title(["jaws"])) == sorted(
        [
            "roy scheider",
            "robert shaw",
            "richard dreyfuss",
            "lorraine gary",
            "murray hamilton",
        ]
    ), "failed actors_by_title test"
    #assert sorted(actors_by_title(["movie not in database"])) == [], "failed actors_by_title not in database test"
    assert sorted(year_by_title(["jaws"])) == sorted(
        [1975]
    ), "failed year_by_title test"
    assert sorted(title_by_actor(["orson welles"])) == sorted(
        ["citizen kane", "othello"]
    ), "failed title_by_actor test"
    assert sorted(search_pa_list(["hi", "there"])) == sorted(
        ["I don't understand"]
    ), "failed search_pa_list test 1"
    assert sorted(search_pa_list(["who", "directed", "jaws"])) == sorted(
        ["steven spielberg"]
    ), "failed search_pa_list test 2"
    assert sorted(
        search_pa_list(["what", "movies", "were", "made", "between", "2020", "and", "2024"])
    ) == sorted(["No answers"]), "failed search_pa_list test 3"

    print("All tests passed!")
