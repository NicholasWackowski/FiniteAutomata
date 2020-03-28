# Nicholas Wackowski
# DFA / NFA project

class DFA:
    # Requires a name (ex. DFA1), and a list of nodes (defined later).
    # Example: name: DFA_Test_1
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
    # for the boolean value at the last node in the DFA.
    def transition(self, alphabet, currentNode, isFirst=True, pathString=""):
        print("Nana:")
        self.prettyPrint()
        transList = currentNode.getTransitionFunction()
        print("Lulu:")
        for x in transList:
            x.prettyPrint()
            
        # Do some prints, so the output is legible
        if(isFirst == True):
            isFirst = False
            pathString = str(currentNode.getName())
        else:
            pathString += ("-->" + str(currentNode.getName()))
            
        # When we reach the last element, 
        if(len(alphabet) == 0):
            print(pathString)
            return currentNode.getIsBool()
        else:
            print("prinprin")
            currentNode.prettyPrint()
            lala = currentNode.getTransitionFunction()
            print("lala:")
            for y in lala:
                y.prettyPrint()
            for trans in currentNode.getTransitionFunction():
                trans.prettyPrint()
                if(alphabet[0] == trans.getInput()):
                    print("Transitioning from", currentNode.getName(), "to", trans.getEnd(), "using", alphabet[0])
                    return self.transition(alphabet[1:], self.getNodeByName(trans.getEnd()), isFirst, pathString)
            # If code reaches this line, it means it reached an ERROR STATE,
            # as that input was not valid for that state.
            printErrorCharacterMessage(currentNode, alphabet[0])
            return False
        
    # Takes in a string input, the name of the node which is skipped to
    def getNodeByName(self, name):
        for x in self.nodesList:
            if(x.getName() == name):
                return x
        # If it reaches this line, there is an error: no such node name exists
        print(name)
        #printErrorNameMessage(name)
        return None
    
    def printErrorCharacterMessage(errorNode, errorCharacter):
        print("ERROR! Invalid transition detected at " + errorNode.getName() + "!")
        print("Invalid character: " + errorCharacter)
        
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
        print("'"+str(self.input)+"' --> "+"'"+str(self.end)+"'")
    def getInput(self):
        return self.input_
    def getEnd(self):
        return self.end
