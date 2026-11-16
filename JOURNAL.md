---
title: "Omni DIrectional Drivebase"
github: ""
description: "Omni directional drivebase powered by 4 motors and mecanum wheels. Goal is to make this a hub for any future projects I might make, such as a robotic arm which can be attached to the drivebase and use its wireless communications. It will also be a good starting point for me to start learning computer vision driven by the SBC."
created_at: "2026-11-04"
total_time: "29h"
---

# November 4, 2026: Set up CAD & Initial research

Today i worked on the initial research and set up Onshape for cadding it. 

## Overall Plan:
### fancy electronics:
 - Rock 4 c+ using my old wireless communications system
 - Arduino uno R4 for microcontroller
 - 2x L298N motor drivers
 - MPU6050 for forward based on driver orientation
### Other:
 - 12 V battery
 - 4x JGB 520 motors
 - 4x 60 mm mecanum wheels
 - 1x 12 V to USB buck converter
 - A lot of m3 screws!
 - Aluminum extrusion square for perimeter
 - 3d printed corner modules for each motor

I also set up Onshape and made a basic piece of aluminum extrusion, along with a wheel hub.
![](https://fabricate.hackclub-assets.com/2c0eade9036cfd0768019eb5c0d678b47e51399511021d02a337e5f062249ee3/image-png/image.png)

![](https://fabricate.hackclub-assets.com/a2492b46fc6986701920af69c6159ac08ae7312433786ccf99324ff9bb330c32/image-png/image.png)

**Total time spent: 1h 12m**

# November 5, 2026: Started designing corner module

Today and yesterday, I started working on the corner modules, the way that the drivebase actually drives. I have learned a lot so far such as: 
 - Screws in onshape
 - Bevel gears in onshape
 - why onshape is so good!

I added some a bearing and retention clip to prevent the axle with the wheel from sliding around since bevel geared assemblys tend to do that.
![](https://fabricate.hackclub-assets.com/cc11b88e8d0148d7e4df641a0a0fd88be415264c1a97108c0fed9ba1bb1cfb25/image-png/image.png)

![](https://fabricate.hackclub-assets.com/e957ffcef5914b72cd6e747b15b44e2999596e361640d2c4163a33fd7d8f49e0/image-png/image.png)
![](https://fabricate.hackclub-assets.com/308de8ca56fd84ce16d30c1c608d5e3036cb2ef9074cde440f86bd410ca3be7b/image-png/image.png)

**Total time spent: 2h 12m**

# November 6, 2026: Started Belly Pan

I started cadding the belly pan. This will be used to secure electronics and increase stabilty and strength. I made basic mounts using T screws so it can attach to the aluminum extrusion, and I added simple extrusions for the L298N drivers. Tomorrow, I will add a place for the Rock 4 C+ and Arduino such that they are next to each other and near the center for the MPU 6050 gyro. I also want to get the battery installing area ready soon too.

P.S. I know that the belly pan is way too large for my a1 mini, so I will do weight optimization and split up the belly pan so it isn't a large sheet of plastic.

![](https://fabricate.hackclub-assets.com/afee89bce27a26d78306c3f4955ee059361b558d2238f2216613eb27341f4f43/image-png/image.png)
![](https://fabricate.hackclub-assets.com/de54cff3d52022445503950c5f3c6f40c9100ab41dffd5ccc3967ca573f0d3de/image-png/image.png)

**Total time spent: 1h 30m**

# November 7, 2026: Cadded the "idea" for the bellypan

Finished bellypan base!!

Today I finished cadding the belly pan or at least the actual functional part. I added mounts for the MPU 6050, Arduino, and Rock 4 C+. I am facing some issues regarding the Rock 4 C+, as there is no public cad for the sheet metal case that I have, so I just measured out the holes for mounting. I also increased the amount of holes for the T nuts to hold the belly pan onto the frame as I am going to split the belly pan into 9 chunks because I my a1 mini is *mini*. I also want to pocket the belly pan to reduce filament use and make it easy to ziptie wires. I am still waiting on some software testing to determine how much power this thing needs, and after that Ill make a hole and battery mount. 
![](https://fabricate.hackclub-assets.com/6b201db24e8ce94e228de55f7feb103da17c69d16fb4c4b436d9d303ca92dcd9/image-png/image.png)
![](https://fabricate.hackclub-assets.com/980b1db1c6d220e58cb75ebe65fae2c8e640411103dc24b3abcdf45ba543822a/image-png/image.png)

**Total time spent: 1h 42m**

# November 8, 2026: Taking a break and doing software!

TLDR: I made communcations =D
I didn't feel like cadding, even though all I have to do is make a circular pattern and split and pocket the belly pan so I set up the remote communications!
It was probably the most annoying thing I have ever done. Today consisted of writing two(mid difficulty) python scripts, one that runs on the SBC, starting a listening server on port 5000, and another listening and communicating over that port. The python scripts themselves weren't that difficult to program, but setting up the wifi communications via a hotspot was very annoying. I decided to use hostapd and dnsmasq, so i can create a network, and communicate over it. Setting up the network was straight forward except for the time i mistook a hyphen for an underscore(+10 min of troubleshooting). The most annoying part was definetly ip assigning. I need to assign the computer 192.168.4.1, so it can communicate successfuly, but obviously that wasn't happening. I took the lazy route and ended up making a startup service that runs a bash script to add the ip address, but a win is a win.

this demo video uses a very arbitrary script on the microcontroller which just repeats what was sent to it, but proves the concept
![](https://fabricate.hackclub-assets.com/92714f3082f52fa744536a9cb737208c48c1ac1b0e26470fcb98bece1201e0c8/video-quicktime/IMG_2383.mov)

**Total time spent: 2h 30m**

# November 9, 2026: Finished pocketing and splitting belly pan!

remind me to never pocket gain.

Today I split up the belly pan into sections printable on my a1 mini and pocketed them. Hypothetically, this should reduce the amount of filament used and maintain structure. This was even more annoying than comms, I had to manually create a pattern for the pocketing, and adjust for screw holes for electronics. I think I might be almost done with cadding, and I can work on the electrical and software front of this project!
Note: I also added a slot for the battery, I need to still cad a support plate for the battery, so I guess back to onshape =(
![](https://fabricate.hackclub-assets.com/58bb598e9ea54222bb25f798f186be86810d225456036ce8e99b7a63a8af1016/image-png/image.png)

**Total time spent: 1h 12m**

# November 10, 2026: Designed battery support plate

Today I was very busy, so I did not get to get as much work as I would have liked. I cadded the battery holder, and attached it to the main assembly. Not much to say as cadding it was pretty easy and assembly took no time.
![](https://fabricate.hackclub-assets.com/1d7cac9833d5a861c8c96dd62ca9d4c368989cf79c200a108d5df4f62d86b4ee/image-png/image.png)

**Total time spent: 42m**

# November 11, 2026: Planned wiring, started firmware

Im back with a few large updates!
I made all of the wiring plans in Fritzing, and decided all of my pin connections. Wiring this should hopefully be easier now that I have this.
![](https://fabricate.hackclub-assets.com/f93af830e673c54bef5474cfe47c592b8441896ffd4f0b933b7fef11d02ca443/image-png/image.png)
> i couldn't find motors, so i just used the defaults. also I am adding a Modulino Pixel for ease of "reading" the state of the arduino. I couldn't add it into the diagram since every arduino uno r4 frpz file was a virus :sob:


I also started coding the firmware, I am using platform io since its the goat.
![](https://fabricate.hackclub-assets.com/4c2800973789eed1919bd9bc0d02fe411aa7dcd1d7c5305419bda2e534941f53/image-png/image.png)

**Total time spent: 3h**

# November 11, 2026: Programmed arduino firmware!

I finished the firmware for the arduino(finally)! This took a lot of time, and I hope that it works out first try:
Overview:
RSL - manages arduino modulino pixels for a status light on what the robot is actively doing
GYRO - manages gyro with calibration, reading sensor data, and processing into useable numbers
MOTORS - OOP class which manages motors regulating the speed, l298n control, and initial setup
MAIN - Manages all scripts, brings everything together with communications, gyro based drive(dependant on constants), and manage enabling/disabling robot motors
![](https://fabricate.hackclub-assets.com/7c2687e292b9568d141e9f5374d6a9870bc88bdbd06e9eb4a0b315d06bb44b0a/image-png/image.png)

**Total time spent: 2h 30m**

# November 12, 2026: WIP BOM

Got really busy today so I got a little time to work on my BOM. I sourced everything from myself or aliexpress. I have the aluminum extrusion and the other stuff. I didn't have time to cover the t3 locking nut for the extrusion since I need to check i have some already.
![](https://fabricate.hackclub-assets.com/3e75217464323826572ede3bfe9691e1f09d1af2cc1ffe4a0b15898cd87c0c39/image-png/image.png)

**Total time spent: 4h 12m**

# November 13, 2026: Started PC app

Today I got started with the PC app. This will display telemetry from the robot with details about communications, and robot status. I decided to use PyQt6 for UI since when made sleek, it looks good, I also decided to make the layout of UI look similar to driverstation in FRC. This is only the UI portion of it. I programmed some functionality, but the functionality in question does not make the app work with the robot
![](https://fabricate.hackclub-assets.com/a7c30187c35d6cb3cfc9fa8e5ba01588c6fb0c7623abaa46260b004d4306ade4/image-png/image.png)

**Total time spent: 2h 12m**

# November 14, 2026: The app now works(somewhat)

I got the app working(took way too long due to the rock script for reassigning 192.168.4.1 breaking). Now instructions can be sent from the app to the robot. I also learned how to ssh into the rock so i won't need to dissasemble the robot to access the rock and connect it to the monitor. Next I plan to set up the  controller input so that the rock recieves the correct input(X:Y:Z) and it moves.
![](https://fabricate.hackclub-assets.com/6bfe1b124f11b1d91443214e99b8e31c17245f98d445dfbe0e791cb303be8530/image-png/image.png)

**Total time spent: 1h 30m**

# November 15, 2026: Station is fully working!

I finally finished controller input and relay to the arduino. Here is a screenshot of it in action:
![](https://fabricate.hackclub-assets.com/4c7a6a2adfca0000386874a9dfb207d8172cfd1de4d172c5ff15115f22e77e8a/image-png/image.png)
I did this by using pygame to get input from my controller, and conjugating it into a string that the arduino will know how to process. I added a dropdown and controller refresh for ease of use, especially since my controllers love to disconnect randomly. I plan to start polishing the repo and everything else for submission for funding now.

**Total time spent: 1h 36m**

# November 15, 2026: Updated readme and BOM, ready to submit!

I updated the readme with renders and instructions for setting up and building! I finalized some other stuff too like the BOM, switching to a different motor vendor so I can actually order 4 motors at a more trusted retailer.
![](https://fabricate.hackclub-assets.com/6f376400499c53d75eba27d2c6d305058e813cc2e75ef3ddd4109ec841fd838d/image-png/image.png)
![](https://fabricate.hackclub-assets.com/518056596aa8fe1b19796475267c89477e594ceab2b64449e4ae7f7ed2a8041c/image-png/image.png)
![](https://fabricate.hackclub-assets.com/35366edec0017775bde7600782d04f0c0de8160e1290af437b6fa858c4e38a95/image-png/image.png)

**Total time spent: 3h**
