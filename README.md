# Drawing2Waveform
Input in image of a scribble, and it will output a single-cycle wav file for a synthesizer.

To use:
1. Make a drawing of a waveform (should be like a function, with only 1 y value per x value, otherwise you will have jumps. Somethimes fun to play with, just important to know. Here's an example:
![Example Image](/Inputphotos/PhonePhoto9.jpg)

2. Take a picture of that waveform in decent enough light and focus, and with as little background or competeing curves as possible.
3. Put the image into the Inputphotos folder.
4. Open Pic2Wav.pyG and go down to the bottom where the main function is run. 
5. Replace input_filename with the name of the image you put into the Inputphotos folder, including the extension.
6. Replace ouput_filename with your desired output name, without extension, as it will always be .wav.
7. Run the script
8. Find the output file in the OutputWavs folder, and plug it into your favorite synthesizer.
9. Jam with your newly drawn sound!

Note: You won't hear anything when playing this in a media player, as this generates only a single cycle waveform, and is therefore very, very short.
