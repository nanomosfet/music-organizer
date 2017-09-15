import unittest
import os
import tempfile
import shutil
import random

import music_organizer

music_names = [
            'Beatles - P.S I Love you.mp3', 
            'Led Zeppelin - Kashmir.mp4',
            'Led Zeppelin - Who cares.mp4',
            'Beatles - Who cares.mp4',
            'Yes - We care.mp4',
            'Koolaid Man - Makes Music Now.mp3',
            'Koolaid Man - Makes Music Now.mp3',
            'Koolaid Man - Makes Music Now.mp3',
            'Koolaid Girl - Makes Music d Now.mp3',
            'Koolaid Fish - Makes Music d Now.mp3',
            'Koolaid Dude - Makes Music Now.mp3',
            'Hell Man - Makes Music Now.mp3',
            'Heaven Man - Makes Music Now.mp3',]

random_categories = [
    'Jazz',
    'WhatEver',
    'Who Cares',
    'Jesus Music']

class TestMusicOrganiztion(unittest.TestCase):
    def setUp(self):

        
        # Create temp test folder
        if os.path.exists('test'):
            shutil.rmtree('test')
        os.mkdir('test')
        os.chdir('test')
        for category in random_categories:
            os.makedirs('unorganized_files/%s' % category)
        
        for name in music_names:
            open('unorganized_files/%s/%s' % (random_categories[random.randint(0,3)], name), 'w')

    def tearDown(self):
        pass




    def test_organization(self):
        print "after Organization list dir:"

        music_organizer.organize_files_by_artist('unorganized_files', 'organized_files')
        print os.listdir('organized_files')    
        self.assertTrue('Beatles' in os.listdir('organized_files'))
        self.assertTrue('Led Zeppelin' in os.listdir('organized_files'))
        self.assertTrue('Yes' in os.listdir('organized_files'))

if __name__ == '__main__':
    unittest.main()