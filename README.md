# README

To run this project, you need to install the latest version of the following packages:

`numpy`

`imageio`

`cryptography`

`matplotlib`


# How to run it ?

To execute the examples without encryption, run the following command:

`python tpLSB.py examples noencryption <pathToImage>`<br/>
where `<pathToImage>` is the path to an image file.

To execute the examples with encryption, run the following command:

`python tpLSB.py examples encryption <pathToImage>`<br/>
where `<pathToImage>` is the path to an image file.

To create ROC curves, according to three different steganographic rates, run the following command:

`python tpLSB.py curves`

To clear directories where files could have been added, run the following command

`python tpLSB.py clear`

