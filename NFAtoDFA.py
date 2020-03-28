# Nicholas Wackowski
# DFA / NFA project
# NOTE: For this project, we are substituting "$" as our epsilon character,
#       due to errors in recognizing the proper epsilon character.

import pandas
import copy

class NFA:
    # Requires a name (ex. NFA1), and a list of nodes (defined later).
    # Example: name: NFA_Test_1
    #          nodesList: [q1, q2, q3, q4]
    def __init__(self, name, nodesList):
        self.name = name
        self.nodesList = nodesList
        
    # Pretty-print function
    def prettyPrint(self):
        print("Name:", self.name)
        for n in self.nodesList:
            n.prettyPrint()
    
    # Transition function; goes from node-to-node, recursively searching
    # for the boolean value at the last node in the NFA.
    def transition(self, alphabet, currentNode, isFirst=True, pathString="", resultsList=[]):
        # Do some prints, so the output is legible
        if(isFirst == True):
            isFirst = False
            pathString = str(currentNode.getName())
        else:
            pathString += ("-->" + str(currentNode.getName()))
            
        
        # Iterate through all the transitions on this node.
        # If there are any epsilons, take that transition, and return the
        # end result of following the remaining alphabet after
        # taking that epsilon transition.
        for trans in currentNode.getTransitionFunction():
            if(trans.getInput() == "$"):
                self.transition(alphabet, self.getNodeByName(trans.getEnd()), isFirst, pathString, resultsList)
            
        # When we reach the last element, append the final node
        # to the resultsList, so it can be saved for possible divergences.
        if(len(alphabet) == 0):
            resultsList.append(currentNode.getName())
            return resultsList
        
        # If there are more characters in the alphabet...
        else:
            for trans in currentNode.getTransitionFunction():
                if(alphabet[0] == trans.getInput()):
                    return self.transition(alphabet[1:], self.getNodeByName(trans.getEnd()), isFirst, pathString, resultsList)
        # If code reaches this line, it means it reached a trap state,
        # as that input was not valid for that state. All inputs from this point forward
        # just loop back on itself.
        # Rather than simulate going through every iteration just to return None, it simply returns nothing.
        return
        
    # Takes in a string input, the name of the node which is skipped to
    def getNodeByName(self, name):
        for x in self.nodesList:
            if(x.getName() == name):
                return x
        # If it reaches this line, there is an error: no such node name exists
        printErrorNameMessage(name)
        return None
    
    def converter(self, allAlphas, initialState):
        originalTable = self.setupOriginalTable(allAlphas)
        
        # The first row will be the results of the starting node, work from there.
        newValuesExist = True
        outerList = []
        if(not isinstance(initialState, str) and not isinstance(initialState, list)):
            initialState = initialState.getName()
        newValues = [initialState]
        while(newValuesExist == True):
            print("Pass... newValues:", newValues)
            for val in newValues:
                print("val:", val)
                innerList = [val]
                for alpha in allAlphas:
                    if alpha != "$":
                        res = self.getEpsilonResult(originalTable, alpha, val)
                        innerList.append(res)
                        
                outerList.append(innerList)
            newValues = self.getNewValues(outerList)
            print("newValues:", newValues)
            if(isinstance(newValues, list) and len(newValues) > 0):
                newValuesExist = True
            else:
                newValuesExist = False
        colnames = self.getColNames(allAlphas)
        epsilonDF = pandas.DataFrame(outerList, columns=colnames)
        return epsilonDF
        
    
    def getEpsilonResult(self, originalTable, alpha, state):
        resultsList = []
        if(isinstance(state, list)):
            for s in state:
                if s is not None:
                    tempResult = originalTable.loc[s, alpha]
                    if(tempResult is not None):
                        tempEpsilonResult = originalTable.loc[tempResult, '$']
                        if(isinstance(tempEpsilonResult, list)):
                            tempEpsilonResult.sort()
                            toAppend = tempEpsilonResult
                            resultsList.append(toAppend)
                        else:
                            toAppend = tempEpsilonResult
                            resultsList.append(toAppend)
                
        else:
            tempResult = originalTable.loc[state, alpha]
            if(tempResult is not None):
                tempEpsilonResult = originalTable.loc[tempResult, '$']
                if(isinstance(tempEpsilonResult, list)):
                    tempEpsilonResult.sort()
                    toAppend = tempEpsilonResult
                else:
                    toAppend = tempEpsilonResult
            else:
                toAppend = tempResult
            resultsList.append(toAppend)
        resultsList = self.flatten(resultsList)
        return resultsList
    
    def flatten(self, inputList):
        needsAnotherPass = True
        while(needsAnotherPass == True):
            newList = []
            needsAnotherPass = False
            for x in inputList:
                if isinstance(x, list):
                    for y in x:
                        needsAnotherPass = True
                        newList.append(y)
                else:
                    newList.append(x)
            inputList = newList
        return newList
    
    def getNewValues(self, currentTable):
        allElements = []
        for x in currentTable:
            for y in x:
                if y not in allElements:
                    allElements.append(y)
        states = []
        for x in currentTable:
            if x not in states:
                states.append(x[0])
        
        tempElements = copy.deepcopy(allElements)
        for el in tempElements:
            if el in states:
                allElements.remove(el)
                
        if None in allElements:
            allElements.remove(None)
        if [None] in allElements:
            allElements.remove([None])
        if [] in allElements:
            allElements.remove([])
        return allElements
                    
    def getColNames(self, alphas):
        colNames = ["State"]
        for char in alphas:
            if char != '$':
                colNames.append(char+'$')
        return colNames
            
                
    def getResults(self, originalTable, state, alpha):
        results = []
        cell = originalTable.loc[state.getName(), alpha]
        results.append(cell)
    
        if(cell is not None):
            cell = originalTable.loc[cell, '$']
            results.append(cell)
        
        tempResults = []
        for element in results:
            if(isinstance(element, list)):
                for x in element:
                    tempResults.append(x)
            else:
                tempResults.append(element)
        results = tempResults
        results = list(set(results))
        return results
    
    def setupOriginalTable(self, allAlphas):
        outerList = []
        for node in self.nodesList:
            innerList = [node.getName()]
            for alpha in allAlphas:
                appended = False
                for trans in node.getTransitionFunction():
                    if(alpha == '$' and alpha == trans.getInput()):
                        innerList.append([node.getName(), trans.getEnd()])
                        appended = True
                        break
                    elif(alpha == trans.getInput()):
                        innerList.append(trans.getEnd())
                        appended = True
                        break
                if(appended == False and alpha == '$'):
                    innerList.append(node.getName())
                    appended = True
                    break
                elif(appended == False):
                    innerList.append(None)
            outerList.append(innerList)
            
        colNames = ["State"] + allAlphas
        df = pandas.DataFrame(outerList, columns=colNames)
        df = df.set_index('State')
        print(df)
        return df
    
    def printErrorNameMessage(self, errorNodeName):
        print("ERROR! Invalid transition detected at " + errorNode.getName() + "!")
        print("No such node exists: " + errorNodeName)
    
    def printErrorCharacterMessage(self, errorNode, errorCharacter):
        print("ERROR! Invalid transition detected at " + errorNode.getName() + "!")
        print("Invalid character: " + errorCharacter)
        
class node:
    # Requires a name (q1, q2, etc), whether or not that node returns true,
    # and the transitionFunction, which is a list of transition equations (defined below).
    # Example: name: q1
    #          isBool: False
    #          transitionFunction: [transitionEquation('a', 'Q2'), transitionEquation('b', 'Q3')]
    def __init__(self, name, isBool, transitionFunction):
        self.name = name
        self.isBool = isBool
        self.transitionFunction = transitionFunction
    def prettyPrint(self):
        print("Node:", name)
        for t in self.transitionFunction:
            t.prettyPrint()
    def getTransitionFunction(self):
        return self.transitionFunction
    def getIsBool(self):
        return self.isBool
    def getName(self):
        return self.name

class transitionEquation:
    # Requires the input and the name of the function which is transitioned to.
    # Example: input: 'a'
    #          end:   'Q2'
    def __init__(self, input_, end):
        self.input_ = input_
        self.end = end
    def prettyPrint(self):
        print("'"+str(self.input)+"' --> "+"'"+str(self.end)+"'")
    def getInput(self):
        return self.input_
    def getEnd(self):
        return self.end

def removeNones(dirtyList):
    newList = []
    for x in dirtyList:
        if x is not None and x != [None]:
            newList.append(x)
    return newList

def ensureList(state):
    if(isinstance(state, str)):
        return [state]
    else:
        return state

def ensureString(inputList):
    newList = []
    for element in inputList:
        if(isinstance(element, list) and len(element) == 0):
            newList.append(None)
        elif(isinstance(element, list) and len(element) > 1):
            newList.append(element)
        elif(isinstance(element, list) and isinstance(element[0], list)):
            newList.append(element[0])
        elif(isinstance(element, list) and isinstance(element[0], str)):
            if(len(element) == 0):
                newList.append(None)
            else:
                newList.append(element[0])
        else:
            newList.append(element)
    return newList

def ensureListFromTable(table):
    trackerList = []
    for row in table.iterrows():
        for cell in row:
            if(isinstance(cell, list)):
                table.loc[row, cell] = cell[0]
    return trackerList
    
def getNewValues(table):
    print(table)
    trackerList = []
    array = table.to_numpy()
    for x in array:
        for y in x:
            if y is not None:
                if(isinstance(y, list)):
                    y.sort()
                    if(list(set(y)) not in trackerList):
                        trackerList.append(list(set(y)))
                    
                elif y not in trackerList:
                    trackerList.append(y)
    columnList = table.States
    for x in columnList:
        if(isinstance(x, list)):
            if( sorted(x) in trackerList):
                trackerList.remove( sorted(x))
            elif( sorted(x, reverse=True) in trackerList):
                trackerList.remove( sorted(x, reverse=True))
        else:
            if x in trackerList:
                trackerList.remove(x)
    return trackerList
    