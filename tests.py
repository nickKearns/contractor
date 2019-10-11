from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId

sample_album_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_album = {
    'title': 'Led Zeppelin III',
    'description': 'Third self titled album',
    'year_released': '1970',
    'category': 'rock'
}
sample_form_data = {
    'title': sample_album['title'],
    'description': sample_album['description'],
    'year_released': sample_album['year_released'],
    'category': sample_album['category']
}


class AlbumsTests(TestCase):
    '''flask tests'''
    def setUp(self):
        '''do before every test'''

        '''flask test client'''
        self.client = app.test_client()
        '''show flask errors during testing'''
        app.config['TESTING'] = True


    def test_index(self):
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'album', result.data)

    def test_new(self):
        """Test the new album creation page."""
        result = self.client.get('/album/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Album', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_album(self, mock_find):
        """Test showing a single album."""
        mock_find.return_value = sample_album

        result = self.client.get(f'/albums/{sample_album_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Led Zeppelin III', result.data)


    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_album(self, mock_find):
        """Test editing a single album."""
        mock_find.return_value = sample_album

        result = self.client.get(f'/albums/{sample_album_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Led Zeppelin III', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_album(self, mock_insert):
        """Test submitting a new album."""
        result = self.client.post('/albums', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_album)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_album(self, mock_update):
        result = self.client.post(f'/albums/{sample_album_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_album_id}, {'$set': sample_album})
if __name__ == '__main__':
    unittest_main()