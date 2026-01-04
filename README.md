# KNN Diabetes Prediction Project

---

## Overview and Objectives

This project introduces the fundamentals of the **K-Nearest Neighbors (KNN)** algorithm and applies it to a real-world medical dataset. The goal is to predict the onset of diabetes using the Pima Indians Diabetes dataset and to analyze how different feature combinations and values of **K** affect model performance.

The project is designed as a **learning-oriented exercise**, focused on understanding the algorithm rather than achieving production-level performance.

---

## Brief KNN Explanation

**K-Nearest Neighbors (KNN)** is a simple, non-parametric supervised machine learning algorithm used for classification and regression. It is a *lazy learning* method, meaning it does not train an explicit model. Instead, it stores the training data and makes predictions by comparing new instances to existing ones.

### How KNN Works

1. Compute the distance (usually Euclidean) between a new data point and all training points.
2. Select the **K** closest neighbors.
3. Assign the class that appears most frequently among those neighbors.

### Key Properties

- **Instance-based:** Uses stored training data directly.
- **Non-parametric:** Makes no assumptions about data distribution.
- **Distance-sensitive:** Feature scaling can strongly affect results.
- **Interpretable:** Easy to understand and visualize.

The value of **K** is a crucial hyperparameter:

- Small K → higher variance (overfitting).
- Large K → higher bias (underfitting).

A common heuristic is to start with:

A common heuristic is to start with:

**K ≈ √N**

where *N* is the number of training samples.

---

## Project Implementation Summary

The entire workflow is implemented in a Jupyter Notebook (`notebook.ipynb`) and includes:

- A **custom KNN implementation from scratch** in Python.
- Loading and splitting the dataset into training and test sets.
- Training multiple KNN models using different feature combinations.
- Experimenting with different values of **K**.
- Visualizing training data and predicted labels.
- Evaluating results using classification accuracy.

### Feature Combinations Tested

To enable 2D visualization, the following feature pairs were evaluated:

- **Glucose & BloodPressure**
- **SkinThickness & BMI**
- **Glucose & BMI**

Each combination was trained and evaluated independently.

---

## Dataset Description

The project uses the **Pima Indians Diabetes Dataset**, available on Kaggle. It contains medical data for **768 women** of Pima Indian heritage, aged 21 or older.

Each record includes the following features:

- Pregnancies  
- Glucose  
- BloodPressure  
- SkinThickness  
- Insulin  
- BMI  
- DiabetesPedigreeFunction  
- Age  
- Outcome (target variable: `0` = no diabetes, `1` = diabetes)

The dataset shows moderate class imbalance (~35% positive cases).

For this project, the data is split into:

- `train.csv` – 618 observations
- `test.csv` – 150 observations

No advanced preprocessing is applied, as the focus is on algorithm understanding.

---

## Repository Structure

The repository is organized as follows:

- `notebook.ipynb` – Jupyter Notebook containing the project code, KNN implementation, analysis steps, and visualizations. Running this notebook step-by-step will reproduce the results and plots discussed.
- `train.csv` – Training portion of the Pima Indians Diabetes dataset (used to fit the KNN model).
- `test.csv` – Test portion of the dataset (used to evaluate model performance on unseen data).
- `requirements.txt` – List of required Python packages and their versions to run the notebook (libraries include NumPy, pandas, scikit-learn, Matplotlib, etc.).


---

## Installation and Usage

### Prerequisites

You will need Python 3.x and a few standard data science libraries. It is recommended to use a Python environment (such as venv or Anaconda) before installing the requirements.

### Setup Instructions

1. Clone the repository to your local machine (or download the ZIP and extract it).
2. Install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all necessary packages. If any package installation issues arise due to the specific versions pinned, you can manually install the latest versions of numpy, pandas, scikit-learn, matplotlib, and seaborn which are used in this project.

### Run the Notebook

Launch Jupyter Notebook or Jupyter Lab in the repository directory and open `notebook.ipynb`. Step through the notebook cells to execute the code. This will:

- Define the KNN class and supporting code.
- Load the dataset (ensure `train.csv` and `test.csv` are in the same directory).
- Perform the KNN predictions for each feature combination.
- Display performance results and plots.

No additional command-line interface is provided since the analysis is done within the notebook. Ensure the CSV data files are present in the working directory so the code can read them.

---

## Key Results and Conclusions

Using the KNN algorithm on the diabetes dataset provided a simple baseline for prediction. After testing three different pairs of features, we observed the following test set accuracies for predicting diabetes:

- **Glucose & BloodPressure:** ~71% accuracy (highest of the three combinations)
- **Glucose & BMI:** ~70% accuracy (very close to the above)
- **SkinThickness & BMI:** ~62% accuracy (significantly lower)

These results suggest that blood glucose level is a particularly important predictor for diabetes in this dataset – the two feature pairs involving Glucose performed substantially better than the pair without it. The combination of Glucose and BloodPressure yielded the best result in our experiment.

It is worth noting that using more features (or all available features) could improve accuracy further, but the project focused on a simple comparison of limited feature sets for illustrative purposes.

In general, the KNN algorithm demonstrated moderate success in diagnosing diabetes from just two features. This illustrates both the strengths and limitations of KNN. On one hand, it is intuitive and easy to implement, and it can model non-linear decision boundaries (as seen in the scatter plot visualizations). On the other hand, the accuracy around 70% indicates there is room for improvement, and more sophisticated models or more features might be needed for higher predictive power in a real medical diagnosis scenario. Additionally, KNN’s performance and speed would be impacted if we scaled up to larger datasets or higher dimensions.

---

## Conclusion

KNN provided a useful baseline and educational example. It confirmed that feature choice and parameter tuning (such as selecting the right k) are critical to the algorithm’s performance. While KNN may not always be the optimal algorithm for a given task, understanding how it works is valuable. Its simplicity makes it a good starting point for beginners in machine learning, and it can perform adequately on small-to-medium structured datasets. For the Pima diabetes data, KNN gave a quick way to test predictive relationships between variables and the outcome. More advanced approaches could build on this to create a more accurate diabetes prediction model.

