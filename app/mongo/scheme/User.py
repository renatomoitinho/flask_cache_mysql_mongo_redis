__author__ = 'renatomoitinhodias'

from mongokit import Document

class RootDocument(Document):
    __database__ = 'test'


def max_length(length):
    def validate(value):
        if len(value) <= length:
            return True
        raise Exception('%s must be at most %s characters long' % length)
    return validate

class User(RootDocument):
    __collection__ = 'users'
    structure = {
        'name': basestring,   #unicode
        'email': basestring,  #unicode
        }
    validators = {
        'name': max_length(50),
        'email': max_length(120)
    }
#    use_dot_notation = True
#    def __repr__(self):
#        return '<User %r>' % self.name