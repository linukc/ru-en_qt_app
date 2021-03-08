class MainWindow_BaseError(Exception):
    pass

class LoginWindow_BaseError(Exception):
    pass

class TestWindow_BaseError(Exception):
    pass

class Wrong_Search_Language(MainWindow_BaseError):
    #error_msg = 'Поменяйте язык для ввода или нажмите на кнопку смены таблиц'
    error_title = "Cannot recognize searching language"
    error_msg = "Switch lang or \n press switch tables button"

class Wrong_Translation_Language(MainWindow_BaseError):
    error_title = "Cannot recognize translation language"
    error_msg = "Switch lang or \n press switch tables button"

class EmptyLine(MainWindow_BaseError):
    error_title = "Note enough"
    error_msg = "One of the stringboxes is empty"