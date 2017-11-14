import unittest
import os
import tempfile
import shutil
import random

import music_organizer

music_names = [
            'Beatles - P.S I Love you.mp3', 
            'Led Zeppelin - Kashmir.mp3',
            'Led Zeppelin - Who cares.mp3',
            'Beatles - Who cares.mp3',
            'Yes - We care.mp3',
            'Koolaid Man - Makes Music Now.mp3',
            'Koolaid Man - Makes Music Now.mp3',
            'Koolaid Man - Makes Music Now.mp3',
            'Koolaid Girl - Makes Music d Now.mp3',
            'Koolaid Fish - Makes Music d Now.mp3',
            'Koolaid Dude - Makes Music Now.mp3',
            'Hell Man - Makes Music Now.mp3',
            'Heaven Man - Makes Music Now.mp3',]


play_list_bank = [
            'So Strange - The Jesters.mp3', 
            'Mama Guitar - Julius LaRosa.mp3',
            'Say It Isnt So - Teddi King.mp3',
            'Next In Line - Johnny Cash.mp3']

random_categories = [
    'Jazz',
    'WhatEver',
    'Who Cares',
    'Jesus Music']


def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def check_list_for_non_ascii(string_list):
    for string in string_list:
        if not is_ascii(string):
            print string
            return False
    return True


class TestMusicOrganiztion(unittest.TestCase):
    def setUp(self):
        if os.path.exists('test'):
            shutil.rmtree('test', ignore_errors=True)
        os.mkdir('test')
        shutil.copy('test-list.txt', 'test')
        os.chdir('test')

    def tearDown(self):
        os.chdir('../')
        shutil.rmtree('test', ignore_errors=True)




    def test_organization(self):
        print "after Organization list dir:"
        # Create temp test folder
        for category in random_categories:
            os.makedirs('unorganized_files/%s' % category)
        
        for name in music_names:
            open('unorganized_files/%s/%s' % (random_categories[random.randint(0,3)], name), 'w')
        music_organizer.organize_files_by_artist('unorganized_files', 'organized_files')    
        self.assertTrue('Beatles' in os.listdir('organized_files'))
        self.assertTrue('Led Zeppelin' in os.listdir('organized_files'))
        self.assertTrue('Yes' in os.listdir('organized_files'))

    # def test_playlist_creator(self):
    #     if os.path.exists('test_playlist_creator'):
    #         shutil.rmtree('test_playlist_creator')
    #     os.mkdir('test_playlist_creator')
    #     os.chdir('test_playlist_creator')

    def test_list_from_csv(self):
        csv_file_name = 'test-list.txt'
        playlist_files = music_organizer.create_list_from_csv(csv_file_name)
        self.assertTrue('Mama Guitar - Julius LaRosa.mp3' in playlist_files)
        self.assertTrue('Say It Isnt So - Teddi King.mp3' in playlist_files)
        self.assertTrue('Next In Line - Johnny Cash.mp3' in playlist_files)
        self.assertTrue('So Strange - The Jesters.mp3' in playlist_files)
        self.assertFalse(' - .mp3' in playlist_files)
        self.assertFalse('' in playlist_files)
        self.assertFalse(' ' in playlist_files)
        self.assertFalse(' .mp3' in playlist_files)


    def test_add_files_to_playlist_folder(self):
        os.mkdir('play-list-bank')

        for name in play_list_bank:
            open('play-list-bank/%s' % name, 'w')

        csv_file_name = 'test-list.txt'
        src = 'play-list-bank'
        dst = 'dest-play-list'
        missing_music_list = music_organizer.create_playlist_from_bank(csv_file_name, src, dst)
        self.assertTrue('So Stranger - The Jesterers.mp3' in missing_music_list)
        self.assertTrue('In Line - Johnny Cash.mp3' in missing_music_list)
        self.assertTrue('Mama Guitar - Julius LaRosa.mp3' in os.listdir(dst))
        self.assertTrue('Say It Isnt So - Teddi King.mp3' in os.listdir(dst))
        self.assertTrue('Next In Line - Johnny Cash.mp3' in os.listdir(dst))
        self.assertTrue('So Strange - The Jesters.mp3' in os.listdir(dst))





if __name__ == '__main__':
    unittest.main()