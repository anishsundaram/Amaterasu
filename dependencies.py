import io 
import pandas as pd 
import numpy as np

  # Used for graphics
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

  # Used to split data and get accuracy measures
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

  # Used for cross validation and hyperparameter tuning
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score

  # The three models we used
from sklearn.ensemble import RandomForestRegressor
from sklearn import neighbors
from sklearn.neural_network import MLPRegressor

  # Additional analysis
from sklearn.decomposition import PCA

    # To import test data 
from google.colab import files
