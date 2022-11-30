# Automated product categorization for e-commerce
**Industries**: e-commerce, delivery apps, marketplaces, many others

**Difficulty level**: ⭐⭐⭐⭐ (4/5)

Creating relevant tags and categories on products allow e-commerce companies (such as Amazon, Wayfair, eBay in the US, Mercado Libre, Dafiti in Latam, or ASOS.com and Zalando in Europe), and super apps and marketplaces (such as Instacart in the US, Rappi, Frubana, JOKR in Latam) to automatically categorize products whether those are new products uploaded by a user or seller products that need large-scale automated categorization. Automation on this subject not only saves time and manual effort but creates a taxonomy system that improves the process of a customer finding what they are looking for, improving their conversion metrics, and activating frictionless and engaging shopping experiences. In this project you will apply natural language processing to create a multi-label system able to classify e-commerce products automatically

## Overview
In a nutshell, this project will result in an API service that is backed by an NLP model that will classify the textual elements of a product record (description, summary etc). The individual components for this project are very similar to what you have implemented in the last three Projects. You can reuse as much code as you want to leave yourself more time for working on the core dataset and model training.

### Deliverables 
**Goal:** The main objective of this project is to build a system/service that will accept a typical "new product"  to classify the product into a set of predefined categories.

In order to graduate from the ML Developer Career, you have to approve the Main Deliverables. You are also welcome to complete the Optional Deliverables if you want to continue to add experience and build your portfolio, although those are not mandatory. 

**Main Deliverables:**

1. Exploratory Dataset Analysis (EDA) Jupyter notebooks and dataset
2. Scripts used for data pre-processing and data preparation
3. Training scripts and trained models. Description of how to reproduce results
4. Implementation and training of the NLP model for product classification
5. API with a basic UI interface for demo (upload of textual description and return of predictions)
6. Everything must be containerized using Docker and deployable into AWS

**Optional Objectives:**

Retraining of model with new data added by users.

**Approach and Milestones**
There are many ways to approach this project and at first sight, this might seem very overwhelming. A good rule of thumb is this:

Get a good overview and idea of what you need to build.
Identify the unknowns and, most importantly, the major risks for the project and allocate time appropriately. For instance: setting up a dockerized API is simple and low risk but dealing with a dirty dataset is a high-risk task. 
Some tasks will take a long time and might be a blocker for other tasks. Try anticipating the unknowns and allocate time as necessary.

A possible approach is this milestone/project plan:

![image](https://user-images.githubusercontent.com/103912003/204822920-2682ec6c-3f9d-4749-a9a9-566fd07def0d.png)
![image](https://user-images.githubusercontent.com/103912003/204823154-bd86b369-6e16-4b30-97b5-f92af45ec4a6.png)

