<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/thornydre/superpipe">
    <img src="assets/img/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Superpipe</h3>

  <p align="center">
    CG project pipeline toolset
    <br />
    <a href="https://github.com/thornydre/superpipe"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/thornydre/superpipe">View Demo</a>
    ·
    <a href="https://github.com/thornydre/superpipe/issues">Report Bug</a>
    ·
    <a href="https://github.com/thornydre/superpipe/pulls">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#scripts-installation">Scripts Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Superpipe is CG project pipeline toolset. It allows creation of a folder hierarchy from pre-production (character design, colorscript, storyboard...) to post-production (compositing, editing...), and managing a project during the production through ah easy to use user interface.


### Built With

The project is built with python 3.10 and PySide6:
* [Python](https://python.org/)
* [PySide6](https://python.org/)

Additional Libraries:
* [NumPy](https://numpy.org/)
* [OpenCV](https://opencv.org/)
* [Pillow](https://python-pillow.org/)
* [Watchdog](https://github.com/gorakhargosh/watchdog)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

You can <a href="https://github.com/thornydre/superpipe/releases">install Superpipe via the Releases page</a>.
Then you can start by clicking `superpipe.exe` and create a new project via the `File` drop down menu : `File > New Project`.


### Scripts Installation
Add shelfs to your software by copying
#### Maya:
`scripts/maya_scripts/shelf_Superpipe.mel` to `Documents/maya/20**/prefs/shelves/`
#### Houdini:
`scripts/houdini_scripts/superpipe_shelf.shelf` to `Documents/houdini**.**/toolbar/`
#### Blender:
You can add the Superpipe add-on for Blender by going into `File > User Preferences > Add-ons` and click on `Install Add-on from file` and pick `scripts/blender_scripts/superpipe_addon.py`.

The ".ma" files in the "src" folder can be modified if you want a different default files as you create a new asset or shot in Superpipe.

<!--
### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/thornydre/superpipe.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```
-->

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

COMING

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] From TKinter to PySide
- [ ] Statistics view
- [ ] Cutomize project hierarchy

See the [open issues](https://github.com/thornydre/superpipe/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

<!--
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
-->

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Lucas BOUTROT - [linkedin@lboutrot](https://linkedin.com/in/lboutrot) - lucas.boutrot@gmail.com

Project Link: [https://github.com/thornydre/superpipe](https://github.com/thornydre/superpipe)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
<!--
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#top">back to top</a>)</p>
-->


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/thornydre/superpipe.svg?style=for-the-badge
[contributors-url]: https://github.com/thornydre/superpipe/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/thornydre/superpipe.svg?style=for-the-badge
[forks-url]: https://github.com/thornydre/superpipe/network/members
[stars-shield]: https://img.shields.io/github/stars/thornydre/superpipe.svg?style=for-the-badge
[stars-url]: https://github.com/thornydre/superpipe/stargazers
[issues-shield]: https://img.shields.io/github/issues/thornydre/superpipe.svg?style=for-the-badge
[issues-url]: https://github.com/thornydre/superpipe/issues
[license-shield]: https://img.shields.io/github/license/thornydre/superpipe.svg?style=for-the-badge
[license-url]: https://github.com/thornydre/superpipe/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/lboutrot
