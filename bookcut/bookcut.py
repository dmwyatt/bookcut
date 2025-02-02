import click
import pyfiglet
from os import name, system
from bookcut.mirror_checker import main as mirror_checker
from bookcut.book import book_find
from bookcut.organise import main_organiser
from bookcut.search import search_downloader, link_finder, search
from bookcut.book_details import main as detailing
from bookcut.bibliography import main as allbooks
from bookcut.bibliography import save_to_txt
from bookcut.settings import initial_config, mirrors_append, read_settings
from bookcut.settings import screen_setting, print_settings, set_destination, path_checker
from bookcut.booklist import booklist_main


@click.group(name='commands')
@click.version_option(version="1.3.3")
def entry():
    """
    for a single book download you can \n
    bookcut.py book --bookname "White Fang" -- author "Jack London"
    \nor  bookcut.py book -b "White Fang" -a "Jack London" \n
*For a more complete help:  bookcut.py [COMMAND] --help\n
*For example: bookcut.py list --help
    """
    # read the settings ini file and check what value for clean screen
    settings = read_settings()
    clean_screen(settings[0])
    title = pyfiglet.figlet_format("BookCut")
    click.echo(title)
    click.echo('**********************************')
    print("Welcome to BookCut! I'm here to"
          '\nhelp you to read your favourite books!')
    print('**********************************')


@entry.command(name='list', help='Download a list of ebook from a .txt file')
@click.option('--file', '-f',
              help='A .txt file in which books are written in a separate line',
              required=True)
@click.option('--destination', '-d',
              help="The destinations folder of the downloaded books",
              default=path_checker())
@click.option('--forced',
              help='Forced option, accepts all books for downloading',
              is_flag=True)
@click.option('--extension', '-ext', help='File type of e-book.')
def download_from_txt(file, destination, forced, extension):
    click.echo('Importing of book list:Started.')
    if forced:
        click.echo(click.style('(!) Forced list downloading:Enabled', fg='green'))
    booklist_main(file, destination, forced, extension)


@entry.command(name='book', help="Download a book in epub format, by inserting"
               '\n the title and the author')
@click.option('--book', '-b', help="Title of Book", required=True)
@click.option('--author', '-a', help='The author of the Book', default=" ")
@click.option('--publisher', '-p', default='')
@click.option('--destination', '-d',
              help="The destinations folder of the downloaded books",
              default=path_checker())
@click.option('--extension', '-ext', help='Filetype of e-book for example:pdf')
@click.option('--forced', is_flag=True)
def book(book, author, publisher, destination, extension, forced):
    if author != ' ':
        click.echo(f'\nSearching for {book.capitalize()} by {author.capitalize()}')
    else:
        click.echo(f'\nSearching for {book.capitalize()}')
    url = mirror_checker()
    if url is not None:
        book_find(book, author, publisher, destination, extension, forced, url)


def clean_screen(setting):
    """ Cleans the terminal screen """
    if setting == 'True':
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')


@entry.command(name='organise',
               help='Organise the ebooks in folders according\n to genre')
@click.option('--directory', '-d', help="Directory of source ", required=True,
              default=path_checker())
@click.option('--output', '-o',
              help="The destination folder of organised books",
              default=path_checker())
def organiser(directory, output):
    print("\nBookCut is starting to \norganise your books!")
    main_organiser(directory)


@entry.command(name='all-books',
               help="Search and return all the books from an author")
@click.option('--author', '-a', required=True, help='Author name')
@click.option('--ratio', '-r', help='Ratio for filtering  book results',
              default='0.7', type=float)
def bibliography(author, ratio):
    print(f'\nStart searching for all books by {author.capitalize()}:')
    lista = allbooks(author, ratio)
    if lista is not None:
        print('**********************************')
        choice = 'y or n'
        while choice != 'Y' or choice != 'N':
            choice = input('\nDo you wish to save the list? [Y/n]: ')
            choice = choice.capitalize()
            if choice == 'Y':
                save_to_txt(lista, path_checker(), author)
                break
            elif choice == 'N':
                print('Aborted.')
                break


@entry.command(name='search',
               help='Search LibGen and choose a book to download')
@click.option('--term', '-t', help='Term for searching')
def searching(term):
    print('Searching for:', term.capitalize())
    c = search(term)
    if c is not None:
        link = c[0]
        #### TODO: to erase
        mirror_used = mirror_checker()
        link = mirror_used + link
        print("First Link:", link)
        details = link_finder(link, mirror_used)
        filename = details[0]
        file_link = details[1]
        search_downloader(filename, file_link)


@entry.command(name='details', help='Search the details of a book')
@click.option('--book', '-b', help='Enter book & author or the ISBN number.',
              required=True, default=None)
def details(book):
    detailing(book)


@entry.command(name='config', help='BookCut configuration settings')
@click.option('--libgen_add', help="Add a Libgen mirror to mirrors list",
              default=None)
@click.option('--restore', help='Restores the settings file to initial state',
              is_flag=True)
@click.option('--settings', help='Prints the current BookCut settings',
              is_flag=True)
@click.option('--clean_screen', help='You can choose if BookCut will'
              ' clean terminal screen', is_flag=True)
@click.option('--download_folder', help="Set BookCut's download folder",
              default=None)
def configure_mode(restore, libgen_add, settings, clean_screen,
                   download_folder):
    if restore:
        prompt = click.confirm('\n Are you sure do you want to restore Settings?')
        if prompt is True:
            initial_config()
        else:
            click.echo('Aborted!')
    elif libgen_add is not None:
        click.echo(f'Adding {libgen_add} to mirrors list')
        mirrors_append(libgen_add)
    elif settings:
        print_settings()
    elif clean_screen:
        prompt = click.confirm('\nDo you want Bookcut to clean command line?')
        if prompt is True:
            screen_setting('True')
        else:
            screen_setting('False')
    elif download_folder is not None:
        set_destination(download_folder)
    else:
        print('Usage: bookcut config [OPTIONS]',
              "\nTry 'bookcut config --help' for help.\n",
              "\nError: Missing option or flag."
              )


if __name__ == '__main__':
    entry()
