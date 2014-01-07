__author__ = 'penguin'


import random

class predict():
    # initial data array based on which job seeker and job provider data will generated randomly
    initialData = ['java', 'c', 'python', 'bash', 'linux', 'php', 'html', 'js', 'cuda', 'opencl', '.net', 'css', 'matlab', 'ruby', 'go', 'dart']
    # number of job seeker and job provider population to be created
    population = 100
    # number of skill to be included for now i m taking it as constant
    size = 5
    # minimum rank value to consider a suggestion healthy
    healthyRank = 3

    # function to generate random data at the start of application
    def createData(self):
        self.data = []
        # job seekers are saved at index 1 and job providers are saved at index 0
        for z in xrange(0, 2):
            output = []
            for x in xrange(0, self.population):
                temp = []
                for y in xrange(0,self.size):
                    loop = True
                    while loop:
                        selectedSkill = self.initialData[random.randint(0, len(self.initialData)-1)]
                        if not selectedSkill in temp:
                            temp.append(selectedSkill)
                            loop = False
                output.append(temp)
            self.data.append(output)
        return self.data

    # function return suggestions based on the skill set of the job seeker
    def suggest(self, userIndex):
        self.selectedUser = self.data[1][userIndex]
        # array of job seekers similar to selected job seeker
        matched = []
        # array with ranks of job seeker saved in matched
        matchedRank = []
        # final skill set which will be used to get the suggested job providers
        searchSkills = []
        # get similar users to selected job seeker based on skills
        for y in xrange(0, len(self.data[1])):
            i = 0
            for x in xrange(0, len(self.selectedUser)):
                if self.selectedUser[x] in self.data[1][y]:
                    i = i+1
            # choose the job seeker if only it have more then healthyRank skills similar to selected job seeker
            if i > self.healthyRank:
                matched.append(y)
                matchedRank.append(i)
        # for each similar job seekers get the unique skill set not common to that of selected job seeker
        for x in xrange(0, len(matchedRank)):
            matchedUser = self.data[1][matched[x]]
            for y in xrange(0,len(matchedUser)):
                if not matchedUser[y] in self.selectedUser and not matchedUser[y] in searchSkills:
                    searchSkills.append(matchedUser[y])
        # get suggested job providers for the similar search skills to that of selected job seeker
        predictedForSimilar = self.predictProvider(searchSkills)
        # get suggested job providers for the skills of selected job seeker
        predictedForUser = self.predictProvider(self.selectedUser)
        # get 3 high ranked suggestions
        finalSelectionForUser = self.selectMaxRanked(predictedForUser, 3, [])
        # get 2 high ranked suggestions
        finalSelectionForSimilar = self.selectMaxRanked(predictedForSimilar, 2, finalSelectionForUser[0])
        # merge both the outputs to form a common output
        finalSelectionForUser[0].extend(finalSelectionForSimilar[0])
        finalSelectionForUser[1].extend(finalSelectionForSimilar[1])
        return finalSelectionForUser

    # get the specified number of max ranked suggestions
    def selectMaxRanked(self, predictedList, iterator, selectedUser):
        maxRanked = [[], []]
        # if predicted list length is less then the iterator then the output will be predictedList only
        if len(predictedList[1]) > iterator:
            for y in xrange(0,iterator):
                maxRank = max(predictedList[1])
                indexOfMaxRank = predictedList[1].index(maxRank)
                if len(selectedUser) > 0:
                    if not predictedList[0][indexOfMaxRank] in selectedUser:
                        maxRanked[0].append(predictedList[0][indexOfMaxRank])
                        maxRanked[1].append(maxRank)
                else:
                    maxRanked[0].append(predictedList[0][indexOfMaxRank])
                    maxRanked[1].append(maxRank)
                del predictedList[1][indexOfMaxRank]
                del predictedList[0][indexOfMaxRank]
        else:
            maxRanked = predictedList
        return maxRanked

    # selected the job providers based on the matching skill
    def predictProvider(self, skills):
        predictedNull = True
        minRank = self.healthyRank
        while predictedNull:
            predicted = [[],[]]
            for x in xrange(0, len(self.data[0])):
                i = 0
                for y in xrange(0, len(skills)):
                    if skills[y] in self.data[0][x]:
                        i = i+1
                if i>minRank:
                    predicted[0].append(x)
                    predicted[1].append(i)
            if len(predicted[1])>1:
                break
            else:
                if minRank ==0:
                    break
                else:
                    minRank = minRank-1
        return predicted
