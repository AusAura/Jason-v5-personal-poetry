import json, os
from command_parser import parse_command, exception_catcher_decorator
from command_parser import WrongArgumentFormat
from interface import (
    InformationOutputManager,
    ConsoleUI,
    Manager,
    Menu,
    UserInput,
    ConsoleUserInput,
    ABCRecord,
)
from typing import Union
import logging

logger = logging.getLogger("Note Debugger")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter_print = logging.Formatter("%(message)s")
formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
ch.setFormatter(formatter_print)
fh = logging.FileHandler("note_debug.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)


# LOW ENTITY CLASSES
# Клас Note представляє окрему нотатку з такими атрибутами:
# title: Рядок, що представляє заголовок нотатки.
# content: Рядок, що містить вміст нотатки.
# tags: Список рядків, які представляють теги, пов'язані з нотаткою.
class Note(ABCRecord):
    def __init__(self, title, content, tags=[]) -> None:
        self.title = title
        self.content = content
        self.tags = tags if tags is not None else []

    def __str__(self) -> str:
        return f"Title: {self.title}\nContent: {self.content}\nTags: {', '.join(self.tags)}"


# Клас Notebook представляє собою колекцію нотаток і надає методи для їх управління. Він має наступні атрибути:
# notes: Список об'єктів Note.
# filename: Назва файлу, який використовується для зберігання нотаток у форматі JSON.
class Notebook:
    def __init__(self, filename: str = "notes.json") -> None:
        self.notes = []
        self.filename = filename
        self.is_finished = False

        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                json.dump([], file)
        else:
            self.load_notes()

    def add_note(
        self, note: Note
    ) -> (
        None
    ):  # Додає нову нотатку до блокнота. Перевіряє наявність нотаток з однаковими заголовками і валідує довжину тегів.
        if any(len(tag) > 15 for tag in note.tags):
            raise WrongArgumentFormat("Invalid format. Tags <= 15")

        # Перевірка на однакові назви
        title = note.title.casefold()
        for existing_note in self.notes:
            if existing_note.title.casefold() == title:
                logger.debug("Note with the same title already exists.")
                return

        self.notes.append(note)
        logger.debug("Note added!")

    def find_notes(
        self, keyword: str
    ) -> (
        list
    ):  # Шукає нотатки, які містять вказане ключове слово в їхніх заголовках, вмісті або тегах.
        """Пошук нотаток за ключовим словом."""
        keyword = keyword.lower()
        matching_notes = []
        for note in self.notes:
            if (
                keyword in note.title.lower()
                or keyword in note.content.lower()
                or keyword in note.tags
            ):
                matching_notes.append(note)
        return matching_notes

    def find_note(
        self, title: str
    ) -> Union[Note, None]:  # Знаходить нотатку за її заголовком.
        title = title.casefold()
        for note in self.notes:
            if note.title.casefold() == title:
                return note
        return None

    def edit_note(self, title: str) -> bool:  # Редагує вміст існуючої нотатки.
        note = self.find_note(title)
        if note is None:
            logger.debug("Note not found!")
            return False

        logger.debug(f"Editing note: {note.title}")
        logger.debug(f"Current content: {note.content}")

        try:
            new_content = input("Enter the new content: ")
            if len(new_content) < 10:
                raise WrongArgumentFormat(
                    "Invalid format. Content length should be >= 10."
                )
        except WrongArgumentFormat as error:
            logger.debug(error)
        else:
            note.content = new_content
            return True

    def _delete_record(self, title: str) -> bool:  #  Видаляє нотатку за заголовком.
        title = title.casefold()
        for note in self.notes.copy():
            if note.title.casefold() == title.casefold():
                self.notes.remove(note)
                return True
        return False

    def list_notes(self) -> None:  # Перелічує всі нотатки у блокноті.
        if not self.notes:
            logger.debug("No notes available.")
        else:
            for i, note in enumerate(self.notes, start=1):
                logger.debug(f"{i}. Title: {note.title}")
                logger.debug(f"   Content: {note.content}")
                logger.debug(f"   Tags: {', '.join(note.tags)}")

    def save_notes(self) -> None:  # Зберігає нотатки у JSON-файлі.
        data = [
            {"title": note.title, "content": note.content, "tags": note.tags}
            for note in self.notes
        ]
        with open(self.filename, "w") as file:
            json.dump(data, file)

    def load_notes(self) -> None:  # Завантажує нотатки з JSON-файлу.
        with open(self.filename, "r") as file:
            data = json.load(file)
            self.notes = [
                Note(note["title"], note["content"], note["tags"]) for note in data
            ]


# Interface Classes
# '''Main IU class that user directly should work with'''
class NoteBookConsoleUI(ConsoleUI):
    def __init__(
        self,
        output_interface: InformationOutputManager,
        manager_interface: Manager,
        menu_interface: Menu,
        input_interface: UserInput,
    ) -> None:
        super().__init__(
            output_interface, manager_interface, menu_interface, input_interface
        )

        # available command list
        self.command_list = {
            "add": manager_interface._add_record,
            "edit": manager_interface._edit_record,
            "delete": manager_interface._delete_record,
            "add tag": manager_interface._add_tag,
            "sort": output_interface._sort_notes_by_tags,
            "list": output_interface._show_all_items,
            "find": output_interface._find,
            "reset": manager_interface._reset,
            "save": manager_interface._save,
            "exit": manager_interface._finish,
            "help": menu_interface.show_menu,
        }

    # Universal command performer/handler
    @exception_catcher_decorator
    def perform_command(self, command: str, notebook, *args, **kwargs) -> None:
        self.command_list[command](notebook, *args, **kwargs)

    def get_user_input(self) -> str:
        return self.input_interface.get_user_input()

    def display_menu(self, *_) -> None:
        self.menu_interface.show_menu()


# '''User Input Manager Class'''
class NoteBookUserInput(ConsoleUserInput):
    ...


# '''Information Output Manager Class'''
class NoteBookInformationOutput(InformationOutputManager):
    @exception_catcher_decorator
    def _find(self, notebook: Notebook, line_list: list) -> None:
        # Пошук нотаток за ключовим словом.
        keyword = line_list[1]
        matching_notes = notebook.find_notes(keyword)
        if matching_notes:
            logger.debug("Found notes:")
            for note in matching_notes:
                logger.debug(note)
        else:
            logger.debug("No notes found.")

    @exception_catcher_decorator
    def _hello(self, *_) -> None:
        logger.debug("How can I help you?")

    @exception_catcher_decorator
    def _show_all_items(self, notebook, *_) -> None:
        # Вивести список нотаток.
        notebook.list_notes()

    @exception_catcher_decorator
    def _sort_notes_by_tags(self, notebook: Notebook, line_list: list, *_) -> None:
        # Cортування нотаток.
        keyword = line_list[1].casefold()

        notes_with_priority = []

        for note in notebook.notes:
            priority = 0

            if any(keyword in tag.lower() for tag in note.tags):
                priority += 3

            if keyword in note.title.lower():
                priority += 2

            if keyword in note.content.lower():
                priority += 1

            notes_with_priority.append((note, priority))

        sorted_notes = sorted(notes_with_priority, key=lambda x: x[1], reverse=True)

        for note, _ in sorted_notes:
            logger.debug(note)


# '''Manager Class That Apply Changes To The Book'''
class NoteBookManager(Manager):
    @exception_catcher_decorator
    def _add_tag(self, notebook: Notebook, line_list: list) -> None:
        # Додати тег до нотатки.
        title = line_list[1]
        note = notebook.find_note(title)

        if note is None:
            logger.debug("Note not found!")

        else:
            new_tags_input = input("Enter Tags (comma-separated or space-separated): ")
            new_tags = [tag.strip() for tag in new_tags_input.replace(",", " ").split()]

            if not new_tags:
                logger.debug("Invalid format. Tags can't be empty.")

            elif all(len(tag) < 20 for tag in new_tags):
                if any(tag.casefold() in note.tags for tag in new_tags):
                    logger.debug("Some tags already exist for this note.")
                else:
                    note.tags.extend(new_tags)
                    logger.debug("Tags added!")

            else:
                logger.debug("Invalid format. Tags <= 20.")

    @exception_catcher_decorator
    def _add_record(self, notebook, line_list, *_) -> None:
        # Додати нотатку.
        try:
            title = line_list[1]
            if len(title) < 5:
                raise WrongArgumentFormat(
                    "Invalid format. Title length should be >= 5."
                )
        except WrongArgumentFormat as error:
            logger.debug(error)
        else:
            try:
                content = input("Enter content: ")
                if len(content) < 10:
                    raise WrongArgumentFormat(
                        "Invalid format. Content length should be >= 10."
                    )
            except WrongArgumentFormat as error:
                logger.debug(error)
            else:
                tags = input("Enter Tags (comma-separated or space-separated): ")
                tags = [tag.strip() for tag in tags.replace(",", " ").split()]
                note = Note(title, content, tags)
                notebook.add_note(note)

    @exception_catcher_decorator
    def _edit_record(self, notebook: Notebook, line_list: list, *_) -> None:
        # Редагувати нотатку.
        title = line_list[1]

        if notebook.edit_note(title):
            logger.debug("Note edited!")

    @exception_catcher_decorator
    def _delete_record(self, notebook: Notebook, line_list: list, *_) -> None:
        # Видалити нотатку.
        title = line_list[1].strip()
        if notebook._delete_record(title.casefold()):
            logger.debug("Note deleted!")
        else:
            logger.debug("Note not found!")

    def _close_without_saving(self, notebook, *_) -> None:
        notebook.is_finished = True
        logger.debug("Will NOT save! BB!")

    def _finish(self, notebook, *_) -> None:
        notebook.is_finished = True
        logger.debug("Good bye!")

    def _reset(self, notebook, *_) -> None:
        notebook.load_notes()
        logger.debug("Notes loaded from the file as it was before the start.")

    def _save(self, notebook: Notebook, *_) -> None:
        # Зберегти нотатки у файл.
        notebook.save_notes()
        logger.debug("Notes saved to the file.")


# '''Menu Class That Works With Menu'''
class NoteBookMenu(Menu):
    def __init__(self) -> None:
        # command vocab with descriptions
        self.command_description = {
            "add": "Add Note (Додати нот)",
            "edit": "Edit Note (Редагувати вміст)",
            "delete": "Delete Note (Видалити)",
            "add tag": "Add Tag (Додати тег)",
            "sort": "Sort Notes (Сортування)",
            "list": "List Notes (Вивести список)",
            "find": "Find Notes(Пошук)",
            "reset": "Reset Session (Збросити зміни)",
            "save": "Save Notes (Зберігання)",
            "exit": "Exit (Вихід без зберігання)",
        }

    def show_menu(self, *_) -> None:
        logger.debug(f"Available commands:")
        for command, description in self.command_description.items():
            logger.debug(f"{command} - {description}")


# MAIN func
def main() -> None:
    output_interface = NoteBookInformationOutput()
    manager_interface = NoteBookManager()
    menu_interface = NoteBookMenu()
    input_interface = NoteBookUserInput()
    ui = NoteBookConsoleUI(
        output_interface, manager_interface, menu_interface, input_interface
    )

    notebook = Notebook()

    logger.debug("*" * 10)
    ui.output_interface._hello()
    logger.debug("*" * 10)
    ui.menu_interface.show_menu()

    while True:
        logger.debug("*" * 10)
        user_input = ui.get_user_input()
        line_list = parse_command(user_input, ui.command_list)
        current_command = line_list[0].casefold()
        ui.perform_command(current_command, notebook, line_list)

        # checker to return to jason.py, bcz decorator over 'perform_command' returns None and makes it tricky
        if notebook.is_finished:
            break


# EXECUTE
if __name__ == "__main__":
    main()
