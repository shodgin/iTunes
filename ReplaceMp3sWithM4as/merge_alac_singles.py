import os
import re
import shutil

def m4aFilesInDir(dir_name):
	outputList = []
	for root, dirs, files in os.walk(dir_name):
		for filename in files:
			if os.path.splitext(filename)[1] == '.m4a':
				outputList.append('/'.join([root, filename]))
	return outputList

def guessMp3FileName(m4aFileName, alacdir, librarydir):
	mp3FileName = librarydir + m4aFileName.split(alacdir)[1]
	mp3FileName = re.sub(r'(.*).m4a$', r'\1.mp3', mp3FileName)
	mp3FileName = re.sub(r'(.*/)([^/-]+- )(.*)', r'\1\3', mp3FileName)
	return mp3FileName

def getNewM4aFileName(mp3FileName):
	return re.sub(r'(.*).mp3$', r'\1.m4a', mp3FileName)

def getItuensFileName(mp3FileName):
	return mp3FileName.replace(' ', '%20').replace('[', '%5B').replace(']', '%5D')


if __name__ == "__main__":

	alacdir = r'/Users/Scott/Desktop/alac/Singles'
	librarydir = r'/Volumes/Time Machine/iTunes/Music/Compilations/Singles'
	hitlist = []
	misslist = []

	m4aFiles = m4aFilesInDir(alacdir)
	for filename in m4aFiles:
		mp3FileName = guessMp3FileName(filename, alacdir, librarydir)
		if os.path.exists(mp3FileName):
			newM4aFileName = getNewM4aFileName(mp3FileName)
            #rename the mp3 filename to the m4a file name so that iTunes will automatiacally
            #link the sond in the database to the new song name
			shutil.move(mp3FileName, newM4aFileName)
			shutil.move(filename, newM4aFileName)
			hitlist.append(mp3FileName)
			print newM4aFileName
		else:
			misslist.append(mp3FileName)

	f1 = open('/Users/Scott/Desktop/mp3Found.txt', 'w')
	for line in hitlist:
		f1.write(line+'\n')
	f1.close()

	f2 = open('/Users/Scott/Desktop/mp3NotFound.txt', 'w')
	for line in misslist:
		f2.write(line+'\n')
	f2.close()

