# SafeDrive - Drowsiness detection and Alert system

This project consists of 3 subparts: Detection, alertion and simulation. 

The detection part uses the webcam of a computer and some python code to manually calculate the EAR and MAR (Eye Aspect Ratio and Mouth Aspect Ratio). When they cross a certain threshold 
(determined by manual testing), the alertion system goes off.

The alertion system consists of 5 LEDs and an ISD 1820 speaker module, powered by an Arduino Mega. The python script sends a boolean variable for yawns and shut-eye, 
refreshing at a rapid rate. When shut-eye is detected, the LEDs light up and the speaker plays, alerting the driver. When the driver is yawning, only the speaker plays. 

The simulation system consists of a basic simulation of a car using JS. It cruises at a set speed, and when drowsiness (ie. only shut-eye) is detected, the car is slowed down at a very controlled rate, eventually stopping if the driver does nothing.
(currently, the simulation system appears to be working but it somehow is not recieving data from the python script, so it is broken)

