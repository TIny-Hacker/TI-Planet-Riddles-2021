## Stuff for the TI-Planet "Riddle of the 3 Doors" contest during December 2021.

I'm mostly using this to document changes easily, and also to make my own comments so that I know what is going on in the code.

Look in the descriptions of each commit for more information and sometimes the clue of that day from TI-Planet. 

I attempted to read some of the QR Codes by hand using some tutorials I found on line along with information from wikipedia. Because the QR Code wasn't complete yet, it was the only way for me to extract the useful information it might contain. However, I only recieved a dead link and the stuff got really weird towards the end.

To decode the QR Code, you need to figure out the encoding, mask, and length. After you know that you can XOR the QR Code data area with the mask pattern, and then convert each section of bits into ASCII (Use your encoding type to figure this out). I left most of the stuff I used in the repo.

After attempting to do this by hand, I decided to use a website with more specific tools for it: https://merricx.github.io/qrazybox/

This will not work on PC/Mac because the dependencies are calculator-specific. It's probably possible to port but I'm too busy/lazy.
