import re
from copy import deepcopy
import numpy as np

def stringNormalize(string):
    return string

def betterScaleToNumeric(vote, rowName, colName, betterVal=2.0, muchBetterVal=5.0):
    dom = None
    numericVote = None
    muchBetterRegexes = [
        r'^(.+)\s+is\s+much\s+better$',
        r'^(.+)\s+is\s+much\s+more',
        r'^(.+)\s+is\s+much\s+preferred'
    ]
    betterRegexes = [
        r'^(.+)\s+is\s+better$',
        r'^(.+)\s+is\s+more',
        r'^(.+)\s+is\s+preferred$'
    ]
    rowName = stringNormalize(rowName)
    colName = stringNormalize(colName)
    if firstParenRegex(muchBetterRegexes, vote) is not None:
        dom = stringNormalize(firstParenRegex(muchBetterRegexes, vote))
        #console.log("Much better: '"+dom+"' hope this makes sense")
        numericVote = muchBetterVal
    elif firstParenRegex(betterRegexes, vote) is not None:
        dom = stringNormalize(firstParenRegex(betterRegexes, vote))
        #console.log("Better: '"+dom+"' hope this makes sense")
        numericVote = betterVal
    elif vote.endswith("equal"):
        #Have an equality vote
        #Doesn't matter which we say is dominant, call it rowName
        dom = rowName
        numericVote = 1
    else:
         raise "Vote '"+vote+"' was neither better, nor much better, nor equals, we give up"
    if dom == rowName:
        #The dominant node was the row node, so return the vote value
        return numericVote
    elif dom == colName:
        #The dominant was the column, so we return the reciprocal of the vote
        return 1.0/numericVote
    else:
        raise Exception("The dominant node from the vote was '"+dom+"' which was neither the row nor the column")

def firstParenRegex(regexes, string):
    for regex in regexes:
        m=re.search(regex, string)
        if m is not None:
            return m.group(1)
    return None

def islist(val):
    return (not (isinstance(val,str))) and (hasattr(val, "__len__"))

def betterScaleDataToNumeric(colHeader, vote, betterVal=2.0, muchBetterVal=5.0,
                         extraColHeaderRegexes=[]):
    if islist(vote):
        # We need to do this for a bunch of items
        rval = deepcopy(vote)
        for i in range(len(vote)):
            rval[i]=betterScaleDataToNumeric(colHeader, vote[i], betterVal, muchBetterVal, extraColHeaderRegexes)
        return rval
    #print("Help me "+str(vote))
    if (vote is None) or np.isreal(vote) or (vote is ""):
        return vote
    regexes = [
        r'^(.+)\s+vs\s+(.+)\s+wrt\s+.+$',
        r'^(.+)\s+vs\s+(.+)$'
    ]
    regexes.extend(extraColHeaderRegexes)
    colHeader = stringNormalize(colHeader)
    vote = stringNormalize(vote)
    rowNode = None
    colNode = None
    #First we need to split the colHeader on the word, we try each regex
    for regex in regexes:
        matches = re.search(regex, colHeader)
        #console.log(matches)
        if matches!=None:
            rowNode = matches[1]
            colNode = matches[2]
            break
    if (rowNode is None) or (colNode is None):
        return
    numericVote = betterScaleToNumeric(vote, rowNode, colNode, betterVal, muchBetterVal)
    #print("'"+rowNode+"' vs '"+colNode+"'"+" vote = "+str(numericVote))
    return numericVote
