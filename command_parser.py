# Custom Exception Types
class TerribleException(Exception):
    pass

class ExcessiveArguments(Exception):
    pass

class WrongArgumentFormat(Exception):
    pass


# Universal Decorator That Catches Main Exceptions
def exception_catcher_decorator(func):
    def inner(*args, **kwargs) -> None:
        try:
            func(*args, **kwargs)

        except TypeError as error:
            print(f'Argument type is not acceptable! {error}')
            return
        except ValueError:
            print(f'Too many arguments for {func.__name__}! Probably you are using too many spaces.')
            return
        except IndexError:
            print(f'Not enough arguments for {func.__name__}!')
            return
        except TerribleException:
            print('''Something REALLY unknown had happened during your command reading! Please stay  
            calm and run out of the room!''')
            return
        except KeyError:
            print('Such command does not exist!')
            return
        except ExcessiveArguments:
            print(f'Too many arguments for {func.__name__}! Probably you are using too many spaces.')
            return
        except WrongArgumentFormat:
            return

    return inner

# Deconstructor that allows using commands with any number or keywords and with any number or passed parameters
def parse_command(input_line: str, command_list: list) -> list:
    line_list = input_line.split(' ')

    if len(line_list) <= 0:
        print('''Something REALLY unknown had happened during your command reading! Please stay  
              calm and run out of the room!''')
        return

    if len(line_list) == 1:
        return line_list

    old_complex_command = line_list[0].casefold()
    new_line_list = line_list.copy()

    for item in line_list:

        if item.casefold() == old_complex_command:
            new_line_list.remove(item)
            continue

        new_complex_command = old_complex_command + ' ' + item.casefold()

        if new_complex_command not in command_list:
            new_line_list.insert(0, old_complex_command)
            break

        new_line_list.remove(item)
        old_complex_command = new_complex_command

        if len(new_line_list) == 0:
            new_line_list.insert(0, old_complex_command)
            break

    return new_line_list