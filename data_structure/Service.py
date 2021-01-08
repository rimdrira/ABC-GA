class Service:

    # constructor

    def __init__(self, activity, responseTime, reliability, availability, price, matchingState):
        self.__activity = activity
        self.__responseTime = responseTime
        self.__reliability = reliability
        self.__availability = availability
        self.__price = price
        self.__matchingState = matchingState

    # get attributs

    def getResponseTime(self):
        return self.__responseTime

    def getPrice(self):
        return self.__price

    def getReliability(self):
        return self.__reliability

    def getAvailability(self):
        return self.__availability

    def getMatching(self):
        return self.__matchingState

    def getActivity(self):
        return self.__activity

    #  Euclidean Distance

    def euclideanDist(self, service):
        drt = self.__responseTime - service.getResponseTime()
        dpr = self.__price - service.getPrice()
        drel = self.__reliability - service.getReliability()
        dav = self.__availability - service.getAvailability()
        return (drt ** 2 + dpr ** 2 + drel ** 2 + dav ** 2) ** 0.5

    # Nearest neighbor 

    def getNeighbor(self, candidates) :
        return min([neighbor for neighbor in candidates if neighbor != self], key=lambda x: self.euclideanDist(x))
