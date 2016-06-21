

class NotConfigFileQPanel(BaseException):
    '''
        This exception is raised when is not possible read file for
        QPanel config.
    '''
    def __init__(self, file_path):
        error = 'Error to open file config. Check if %s file exist' % file_path
        super(NotConfigFileQPanel, self).__init__(error)

