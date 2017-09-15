import os
import datetime
import argparse

def write_log(s):    
    with open('logfile.out', 'a+') as f:
        f.write('time: %s Action: %s \n' % (str(datetime.datetime.now()), s))


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




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Organize Music files in a folder to a destination folder')
    parser.add_argument('source', type=str, nargs=1)
    parser.add_argument('destination', type=str, nargs=1)
    args = parser.parse_args()
    organize_files_by_artist(args.source[0], args.destination[0])

