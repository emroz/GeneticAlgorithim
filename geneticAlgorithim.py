# How to Play:
# Enter values for Population,Generation,MutationRate and MazeNumber(separeted by commas)
# in the pop-up to start the Genetic Algorithm
# MazeNumber corresponds to the maze index in the maze_samples file
# Clicking OK in the pop-up runs the Algorithm until the generation runs out or a solution is found
# Fittest individual is displayed in the maze grid at the end
# You can comment out the visualize part and still the genetic algorithim will work


import maze
import maze_samples
import turtle
import random



class InputReader :

    def readGeneticAlogorithimInput(self):
        print('')
        enteredValue = turtle.textinput("GA", "Enter popolation,generation,mutationRate,maze number")
        if enteredValue != None:
            inputList = enteredValue.split(',')
            if len(inputList) == 4:
                return ( int(inputList[0]),int(inputList[1]),int(inputList[2]),int(inputList[3]))
            else:
                return None
        return None


class Visualize :


    def ShowMaze(self,fittestIndividual, mazeGrid):

        M = maze.Maze(mazeGrid)
        M.Visualize()
        M.RunMaze(fittestIndividual.getChromosomes())
        turtle.done()


class FitnessResults:


    def __init__( self, fitnessScore, cheeseAtFinalPosition, canReachCheese, foundBlockedMove, moveBlockedTillCount, totalMove ):
        self.fitnessScore = fitnessScore
        self.cheeseAtFinalPosition = cheeseAtFinalPosition
        self.canReachCheese = canReachCheese
        self.foundBlockedMove = foundBlockedMove
        self.moveBlockedTillCount = moveBlockedTillCount
        self.totalMove = totalMove


    def display(self):
        print('############ Fitness Score Summary #########################')
        print('Fitness Score                                        = ', self.fitnessScore)
        print('Finished Position was at cheese                      = ', self.cheeseAtFinalPosition)
        print('Found cheese during the move                         = ', self.canReachCheese)
        print('Was blocked or moved out of maze                     = ', self.foundBlockedMove)
        print('Number of move till path was blocked or out of maze  = ', self.moveBlockedTillCount)
        print('Total number of move                                 = ', self.totalMove)




class Individual:


    def __init__(self, size,  chromosomes = None):
        self.size = size
        self.chromosomes = []
        self.mutationProbalility = random.randint(0,100)
        self.fitnessResult = None
        if (chromosomes == None):
            for i in range(0, size):
                self.chromosomes.append(self.getRandomGene())
        else:
            self.chromosomes = chromosomes


    def setFitnessResults(self, fitnessResults):
        self.fitnessResult = fitnessResults


    def getFitnessResults(self):
        return self.fitnessResult


    def getChromosomes(self):
        return self.chromosomes


    def mutate(self,mutationRate):
        if self.mutationProbalility < mutationRate:
            idx = random.randint(0,self.size-1)
            changedGene = self.getRandomGene()
            self.chromosomes[idx] = changedGene

    def getRandomGene(self):
        geneList = ['U', 'D', 'R', 'L']
        rand = random.randint(0,3)
        return geneList[rand]

    def display(self):
        print('********* Individual  Summary *************************')
        print('Chromosomes                                          = ', self.chromosomes)
        print('Mutation Probalility                                 = ', self.mutationProbalility)
        print('')
        self.fitnessResult.display()
        print('')


class GridPosition:
    def __init__( self, r, c ):
        self.r = r
        self.c = c



class Fitness :

    def __init__(self, values):
        self.row_dim = len(values)
        self.col_dim = len(values[0])
        self.values = values
        self.cheese_pos = None
        self.start_pos = None
        self.openSpace = 0
        self.FindStartFinishAndOpenSpace()

    def calculateFitness(self, chromosomes, stringLength ):
        result = self.CheckPathInMaze(chromosomes)
        fitnessScore = 0

        if result.cheeseAtFinalPosition == True :
            fitnessScore += stringLength

        if result.canReachCheese == True :
            fitnessScore += stringLength
        else:
            fitnessScore += self.openSpace

        if result.foundBlockedMove == True :
            fitnessScore += result.moveBlockedTillCount
        else:
            fitnessScore += result.totalMove

        result.fitnessScore = fitnessScore
        return result


    def FindStartFinishAndOpenSpace(self):
        for r in range(self.row_dim):
            for c in range(self.col_dim):
                if self.values[r][c] == 'C':
                    self.cheese_pos = GridPosition(r,c)
                elif self.values[r][c] == 'M':
                    self.start_pos = GridPosition(r,c)
                elif self.values[r][c] == '-':
                    self.openSpace += 1


    def CheckPathInMaze(self, moves):
        canReachCheese = False
        cheeseAtFinalPosition = False
        foundBlockedMove = False
        moveBlockedTillCount = 0
        totalMove = 0
        r = self.start_pos.r
        c = self.start_pos.c
        for el in moves:
            totalMove += 1
            new_r, new_c = r,c
            if el=='U': new_r += 1
            elif el=='D': new_r -= 1
            elif el=='R': new_c += 1
            elif el=='L': new_c -= 1
            else:
                print('Unrecognized Command')
                return
            if 0 <= new_r and new_r < self.row_dim \
            and 0 <= new_c and new_c < self.col_dim:
                if self.values[new_r][new_c] in ['M', '-', 'C']:
                    r,c = new_r, new_c
                    if self.values[new_r][new_c] == 'C':
                        canReachCheese = True
                    if foundBlockedMove == False :
                        moveBlockedTillCount += 1
                elif self.values[new_r][new_c] == 'x':
                    if foundBlockedMove == False :
                        moveBlockedTillCount += 1
                        foundBlockedMove = True
            else:
                if foundBlockedMove == False:
                    moveBlockedTillCount += 1
                    foundBlockedMove = True
        if r == self.cheese_pos.r and c == self.cheese_pos.c:
            cheeseAtFinalPosition = True

        results = FitnessResults(0,cheeseAtFinalPosition, canReachCheese, foundBlockedMove, moveBlockedTillCount, totalMove)
        return results

    def display(self):
        print('&&&&&&&&& Maze  Summary &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        print('Number Of Open Space                                 = ', self.openSpace)
        print('')


class MonteCarlo:

  def getKey(self,item):
    return item[0]

  def SortIndividualListByFitness(self, populationListWithFitnessScore):
    sortedList = sorted(populationListWithFitnessScore, key=self.getKey, reverse=True)
    return sortedList


  def SetWeightsForMonteCarloSelection(self, populationWithFitnessResultList):
    totalFitnessScore = 0
    for i, p in enumerate(populationWithFitnessResultList):
      totalFitnessScore += p[0]

    normalized_values = []
    for i, p in enumerate(populationWithFitnessResultList):
      normalizedScore = int(p[0]/totalFitnessScore*100+.5)
      normalized_values.append((normalizedScore, p[1]))

      accum = 0
      selection_weights = []
      for i, p in enumerate(populationWithFitnessResultList):
        accum += p[0]
        selection_weights.append((accum, p[1]))
      return selection_weights

  def MonteCarloSelection(self, selection_weights):
    selection = random.randint(0, selection_weights[-1][0])
    for i, p in enumerate(selection_weights):
      if selection <= p[0]:
        return p[1]


class GeneticAlogorithim:

    def __init__(self, populationCount, generationCount, mutationRate):
        self.populataionCount = populationCount
        self.generationCount = generationCount
        self.mutationRate = mutationRate
        self.populationDict = {}
        self.fittestIndividual = None

    def initializePopulataion(self, size):
        # Create # individual as same as the populatatonCount and add them in population dictionary
        populationList = []
        for index in range(0,self.populataionCount ):
            populationList.append(Individual(size))
        # Add populationList to the population dictionary using generation index as key and populationlist as valies
        self.populationDict.update({0:populationList})

    def getFittestIndividual(self):
        return self.fittestIndividual


    def crossBreeding(self,  parent1,  parent2, size):
        breakPoint = random.randint(0,size)
        firstInvidual = Individual(size, parent1.getChromosomes()[0:breakPoint] + parent2.getChromosomes()[breakPoint:size])
        secondIndividual = Individual(size, parent2.getChromosomes()[0:breakPoint] + parent1.getChromosomes()[breakPoint:size])
        return (firstInvidual, secondIndividual)


    def solve(self, stringLength, mazeValues):


        monteCarlo = MonteCarlo()
        fitness = Fitness(mazeValues)
        self.initializePopulataion(stringLength)
        generationIndex = 0
        keepLooping = True
        populationWithFitnessResultList = []
        runningTotalOfPopulaiton = 0
        while keepLooping:
            populationList = self.populationDict[generationIndex]
            populationWithFitnessResultList.clear()
            for i, p in enumerate(populationList):
                runningTotalOfPopulaiton += 1
                fitnessResult = fitness.calculateFitness(p.getChromosomes(), stringLength)
                p.setFitnessResults(fitnessResult)
                if self.fittestIndividual == None:
                    self.fittestIndividual = p
                elif p.getFitnessResults().fitnessScore > self.fittestIndividual.getFitnessResults().fitnessScore:
                    self.fittestIndividual = p
                populationWithFitnessResultList.append((fitnessResult.fitnessScore, p))

                if fitnessResult.cheeseAtFinalPosition == True:
                    keepLooping = False
                    print('')
                    print('!!!!!!!!!!!!!! HOORAY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    print('###### INDIVIDUAL FINISHED AT CHEESE LOCATION #######')
                    print('')
                    self.fittestIndividual = p
                    break

            if generationIndex >= self.generationCount-1:
                keepLooping = False


            if keepLooping == False:
                break


            generationIndex += 1


            SortedpopulationWithFitnessResultList = monteCarlo.SortIndividualListByFitness(populationWithFitnessResultList)
            weightedList = monteCarlo.SetWeightsForMonteCarloSelection(SortedpopulationWithFitnessResultList)

            nextGenPopulationList = []
            for p in range(0, self.populataionCount // 2):
                parent1 = monteCarlo.MonteCarloSelection(weightedList)
                parent2 = monteCarlo.MonteCarloSelection(weightedList)
                individualTuple = self.crossBreeding(parent1, parent2, stringLength)
                individualTuple[0].mutate(self.mutationRate)
                individualTuple[1].mutate(self.mutationRate)
                nextGenPopulationList.append(individualTuple[0])
                nextGenPopulationList.append(individualTuple[1])
            self.populationDict.update({generationIndex: nextGenPopulationList})


        print('$$$$$$$ Genetic Algorithim Completed $$$$$$$$$$$$$$$$$$$$$$$')
        print('Generation Count                                     = ', self.generationCount)
        print('Population Count                                     = ', self.populataionCount)
        print('Mutation Rate                                        = ', self.mutationRate)
        print('Number Of Generation Looped                          = ', generationIndex+1)
        print('Total Number Of population tested                    = ', runningTotalOfPopulaiton)
        print('')
        fitness.display()



def main():

    reader = InputReader()
    userInput = reader.readGeneticAlogorithimInput()
    if userInput != None :
        mazeNumber = userInput[3]
        geneticAlgo = GeneticAlogorithim(userInput[0], userInput[1], userInput[2])
        geneticAlgo.solve(maze_samples.string_length[mazeNumber], maze_samples.maze[mazeNumber])
        fittestIndividual = geneticAlgo.getFittestIndividual()
        print('********* Fittest Individual   *************************')
        fittestIndividual.display()

        visualize = Visualize()
        visualize.ShowMaze(fittestIndividual, maze_samples.maze[mazeNumber] )




if __name__ == '__main__':
    main()

