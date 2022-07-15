# bottleneck_vehicle_velocity_adaptation

The aim of this project is to get the relevant data of the surrounding vehicles (position and velocity) and adapt the velocity of the modelled vehicle accordingly.

The problem this project tries to solve is the worsened traffic flow of the vehicles near a traffic bottleneck. With the development of ITS, especially IoV and V2V communication, we are able to gather the data of interest from the surrounding vehicles in-real-time and act accordingly, in order to improve safety and traffic flow.

This repository contains 2 files - 'traffic_model' and 'vehicle_longitudinal_jupyter'. 

The traffic model contains 2 lanes, which are represented as a list of 3m-long cells, mimicing the idea behind cellular automata. However, the movement of the vehicles does not follow a CA-ruleset, as usually implemented in traffic flow simulations, but the vehicles are assigned random velocities in the range from 11m/s to 33m/s and at each time step, calculations about the new position of the vehicle and the adjusted velocity take place. It also spots the index and the target velocity of the modelled vehicle, which should the passed to the longitudinal dynamics model in order to give the appropriate torque as input.

The 'vehicle_longitudinal_jupyter' contains a longitudinal dynamics model of a vehicle. At the moment, there is a hardcoded torque input. However, the logic should be modified, so that the necessary torque would be calculated in-real-time, in order to see the behaviour of the vehicle in the traffic model.
