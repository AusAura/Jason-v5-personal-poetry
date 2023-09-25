import address_book, note_book, file_sort


# inner jason.py fnctions
# avoiding next cycle execution and I/O exception after basic exit() with 'is_finished' var
def exit() -> bool:
    return True


# simplified version without advanced interface, for now
def show_help() -> None:
    command_help = {
        "address": "Address book of your victims",
        "note": "Notebook for special murders",
        "sort": "Sort files in some folder",
        "exit": "Exit",
    }

    for key, value in command_help.items():
        print(f"'{key}': {value}")


command_list = {
    "address": address_book.main,
    "note": note_book.main,
    "sort": file_sort.main,
    "exit": exit,
    "help": show_help,
}


# MAIN
def main() -> None:
    is_finished = False

    while True:
        show_help()
        choice = input("Choose program: ")

        try:
            is_finished = command_list[choice]()
        except:
            print("Use only specified commands!")

        if is_finished:
            break


# EXECUTE
if __name__ == "__main__":
    main()
