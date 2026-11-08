---
title: "Omni DIrectional Drivebase"
github: ""
description: "Omni directional drivebase powered by 4 motors and mecanum wheels. Goal is to make this a hub for any future projects I might make, such as a robotic arm, which I can attach to the drivebase and leverage its wireless communication I developed a few months ago."
created_at: "2026-11-04"
total_time: "6h 36m"
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
