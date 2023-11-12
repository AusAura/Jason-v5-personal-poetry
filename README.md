Run Jason with the Docker image: docker run -it amarakheo/jason-bot

# Jason-personal-assistant-bot
Planning a bloody revenge has never been so convenient.

(Personal version of the application: https://github.com/AusAura/Jason-personal-assistant-bot-team-version-)

### Warning: both README and application concept contain humor content

# What are the differences in this personal version?

- Notebook is also updated with currying and command parser.
- Jason could be run with Docker image now inside of the container.
- For training purposes, SOLID principles were applied.
- Project is using Poetry now.
- Added logging into the file.

## Address Book:
The program stores records of your future victims: their names, numbers, email, and physical address. Also, their birthdays if you want a special greeting.

**It has the following command-functions:**

**№1) The program correctly saves records in save.json and reads them on startup.**

**№2) add <_name> <_phone_number> <_email> <_adress>**
Allows adding a new entry to the address book.

<_name> = str, 1 word
<_phone_number> = Must contain 10-13 symbols and must match one of the current formats: +380001112233 or 80001112233 or 0001112233
<_email> = Must contain min 2 characters before "@" and 2-3 symbols in TLD! Example: aa@example.net or aa@example.com.ua
<_adress> = str

    Doesn't work without any parameters.
    Doesn't work if parameters exceed the specified template.
    Only <_name> and <_phone_number> are mandatory.
    If one or more additional parameters are missing, it still creates a record with empty values for those parameters.
    Phone in the wrong format causes an error.
    Email in the wrong format causes an error.
    If a record with the entered name already exists, overwriting it with a new one is considered correct behavior.

**№3) add phone <_name> <_phone_number>**
Allows adding a new phone to the created entry.

<_name> = str, 1 word
<_phone_number> = Must contain 10-13 symbols and must match one of the current formats: +380001112233 or 80001112233 or 0001112233

    Doesn't work without any parameters.
    Doesn't work if parameters exceed the specified template.
    <_name> and <_phone_number> are mandatory.
    If one of the additional parameters is missing, it gives the corresponding error.
    Phone in the wrong format causes an error.
    If a record with the entered name does not exist, it gives an error.
    If the added phone already exists in the entry, it gives an error.

**№4) edit phone <_name> <_phone_number>**
Allows editing the phone in the created entry.

<_name> = str, 1 word
<_phone_number> = Must contain 10-13 symbols and must match one of the current formats: +380001112233 or 80001112233 or 0001112233

    Doesn't work without any parameters.
    Doesn't work if parameters exceed the specified template.
    <_name> and <_phone_number> are mandatory.
    If one of the additional parameters is missing, it gives the corresponding error.
    If the record with the entered name does not exist, it gives an error.
    If the entered phone does not exist in the entry, it gives an error.
    If it exists, it asks which phone to replace it with.
    The new phone in the wrong format causes an error.
    If the new phone matches the old one in the entry, it still makes the change.

**№5) show all**
Displays all existing entries in the book with all the information about them.

    Doesn't work if it has any parameters.
    If there are parameters, it gives the corresponding error.
    Displays all existing records and all available information about them.
    If some field is empty, it displays emptiness.
    If the book is empty, it displays the appropriate message.

**№6) show some**
Displays all existing entries in the book with all the information about them, but step by step in the specified quantity.
(Generator, for decreasing potential load on the server and execution time from showing all existing entries)

    Doesn't work if it has any parameters.
    If there are parameters, it gives the corresponding error.
    Asks how many entries to display in 1 iteration.
    If the quantity < 0, it displays an error.
    If the entered value != int, it displays an error.
    If the entered quantity exceeds the total number of entries in the book, it displays the appropriate message and shows all entries available.
    Displays all existing records and all available information about them.
    If there are still unprinted entries in the address book, it asks whether to display them.
    If 'y' is entered (the command is not case-sensitive), it shows the next batch of entries.
    If 'n' is entered, the function terminates and returns to the address book subprogram menu.
    If some field is empty, it displays emptiness.
    If the book is empty, it displays the appropriate message.

**№7) delete phone <_name> <_phone_number>**
Deletes the specified phone from the created entry.

<_name> = str, 1 word
<_phone_number> = Must contain 10-13 symbols and must match one of the current formats: +380001112233 or 80001112233 or 0001112233

    Doesn't work without any parameters.
    Doesn't work if parameters exceed the specified template.
    <_name> and <_phone_number> are mandatory.
    If one of the additional parameters is missing, it gives the corresponding error.
    If the record with the entered name does not exist, it gives an error.
    If the entered phone does not exist in the entry, it gives an error.
    Phone in the wrong format causes an error.
    If the phone matches the one found in the entry, it deletes it.

**№8) delete contact <_name>**
Deletes the specified entry completely.

    Doesn't work without any parameters.
    Doesn't work if parameters exceed the specified template.
    <_name> is mandatory.
    If one of the additional parameters is missing, it gives the corresponding error.
    If the record with the entered name does not exist, it gives an error.
    If the name matches the one found in the record, it deletes the record from the address book object.

#9) set bday <_name>
Allows adding a birthday to an existing entry.

<_name> = str, 1 word

    Doesn't work without any parameters.
    Doesn't work if parameters exceed the specified template.
    <_name> is mandatory.
    If one of the additional parameters is missing, it gives the corresponding error.
    If the record with the entered name does not exist, it gives an error.
    If it exists, it asks to enter the birthday following the template (10 January 2020).
    A template in the wrong format should cause an error.
    A correctly entered template should add a birthday entry to the Record and display a success message.
    If a birthday entry already exists, it overwrites it.

**#10) set email <_name>**
Allows adding an email address to an existing entry.

    Doesn't work without any parameters.
    Doesn't work if parameters exceed the specified template.
    <_name> is mandatory.
    If one of the additional parameters is missing, it gives the corresponding error.
    If the record with the entered name does not exist, it gives an error.
    If it exists, it asks to enter the email following the template (myemail@google.com).
    A template in the wrong format should cause an error:
    Must contain min 2 characters before "@" and 2-3 symbols in TLD!
    A correctly entered template should add an email entry to the Record and display a success message.
    If an email entry already exists, it overwrites it.

**#11) set address <_name>**
Allows adding a physical address to an existing entry.

<_name> = str, 1 word

    Doesn't work without any parameters.
    Doesn't work if parameters exceed the specified template.
    <_name> is mandatory.
    If one of the additional parameters is missing, it gives the corresponding error.
    If the record with the entered name does not exist, it gives an error.
    If it exists, it asks to enter the address (no template).
    Should add an address entry to the Record and display a success message.
    If an address entry already exists, it overwrites it.

**#12) show bday <_name>**
Displays the birthday date and the number of days until it for the specified entry.

<_name> = str, 1 word

    Doesn't work without any parameters.
    Doesn't work if parameters exceed the specified template.
    <_name> is mandatory.
    If the record with the entered name does not exist, it gives an error.
    If it exists, it displays the birthday date from the entry and the correct number of days until it.
    If the date is not set, it displays the appropriate message.

**#13) show email <_name>**
Displays the email for the specified entry.

<_name> = str, 1 word

    Doesn't work without any parameters.
    Doesn't work if parameters exceed the specified template.
    <_name> is mandatory.
    If the record with the entered name does not exist, it gives an error.
    If it exists, it displays the correct email for it.
    If the email is not set, it displays the appropriate message.

**#14) show address <_name>**
Displays the physical address for the specified entry.

<_name> = str, 1 word

    Doesn't work without any parameters.
    Doesn't work if parameters exceed the specified template.
    <_name> is mandatory.
    If the record with the entered name does not exist, it gives an error.
    If it exists, it displays the correct address for it.
    If the address is not set, it displays the appropriate message.

**#15) find <_something>**
Fast search for the specified string in names, phone numbers, emails, and physical addresses. Displays a full list of matches.

<_something> = str, 1 word

    Doesn't work without any parameters.
    Doesn't work if parameters exceed the specified template.
    <_something> is mandatory.
    If <_something> is not found in names, phone numbers, addresses, or emails of all existing entries, it gives an error.
    If found, it displays entries that have <_something>.

**#16) help**
Displays all available commands.

    Doesn't work if it has any parameters.
    If there are parameters, it gives the corresponding error.
    Displays all existing commands.

**#17) bday in <_days>**
Displays all existing entries in which birthdays will occur in the specified number of days.

<_days> = int > 0

    Doesn't work without parameters.
    Doesn't work if it has additional parameters.
    <_days> is mandatory.
    If <_days> is not a number, it gives an error.
    If <_days> <= 0, it gives an error.
    Displays all existing entries with names, dates, and the number of days until the birthday if they are earlier than or equal to <_days>.
    If there are none, it displays the appropriate message.

**#18) good bye**
Terminates the program, saving changes.

    Doesn't work if it has any parameters.
    If there are parameters, it gives the corresponding error.
    Ends the operation of the address book, returning to the main program.
    All entries will be correctly saved to the file save.json.

**#19) close**
Terminates the program, saving changes.

    Doesn't work if it has any parameters.
    If there are parameters, it gives the corresponding error.
    Ends the operation of the address book, returning to the main program.
    All entries will be correctly saved to the file save.json.

**#20) hello**
Displays a greeting because even bloody revenge does not interfere with politeness.

    Doesn't work if it has any parameters.
    If there are parameters, it gives the corresponding error.
    Displays a greeting.

**#21) not save**
Terminates the program WITHOUT SAVING CHANGES.

    Doesn't work if it has any parameters.
    If there are parameters, it gives the corresponding error.
    Ends the operation of the address book, returning to the main program.
    All changes will NOT be saved to the file save.json.


## Notebook: 
This program allows you to create, edit, delete, and view notes. Each note has a title, content, and a list of tags. Additionally, you can add tags to existing notes and modify their content.

**Supported commands:**

**№1) add (Add a note) -**
The add_note() function allows users to create new notes. The user enters the note's title (minimum 5 characters), content (minimum 10 characters), and tags separated by commas or spaces (1 to 20 characters each).

    Does not work without any parameters.
    Does not work if the entered data does not meet the conditions, such as the length of the title, content, or tag.
    Only Title and Content are mandatory.

**№2) edit (Edit a note) -**
The edit_note() function allows users to edit existing notes. The user enters the title of the note they want to edit and then enters the new content of the note.

    Does not work if the note with the entered title does not exist.
    Does not work if the entered data does not meet the conditions for the length of the content.

**№3) delete (Delete a note) -**
The delete_note() function allows users to delete notes. The user enters the title of the note they want to delete.

    Does not work if the note with the entered title does not exist.

**№4) tag (Add a tag to a note) -**
The add_tag_to_note() function allows users to add tags to existing notes. The user enters the title of the note to which they want to add a tag and then enters new tags separated by commas or spaces.

    Does not work if the note with the entered title does not exist.
    Does not work if trying to add tags that already exist for this note.
    Does not work if the entered data does not meet the conditions for the length of the tag.

**№5) sort (Sort notes) -**
The sort_notes() function allows users to sort notes based on keywords in tags, titles, or content.

**№6) list (List notes) -**
The display_notes() function displays all available notes.

**№7) search (Search notes) -**
The search_notes() function allows users to search for notes based on keywords in titles, content, or tags.

**№8) load (Load notes) -**
The load_notes() function allows users to load notes from a file. The user enters the file name to load notes from. The file must be in JSON format.

    Does not work if the file with notes (.json) does not exist or has an incorrect format.

**№9) save (Save notes) -**
The save_notes() function saves all notes to a file in JSON format.

**№10) exit (Exit) -**
Exits the program, saving notes to a file.


## File sorter:
The subroutine serves as your personal black belt in sorting and cleaning.

Certainly, you have a folder where clutter constantly accumulates in the form of old photos of eliminated targets, videos of past interrogations, once-popular songs, secret old archives with documents, and various other files. In this case, your pocket cleaner comes into play.

All you need to do is simply **specify the path to the folder with all the clutter**, and this program will sort all the files and move them to a new folder. Inside this new folder, there will be subfolders with appropriate names containing files sorted according to the format. Archives will be unpacked and placed in folders with names corresponding to the names of the archives.

During the sorting process, **all file names written in Cyrillic characters will be replaced with Latin characters while preserving the names.**
