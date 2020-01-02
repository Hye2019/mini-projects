'''
Plagiarism Detector
Author: Heidi Ye
Last Modified: April 14 2019
'''

import glob
import os
from itertools import combinations

numOfFilePairs = len(list(combinations(glob.glob('*txt'),2))) #number of unique file pairs in directory
PLAGIARISM_THERSHOLD = 0.55 #above 55% considered to be plagiarism
SHINGLE_LOW_RANGE = 2
SHINGLE_HIGH_RANGE = 5

def shingleLine(line,w):
    '''returns a w-width shingle set for a single line of lowercase text'''
    line = line.lower()
    shingle = []
    start = 0
    end = w
    word = tuple(line.split())
    for window in range(len(word)-w + 1):
        shingle.append(word[start:end])
        start = start + 1
        end = end + 1
    return set(shingle)

assert len(shingleLine("here is a test to run",3)) == 4
assert len(shingleLine("test this please",3)) == 1
assert len(shingleLine("test this one please",2)) == 3
    
def shingleFile(file,w):
    '''returns a w-width shingle set for an entire file'''
    with open(file,'r') as file:
        shingledSet = set()
        for line in file:
            shingled = shingleLine(line,w)
            shingledSet = shingledSet | shingled
        return shingledSet

def similarityIndex(set1,set2):
    '''computes Jacquard's Similarity Index between two sets of data'''
    similarity = (len(set1 & set2))/(len(set1 | set2))
    return similarity

assert (similarityIndex({1,2,3},{1,2,3})) == 1
assert (similarityIndex({1,2,3},{4,5,6})) == 0
assert (similarityIndex({1,2,4},{4,5,2})) == 0.5

def computeFileSimilarity(file1,file2,w):
    ''' returns Jacquard's Similary Index between two files'''
    filename1 = file1
    filename2 = file2
    setFile1 = shingleFile(filename1,w)
    setFile2 = shingleFile(filename2,w)
    similarity = similarityIndex(setFile1,setFile2)
    return similarity

assert computeFileSimilarity('rents1.txt','rents1copy.txt',3) == 1

def similarityStats(file1,file2):
    '''returns a list containing min, max and avg similarity of two files given set shingle range, rounded to 3 decimals'''
    similarity = []
    counter = 0
    for w in range(SHINGLE_LOW_RANGE,SHINGLE_HIGH_RANGE):
        rangeValue = computeFileSimilarity(file1,file2,w)
        similarity.append(rangeValue)
        counter = counter + 1
    return round(min(similarity),3), round(max(similarity),3), round(sum(similarity)/counter,3)

assert similarityStats('rents1.txt','rents1copy.txt') == (1.0,1.0,1.0)

def plagiarismStatus(file1,file2):
    ''' returns "Plagiarized" if the avg similarity between two files is greater than 0.5, otherwise returns "Not Plagiarized"'''
    result = []
    if similarityStats(file1,file2)[2] > PLAGIARISM_THERSHOLD:
        result.append("Plagiarized")
    else:
        result.append("Not Plagiarized")
    return tuple(result)

assert plagiarismStatus('rents1.txt','rents1copy.txt') == ("Plagiarized",)
assert plagiarismStatus('rents1.txt','blues.txt') == ("Not Plagiarized",)

def plagiarismStatusFiles():
    '''returns a list containing file names, similiarity stats and plagiarism status for each two file combo being analyzed in the current directory'''
    inputFiles = tuple(combinations(glob.glob('*txt'),2))
    combo = 0
    fileByStatus = []
    for combo in range(len(inputFiles)):
        fileByStatus.append(inputFiles[combo] + similarityStats(inputFiles[combo][0],inputFiles[combo][1]) + plagiarismStatus(inputFiles[combo][0],inputFiles[combo][1]))
        combo = combo + 1
    return fileByStatus

def numOfPlagiarizedFiles():
    '''returns the number of plagiarized files in the current directory'''
    fileData = plagiarismStatusFiles()
    count = 0
    for pair in range(numOfFilePairs):
        if fileData[pair][5] == "Plagiarized":
            count = count + 1
    return count

def currentDirectory():
    '''returns current directory'''
    return os.getcwd()

def drawReport():
    '''returns plagiarism report in a table format with the inputs calculated from plagiarismStatusFiles()'''
    import texttable as tt
    tab = tt.Texttable()
    tableItems = [[]]
    for row in range(numOfFilePairs):
        tableItems.append(plagiarismStatusFiles()[row])
    tab.add_rows(tableItems)
    tab.set_cols_align(['c']*(numOfFilePairs))
    tab.header(['File 1','File 2','Min.','Max.','Avg. Similarity','Status'])
    print(tab.draw())

def main():
    '''scans all files in the current directory and returns a report outlining which files are likely plagiarized'''
    print("Plagiarism Detection App:" "\n")
    print("Analyzing all .txt files in", currentDirectory())
    drawReport()
    print("You have",numOfPlagiarizedFiles(),"plagiarized file(s)!")
    
main()
