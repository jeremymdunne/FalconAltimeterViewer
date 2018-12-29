class ParabolicKinematicEngine:
    def __init__(self, initialAltitude, initialVelocity, timestep):
        self.initialVelocity = initialVelocity
        self.timestep = timestep
        #get the time to the halfway point
        self.gravity = 9.81

    def compute(self, initialAltitude, dryMass, propellantMass, averageThrust, thrustDuration, coefficientOfDrag, area):
        self.dryMass = dryMass
        self.initialAltitude = initialAltitude
        self.propellantMass = propellantMass
        self.averageThrust = averageThrust
        self.thrustDuration = thrustDuration
        self.averageThrust = averageThrust
        self.coefficientOfDrag = coefficientOfDrag
        self.area = area
        boostData = self.boostPhase()
        coastData = self.coastPhase()
        recoveryData = self.recoveryPhase()
        return boostData + coastData + recoveryData

    def recoveryPhase(self):
        velocity = self.velocityAtEndOfCoast
        altitude = self.altitudeAtEndOfCoast
        time = self.timeAtEndOfCoast
        weight = self.dryMass
        data = []
        i = 0
        while altitude > self.initialAltitude:
            i += 1
            time += self.timestep
            dragIntegral = self.computeDragForce(velocity, altitude)*self.timestep
            velocity += (dragIntegral - self.gravity*self.timestep)/weight
            altitude += velocity*self.timestep
            #print("time: " + str(time))
            #print("weight: " + str(weight))
            #print("dragIntegral: " + str(dragIntegral))
            #print("velocity: " + str(velocity))
            tempData = [0,0]
            tempData[0] = time
            tempData[1] = altitude
            data.append(tempData)
        self.velocityAtEndOfRecovery = velocity
        self.altitudeAtEndOfRecovery = altitude
        self.timeAtEndOfRecovery = time
        return data

    def coastPhase(self):
        velocity = self.velocityAtEndOfBoost
        altitude = self.altitudeAtEndOfBoost
        weight = self.dryMass
        data = []
        i = 0
        time = self.timeAtEndOfBoost
        while velocity > 0:
            i += 1
            time += self.timestep
            dragIntegral = self.computeDragForce(velocity,altitude)*self.timestep
            velocity -= (dragIntegral + self.gravity*self.timestep)/weight
            altitude += velocity*self.timestep
            #print("time: " + str(time))
            #print("weight: " + str(weight))
            #print("dragIntegral: " + str(dragIntegral))
            #print("velocity: " + str(velocity))
            tempData = [0,0]
            tempData[0] = time
            tempData[1] = altitude
            data.append(tempData)
        self.velocityAtEndOfCoast = velocity
        self.altitudeAtEndOfCoast = altitude
        self.timeAtEndOfCoast = time
        return data

    def boostPhase(self):
        #handle the boost phase calculation
        velocity = 0
        altitude = self.initialAltitude
        weight = self.dryMass + self.propellantMass
        data = []
        time = 0
        #print(self.thrustDuration)
        #print(int(self.thrustDuration/self.timestep))
        for i in range(0,int(self.thrustDuration/self.timestep) + 1):
            time = i*self.timestep
            weight = self.dryMass - self.propellantMass/(self.thrustDuration/self.timestep)*i
            thrustIntegral = self.averageThrust * self.timestep
            dragIntegral = self.computeDragForce(velocity,altitude)*self.timestep
            velocity += (thrustIntegral - dragIntegral - self.gravity*self.timestep)/weight
            altitude += velocity*self.timestep
            #print("time: " + str(time))
            #print("weight: " + str(weight))
            #print("thrustIntegral: " + str(thrustIntegral))
            #print("dragIntegral: " + str(dragIntegral))
            #print("velocity: " + str(velocity))
            tempData = [0,0]
            tempData[0] = time
            tempData[1] = altitude
            data.append(tempData)
        self.velocityAtEndOfBoost = velocity
        self.altitudeAtEndOfBoost = altitude
        self.timeAtEndOfBoost = time
        return data

    def computeDragForce(self, velocity, altitude):
        #drag force modeled by D = Cd * p * V^2/2 * A
        # for now, Cd and A = coefficientOfDrag
        drag = self.coefficientOfDrag * self.area * self.calculateAirDensity(altitude) * velocity**2 / 2
        return drag

    def calculateAirDensity(self, altitude):
        temp = 288.16 - .0065*altitude
        return 1.225*(pow(temp/288.16,5.2561-1))

"""
    def compute(self):
        timeToHalfway = self.initialVelocity/self.gravity
        print(timeToHalfway)
        data = []
        for i in range(0,int(timeToHalfway*2/self.timestep + 1)):
            temp = [0,0]
            temp[0] = i*self.timestep
            print(temp[0])
            temp[1] = self.initialVelocity * temp[0] - .5*self.gravity*pow(temp[0],2)
            data.append(temp)
        return data
"""

if __name__ == '__main__':
    p = ParabolicKinematicEngine(0,9.9,.01)
    print(p.compute(0,1,.2,25,1,.8,.10**2*3.14))
