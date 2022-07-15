import numpy as np
import random as rnd


vehicle_props_lane1 = [] # a list of dictionaries containing the positions and velocities of the vehicles in the lane
vehicle_props_lane2 = [] 
speeds_lane1 = [] # a list containing the velocities in the vehicles in the lane
speeds_lane2 = []

def generate_lane_population():
    vehicles_lane1 = np.random.choice([0, 1], size=50, p=[.75, .25])
    vehicles_lane1[0] = 1 # my vehicle

    vehicles_lane2 = np.random.choice([0, 1], size=50, p=[.75, .25])
    vehicles_lane2[0] = 0 # the speed of the vehicle right next to ours is irrelevant

    return [vehicles_lane1, vehicles_lane2]

def vehicle_props(vehicles_lane1, vehicles_lane2):
    # generating vehicles and their velocities - first lane (containing our vehicle)
    for i in range(len(vehicles_lane1)):
        if vehicles_lane1[i] == 1: # == if there's a vehicle on the lane
            speed = rnd.randint(11,33) # generating random speeds in the range of (11-33) m/s
            vehicle_props_lane1.append({"position": i + 1, "speed": speed})
            speeds_lane1.append(speed)
        else:
            vehicle_props_lane1.append({"position": i + 1, "speed": 0})
            speeds_lane1.append(0)

    # generating vehicles and their velocities - second lane
    for i in range(len(vehicles_lane2)):
        if vehicles_lane2[i] == 1:
            speed = rnd.randint(11,33)
            vehicle_props_lane2.append({"position": i + 1, "speed": speed})
            speeds_lane2.append(speed)
        else:
            vehicle_props_lane2.append({"position": i + 1, "speed": 0})
            speeds_lane2.append(0)

    return [speeds_lane1, speeds_lane2]

def vehicleInFront (speeds_lane1, speeds_lane2): # finding the last vehicles in both lanes
    myVehicleFlag = 0

    # first lane:
    for index, speed in enumerate(speeds_lane1):
        if index == len(speeds_lane1)-1: # last vehicle (preventing "out of range" error message)
            next_vehicle_lane1 = {"speed": 200, "position": index+2}
            myVehicle = {"speed": 200, "position": index+2}
            break
        if speed != 0:
            if myVehicleFlag == 0:
                myVehicle = {"speed": speed, "position": index+1}
                myVehicleFlag = 1 # (targets our vehicle and skips it in the next iterations)
            else:
                next_vehicle_lane1 = {"speed": speed, "position": index+1}
                break
    
    # second lane:
    for index, speed in enumerate(speeds_lane2):
        if index == len(speeds_lane2)-1:
            next_vehicle_lane2 = {"speed": 200, "position": index+2}
            break
        if speed != 0:
            next_vehicle_lane2 = {"speed": speed, "position": index+1}
            break

    # checking which of the two found vehicles is closer to ours (meaning it would have to merge before our vehicle)
    if next_vehicle_lane1["position"] < next_vehicle_lane2["position"] or next_vehicle_lane2["speed"] == 0: # the vehicle in our lane is closer to us, meaning it should merge right before us
        next_vehicle = {"speed": next_vehicle_lane1["speed"], "position": next_vehicle_lane1["position"]}
    else: # if the vehicle is on the same position as our vehicle, or it's closer than the one on our lane
        if next_vehicle_lane2["position"] < myVehicle["position"]: # if the vehicle from the second lane is behind ours
            next_vehicle = {"speed": next_vehicle_lane1["speed"], "position": next_vehicle_lane1["position"]} # then we take into consideration the one in our lane
        elif next_vehicle_lane2["position"] == myVehicle["position"]:
            if next_vehicle_lane2["speed"] < myVehicle["speed"]:
                next_vehicle = {"speed": next_vehicle_lane1["speed"], "position": next_vehicle_lane1["position"]}
            else:
                next_vehicle = {"speed": next_vehicle_lane2["speed"], "position": next_vehicle_lane2["position"]}
        else:
            next_vehicle = {"speed": next_vehicle_lane2["speed"], "position": next_vehicle_lane2["position"]}

    return [next_vehicle["speed"], next_vehicle["position"], myVehicle["speed"], myVehicle["position"]]

def adaptSpeed (speeds_array, position, hasMoved): # hasMoved == faster lane; !hasMoved == slower lane
    if hasMoved:
        if position+2 < len(speeds_array) and speeds_array[position+2] != 0:
            if speeds_array[position] > speeds_array[position+2]:
                speeds_array[position] = speeds_array[position+2]
    if not hasMoved:
        if position+1 != 0:
            if speeds_array[position] > speeds_array[position+1] and speeds_array[position+1] != 0:
                speeds_array[position] = speeds_array[position+1]
        if position+2 < len(speeds_array) and speeds_array[position+2] != 0:
            if speeds_array[position] > speeds_array[position+2]:
                speeds_array[position] = speeds_array[position+2]
    return speeds_array[position]

if __name__ == '__main__':
    time_step = 0.2; # seconds (loop on 0.1 !!!!)
    [vehicles_lane1, vehicles_lane2] = generate_lane_population()
    [speeds_lane1, speeds_lane2] = vehicle_props(vehicles_lane1, vehicles_lane2)
    target_velocity = speeds_lane1[0]
    
    while(1):
        if speeds_lane1[-1] != 0 and speeds_lane2[-1] != 0: # if both lanes have vehicles on the last slot, we should decide which one will merge first
            if speeds_lane1[-1] >= speeds_lane2[-1]: # if the first lane has greater velocity
                for i in reversed(range(len(speeds_lane1))): # iterating from the end towards the beginning of the list, in order to prevent overwrite
                    if i == len(speeds_lane1) - 1: # if the iterator is in the last slot of the lane
                        speeds_lane2[i] = speeds_lane2[i] # the vehicle in lane2 stays, because the one from the first lane merged
                        speeds_lane1[i] = 0 # the first lane doesn't have a vehicle in the last slot anymore, because it had already merged

                    if i > 0 and i != len(speeds_lane1) - 1: # if the iterator is in a middle slot of the first lane

                        if speeds_lane1[i] != 0: # if the slot is non-empty
                            delta_x_1 = round(time_step * speeds_lane1[i] / 3) # calculates how many cells has the vehicle moved forward

                            if i + delta_x_1 > len(speeds_lane1)-1: # if the number of moved cells forwards exceeds the length of the lane
                                j = 1
                                while(1): # checks where the vehicle would go
                                    if len(speeds_lane1) - j == i:
                                        speeds_lane1[i] = adaptSpeed(speeds_lane1, i, True)
                                        break
                                    if speeds_lane1[len(speeds_lane1) - j] == 0:
                                        speeds_lane1[len(speeds_lane1) - j] = adaptSpeed(speeds_lane1, i, True)
                                        if len(speeds_lane1) - j != i: # if it hasn't moved, the slot shouldn't be emptied
                                            speeds_lane1[i] = 0
                                        break
                                    j += 1                        

                            elif speeds_lane1[i + delta_x_1] != 0:
                                j = 1
                                while (1): 
                                    if j == delta_x_1:
                                        speeds_lane1[i] = adaptSpeed(speeds_lane1, i, True)
                                        break
                                    if speeds_lane1[i + delta_x_1 - j] == 0:
                                        speeds_lane1[i + delta_x_1 - j] = adaptSpeed(speeds_lane1, i, True)
                                        if j != delta_x_1:
                                            speeds_lane1[i] = 0
                                        break
                                    j += 1

                            else:
                                speeds_lane1[i + delta_x_1] = adaptSpeed(speeds_lane1, i, True)
                                speeds_lane1[i] = 0

                    if i > 0 and i != len(speeds_lane2) - 1:
                        if speeds_lane2[i] != 0:
                            delta_x_2 = round(time_step * speeds_lane2[i] / 3)

                            if i + delta_x_2 > len(speeds_lane2)-1:
                                j = 1
                                while(1): # checks where the vehicle should move to
                                    if len(speeds_lane2) - j == i:
                                        speeds_lane2[i] = adaptSpeed(speeds_lane2, i, False)
                                        break
                                    if speeds_lane2[len(speeds_lane2) - j] == 0:
                                        speeds_lane2[len(speeds_lane2) - j] = adaptSpeed(speeds_lane2, i, False)
                                        speeds_lane2[i] = 0
                                        break
                                    j += 1

                            elif speeds_lane2[i + delta_x_2] != 0:
                                j = 1
                                while(1):
                                    if j == delta_x_2:
                                        speeds_lane2[i] = adaptSpeed(speeds_lane2, i, False)
                                        break
                                    if speeds_lane2[i + delta_x_2 - j] == 0:
                                        speeds_lane2[i + delta_x_2 - j] = adaptSpeed(speeds_lane2, i, False)
                                        speeds_lane2[i] = 0
                                        break
                                    j += 1

                            else:
                                speeds_lane2[i + delta_x_2] = adaptSpeed(speeds_lane2, i, False)
                                speeds_lane2[i] = 0

    ############################################################################################################################################
            elif speeds_lane1[-1] < speeds_lane2[-1]: # if the velocity of the vehicle on the second lane is greater
                 for i in reversed(range(len(speeds_lane1))):
                    if i == len(speeds_lane1) - 1:
                        speeds_lane1[i] = speeds_lane1[i]
                        speeds_lane2[i] = 0

                    if i > 0 and i != len(speeds_lane1) - 1: # if the iterator is in a middle slot

                        if speeds_lane1[i] != 0: # if the slot is non-empty
                            delta_x_1 = round(time_step * speeds_lane1[i] / 3) # calculated how many cells will the vehicle move forward

                            if i + delta_x_1 > len(speeds_lane1)-1: # if the number of cells exceeds the lane length
                                j = 1
                                while (1): # checks which slot the vehicle will move to
                                    if len(speeds_lane1) - j == i:
                                        speeds_lane1[i] = adaptSpeed(speeds_lane1, i, False)
                                        break
                                    if speeds_lane1[len(speeds_lane1) - j] == 0:
                                        speeds_lane1[len(speeds_lane1) - j] = adaptSpeed(speeds_lane1, i, False)
                                        speeds_lane1[i] = 0
                                        break
                                    j += 1

                            elif speeds_lane1[i + delta_x_1] != 0:
                                j = 1
                                while (1): 
                                    if j == delta_x_1:
                                        speeds_lane1[i] = adaptSpeed(speeds_lane1, i, False)
                                        break
                                    if speeds_lane1[i + delta_x_1 - j] == 0:
                                        speeds_lane1[i + delta_x_1 - j] = adaptSpeed(speeds_lane1, i, False)
                                        speeds_lane1[i] = 0 
                                        break
                                    j += 1

                            else:
                                speeds_lane1[i + delta_x_1] = adaptSpeed(speeds_lane1, i, False)
                                speeds_lane1[i] = 0

                    if i > 0 and i != len(speeds_lane2) - 1:

                        if speeds_lane2[i] != 0:
                            delta_x_2 = round(time_step * speeds_lane2[i] / 3)

                            if i + delta_x_2 > len(speeds_lane2)-1:
                                j = 1
                                while(1):
                                    if len(speeds_lane2) - j == i:
                                        speeds_lane2[i] = adaptSpeed(speeds_lane2, i, True)
                                        break
                                    if speeds_lane2[len(speeds_lane2) - j] == 0:
                                        speeds_lane2[len(speeds_lane2) - j] = adaptSpeed(speeds_lane2, i, True)
                                        speeds_lane2[i] = 0
                                    j +=1

                            elif speeds_lane2[i + delta_x_2] != 0:
                                j = 1
                                while(1):
                                    if j == delta_x_2:
                                        speeds_lane2[i] = adaptSpeed(speeds_lane2, i, True)
                                    if speeds_lane2[i + delta_x_2 - j] == 0:
                                        speeds_lane2[i + delta_x_2 - j] = adaptSpeed(speeds_lane2, i, True)
                                        speeds_lane2[i] = 0
                                        break
                                    j += 1

                            else:
                                speeds_lane2[i + delta_x_2] = adaptSpeed(speeds_lane2, i, True)
                                speeds_lane2[i] = 0

    ############################################################################################################################################                           
        else:
            for i in reversed(range(len(speeds_lane1))): # iterating from the end towards the beginning in order to prevent overwrite

                if speeds_lane1[i] != 0: # if the slot is non-empty
                    delta_x = round(time_step * speeds_lane1[i] / 3)

                    if i + delta_x > len(speeds_lane1)-1: # if the new position it ourside of the lane range
                        speeds_lane1[i] = 0 # the vehicle will merge, and the slot will be emptied

                    elif speeds_lane1[i + delta_x] != 0: # if the new position is non-empty
                        j = 1
                        while (1): 
                            if j == delta_x:
                                speeds_lane1[i] = adaptSpeed(speeds_lane1, i, True)
                                break
                            if speeds_lane1[i + delta_x - j] == 0:
                                speeds_lane1[i + delta_x - j] = adaptSpeed(speeds_lane1, i, True)
                                speeds_lane1[i] = 0 # the slot gets emptied because the vehicle moved
                                break
                            j += 1
                    

                    else: 
                        speeds_lane1[i + delta_x] = adaptSpeed(speeds_lane1, i, True)
                        speeds_lane1[i] = 0

                if speeds_lane2[i] != 0: # if the slot is non-empty
                    delta_x = round(time_step * speeds_lane2[i] / 3)

                    if i + delta_x > len(speeds_lane2)-1: # if the new position it ourside of the lane range
                        speeds_lane2[i] = 0 # the vehicle will merge, and the slot will be emptied

                    elif speeds_lane2[i + delta_x] != 0: # if the new position is non-empty
                        j = 1
                        while (1): 
                            if j == delta_x:
                                speeds_lane2[i] = adaptSpeed(speeds_lane2, i, True)
                                break
                            if speeds_lane2[i + delta_x - j] == 0:
                                speeds_lane2[i + delta_x - j] = adaptSpeed(speeds_lane2, i, True)
                                speeds_lane2[i] = 0 # the slot gets emptied because the vehicle moved
                                break
                            j += 1

                    else:
                        speeds_lane2[i + delta_x] = adaptSpeed(speeds_lane2, i, True)
                        speeds_lane2[i] = 0

        [nextVehicleSpeed, nextVehiclePosition, myVehicleSpeed, myVehiclePosition] = vehicleInFront (speeds_lane1, speeds_lane2)
        print("Distance between our vehicle and the one in front of us: ", (nextVehiclePosition - myVehiclePosition - 1) * 3, " meters.")
        print(speeds_lane1)
        print(speeds_lane2)
        print(" ")

        if all(el==0 for el in speeds_lane1):
            break