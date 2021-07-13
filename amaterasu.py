# -*- coding: utf-8 -*-
"""Amaterasu Solar Energy Design Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/anishsundaram/Amaterasu/blob/master/Amaterasu_Solar_Energy_Design_Project.ipynb

## Amateratsu Solar Project Code
"""

# Libraries used throughout the project:

import dependencies.py

"""# 1. Import the dataset into a Pandas Dataframe.

- What are the number of instances/samples in the DataFrame?
> There are 32686 samples in this DataFrame.

- How many missing instances are there in the DataFrame? 
> There are 2 missing instances

- Which features are missing instances?
> Both instances are missing the radiation feature
"""

# Upload SolarEnergyData.csv

uploaded = files.upload()

# Read in the dataset as a pandas dataframe

df = pd.read_csv(io.BytesIO(uploaded['SolarEnergyData.csv'])) 
df.head()

# Drops the NaN (missing) values

print(df.isnull().sum())
df = df.dropna(axis=0)

"""# 2. Feature Engineering
- Convert the 'Date', 'Time', 'TimeSunRise' and 'TimeSunSet' features into 'DayOfYear',
'MonthOfYear', 'TimeOfDay', and 'DayLength'. This will enable examination of how
the solar radiation changes across different timescales.
"""

# Converting select features into more useful time-based features

df['DayOfYear'] = pd.DatetimeIndex(df['Date']).day
df['MonthOfYear'] = pd.DatetimeIndex(df['Date']).month

df['TimeOfDay'] = pd.to_timedelta(df['Time'])
df['TimeOfDay'] = df['TimeOfDay'].dt.total_seconds()

df['DayLength'] = pd.to_datetime(df['TimeSunSet']) - pd.to_datetime(df['TimeSunRise'])
df['DayLength'] = df['DayLength'].dt.total_seconds()

# Gives statistical information about the dataset
df.describe()

plt.scatter(df['UNIXTime'], df['Radiation'])
plt.xlabel('UNIXTime')
plt.ylabel('Radiation')
plt.title('Radiation Over Time')

"""# 3. Investigate correlations between the features. Discuss your findings.
> We found that temperature and radiation have the strongest positive Pearson correlation. The other features have very weak Pearson correlations with radiation. Day length and month of year have a strong negative correlation; however, the correlation between these two features is not important for our analysis since we are only looking at predicting radiation.
"""

# Heatmap of the Pearson Correlation between the features used in our models

cols = ['DayOfYear', 'MonthOfYear', 'TimeOfDay', 'DayLength', 'Radiation', 'Pressure', 'Temperature','Humidity','WindDirection']

df[cols].corr()
hm = sns.heatmap(df[cols].corr(), cbar=True,
                 annot=True,
                 square=True,
                 fmt='.2f',
                 annot_kws={'size': 7},
                 yticklabels=cols,
                 xticklabels=cols)

fig = hm.get_figure()
fig.savefig("heatmap.png")

# Scatter plot of Temperature vs Radiation - the strongest Pearson correlation

plt.scatter(df['Temperature'], df['Radiation'])
plt.xlabel('Temperature (F)')
plt.ylabel('Radiation (W/m^2)')
plt.title('Strongest Pearson Correlation')
plt.savefig(fname='feature_corr.png')

# Scatter plot of Time of Day vs Radiation

plt.scatter(df['TimeOfDay'], df['Radiation'])
plt.xlabel('Time of Day (s)')
plt.ylabel('Radiation (W/m^2)')
plt.title('Radiation During the Day')
plt.savefig(fname='feature_corr.png')

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Top 2 Most Important Features vs. Radiation (W/m^2)')
ax1.set_ylabel('Radiation (W/m^2)')
ax1.set_xlabel('Temperature (F)')
ax2.set_xlabel('Time of Day (s)')

ax1.scatter(df['Temperature'], df['Radiation'])
ax2.scatter(df['TimeOfDay'], df['Radiation'])

"""# 4. Visualize the data (i.e., plot a variety of features and analyze their distributions, etc) and provide some general comments on the visualized data.
> TimeOfDay and Radiation have a bell-curve like plot: the middle of the day has the highest radiation.

> MonthOfYear and Radiation have a slight downward trend: only have data for the last four months, radiation decreases in Sept - Dec.

> Many features have a near-zero Pearson Correlation.

"""

# Scatter plots of every pair of features
sns.pairplot(df,height=1.5)

"""# 5. Build supervised regression models to predict Radiation. Consider two different supervised ML algorithms.
- Justify your choice of the train/test split and ML model selection choice.
> Used a train/test split of 70/30. We want a slightly larger test size to report the accuracy of our model to our client. We have a decent amount of samples and are using cross validation. This allows us to pick a larger test set.

-   Justify your choice of ML model selection choice.
> Random forest is recommended, a good supervised regression model. K-neighbors regressor is a different approach using a distance metric.

- Use k-fold cross validation.

- What is the cross-validation (CV) score using cross_val_score (report the mean and standard deviation)? What is the Mean Absolute Error (MAE) and root-mean-square error (RMSE) on test set for each model?
> See information below each model
"""

# Splits dataset into X/Y as well as test/train sets

cols = ['Temperature','Pressure','Humidity','WindDirection','Speed','DayLength','TimeOfDay','MonthOfYear','DayOfYear']
X = df[cols]
y = df['Radiation']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

  # Make an additional standardized version of the test/train X values to use with KNN model
feature_scaler = StandardScaler()
X_train_std = feature_scaler.fit_transform(X_train)
X_test_std = feature_scaler.transform(X_test)

"""**Random Forest Regressor**"""

forest = RandomForestRegressor()
forest.fit(X_train, y_train)



"""**K-Nearest Neighbors Regressor**"""

knn = neighbors.KNeighborsRegressor()
knn.fit(X_train_std,y_train)

# K-FOLD CROSS VALIDATION - KNN

accuracies = cross_val_score(estimator=knn, X=X_train_std, y=y_train)

y_train_pred_knn = knn.predict(X_train_std)
y_test_pred_knn = knn.predict(X_test_std)

print('cv scores: ', accuracies)
print('mean cv score: ', accuracies.mean())
print('standard deviation of cv score: ', accuracies.std())

print('MAE test: ', mean_absolute_error(y_test, y_test_pred_knn))
print('RMSE test: ', np.sqrt(mean_squared_error(y_test, y_test_pred_knn)))

print('R^2 test: ', r2_score(y_test, y_test_pred_knn))

"""# 6. Repeat analysis (5) but tune the hyperparameters of the models using a grid search.

- Justify your choice of which hyperparameters to optimize.
> Random Forest: optimized number of estimators and max depth. Two of the most important hyperparameters that determine the size and complexity of model. We wanted these hyperparameters to be optimized without increasing the models runtime.

> KNN: optimized the number of neighbors and distance metric. These are two main hyperparameters. 

- What is the best CV score and the RMSE and MAE on test set for each of the models after hyperparameter tuning?
> See below each model.

- What performance improvement on the test set was obtained by hyperparameter
tuning?
> Random Forest: MAE improved by 0.5% and RMSE improved by 0.8%
> KNN: MAE improved by 11.8% and RMSE improved by 8.4%

- Which model is performing best and why do you think this is the case?
> Our Random Forest model is performing best. Random Forest is a more complex model with generally higher regression accuracy. Additionally, the dataset has low variance across many of its features which is more harmful to KNN.

**Random Forest Regressor**
"""

# Grid search cross validation to optimize hyperparameters

# Ran GridSearch many times, with changing parameters - 
  # run with params = {'n_estimators': [50,100], 'max_depth': [2, 5, 10]}, final model: n_est = 100, max_depth = 10
  # run with params = {'n_estimators': [100,200,300], 'max_depth': [5,10,15]}, final model: n_est = 300, max_depth = 15
  # run with params = {'n_estimators': [300,400,500], 'max_depth': [20,25]}, final model: n_est = 500, max_depth = 25

params = {'n_estimators': [100,200,400,500], 'max_depth': [10,20,25]}

forest = GridSearchCV(RandomForestRegressor(criterion='mse', random_state=42), params, cv=5)

forest.fit(X_train, y_train)
y_train_pred_rf = forest.predict(X_train)
y_test_pred_rf = forest.predict(X_test)

# Best model used with n_estimators = 500 and max_depth = 25
forest.best_estimator_

# Prints the CV accuracies for the test set
accuracies = cross_val_score(estimator=forest, X=X_train_std, y=y_train, cv=5, n_jobs=-1)

print('cv scores: ', accuracies)
print('mean cv score: ', accuracies.mean())
print('standard deviation of cv score: ', accuracies.std())
print('MAE test: ', mean_absolute_error(y_test, y_test_pred_rf))
print('RMSE test: ', np.sqrt(mean_squared_error(y_test, y_test_pred_rf)))
print('R^2 test: ', r2_score(y_test, y_test_pred_rf))

# Prints the CV accuracies for training set
  # - Similar accuracies on test and training set show that model is not overfit
print('cv scores: ', accuracies)
print('mean cv score: ', accuracies.mean())
print('standard deviation of cv score: ', accuracies.std())
print('MAE test: ', mean_absolute_error(y_train, y_train_pred_rf))
print('RMSE test: ', np.sqrt(mean_squared_error(y_train, y_train_pred_rf)))
print('R^2 test: ', r2_score(y_train, y_train_pred_rf))

"""**K-Nearest Neighbors Regressor**"""

# Grid search cross validation to optimize hyperparameters

params = {'n_neighbors':[1,2,3,5,7,10], 'metric':['euclidean', 'minkowski', 'manhattan']}

knn = GridSearchCV(neighbors.KNeighborsRegressor(), params, cv=3)

knn.fit(X_train_std, y_train)
y_train_pred_knn = knn.predict(X_train_std)
y_test_pred_knn = knn.predict(X_test_std)

# Best model used with n_neighbors = 5 and metric = manhattan
knn.best_estimator_

# KNN
accuracies = cross_val_score(estimator=knn, X=X_train_std, y=y_train, cv=5)
print('cv scores: ', accuracies)
print('mean cv score: ', accuracies.mean())
print('standard deviation of cv score: ', accuracies.std())
print('MAE test: ', mean_absolute_error(y_test, y_test_pred_knn))
print('RMSE test: ', np.sqrt(mean_squared_error(y_test, y_test_pred_knn)))
print('R^2 test: ', r2_score(y_test, y_test_pred_knn))

# Prints the CV accuracies for training set
  # - Similar accuracies on test and training set show that model is not overfit
print('cv scores: ', accuracies)
print('mean cv score: ', accuracies.mean())
print('standard deviation of cv score: ', accuracies.std())
print('MAE test: ', mean_absolute_error(y_train, y_train_pred_knn))
print('RMSE test: ', np.sqrt(mean_squared_error(y_train, y_train_pred_knn)))
print('R^2 test: ', r2_score(y_train, y_train_pred_knn))

"""# 7. Based on your analysis, which single feature is the most important? Does this make sense?
> Temperature is the most important feature. This makes sense since temperature and radiation have the strongest correlation.
"""

forest = RandomForestRegressor(criterion='mae', random_state=42, n_estimators=500, max_depth=25)
forest.fit(X_train,y_train)

y_train_pred_rf = forest.predict(X_train)
y_test_pred_rf = forest.predict(X_test)

# Prints the features importances as given by the random forest model
importances = forest.feature_importances_

print(importances)

# Bar plot of above feature importances

plt.figure(figsize=(15, 3))
cols = ['Temperature','Pressure','Humidity','WindDirection','Speed','DayLength','TimeOfDay','MonthOfYear','DayOfYear']
plt.bar(cols, importances, align='center', width=.75)
plt.title('Random Forest Feature Importances')
plt.xlabel('Features')
plt.ylabel('Importances')

plt.savefig('RF_feature.png')

"""# 8. Plot your best fit models for predicted Solar Radiation vs. Date/Time and compare with the actual, observed, solar irradiance. It may be helpful to visualize your data over different time scales.
- And/or plot the predicted solar energy output (J/m2) compared to the observed vs the day.
"""

# Predicts Radiation values across entire range of samples
rf_radiation = forest.predict(X)
X_std = feature_scaler.transform(X)
knn_radiation = knn.predict(X_std)

"""**Random Forest Plots**"""

# Plot of TimeOfDay vs. Radiation

f, (ax1, ax2) = plt.subplots(1, 2)

ax1.scatter(df['TimeOfDay'], rf_radiation)
ax1.set_title('Random Forest')

ax2.scatter(df['TimeOfDay'], y)
ax2.set_title('Actual')

ax2.set_xlabel('Time of Day (s)')
ax1.set_ylabel('Radiation (J/m2)')

f.savefig(fname='rf_timeofday.png')

# Plot of MonthOfYear vs. Radiation

f, (ax1, ax2) = plt.subplots(1, 2)

ax1.scatter(df['MonthOfYear'], rf_radiation)
ax1.set_title('Random Forest')

ax2.scatter(df['MonthOfYear'],y)
ax2.set_title('Actual')

ax2.set_xlabel('Month of Year')
ax1.set_ylabel('Radiation (J/m2)')

f.savefig(fname='rf_monthofday.png')

# Plot of DayOfYear vs. Radiation

f, (ax1, ax2) = plt.subplots(1, 2)
ax1.scatter(df['DayOfYear'], rf_radiation)
ax1.set_title('Random Forest')

ax2.scatter(df['DayOfYear'],y)
ax2.set_title('Actual')

ax2.set_xlabel('Day of Year')
ax1.set_ylabel('Radiation (J/m2)')

f.savefig(fname='rf_dayofyear.png')

"""**K-Nearest Neighbors**"""

# Plot of TimeOfDay vs. Radiation

f, (ax1, ax2) = plt.subplots(1, 2)
ax1.scatter(df['TimeOfDay'], knn_radiation)
ax1.set_title('K-Nearest Neighbors')

ax2.scatter(df['TimeOfDay'], y)
ax2.set_title('Actual')

ax2.set_xlabel('Time of Day (s)')
ax1.set_ylabel('Radiation (J/m2)')

f.savefig(fname='knn_timeofday.png')

# Plot of MonthOfYear vs. Radiation

f, (ax1, ax2) = plt.subplots(1, 2)
ax1.scatter(df['MonthOfYear'], knn_radiation)
ax1.set_title('K-Nearest Neighbors')

ax2.scatter(df['MonthOfYear'],y)
ax2.set_title('Actual')

ax2.set_xlabel('Month of Year')
ax1.set_ylabel('Radiation (J/m2)')

f.savefig(fname='knn_monthofday.png')

# Plot of DayOfYear vs. Radiation

f, (ax1, ax2) = plt.subplots(1, 2)
ax1.scatter(df['DayOfYear'], knn_radiation)
ax1.set_title('K-Nearest Neighbors')

ax2.scatter(df['DayOfYear'],y)
ax2.set_title('Actual')

ax2.set_xlabel('Day of Year')
ax1.set_ylabel('Radiation (J/m2)')

f.savefig(fname='knn_dayofyear.png')

"""# 9. Create two of your own questions to answer and report on it

# principle component analysis
> We ran our KNN model with only 7 features. Our scores decreased, so we want to keep all features in our final model.
"""

# Principle Component Analysis

pca = PCA()
X_train_pca = pca.fit_transform(X_train_std)
pca.explained_variance_ratio_

# Seeing how our knn model runs with only 7 features

pca = PCA(n_components=7)
X_train_pca = pca.fit_transform(X_train_std)
X_test_pca = pca.transform(X_test_std)

knn.fit(X_train_pca,y_train)
y_test_pred_pca = knn.predict(X_test_pca)

accuracies = cross_val_score(estimator=knn, X=X_train_pca, y=y_train, cv=2)
print('cv scores: ', accuracies)
print('mean cv score: ', accuracies.mean())
print('standard deviation of cv score: ', accuracies.std())
print('MAE test: ', mean_absolute_error(y_test, y_test_pred_pca))
print('RMSE test: ', np.sqrt(mean_squared_error(y_test, y_test_pred_pca)))
print('R^2 test: ', r2_score(y_test, y_test_pred_pca))

"""# Multi-Layer Perceptron Regressor Model"""

# Optimize hyperparameters for MLP Regressor
  # Optimized the hidden layer sizes and maximum iterations, since these two hyperparameters determine model complexity.
  # We want an accurate model without requiring a large runtime
params = {'hidden_layer_sizes': [10,50,100,200,500], 'max_iter': [100,200,500,750]}

mlp = GridSearchCV(MLPRegressor(activation='relu',solver='adam',validation_fraction = 0.3), params, cv=5)
mlp.fit(X_train, y_train)

# Best MLP model with 100 hidden layers and 200 max iterations
mlp.best_estimator_

mlp = MLPRegressor(hidden_layer_sizes=100, max_iter=200, activation='relu',solver='adam',validation_fraction = 0.3)
mlp.fit(X_train_std, y_train)
y_train_pred_mlp = mlp.predict(X_train_std)
y_test_pred_mlp = mlp.predict(X_test_std)

# Prints the CV accuracies for test set
accuracies = cross_val_score(estimator=mlp, X=X_train_std, y=y_train, cv=5)
print('cv scores: ', accuracies)
print('mean cv score: ', accuracies.mean())
print('standard deviation of cv score: ', accuracies.std())
print('MAE test: ', mean_absolute_error(y_test, y_test_pred_mlp))
print('RMSE test: ', np.sqrt(mean_squared_error(y_test, y_test_pred_mlp)))
print('R^2 test: ', r2_score(y_test, y_test_pred_mlp))

# Prints the CV accuracies for training set
  # - Similar accuracies on test and training set show that model is not overfit
print('cv scores: ', accuracies)
print('mean cv score: ', accuracies.mean())
print('standard deviation of cv score: ', accuracies.std())
print('MAE test: ', mean_absolute_error(y_train, y_train_pred_mlp))
print('RMSE test: ', np.sqrt(mean_squared_error(y_train, y_train_pred_mlp)))
print('R^2 test: ', r2_score(y_train, y_train_pred_mlp))

# Predicts values over entire sample
nn_radiation = mlp.predict(X)

# Plot of TimeOfDay vs. Radiation

f, (ax1, ax2) = plt.subplots(1, 2)
ax1.scatter(df['TimeOfDay'], nn_radiation)

ax1.set_title('Multi-Layer Perceptron')

ax2.scatter(df['TimeOfDay'], y)
ax2.set_title('Actual')

ax2.set_xlabel('Time of Day (s)')
ax1.set_ylabel('Radiation (J/m2)')

f.savefig(fname='nn_timeofday.png')

# Plot of MonthOfYear vs. Radiation

f, (ax1, ax2) = plt.subplots(1, 2)
ax1.scatter(df['MonthOfYear'], nn_radiation)
ax1.set_title('Multi-Layer Perceptron')

ax2.scatter(df['MonthOfYear'],y)
ax2.set_title('Actual')


ax2.set_xlabel('Month of Year')
ax1.set_ylabel('Radiation (J/m2)')

f.savefig(fname='nn_monthofday.png')

# Plot of DayOfYear vs. Radiation

f, (ax1, ax2) = plt.subplots(1, 2)
ax1.scatter(df['DayOfYear'], nn_radiation)
ax1.set_title('Multi-Layer Perceptron')

ax2.scatter(df['DayOfYear'],y)
ax2.set_title('Actual')

ax2.set_xlabel('Day of Year')
ax1.set_ylabel('Radiation (J/m2)')

f.savefig(fname='nn_dayofyear.png')

"""# Plot of residual error for random forest model"""

forest = RandomForestRegressor(criterion='mae', random_state=42, n_estimators=500, max_depth=25)
forest.fit(X_train,y_train)
y_train_pred_rf = forest.predict(X_train)
y_test_pred_rf = forest.predict(X_test)

plt.scatter(y_train_pred_rf,  
            y_train_pred_rf - y_train, 
            c='steelblue',
            edgecolor='white',
            marker='o', 
            s=35,
            alpha=0.9,
            label='training data')
plt.scatter(y_test_pred_rf,  
            y_test_pred_rf - y_test, 
            c='limegreen',
            edgecolor='white',
            marker='s', 
            s=35,
            alpha=0.9,
            label='test data')

plt.xlabel('Predicted values')
plt.ylabel('Residuals')
plt.legend(loc='upper left')
plt.hlines(y=0, xmin=-10, xmax=50, lw=2, color='black')
plt.xlim([-10, 50])
plt.tight_layout()

plt.show()
plt.savefig(fname="rf_residuals.png")
