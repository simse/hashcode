# Imports
from multiprocessing import Pool

# Class definitions
class Library:
    _id = 0
    _signup_delay = 0
    _scanning_ability = 0
    _books = []

    def __init__(self, input_id, input_delay, input_scanning_ability, books):
        self._id = input_id
        self._signup_delay = input_delay
        self._scanning_ability = input_scanning_ability
        self._books = books


class Book:
    _id = 0
    _score = 0

    def __init__(self, book_id, score):
        self._id = book_id
        self._score = score


INPUT_FILE = 'b_read_on.txt'


# Read input
book_count = 0
library_count = 0
day_count = 0
libraries = []
books = []

input_file = open('input/' + INPUT_FILE, 'r')
meta_line = input_file.readline()
book_line = input_file.readline()
raw_books = book_line.split(' ')

# Evaluate meta line
book_count = int(meta_line.split(' ')[0])
library_count = int(meta_line.split(' ')[1])
day_count = int(meta_line.split(' ')[2])

# Read books
for book_id in range(book_count):
    books.append(Book(book_id, int(raw_books[book_id])))



#print("ENTERING LIBRARY SECTIONS")
# Read library sections
for library_id in range(library_count):
    # Read library meta
    meta_line = input_file.readline()
    books_in_library = int(meta_line.split(' ')[0])
    sign_up_time = int(meta_line.split(' ')[1])
    scanning_ability = int(meta_line.split(' ')[2])
    library_book_ids = input_file.readline()
    library_books = []

    #print("GATHERED LIBRARY METADATA")

    # Gather el books
    for book_id in library_book_ids.split(' '):
        book_id = int(book_id)
        library_books.append(books[book_id])

    #print("GATHER LIBRARY BOOKS")

    libraries.append(Library(library_id, sign_up_time, scanning_ability, library_books))


# Input variables
# day_count = days
# libraries = list of libraries
# books = list of books
#
#

# Runtime variables
scanned_books = [] # <- Books scanned by a library
days_left = day_count
picked_libraries = [] # <- List of library IDs


# Process
def sum_book_score(library):
    score = 0

    for book in library._books:
        if book._id not in scanned_books:
            score += book._score

    return score


def score_per_scanning_day(library):
    score = sum_book_score(library)

    return score / library._scanning_ability


def score_per_signup_day(library):
    score_per_day = score_per_scanning_day(library)

    return score_per_day / library._signup_delay


def efficiency(library):
    return (library._id, score_per_signup_day(library) * 100)


def pick_library():
    max_efficiency = 0
    max_id = 0
    library_efficiency = []

    with Pool(20) as p:
        library_efficiency = p.map(efficiency, libraries)

    # exit(library_efficiency)

    for library in libraries:
        if library._id not in picked_libraries:
            e = 0

            for l in library_efficiency:
                if l[0] == library._id:
                    e = l[1]

            if e > max_efficiency:
                max_efficiency = e
                max_id = library._id

    picked_libraries.append(max_id)
    return max_id


def library_books_to_be_scanned(library, days_left):
    # Get and sort by score
    sorted_books = sorted(library._books, key=lambda book: book._score, reverse=True)

    # Calculate capability of library
    books_to_be_scanned = (days_left - library._signup_delay) * library._scanning_ability

    # Get books to be scanned
    books_to_scan = sorted_books[:books_to_be_scanned]

    # Register as scanned
    for book in books_to_scan:
        scanned_books.append(book._id)

    return books_to_scan


# For each library:
    # Add up total score of all unscanned books in library
    # Total score / scannable books per day = average score accomplished per scanning day
    # average score per scanning day / Number of days to finish signup = score per scanning day per day of signup (efficiency of the library)



# Generate output
output_library_count = 0
library_lines = []




while days_left > 0:
    # Pick el library
    best_library = libraries[pick_library()]

    #print(best_library._signup_delay)

    # Scan its books
    books_to_scan = library_books_to_be_scanned(best_library, days_left)

    print(days_left)

    # Move time forward
    days_left -= best_library._signup_delay

    #print(days_left)

    # Generate string
    output_library_count += 1
    library_lines.append("{} {}".format(best_library._id, len(books_to_scan)))

    books_string = ""
    for b in books_to_scan:
        books_string += str(b._id) + ' '

    library_lines.append(books_string)

    # Exit conditions
    # All libraries have been signed up
    if len(libraries) == len(picked_libraries):
        break

    # 

# Actual output
output = str(output_library_count) + '\n'
for line in library_lines:
    output += line + '\n'


output_file = open('output/' + INPUT_FILE, 'w')
output_file.write(output)
output_file.close()

print(output)