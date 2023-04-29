from matplotlib import pyplot as plt
import random
import statistics
from colorama import Fore


def display_title():
    print(Fore.BLUE + "\n** ** ** ** ** My Movies Database ** ** ** "
                      "** **")


def display_menu():
    print(Fore.LIGHTCYAN_EX +
          """
Menu:
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Create Rating Histogram
        """)


def get_user_input():
    user_input = int(input('Enter choice (1-8): '))
    return user_input


def list_movies(movies_dict: dict):
    """ This function gets a dataset of movies and their ratings from
        dictionary and prints the list of current movies in the dictionary
        and their ratings """

    print(Fore.LIGHTBLUE_EX + "\n{len(movies)} movies in total")
    for movie, rating in movies_dict.items():
        print(f"{movie}: {rating}")


def add_movie(movies_dict):
    """ This function gets a dataset of movies and their ratings from
        dictionary and ask user for name of movie to be added and the rating
        for the movie """

    movie_name = input("Enter new movie name: ")
    movie_rating = input("Enter new movie rating (0-10): ")
    movies_dict[movie_name] = movie_rating
    print(Fore.LIGHTYELLOW_EX + f"Movie {movie_name} successfully added")


def delete_movie(movies_dict: dict):
    """ This function gets a dataset of movies and their ratings from
        dictionary and ask user for name of movie to be deleted """

    movie_name = input("Enter movie name to delete: ")
    if movie_name in movies_dict:
        # del movies_dict[movie_name]
        movies_dict.pop(movie_name)
        print(Fore.LIGHTWHITE_EX + f"Movie {movie_name} successfully deleted")
    else:
        print(f"Movie {movie_name} doesn't exist!")


def update_movie(movies_dict: dict):
    """ This function gets a dataset of movies and their ratings from
    dictionary and ask user for name of movie to be updated and the rating
    for the movie to be updated """

    movie_name = input("Enter movie name to update: ")
    movie_rating = input("Enter new movie rating (0-10): ")

    for name in movies_dict:

        if movie_name.lower() == name.lower():
            movies_dict[name] = int(movie_rating)
            print(f"Movie {name} successfully updated")
            break
    else:
        print(f"Movie {movie_name} doesn't exist!")


def movie_stats(movies_dict: dict):
    """ This function gets a dataset of movies and their ratings
    and prints the movies with average rating, median rating,
    best rating and worst rating. """

    average_rating = statistics.mean(movies_dict.values())
    median_rating = statistics.median(movies_dict.values())
    movies_sorted = sorted(movies_dict.items(), key=lambda item: item[1],
                           reverse=True)
    best_movie, best_rating = movies_sorted[0]
    worst_movie, worst_rating = movies_sorted[-1]
    print(Fore.LIGHTMAGENTA_EX +
          f"""Average rating: {average_rating}
Median rating: {median_rating}
Best Movie: {best_movie}, {best_rating}
Worst Movie: {worst_movie}, {worst_rating}"""
          )


def random_movie(movies_dict: dict):
    """This function gets data from the dictionary and generates a random
    movie for the user """

    movie, rating = random.choice(list(movies_dict.items()))
    print(
        Fore.LIGHTGREEN_EX + f"Your movie for tonight: {movie}, it's rated {rating}")


def search_movies(movies_dict: dict):
    """This function gets data from movies dictionary, and gets search
    string from user. It prints the name of the movie and rating if found """

    movie_name = input('Enter part of movie name: ')
    movies_lowercase = {key.lower(): value
                        for key, value in movies_dict.items()}
    for movie, rating in movies_lowercase.items():
        if movie_name.lower() in movie:
            print(Fore.LIGHTYELLOW_EX + f"{movie.title()}, {rating}")


def movies_sorted_by_rating(movies_dict: dict):
    """This function gets data from movies dictionary, and prints the a
    sorted list of movies based on their ratings """

    movies_sorted = sorted(movies_dict.items(),
                           key=lambda item: item[1],
                           reverse=True)
    for number in range(len(movies_dict)):
        print(f"{movies_sorted[number][0]}: {movies_sorted[number][1]}")


def create_ratings_histogram(movies_dict: dict):
    """This function gets the data in movies dictionary and creates a
    histogram plot of movie ratings. """

    ratings = list(movies_dict.values())
    plt.hist(ratings, bins=5, color='#86bf91', ec='black')
    plt.title('histogram of movie ratings')
    plt.xlabel('movie ratings')
    plt.ylabel('frequency ')
    plt.show()
    plt.savefig('histogram_movie_rating.png')


def continue_with_movies_app(user_input, user_choice_func, movies_dict):
    """ This function gets user input, user choice and movies dictionary.
   The function prompts user to continue using the app and then calls the
   appropriate function based on user input and user choice """

    while True:
        input("\nPress enter to continue")
        display_menu()
        new_user_input = get_user_input()
        if new_user_input == user_input:
            user_choice_func(movies_dict)
        else:
            return new_user_input


def main():
    # Dictionary to store the movies and the rating
    movies = {
        "The Shawshank Redemption": 9.5,
        "Pulp Fiction": 8.8,
        "The Room": 1,
        "The Godfather": 9.2,
        "The Godfather: Part II": 9.0,
        "The Dark Knight": 9.0,
        "12 Angry Men": 8.9,
        "Everything Everywhere All At Once": 8.9,
        "Forrest Gump": 8.8,
        "Star Wars: Episode V": 8.7
    }

    display_title()
    display_menu()
    user_input = get_user_input()
    exit_app = False
    while not exit_app:
        # Exits movie app if user enters number outside the range: 1-10
        if user_input not in range(10):
            exit_app = True
        else:
            # Dispatch Table from Menu
            user_choice = {
                1: [list_movies, continue_with_movies_app],
                2: [add_movie, continue_with_movies_app],
                3: [delete_movie, continue_with_movies_app],
                4: [update_movie, continue_with_movies_app],
                5: [movie_stats, continue_with_movies_app],
                6: [random_movie, continue_with_movies_app],
                7: [search_movies, continue_with_movies_app],
                8: [movies_sorted_by_rating,
                    continue_with_movies_app],
                9: [create_ratings_histogram,
                    continue_with_movies_app]
            }

            # Dispatches the actions to be performed based on user_input
            user_choice[user_input][0](movies)
            user_input = user_choice[user_input][1](user_input,
                                                    user_choice[user_input][0],
                                                    movies)


if __name__ == "__main__":
    main()
