# 🔄 Safe Looping - Gizathon Project

> 🏗️ `Work In Progress` : This repo is being actively developed and does not represent final quality of the model.

> 📊 For statical and math analysis deep dive on our model, please visit our paper release: 


####   

##  🗂️ Table of Contents

- [Leverage & Liquidations: The Defi Dance Off](#leverage--liquidations-the-defi-dance-off)
    - [Context](#context)
    - [The Problem](#features)
    - [Why Is This Problem Worth Solving?](#why-is-this-problem-worth-solvin)
- [Our Proposal: Smarter & Safer Looping](#🌟-our-proposal-smarter--safer-looping)
    - [Model Archithecture](#model-architecture)
    - [Why Giza?](#why-giza)
    - [Modules Description](#modules-description)
        - [datasets.py](#1-datasetspy)
        - [datacombination.py](#2-data_combinationpy)
        - [looping_descriptivemodel.py](#3-looping_descriptivemodelpy)
- [Prerequisites](#prerequisites)
    - [Install Dependencies](#Install-dependencies)
- [Tool Usage](#usage)
  - [Examples](#command-examples)
- [License](#license)
- [Contact](#contact)
- [FAQs / Troubleshooting](#faqs--troubleshooting)
- [Versioning and Changelog](#versioning-and-changelog)

<br>

## 📝 **Leverage & Liquidations: The DeFi Dance-Off**

DeFi investors are often tempted by the high returns of leveraging their positions by using looping strategies but are equally exposed to the threat of liquidations in a downturn market. 

This portrays the constant interplay between leveraging for higher gains and the threat of liquidation. In a dance-off, participants try to outperform each other with their moves. Similarly, investors are trying to outmaneuver the market by leveraging their positions for profit while avoiding the 'missteps' that lead to liquidation.

<br>

> ***🧠 The challenge lies in mastering these strategies to maximize gains while safeguarding against the volatile dips of the market.***

<br>

And this delicate balance is at the heart of the issues we are tackling.

SafeLooping's mission is to assist Defi investors in the path to sustainable investment by **calculating the optimal looping lever (leverage rate) for an expected weekly price variation**, by ensuring that profits don't come at the cost of security through an **expected return model that penalizes liquidation risk by leverage rate**.

<br>

## **📊 Context**

In the volatile world of DeFi, investors chase high returns, often embracing excessive risks. 


> 💡 A promising yet complex strategy that has emerged within this context is the use of "looping strategies." These strategies involve **reinvesting borrowed assets back into lending platforms to create a leverage loop**, amplifying the potential returns on the initial capital.


Amidst rising bullish sentiment, over-optimism leads to over-leverage, setting the stage for familiar pitfalls.

> “The volume of loans liquidated on Ethereum lending markets **has hit its highest monthly value since June 2022** (Terra crash)**, despite April not even being half over.”** - *[The Block Data](https://www.theblock.co/post/288212/aprils-first-two-weeks-saw-more-ethereum-loans-liquidated-than-any-month-since-june-2022)*
> 
**Lending markets**, crucial in this leverage play, facilitate strategies that magnify returns through **deposit and borrow _"loops"_**.

 However, the allure of these looping strategies comes with heightened risks of liquidation.

## ❓ Problem

The central problem this model aim to address is:

> ***What is the optimal looping strategy that maximizes expected returns while mitigating the risk of liquidation?***

And this problem has mainly two rationales:

1. **Maximizing Returns:**
    - The efficient use of looping strategies can significantly increase the gains of DeFi participants. 
2. **Minimizing Liquidation Risk:**
    - Pursuing higher returns inherently involves greater risks, particularly in a market known for its volatility where collateral values can plummet rapidly. 
    
 The critical element is **identifying the optimal number of loops to achieve maximum yield if price prediction over a period is bullish, without getting liquidated** by market volatility while position is opened.

## 🤔 **Why Is This Problem Worth Solving?**

Addressing this problem is important for several reasons:

- **Democratizing Access to Advanced DeFi Strategies & Leverage Risk**
    - By simplifying and automating the execution of analysis for looping strategies, this model aims to ***make advanced yield optimization techniques accessible to a broader audience***, not just to sophisticated or institutional investors with the resources and expertise to navigate these complexities with complex quant models.
    - By showcasing liquidation ocurrence probability, ***we aim to educate people to take more responsible financial decisions***. 
    
    <br>

- **Fostering Innovation in Financial Engineering:**
    - The development of a looping strategy optimization model represents a leap forward in financial engineering within the blockchain space. **It showcases the potential for innovative algorithms and mathematical models to solve complex financial challenges**, using blockchain available data in investors favor.

<br>

## 🌟 **Our Proposal: Smarter & Safer Looping**

 ![Static Badge](https://img.shields.io/badge/Safe_Looping_v1%20-%20black?style=for-the-badge&label=Gizathon)     

### Model Architecture

![SafeLoopingArchitecture](images/SafeLooping-Architecture _Overview.png)

### Giza Implementation

- **Giza Datasets** 
    - [Tokens Daily Information](https://datasets.gizatech.xyz/hub/aggregated-datasets/tokens-daily-information)
    - [AAVE Daily Deposits & Borrows](https://datasets.gizatech.xyz/hub/aave/daily-deposits-and-borrows-v3)
    - [AAVE Daily Exchange Rates & Indexes](https://datasets.gizatech.xyz/hub/aave/daily-exchange-rates-and-indexes-v3)

- **Inference Endpoint Deployment**
- **AI Actions**
- **zk-Proof Generation**
- **Giza Agent _(coming soon)_***

## Why Giza?

#### ***1. Accessible, Quality-Assured Datasets***
Giza Datasets open the door to an enriched pool of structured and curated blockchain data, vital for any linear regression. By providing open-sourced datasets, Giza addresses one of the critical challenges in blockchain analytics: the availability of high-quality data and keeping that data updated

#### ***2. Computational Efficiency in Asymmetric Environments***
 The GIZA platform provides an environment where the asymmetry in computational efficiency is pronounced — for instance, between blockchain computations and off-chain computations.

#### ***3. Cost & Development Effectiveness***
 Giza provides the structure and support for the execution of verifiable machine learning models. Computational tasks like proof generation are typically more resource-intensive than inference or proof verification. GIZA offers the infrastructure to perform these intensive tasks more efficiently, without the need to develop them ourselves.

### Modules Description

### 1. `datasets.py`

This module is responsible for loading all datasets downloaded from Giza.

#### Key Components:
- **Data Import:** Load multiple datasets into the Python environment.
- **Preprocessing:** Initial data cleaning and formatting.

### 2. `data_combination.py`

This script combines and preprocesses the loaded datasets to prepare them for analysis.

#### Key Components:
- **Data Merging:** Merge multiple datasets using specific filtering criteria.
- **Column Renaming and Sorting:** Rename and reorder dataset columns for uniformity and ease of analysis.
- **Calculation of Statistics:** Compute means, minimums, maximums, and moving averages for various financial metrics such as prices, volumes, deposits, borrows, and rates.
- **Date Filtering:** Focus on the dataset from January 27, 2023, to January 23, 2024, to match the availability of rate data for Aave. _This is a restriciont  that we made to match our model to giza datasets, as more data became available this restriction will not apply, making our model more robust._

### 3. `looping_descriptivemodel.py`

This module includes several components that analyze the risk of liquidation based on different looping levels with cryptocurrencies.

#### Key Components:
1. **Looping Matrix:** Calculate the initial amounts of ETH and USDC based on the loop level.
2. **Liquidation 7 Day Check:** Monitor the collateral health over a 7-day period for various loop levels to identify potential risks.
3. **Liquidation Occurrence Matrix:** Map the frequency of liquidations starting from a specific day for each loop level.
4. **Liquidation Probability by Loop Level:** Estimate the percentage probability of liquidation for each loop level.

### 4. `main_model.py`

This script is central to our predictive analytics, encompassing several models designed to forecast financial metrics and optimize investment strategies based on data processed by previous modules. The functionalities are outlined below:

#### **1. 7-Day Price Variation Predictive Model**

This component utilizes a linear regression model to predict weekly price variations of cryptocurrencies. The model is trained on historical data to identify trends and forecast future price movements.

#### Key Processes:
- **Model Training:** Train a linear regression model on historical price data to predict 7-day price variations.
- **Data Analysis:** Analyze price trends to improve the accuracy of predictions.

#### **2. Predictive Model Deployment to GIZA & Endpoint Creation**

After training, the 7-Day Price Variation Predictive Model is prepared for deployment in a production environment.

#### Key Steps:
1. **ONNX Conversion:** Convert the trained linear regression model to the Open Neural Network Exchange (ONNX) format for interoperability.
2. **Transpilation to Orion Cairo:** Transpile the ONNX model into Orion Cairo, suitable for deployment on Giza's decentralized infrastructure.
3. **Endpoint Deployment:** Deploy an inference endpoint to facilitate real-time predictions.

#### Outcome:
- The deployment culminates in a zkML Weekly Price Variation Linear Regression Endpoint, enabling secure and scalable predictions.

#### **3. Expected Return Model**

This predictive model aims to optimize financial returns by calculating the optimal looping level based on the weekly expected return, influenced by predicted weekly price variations.

#### Inputs:
- **Looping Descriptive Model Output:** Utilizes output from `looping_descriptive_model.py`, providing data on different looping levels and their historical performance.
- **7-Day Price Variation Prediction:** Integrates forecasts from the 7-Day Price Variation Predictive Model to adjust return expectations based on predicted market movements.

#### Functionality:
- **Return Optimization:** Analyzes combined data to identify the looping level that maximizes expected returns based on predicted price variations.


## Installation

To set up the project environment, follow these steps:
1. Clone the repository: `git clone [repository-url]`
2. Install required Python packages: `pip install -r requirements.txt`

## Usage

To run the scripts, navigate to the project directory and execute:
```bash
python datasets.py
python data_combination.py
python looping_descriptivemodel.py
<br>

## 🔍 **Prerequisites**

Before installing the tool, you need to ensure that you have `pnpm` installed, as it is required to manage the project's dependencies.

<br>

### **Install dependencies**

## Project Dependencies

- [**pandas**](https://pandas.pydata.org/)
- [**numpy**](https://numpy.org/)
- [**certifi**](https://pypi.org/project/certifi/)
- [**polars**](https://github.com/pola-rs/polars)
- [**matplotlib**](https://matplotlib.org/)
- [**seaborn**](https://seaborn.pydata.org/)
- [**giza_datasets**](https://gizatech.xyz/)
- [**sklearn (scikit-learn)**](https://scikit-learn.org/stable/)
- [**skl2onnx**](https://github.com/onnx/sklearn-onnx)
- [**giza_actions**](https://gizatech.xyz/)

<br>

## 🛠️ **Usage**

<br>

### **Run the Tool**

<br>

## 🧪 Testing

This command will execute all automated tests associated with the tool, verifying that all components operate as expected.

## 📄 **License**

[Placeholder] This project is licensed under the MIT License. For more details, see the LICENSE file in the repository.

## 📬 **Contact**

[Placeholder]
For support, inquiries, or contributions, please contact us at [Check Contact]. You can also raise an issue directly in the GitHub repository for any bugs or feature requests.

<br>

## ❓ **FAQs / Troubleshooting**

[Placeholder]

<br>

<details> 
    <summary> 
      Question 1
    </summary>
Question 1 Info
</details>
<br>
<details> 
    <summary> 
      Question 2
    </summary>
Question 2 Info
</details>
<br>

## 📌 **Versioning and Changelog**
[Placeholder]

We adhere to Semantic Versioning (SemVer) for this project. The changelog is regularly updated and can be found in the CHANGELOG.md file. Each release also includes detailed notes on the additions, changes, and fixes made to the software.

To view the versions available, visit the Releases section of our GitHub repository.

<br>
                                                                          






giza transpile linear_regression.onnx --output-path verifiable_lr
giza endpoints deploy --model-id 517 --version-id 2
https://endpoint-rodriguezmatid-517-2-e5a2ea0d-7i3yxzspbq-ew.a.run.app
giza workspaces get
python3 verifiable_inference
giza endpoints get-proof --endpoint-id 156 --proof-id b229901247874c7eb856fab2f48e9f0e
giza endpoints download-proof --endpoint-id 156 --proof-id b229901247874c7eb856fab2f48e9f0e

Model id 517, id version 2, endpoint id 156