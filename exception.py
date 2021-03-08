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


class TestWindow_BaseError(Exception):
    pass
