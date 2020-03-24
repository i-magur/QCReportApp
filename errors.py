class CellIsNotBlank(Exception):
    def __init__(self, msg="Cell is not blank", *args, **kwargs):
        super(CellIsNotBlank, self).__init__(msg, *args, **kwargs)
