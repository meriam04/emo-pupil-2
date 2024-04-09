<a name="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/meriam04/emotion-watchers">
    <img src="images/transparent_logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Emotion Watchers</h3>

  <p align="center">
    An emotion classification machine learning model that fuses pupillometry and facial recognition.
    <br />
    <a href="https://github.com/meriam04/emotion-watchers/tree/main/demo/design_fair.ipynb">View Demo</a>
    ·
    <a href="https://github.com/meriam04/emotion-watchers/issues">Report Bug</a>
    ·
    <a href="https://github.com/meriam04/emotion-watchers/issues">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#system-overview">System Overview</a></li>
    <li><a href="#next-steps">Next Steps</a></li>
    <li><a href="#references">References</a></li>
    <!--
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    -->
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!--
![Emotion Watchers Screen Shot][product-screenshot]
-->

This is a research project, meant to examine the effects of fusing facial expressions and pupillometry for emotion detection. Traditionally, facial expressions have been used for emotion detection. They are well researched and able to predict emotions with a high accuracy, but are subject to bias and can be faked. Pupillometry is a subconscious biometric that is also determined by an individual's emotional state. Although pupillometry is less researched and has a lower accuracy, it is not as biased as face detection and cannot be faked. By combining the high accuracy of the face modality with the low bias of the pupillometry modality, it should be possible to create an emotion detection machine learning model that predicts correctly with a high accuracy, has low bias, and cannot be faked.

This project continues the research of EmoPupil, a research project conducted by Bilal Taha under Dr. Dimitrios Hatzinakos at the University of Toronto. EmoPupil studied the use of pupillometry for emotion detection and its result were crucial to the creation of a model that fused pupillometry with facial detection.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- SYSTEM OVERVIEW -->
## System Overview

![System Overview][system-overview]

### Data Collection

An experiment was conducted where participants were shown a series of music videos that each evoked one of the following emotions:
- Anger
- Calm
- Fear
- Fun
- Happy
- Joy
- Sad

Each participants' facial reaction, pupillometry response, and emotion were recorded.

### Data Processing

The face videos were split into series of images. Those images were converted to grayscale and then cropped to only include the face.

The series of pupillometry responses were passed through a series of scripts. The first script removed any outliers from the pupillometry data. The second script converted the discrete data into a continuous function using interpolation.

For more information about our Data Processing read the dedicated <a href="https://github.com/meriam04/emotion-watchers/tree/main/data_processing/README.md">README</a>

### Facial Model

![Face Model][face-model]

The facial model used convolution layers to extract features (e.g. mouth) from the face images. It then used two linear layers to interpret those features and predict an emotion.

### Pupillometry Model

![Pupil Model][pupil-model]

The pupillometry model used LSTM layers to determine if the pupils were expanding/contracting over time, and detect other patterns over time. The convolution layers were used to extract features from the dilation sequences. The linear layer used the output of the LSTM and Convolution layers to make a prediction.

### Fusion Model

The fusion model took the probabilities outputted by the facial and pupillometry model and summed them together. The emotion with the highest total was used as the prediction of the fusion model.

For more information about our Models read the dedicated <a href="https://github.com/meriam04/emotion-watchers/tree/main/models/README.md">README</a>

### Verification

Subsets of each dataset were saved for testing. The testing dataset was also split into one dataset for each participant so that we could see which participants performed better/worse. We also created a confusion matrix from the Fusion Model's prediction so that we could see where the model gets confused.

Example of a Confusion Matrix:
![Confusion Matrix][confusion-matrix]

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- NEXT STEPS -->
## Next Steps

- [ ] Improve the pupillometry model's accuracy
- [ ] Add prompt to rename files if they do not match our naming schema
- [ ] Gather more data

See the [open issues](https://github.com/meriam04/emotion-watchers/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- REFERENCES -->
## References

- [ReadMe Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->

<!--

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

-->

<!-- LICENSE -->

<!--

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

-->

<!-- CONTACT -->

<!--

## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

Project Link: [https://github.com/meriam04/emotion-watchers](https://github.com/meriam04/emotion-watchers)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

-->

<!-- ACKNOWLEDGMENTS -->

<!--

## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>

-->

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[system-overview]: images/system_overview.png
[face-model]: images/face_model.png
[pupil-model]: images/pupil_model.png
[confusion-matrix]: images/confusion_matrix.png
