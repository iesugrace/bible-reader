import os

class Config:
    """ Process and store the user settings

    Subclass can redefine the attribute 'fileName'
    and the method 'validate' to suite the needs.
    """

    fileName = '.biblerc'

    def __init__(self, path=None):
        if not path:
            path = os.path.join(os.getenv('HOME'), self.fileName)
        code = open(path).read()
        configs = {}
        exec(code, configs)
        configs = {k: v for k, v in configs.items() if k[0] != '_'}
        self.data = configs
        self.validate()

    def __getattr__(self, name):
        return self.data[name]

    def validate(self):
        """Validate the config items"""
        assert self.data.get('TOTD_parts'), "config: TOTD_parts not set"
        assert self.data.get('player'), "config: audio player not set"
