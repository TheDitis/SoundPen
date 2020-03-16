# Drawing2Waveform
Input an image of a scribble, and get back a single-cycle wav file for a synthesizer.

<br/><br/>
## To use:
1. Make a drawing of a waveform (should be like a function, with only 1 y value per x value, otherwise you will have jumps. Somethimes fun to play with, just important to know.) 
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
