class LoginWindow_BaseError(Exception):
    pass

class LoginForbiddenSymbols(LoginWindow_BaseError):
    error_title = "forbidden symbols in login"
    error_msg = "only eng symbols with numbers" 

class PasswordForbiddenSymbols(LoginWindow_BaseError):
    error_title = "forbidden symbols in password"
    error_msg = "only eng symbols with numbers" 

class EmptyLine_LW(LoginWindow_BaseError):
    error_title = 'Warning'
    error_msg = "One of the stringboxes is empty"

class ExistedUser(LoginWindow_BaseError):
    error_title = 'Warning'
    error_msg = 'existed login'

class WrongLoginOrPassword(LoginWindow_BaseError):
    error_title = 'Warning'
    error_msg = 'wrong login or password'


class MainWindow_BaseError(Exception):
    pass

class Wrong_Search_Language(MainWindow_BaseError):
    error_msg = 'Поменяйте язык для ввода или нажмите на кнопку смены таблиц'
    #error_title = "Cannot recognize searching language"
    #error_msg = "Switch lang or \n press switch tables button"

class Wrong_Translation_Language(MainWindow_BaseError):
    #error_title = "Cannot recognize translation language"
    error_msg = "Switch lang or \n press switch tables button"

class EmptyLine(MainWindow_BaseError):
    #error_title = "Note enough"
    error_msg = "One of the stringboxes is empty"

class ExistedWord(MainWindow_BaseError):
    error_msg = "Existed word"

class WordIsMissing(MainWindow_BaseError):
    error_msg = "Word Is Missing"

class SmallTestSet(MainWindow_BaseError):
    error_msg = "select at least 4 word for testing"


class TestWindow_BaseError(Exception):
    pass


class DB_BaseError(Exception):
    pass

class NotConnectionToDB(DB_BaseError):
    error_title = 'critical'
    error_msg = "Unable to establish a database connection. Contact the dev"

class WrongDbQuery(DB_BaseError):
    error_title = 'Warning'
    def __init__(self, error_msg):
        WrongDbQuery.error_msg = error_msg