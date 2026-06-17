


class FailedConnectionSql(Exception):
    '''
    raise when failed to connect the SQL database. 
    '''
    pass

class InvalidRank(Exception):
    '''
    raise when user enter invalid agent rank
    '''
    pass

class InvalidAmount(Exception):
    '''
    raise when user enter invalid amount (>10 | < 0)
    '''
    pass