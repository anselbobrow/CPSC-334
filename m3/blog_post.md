# Synesthesia Box

### Overview

My project was conceived after a long afternoon of brainstorming in the CEID. I went with something reminiscent of the “ViewMaster” children’s toy that allows you to look at a collection of slides (usually some characters from a TV show etc.through these goggles, based on backlighting.

![Figure 1.1: the ViewMaster](Synesthesia%20Box%20ff350a98e9274aa5bd97715582a90696/Untitled.png)

Figure 1.1: the ViewMaster

Similarly, my project has insertable slides that can be swapped out or even built by the user, with different semi-transparent materials that block out varying degrees of light.

![D388367A-44FC-4D94-9E0D-1C519A2388AA_1_201_a.jpeg](Synesthesia%20Box%20ff350a98e9274aa5bd97715582a90696/D388367A-44FC-4D94-9E0D-1C519A2388AA_1_201_a.jpeg)

![87107167-EC6F-44F5-AAC9-775E579E7B99.jpeg](Synesthesia%20Box%20ff350a98e9274aa5bd97715582a90696/87107167-EC6F-44F5-AAC9-775E579E7B99.jpeg)

The user looks through the eyeholes, and should experiment with facing different light sources, inside or outside. On the inside of the box, 5 photoresistors are aligned with the 5 stripes pick up the amount of light filtered through each one independently. 

![8B87B835-620B-4B0D-B082-451237C3728C.jpeg](Synesthesia%20Box%20ff350a98e9274aa5bd97715582a90696/8B87B835-620B-4B0D-B082-451237C3728C.jpeg)

The ESP-32 sends this information as OSC messages over UDP to the Pi, which is out of sight somewhere on the network running a supercollider server that sonifies the data. The audio is sent back over bluetooth to the user’s headphones, which play a unique textural piece generated from the combination of slide and light source.

### Enclosure

![IMG_7938.jpeg](Synesthesia%20Box%20ff350a98e9274aa5bd97715582a90696/IMG_7938.jpeg)

The enclosure is primarily constructed from cardboard found at the CEID and the Hopper recycling bins. I carefully measured out the dimensions that would be required to fit the mcu/battery and photoresistor array, and provide enough vertical viewing angle to be immersive. I then proceeded to wrongly cut the only piece of ¼ ply cardboard available to me—so I ended up winging it a bit. The overall design remains the same, if slightly less immersive.

The design of leaving a slot at the back to fit the slides in hindsight is weakness in the design. If making a sturdier prototype I would consider alternate attachment options such as elastic wrapped around the top and bottom of the slide, or tiny embedded magnets or velcro. The slot design could be more durable with laser cut wood and smaller slots on the top and bottom in the back of the box that are less snap-offable.

![63FE7252-37EA-41B8-B6A8-8A656BFAE761_1_201_a.jpeg](Synesthesia%20Box%20ff350a98e9274aa5bd97715582a90696/63FE7252-37EA-41B8-B6A8-8A656BFAE761_1_201_a.jpeg)

### Code & Electronics

![62CE4624-3CA2-45BA-91C8-913AD21BBCE8_1_201_a.jpeg](Synesthesia%20Box%20ff350a98e9274aa5bd97715582a90696/62CE4624-3CA2-45BA-91C8-913AD21BBCE8_1_201_a.jpeg)

The networking code from the last lab (broadcasting photoresistor info over wifi) served as a starting point. I modified it to use OSC messages instead of simple strings, using the library here: ‣ The library had to be installed as a zip file, it wasRt searchable in the Arduino IDE Library Manager. OSC worked pretty easily and successfully, notably the UDP port in the broadcasting script should be the one supercollider expects incoming OSC messages on: 57120. The IP address is the raspberry pi in the final code. For testing and writing the Supercollider script I used my laptop. 

I built supercollider on the Pi following the instructions here: [https://github.com/supercollider/supercollider/blob/develop/README_RASPBERRY_PI.md](https://github.com/supercollider/supercollider/blob/develop/README_RASPBERRY_PI.md). I also set up a VNC connection with the Pi to be able to use the Supercollider IDE easily without needing a monitor. The resources that helped me do that were: [https://help.realvnc.com/hc/en-us/articles/360002249917-VNC-Connect-and-Raspberry-Pi#establishing-a-cloud-connection-0-3](https://help.realvnc.com/hc/en-us/articles/360002249917-VNC-Connect-and-Raspberry-Pi#establishing-a-cloud-connection-0-3) (establishing a direct connection), and this forum post which helped make the connection usable at 1980x1080 and much less lag: [https://forums.raspberrypi.com/viewtopic.php?p=1983061&sid=eaf6504ffd4e15374cbd86907d954c67#p1983061](https://forums.raspberrypi.com/viewtopic.php?p=1983061&sid=eaf6504ffd4e15374cbd86907d954c67#p1983061).

I could have also chosen to use headless `sclang` evaluation of a source code file on the Pi, written on my laptop—I think this is probably a more reasonable approach, but there were a lot of issues getting audio working on the Pi through SC and it was nice to have a GUI at points to troubleshoot.

The GitHub page above that tells how to install Supercollider on the Pi also has a section on running code at startup using Crontab.

The ESP is battery powered on a single 3.7 volt rechargeable battery found in AKW123. I use a LD111733v from the CEID to regulate voltage wired to the 3.3v input on the  ESP, which is sufficient to power the device and the photoresistors all off of a single battery. I have a slight issue with the photoresistors, one is unresponsive entirely and another seems to have a different resistance than the other 3 in the array or something, it’s values are significantly off, which unfortunately takes the project to 3.5/5 capacity until I am able to find more working photoresistors.

### Expansion Options

Besides building a better, laser cut enclosure, and designing more slides, I think it’d be interesting to have a different Supercollider file triggered by each slide, so that each has a definable sonic characteristic associated with it. It would be cool to have a sensor detect which slide was inserted automatically and use the corresponding sound generation file. Also, using color sensors as well as light sensor since the slides are all colorful so far would add more complexity and variation to the possibilities for sound generation.

### Video Demonstration

TODO