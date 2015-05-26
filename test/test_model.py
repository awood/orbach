from orbach.model import Gallery, GalleryProperty

from test.test_orbach import OrbachTest


class ModelTest(OrbachTest):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.session = self.app.db.session

    def test_gallery_properties(self):
        g = Gallery()
        g.name = 'x'
        g.description = 'description'
        g.properties['hello'] = GalleryProperty('hello', 'world')
        self.session.add(g)
        self.session.commit()

        results = self.session.query(Gallery)
        self.assertEqual(1, results.count())

        result = results.first()
        self.assertEqual('x', result.name)
        self.assertEqual('world', result.properties['hello'].value)

        self.session.delete(g)
        self.session.commit()
        self.assertEqual(0, self.session.query(Gallery).count())
