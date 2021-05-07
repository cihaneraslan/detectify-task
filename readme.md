



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/cihaneraslan/detectify-task">
    <img src="https://detectify.com/site/themes/detectify/img/primary_logo.svg" alt="Logo" width="80" height="80">

  </a>

  <h3 align="center">Report Generator</h3>

  <p align="center">
    Exports high severity findings of a scan to an Excel file
    <br />
  </p>




<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#TargetAudience">Target Audience</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


Extracts high severity findings of the latest scan for each scan profile and reports findings in Excel
* detectify.py : Authentication scheme implementation and API calls
* report-generator.py : Reporting features
### TargetAudience

* []()Internal
* []()System Integrators
* []()Clients



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* Following packages needs to be installed:
`requests`
`xlsxwriter`

  ```sh
  pip3 install -r requirements.txt
  ```
  
* Following environment variables needs to set:
  ```sh
  API_KEY
  ```
  ```sh
  API_SECRET_KEY
  ```



<!-- USAGE EXAMPLES -->
## Usage
* Run the following command on terminal
   ```sh
   python3 report-generator.py
   ```
<!-- OUTPUT -->
## Output
* Findings will be listed on terminal for a quick check
* Following file will be created at the same level as `report-generator.py` after successful run:
   ```sh
   Findings.xlsx
   ```
For completed (verified) analysis;  findings will be listed with the following attributes; `Profile Name`, `Title`, `Score`, `Found At`, `Date`

![report-generator][product-screenshot]

For incomplete analysis; a blank sheet will be generated with the scan profile name 





<!-- CONTACT -->
## Contact

Cihan Eraslan - cihaneraslan@gmail.com

Project Link: [https://github.com/cihaneraslan/detectify-task](https://github.com/cihaneraslan/detectify-task)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: images/SampleOutput.png
