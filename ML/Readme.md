# Machine Learning

### Additional Materials
1️⃣ [Neural Network Fundamentals](https://github.com/Glareone/AI-LLM-RAG-best-practices/blob/main/ML/Neural%20Network%20Fundamentals.md)  
2️⃣ [CNN Advanced Concepts](https://github.com/Glareone/AI-LLM-RAG-best-practices/blob/main/ML/CNN%20Advanced%20Concepts.md) (IN PROGRESS)   
3️⃣ [Advanced Training Techniques](https://github.com/Glareone/AI-LLM-RAG-best-practices/edit/main/ML/Readme.md) (IN PROGRESS)    

## Data Centric Approach
<img width="704" alt="image" src="https://github.com/user-attachments/assets/cd26f12a-dc14-4896-ba30-1025c3b19890" />

### Basics & Guide
It is not exaggerating to say that the data dictates how the machine learning model is built. In the following graph, we illustrate a typical workflow involved in a project of machine learning.

Starting from the data, we first determine which type of machine learning problems we would like to solve, i.e. supervised vs. unsupervised.  
We say that the data is labeled, if one of the attributes in the data is the desired one, i.e. the target attribute.  
For instance, in the task of telling whether there is a cat on a photo, the target attribute of the data could be a boolean value [Yes|No].  
If this target attribute exists, then we say the data is labeled, and it is a supervised learning problem. 

For the supervised machine learning algorithms, we further determine the type of the generated model: **classification** or **regression**, based on the expected output of the model, i.e. discrete value for classification model and continuous value for the regression model.  
Once we determine on the type of model that we would like to build out of the data, we then go ahead to perform the feature engineering, which is a group of activities that transform the data into the desired format.  


#### Examples:
1. For almost all cases, we split the data into two groups: training and testing. The training dataset is used during the process to train a model, while the testing dataset is then used to test or validate whether the model we build is generic enough that can be applied to the unseen data. 
2. The raw dataset is often incomplete with missing values. Therefore, one might need to fill those missing values with various strategies such as filling with the average value. 
3. The dataset often contains categorical attributes, such as country, gender etc. And it is often the case that one needs to encode those categorical string values into numerical one, due to the constraints of algorithm. For example, the Linear Regression algorithm can only deal with vectors of real values as input. 

### Underlifting vs Overlifting
<img width="622" alt="image" src="https://github.com/user-attachments/assets/bf45e84d-00ac-43f1-bc2b-46b8614628ab" />

* For supervised learning algorithms, e.g. **classification** and **regression**, there are two common cases where the generated model does not fit well the data: underfitting and overfitting. 
* An important measurement for supervised learning algorithms, is the generalization, which measures how well that a model derived from the training data can predict the desired attribute of the unseen data. When we say a model is underfitting or overfitting, it implies that the model does not generalized well to the unseen data. 

#### Underlifting
An underfitting model is the one that does not fit well with the training data, i.e. significantly deviated from the ground truth.  
One of the causes of underfitting could be that the model is over-simplified for the data, therefore it is not capable to capture the hidden relationship within the data.  

#### Overlifting
An overfitting model is the one that fits well with the training data, i.e. little or no error, however it does not generalized well to the unseen data.  
Contrary to the case of underfitting, an over-complicated model that is able to fit every bit of the data, would fall into the traps of noises and errors. As one can see from the above graph No. (3), the model managed to have less misclassification in the training data, yet it is more likely that it would stumble on the unseen data.

