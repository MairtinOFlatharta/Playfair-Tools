<div id="top"></div>
<h3 align="center">Playfair Encryption, Decryption, and Frequency Analysis</h3>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <ul>
      <a href="#about-the-repo">About The Repo</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </ul>
  </ol>
</details>

<!-- ABOUT THE REPO -->
## About The Repo
This repo contains 2 Python scripts. [playfair_tool.py](./playfair_tool.py) is used
to both encrypt and decrypt messages using the [Playfair cipher](https://en.wikipedia.org/wiki/Playfair_cipher).
[analyse_pair_freq.py](./analyse_pair_freq.py) is used to analyse the frequency
of letter pairs in a given text file. These frequencies can then be used to assist
in cracking an encrypted message without knowing the key.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- BUILT WITH -->
### Built With
These are the requirements for using these scripts:
* [Python 3](https://www.python.org/downloads/)
* [matplotlib](https://matplotlib.org/)
* [numpy](https://numpy.org/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE -->
### Usage
To use the [playfair_tool.py](./playfair_tool.py) script, it can be invoked
directly in the command line by entering the directory of the script and running:
```./playfair_tool.py```

Alternatively, it can be invoked directly using ```python playfair_tool.py```
or ```python3 playfair_tool.py```.

To use the [analyse_pair_freq.py](./analyse_pair_freq.py) script, install the numpy
and matplotlib libraries. A text file must also be provided (-f option) when running this script,
either in English or in German (or other languages that don't use special characters).

An example of running would be:
```./analyse_pair_freq.py -f sample.txt```

<p align="right">(<a href="#top">back to top</a>)</p>
