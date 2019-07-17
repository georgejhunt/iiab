### Start a Video Campaign
* My first video effort had a nummber of failings:
   1. It was not scripted, was too long, and planned on the fly.
   2. There was no written correlated material.
   3. No plan or strategy existed for making the material available in other languages.
   4. It relied on specialized hardware (my Macbook), which did not permit others who didn't have a Macbook to gain from my experience.
* Are there folks on the XSCE mailing list who might be enticed do research and create "howto videos" for capabilities that we already have in IIAB?
* Could we develop a curated selection of "howto Videos" to facilitate expanded use of current offerings?
#### New Strategy
1. Find a suite of software and hardware which makes video generation as easy on the RPI as it is on the MAC.
2. Create a video showing how to create videos.
3. Develop a system similar to gettext for internationalization of these "How-to Videos".
4. Make a list of needed "How-tos".


#### Videos Needed
1. Set up and debug sound on the rpi.
2. A first recording.
2. Video editing suggested standards.
3. Use wordpress as story board, and input to gettext
4. Set up gettext work flow, and document via video.
5. Find video editor which will let native speakers redub videos created in english.

#### How to Join in 
(everything including rpi for under $100 -- if you already have monitor/keyboard)
1. In addition to the rpi (and a hefty 3A power supply -- weak PS will cause unreliabity):
   1. Pull the current project
   ```
      git remote add ghunt http://github.com/georgejhunt/iiab
      git checkout -b video ghunt/video
      ./runrole video
      ## the video project is evolving, later you may need to:
      git checkout video
      git pull ghunt video
      ./runrole video (to get the latest stuff
   ```
   2. Purchase USB audio -- required but not available on the RPI motherboard
      1. I had an extra iphone ear bud with mic -- so I just purchased a $15 USB sound dongle - https://www.amazon.com/gp/product/B06XP5R449 -- and I'm very please with the comfort and sound quality.
      2. I'm also impressed with the price/comments about headset/USB dongle combination for $25 - https://www.amazon.com/Vtin-Microphone-Headphone-Cancelling-Hands-Free/dp/B075ZMFBW8
      
