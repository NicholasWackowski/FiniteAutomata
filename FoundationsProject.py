# Nicholas Wackowski
# DFA / NFA project

import pandas
import copy

class DFA:
    # Requires a name (ex. DFA1), and a list of nodes (defined later).
    # Example: name: DFA_Test_1
    #          nodesList: [q1, q2, q3, q4]
    def __init__(self, name, nodesList):
        self.name = name
        self.nodesList = nodesList
        
    # Pretty-print function
    def prettyPrint(self):
        print("DFA: Name:", self.name)
        for n in self.nodesList:
            n.prettyPrint()
    
    # Transition function; goes from node-to-node, recursively searching
    # for the boolean value at the last node in the DFA.
    def transition(self, alphabet, currentNode, isFirst=True, pathString=""):            
        currentNode = self.getNodeByName(currentNode.getName())
            
        # Do some prints, so the output is legible
        if(isFirst == True):
            isFirst = False
            pathString = str(currentNode.getName())
        else:
            pathString += ("-->" + str(currentNode.getName()))
            
        # When we reach the last element, 
        if(len(alphabet) == 0):
            if(currentNode.getIsBool()):
                return "Yes"
            else:
                return "No"
        else:
            for trans in currentNode.getTransitionFunction():
                if(alphabet[0] == trans.getInput()):
                    print("Transitioning from", currentNode.getName(), "to", trans.getEnd(), "using", alphabet[0])
                    return self.transition(alphabet[1:], self.getNodeByName(trans.getEnd()), isFirst, pathString)
            # If code reaches this line, it means it reached an ERROR STATE,
            # as that input was not valid for that state.
            self.printErrorCharacterMessage(currentNode, alphabet[0])
            return "No"
        
    # Takes in a string input, the name of the node which is skipped to
    def getNodeByName(self, name):
        for x in self.nodesList:
            if(x.getName() == name):
                return x
        # If it reaches this line, there is an error: no such node name exists
        print(name)
        #printErrorNameMessage(name)
        return None
    
    def printErrorCharacterMessage(self, errorNode, errorCharacter):
        print("ERROR! Invalid transition detected at " + errorNode.getName() + "!")
        print("Invalid character: " + errorCharacter)
        
    def validate(self):
        isValid = True
        if(self.checkEmptyStates() == False):
            isValid = False
        if(self.checkMultiArrows() == False):
            isValid = False
        return isValid
    
    def checkEmptyStates(self):
        nodesList = self.nodesList
        if len(nodesList) == 0:
            print("VALIDATION ERROR: No states found in DFA " + self.name)
            return False
        else:
            return True
    
    def checkMultiArrows(self):
        nodesList = self.nodesList
        for n in nodesList:
            inputList = []
            for trans in n.getTransitionFunction():
                if trans.getInput() in inputList:
                    print("VALIDATION ERROR: multiple transitions in state " + n.getName() + " with input " + trans.getInput())
                    return False
                inputList.append(trans.getInput())
        return True
    
def printErrorNameMessage(errorNodeName):
    print("ERROR! Invalid transition detected at " + errorNodeName + "!")
    print("No such node exists: " + errorNodeName)
        
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
        print("Node:", self.name)
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
        print("'"+str(self.input_)+"' --> "+"'"+str(self.end)+"'")
    def getInput(self):
        return self.input_
    def getEnd(self):
        return self.end

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
    
    def transitionWrapper(self, alphabet, currentNode, isFirst=True, pathString="", resultsList=[]):
        results = self.transition(alphabet, currentNode, isFirst, pathString, resultsList)
        if(results is None or len(results) <= 0):
            return "No"
        else:
            return "Yes"
        
    # Transition function; goes from node-to-node, recursively searching
    # for the boolean value at the last node in the NFA.
    def transition(self, alphabet, currentNode, isFirst=True, pathString="", resultsList=[]):
        print("At: ", currentNode.getName(), "Input: ", alphabet)
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
        self.printErrorNameMessage(name)
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
#            print("Pass... newValues:", newValues)
            for val in newValues:
#                print("val:", val)
                innerList = [val]
                for alpha in allAlphas:
                    if alpha != "$":
                        res = self.getEpsilonResult(originalTable, alpha, val)
                        innerList.append(res)
                        
                outerList.append(innerList)
            newValues = self.getNewValues(outerList)
#            print("newValues:", newValues)
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
#        print(df)
        return df
    
    def printErrorNameMessage(self, errorNodeName):
        print("ERROR! Invalid transition detected at " + errorNode.getName() + "!")
        print("No such node exists: " + errorNodeName)
    
    def printErrorCharacterMessage(self, errorNode, errorCharacter):
        print("ERROR! Invalid transition detected at " + errorNode.getName() + "!")
        print("Invalid character: " + errorCharacter)

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

def DFAwrapper(nodesTable, allAlphas, successInputs):
    # For each row in the table, construct a node. Each non-empty column in that row is a transition
    outerList = []
    for count, row in nodesTable.iterrows():
        innerList = []
        transitionList = []
        innerCount = 0
        for col in row:
            if innerCount == 0:
                innerList.append(ensureNodeName(col))
                innerList.append(containsSuccess(col, successInputs))
            elif col is not None and col != [None] and col != []:
                transitionList.append(transitionEquation(ensureNodeName(allAlphas[innerCount-1]), ensureNodeName(col)))
            innerCount += 1
        innerList.append(transitionList)
        outerList.append(innerList)
    
    nodeList = []
    #print(pandas.DataFrame(outerList))
    for element in outerList:
        nodeList.append(node(*element))
    return DFA(name="temp", nodesList=nodeList)

def converttostr(input_seq, seperator):
    # Join all the strings in list
    final_str = seperator.join(input_seq)
    return final_str

def ensureNodeName(node):
    if(isinstance(node, list)):
        return converttostr(node, "")
    else:
        return node

def nodesToNames(nodesList):
    if(isinstance(nodesList, list)):
        newList = []
        for x in nodesList:
            newList.append(x.getName())
        return newList
    else:
        return newList.getName()
    
def containsSuccess(state, successfulInputsList):
    successfulInputsList = nodesToNames(successfulInputsList)
    if isinstance(state, list): # If it's a list of states,
        for x in state:         # check each state and if there
            if x in successfulInputsList: # is a state in the input list
                return True     # which matches, return true. Otherwise, it's a fail state.
        return False
    else: # If it's just a single string/state, check if it is true or false
        if state in successfulInputsList:
            return True
        else:
            return False
        

# =============================================== TESTS =================================================

def testValidationEmptyStates():
    nodeList = []
    initialState = None
    testDFA = DFA("EmptyDFA", nodeList)
    print(testDFA.validate())
    
def testMultiArrows():
    q1 = node("q1", True, [transitionEquation('b', 'q2'), transitionEquation('b', 'q1')])
    q2 = node("q2", False, [transitionEquation('a', 'q2'), transitionEquation('c', 'q1')])
    nodeList = [q1, q2]
    initialState = q1
    testDFA = DFA(name='multiArrowDFA', nodesList=nodeList)
    print(testDFA.validate())

    
# A sample DFA diagram, where receiving "a" causes a transition
# between Q1 <--> Q2 and "b" causes the node to remain the same.
def DFAtest1():
    Q1 = node("Q1", True, [transitionEquation('a', 'Q2'), transitionEquation('b', 'Q1')])
    Q2 = node("Q2", False, [transitionEquation('a', 'Q1'), transitionEquation('b', 'Q2')])
    testNodeList = [Q1, Q2]
    # DFA: def __init__(self, name, nodesList):
    testDFA = DFA(name='testDFA', nodesList=testNodeList)
    alphabet = 'aba'
    print(alphabet)
    print(testDFA.transition(alphabet=alphabet, currentNode=Q1))
    print('---')
    
    alphabet = 'abbba'
    print(alphabet)
    print(testDFA.transition(alphabet=alphabet, currentNode=Q1))
    print('---')
    
    alphabet = 'aaaab'
    print(alphabet)
    print(testDFA.transition(alphabet=alphabet, currentNode=Q1))

# A diagram where all a's lead to Q1, all b's lead to Q2, and all c's lead to Q3.
# Q3 is the only node which succeeds.
def DFAtest2():
    Q1 = node("Q1", False, [transitionEquation('a', 'Q1'), transitionEquation('b', 'Q2'), transitionEquation('c', 'Q3')])
    Q2 = node("Q2", False, [transitionEquation('a', 'Q1'), transitionEquation('b', 'Q2'), transitionEquation('c', 'Q3')])
    Q3 = node("Q3", True,  [transitionEquation('a', 'Q1'), transitionEquation('b', 'Q2'), transitionEquation('c', 'Q3')])
    testNodeList = [Q1, Q2, Q3]
    # DFA: def __init__(self, name, nodesList):
    testDFA = DFA(name='testDFA', nodesList=testNodeList)
    alphabet = 'abca'
    print(alphabet)
    print(testDFA.transition(alphabet=alphabet, currentNode=Q1))
    print('---')
    
    alphabet = 'accbab'
    print(alphabet)
    print(testDFA.transition(alphabet=alphabet, currentNode=Q1))
    print('---')
    
    alphabet = 'QQQ'
    print(alphabet)
    print(testDFA.transition(alphabet=alphabet, currentNode=Q1))
    
    

def DFAtest3():
    Q1 = node("Q1", False, [transitionEquation('a', 'Q1'), transitionEquation('b', 'Q1'), transitionEquation('c', 'Q2'), transitionEquation('d', 'Q3')])
    Q2 = node("Q2", True,  [transitionEquation('a', 'Q3'), transitionEquation('b', 'Q2'), transitionEquation('c', 'Q1'), transitionEquation('d', 'Q3')])
    Q3 = node("Q3", False, [transitionEquation('a', 'Q4'), transitionEquation('b', 'Q4'), transitionEquation('c', 'Q3'), transitionEquation('d', 'Q4')])
    Q4 = node("Q4", True,  [transitionEquation('a', 'Q1'), transitionEquation('b', 'Q4'), transitionEquation('c', 'Q1'), transitionEquation('d', 'Q4')])
    testNodeList = [Q1, Q2, Q3, Q4]
    # DFA: def __init__(self, name, nodesList):
    testDFA = DFA(name='testDFA', nodesList=testNodeList)
    alphabet = 'abccd'
    print(alphabet)
    print(testDFA.transition(alphabet=alphabet, currentNode=Q1))
    print('---')
    
    alphabet = 'cbdb'
    print(alphabet)
    print(testDFA.transition(alphabet=alphabet, currentNode=Q1))
    print('---')
    
    alphabet = 'abcd'
    print(alphabet)
    print(testDFA.transition(alphabet=alphabet, currentNode=Q1))
    

def NFAtest1():
    Q1 = node("Q1", False, [transitionEquation('a', 'Q2'), transitionEquation('c', 'Q4')])
    Q2 = node("Q2", False, [transitionEquation('b', 'Q3'), transitionEquation('$', 'Q1')])
    Q3 = node("Q3", True, [transitionEquation('a', 'Q2')])
    Q4 = node("Q4", False, [transitionEquation('c', 'Q3'), transitionEquation('$', 'Q3')])
    testNodeList = [Q1, Q2, Q3, Q4]
    initialState = Q1
    # DFA: def __init__(self, name, nodesList):
    testNFA = NFA(name='testNFA1', nodesList=testNodeList)
    alphabet='caa'
    print(testNFA.transitionWrapper(alphabet=alphabet, currentNode=initialState))
    print("---")
    
    alphabet='abab'
    print(testNFA.transitionWrapper(alphabet=alphabet, currentNode=initialState))
    print("---")
    
    alphabet='ccac'
    print(testNFA.transitionWrapper(alphabet=alphabet, currentNode=initialState))
    
def NFAtest2():
    q1 = node("q1", True, [transitionEquation('b', 'q2'), transitionEquation('$', 'q3')])
    q2 = node("q2", False, [transitionEquation('a', 'q2'), transitionEquation('c', 'q3')])
    q3 = node("q3", False, [transitionEquation('a', 'q1')])
    nodeList = [q1, q2, q3]
    initialState = q1
    testNFA = NFA(name='testNFA2', nodesList=nodeList)
    
    alphabet='baaca'
    print(testNFA.transitionWrapper(alphabet=alphabet, currentNode=initialState))
    print("---")
    
    alphabet='bca'
    print(testNFA.transitionWrapper(alphabet=alphabet, currentNode=initialState))
    print("---")
    
    alphabet='baac'
    print(testNFA.transitionWrapper(alphabet=alphabet, currentNode=initialState))
    
    


def testConvert1():
    Q1 = node("Q1", False, [transitionEquation('a', 'Q2'), transitionEquation('c', 'Q4')])
    Q2 = node("Q2", False, [transitionEquation('b', 'Q3'), transitionEquation('$', 'Q1')])
    Q3 = node("Q3", True, [transitionEquation('a', 'Q2')])
    Q4 = node("Q4", False, [transitionEquation('c', 'Q3'), transitionEquation('$', 'Q3')])
    testNodeList = [Q1, Q2, Q3, Q4]
    initialState = Q1
    # DFA: def __init__(self, name, nodesList):
    testNFA = NFA(name='testNFA1', nodesList=testNodeList)
    allAlphas=["a", "b", "c", "$"]
    
    convertedTable = testNFA.converter(allAlphas=allAlphas, initialState=initialState)
    
    converted = DFAwrapper(convertedTable, allAlphas, [Q3])

    print("New DFA is:")
    converted.prettyPrint()

    alphabet='aab'
    print(converted.transition(alphabet=alphabet, currentNode=initialState))
    print("---")
    alphabet='a'
    print(converted.transition(alphabet=alphabet, currentNode=initialState))
    print("---")
    alphabet='cb'
    print(converted.transition(alphabet=alphabet, currentNode=initialState))
    

def testConvert2():
    q1 = node("q1", True, [transitionEquation('b', 'q2'), transitionEquation('$', 'q3')])
    q2 = node("q2", False, [transitionEquation('a', 'q2'), transitionEquation('c', 'q3')])
    q3 = node("q3", False, [transitionEquation('a', 'q1')])
    nodeList = [q1, q2, q3]
    initialState = q1
    testNFA = NFA(name='testNFA2', nodesList=nodeList)
    allAlphas = ['a', 'b', 'c', '$']
    
    convertedTable = testNFA.converter(allAlphas=allAlphas, initialState=initialState)
    
    convertedDFA = DFAwrapper(convertedTable, allAlphas, [q1])
    
    print("New DFA is:")
    convertedDFA.prettyPrint()
    alphabet = 'baaca'
    print(convertedDFA.transition(alphabet=alphabet, currentNode=initialState))
    print("---")
    alphabet = 'bca'
    print(convertedDFA.transition(alphabet=alphabet, currentNode=initialState))
    print("---")
    alphabet = 'baac'
    print(convertedDFA.transition(alphabet=alphabet, currentNode=initialState))


def allTests():
    print("=== DFA validation tests === ")
    testValidationEmptyStates()
    testMultiArrows()
    print("")
    print("")
    print("=== DFA test 1 === ")
    DFAtest1()
    print("")
    print("")
    print("=== DFA test 2 === ")
    DFAtest2()
    print("")
    print("")
    print("=== DFA test 3 === ")
    DFAtest3()
    print("")
    print("")
    print("=== NFA test 1 ===")
    NFAtest1()
    print("")
    print("")
    print("=== NFA test 2 ===")
    NFAtest2()
    print("")
    print("")
    print("=== NFA conversion test 1 ===")
    testConvert1()
    print("")
    print("")
    print("=== NFA conversion test 2 ===")
    testConvert2()
    
allTests()