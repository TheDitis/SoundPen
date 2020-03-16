# Drawing2Waveform
Input an image of a scribble, and get back a single-cycle wav file for a synthesizer.

<br/><br/>
## To use:
1. Make a drawing of a waveform (should be like a function, with only 1 y value per x value, otherwise you will have jumps. Somethimes fun to play with, just important to know. See image at bottome for clarification.) 
2. Take a picture of that waveform in decent enough light and focus, and with as little background or competeing curvature as possible Here's an example:

![Example Image](/Inputphotos/PhonePhoto5.jpg)

3. Put the image into the **Inputphotos** folder.
4. Open **Pic2Wav.py** and go down to the bottom where the main function is run. 
5. Replace *input_filename* with the name of the image you put into the Inputphotos folder, including the extension.
6. Replace *ouput_filename* with your desired output name, **without extension**, as it will always be .wav.
7. Run the script
8. Find the output file in the OutputWavs folder, and plug it into your favorite synthesizer.
9. Jam with your newly drawn sound!

### Note: You won't hear anything when playing this in a media player, as this generates only a single cycle waveform, and is therefore very, very short.

<br/><br/>
## Checking & Debugging
The fastest way to check if things went as expected is to check the **DebugImages** folder. For each run, 2 image files are automatically generated. The first in the chain is **ThresholdTest.png** and the second is **ContourCheck.png**, which will very quickly tell you whether or not your sound will be easily playable. Here's what *ContourCheck.png* should look like on a successful run:

![Example Image](/DebugImages/ContourCheck.png)

Here is what *ThresholdTest.png* should roughly look like on a good run:

![Example Image](/DebugImages/ThresholdTest.png)
Don't worry if your threshold looks a bit more messy, as long as *ContourCheck.png* looks good, it should play just fine.

<br/><br/>
## Top-Down Model
The way the algorithm currently works once it has identified the largest curve in the image, is to take the uppermost pixel that is part of the curve for every column of pixels. This, of course, means that any sort of concave or non-function-like curves will result in square-wave like jumps. Here is an example of what that looks like:

![Example Image](/doc_resources/TopDownDemo.png)

<br/><br/>
## Other Things To Know
Along with understanding that any overhangs will cause jumps, it helps to know how sharp jumps can be avoided in the looping in your synthesizer.

- The algorithm takes the average of the last couple of samples, and averages that with the average of the first couple of samples, and then shifts the waveform values vertically so that the two ends straddle the center line as closely as possible

- This means that, if both of your end-points are either low or high compared to the majority of the rest of the drawing, you will get a sort of lopsided waveform, which isn't necessarily a bad thing, just know that the volume won't be as loud.

- It also means that if the endpoints of your audio file are on opposite ends vertically, than you will get more of a squarewave-like character when you play it through a synthesizer, unless your synthesizer has a crossfade parameter.

- Even when you start and end your waveform nicely on the center line, there will likely still be small jumps on cycling, due to anything from the angle of the photo to the bleed of the marker, so it is recommended to use a synthesizer that does have crossfade parameter.

- Once the wave has been centered using the front and end points, it automatically scales the amplitude to maximize volume, so you don't need to be concerned with how tall or short your drawing is. It can be very interesting to play with making as squished of a waveform you can, and seeing what it sounds like when the tiny bumps are amplified.
<br/>
![Example Image](/doc_resources/WaveformDrawDemo.png)

