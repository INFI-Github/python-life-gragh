import matplotlib.pyplot as plt
from details import details
import pymongo
from datetime import date
import typer
from colorama import Fore


app = typer.Typer()

mongo = pymongo.MongoClient(details.MONGO_URI)
database = mongo['life-graph']['ratings']


def make_a_graph(x, y):
    for i in database.find({}):
        y.append(i['rating'])
        x.append(i['date'])
    plt.plot(x, y)
    plt.show()


def insert_a_rating(rating, comment):
    database.insert_one(
        {'date': str(date.today()), 'rating': rating, 'comment': comment})


@app.command()
def rate():
    try:
        if database.find_one({'date': str(date.today())}):
            print(Fore.YELLOW+'You have already rated today' + Fore.RESET)
            print()
        else:
            rating = typer.Typer.input('Enter your rating: ')
            comment = typer.Typer.input('Enter your comment: ')
            insert_a_rating(rating, comment)
            print(Fore.GREEN + 'Rating Saved !')
    except:
        print(Fore.RED + 'Something went wrong !')


@app.command()
def show_graph():
    try:
        y = []
        x = []
        make_a_graph(x, y)
        print(Fore.GREEN + 'Graph Generated !' + Fore.RESET)
    except:
        print(Fore.RED + 'Something went wrong !' + Fore.RESET)

@app.command()
def delete_data():
    confirmation = input(Fore.RED + 'Are you sure you want to delete all data ? (y/n) : ' + Fore.RESET)
    if confirmation == 'y':
        try:
            database.delete_many({})
            print(Fore.GREEN + 'Data Deleted !' + Fore.RESET)
        except:
            print(Fore.RED + 'Something went wrong !' + Fore.RESET)
    else:
        print(Fore.GREEN + 'Data not deleted !' + Fore.RESET)


if __name__ == '__main__':
    app()
