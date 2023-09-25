from abc import ABC, abstractmethod

# Abstract interface classes
class UserInterface(ABC):
    @abstractmethod
    def perform_command(self):
        ...

    @abstractmethod
    def get_user_input(self):
        ...

    @abstractmethod
    def display_menu(self):
        ...


class InformationOutputManager(ABC):
    @abstractmethod
    def _show_all_items(self):
        ...

    @abstractmethod
    def _find(self):
        ...


class Manager(ABC):
    @abstractmethod
    def _add_record():
        ...

    @abstractmethod
    def _delete_record():
        ...


class Menu(ABC):
    @abstractmethod
    def show_menu(self):
        ...


class UserInput(ABC):
    @abstractmethod
    def get_user_input(self):
        ...


class ABCRecord(ABC):
    ...


class ConsoleUserInput(UserInput):
    def get_user_input(self) -> str:
        return input("Put your request here: ")


class ConsoleUI(UserInterface):
    def __init__(
        self,
        output_interface: InformationOutputManager,
        manager_interface: Manager,
        menu_interface: Menu,
        input_interface: UserInput,
    ) -> None:
        super().__init__()
        self.output_interface = output_interface
        self.manager_interface = manager_interface
        self.menu_interface = menu_interface
        self.input_interface = input_interface
