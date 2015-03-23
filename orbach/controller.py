from orbach import app

from orbach.model import Gallery, User


class GalleryController(object):
    '''
    Class used to perform all manipulations on Gallery objects
    '''

    def __init__(self, gallery):
        self.gallery = gallery

    @staticmethod
    def create(gallery):
        pass

    @staticmethod
    def get_all():
        return Gallery.query.order_by(Gallery.name).all()

    def get(self):
        pass

    def modify(self):
        pass

    def delete(self):
        pass


class UserController(object):
    '''
    Class used to perform all manipulations on User objects
    '''

    def __init__(self, user):
        self.gallery = user

    @staticmethod
    def create(user):
        pass

    @staticmethod
    def get_all():
        return User.query.order_by(User.username).all()

    def get(self):
        pass

    def modify(self):
        pass

    def delete(self):
        pass
