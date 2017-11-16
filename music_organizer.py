import os
import datetime
import argparse
import shutil
import re

def write_log(s):    
    with open('logfile.out', 'a+') as f:
        f.write('time: %s Action: %s \n' % (str(datetime.datetime.now()), s))

def write_report(path ,s):    
    with open('%s/report.out' % path, 'a+') as f:
        f.write('%s\n' % s)


def organize_files_by_artist(src, dst):
    if not os.path.exists(src):
        print 'File does not exist'
    else:
        for root, dirnames, filenames in os.walk(src):
            for file in filenames:
                band_name = file.split(' - ')[0]
                print os.path.join(root, file)
                print os.path.join(dst, band_name, file)
                try:
                    write_log('Trying to organize %s' % os.path.join(root, file))
                    os.renames(os.path.join(root, file), os.path.join(dst, band_name, file))
                    write_log('Successfully moved %s to %s' % (os.path.join(root, file), os.path.join(dst, band_name, file)))
                except Exception as error:
                    write_log('Error occured moving  %s to %s' % (os.path.join(root, file), os.path.join(dst, band_name, file)))
                    write_log('Error is %s' % error)

def clean_string(s):
    res = ''.join([i if ord(i) < 128 else '' for i in s])
    res.replace('.mp3', '.mp3').replace('\'', '').replace('"', '')
    return res

def create_list_from_csv(list_csv):
    res = []
    with open(list_csv) as f:
        for line in f:
            if line == ',':
                pass
            else:
                new_line = clean_string(line).lower().replace('\n', '').replace('the ', '').replace(',', '').replace('\'', '').replace('"', '')
                new_line = re.sub(r'\([^)]*\)', '', new_line).replace(' .', '.').split('\t')
                res.append(new_line)
                
    return res

def create_playlist_from_bank(playlist_csv, src, dst):
    try:        
        playlist = create_list_from_csv(playlist_csv)
    except:
        print 'Error Reading csv'
        write_log('Error Reading_csv')

    try:
        os.mkdir(dst)
    except OSError:
        print "Output File already Exists, Will Continue to put files in this directory "
        write_log("Output File already Exists , Will Delete folder and Continue to put files in this directory")

    if not os.path.exists(src):
        print 'File does not exist'
        write_log('Source File does not exist')
    else:
        for root, dirnames, filenames in os.walk(src):
            for file in filenames:
                if ' - ' in file:
                    file_cleaned = clean_string(file).lower().replace('\n', '').replace('the ', '').replace(',', '').replace('\'', '').replace('"', '')
                    file_cleaned = re.sub(r'\([^)]*\)', '', file_cleaned).replace(' .', '.').split(' - ')
                    for song in playlist:
                        try:
                            if song[0] in file_cleaned[0] and song[1] in file_cleaned[1]:
                                shutil.copy(os.path.join(root, file), os.path.join(dst, file))
                                playlist.remove(song)
                        except IndexError:
                            print file
    print "the following files have not been found in your song bank:"
    write_report(dst, "the following files have not been found in your song bank:")
    for item in playlist:
        print '%s - %s' % (item[0], item[1])
        write_report(dst, '%s - %s' % (item[0], item[1]))
    write_report(dst, "There are %s not found in your music bank" % len(playlist))
    return playlist



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Organize Music files in a folder to a destination folder')
    parser.add_argument('cmd', type=str, nargs=1)
    parser.add_argument('source', type=str, nargs=1)
    parser.add_argument('-f', '--file', type=str, nargs=1)
    parser.add_argument('destination', type=str, nargs=1)
    args = parser.parse_args()
    if args.cmd[0] == 'organize':
        organize_files_by_artist(args.source[0], args.destination[0])
    elif args.cmd[0] == 'make_playlist':
        create_playlist_from_bank(args.file[0], args.source[0], args.destination[0])


