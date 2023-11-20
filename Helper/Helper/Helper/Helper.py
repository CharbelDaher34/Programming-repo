import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import tensorflow as tf
#def PredictStringMissingValues(df,y):
#  # Find columns with null values
#  columns_with_nulls = df.columns[df.isnull().any()].tolist()
  
#  # Remove 'y' from the list of columns with null values
#  columns_to_drop = [col for col in columns_with_nulls if col != y]
#  dropped=df[columns_to_drop]
#  # Drop the columns containing null values except for 'y'
#  df= df.drop(columns=columns_to_drop)

#  #take training and data to be predicted 
#  predict_data = df[df[y].isnull()]
#  train_data = df[df[y].notnull()]
#  X_train=train_data.drop(y,axis=1)
#  y_train=train_data[y]
#  #take the categorical variables and train the encoder on the train data 
#  index=train_data.index
#  object_vars = X_train.columns[X_train.dtypes == 'object']
#  X_train_categorical = X_train[object_vars]
#  encoder = OneHotEncoder(handle_unknown='ignore')
#  encoder.fit(X_train_categorical)
#  #transform the categorical variables of  X_train using the encoder and add them to the numerical columns from the original X_Train
#  X_train_encoded_categorical = encoder.transform(X_train_categorical)
#  X_train_encoded = pd.DataFrame(X_train_encoded_categorical.toarray(), columns=encoder.get_feature_names_out(object_vars),index=index)
#  X_train = pd.concat([X_train.drop(object_vars, axis=1), X_train_encoded], axis=1)
#  #LabelEncode the target variable
#  label_encoder = LabelEncoder()
#  label_encoder.fit(y_train)
#  y_encoded=label_encoder.transform(y_train)
#  #train the model on the
#  clf = svm.SVC(kernel='rbf')
#  clf.fit(X_train, y_encoded)
#  #transform the predict data to the format compatible with my model
#  Xpred=predict_data[object_vars]
#  Xpred=encoder.transform(Xpred)
#  Xpred=pd.DataFrame(Xpred.toarray(),columns=encoder.get_feature_names_out(object_vars),index=predict_data.index)
#  X_predict=pd.concat([predict_data.drop(object_vars,axis=1),Xpred],axis=1)
#  #make the predictions and return it
#  y_predict=clf.predict(X_predict.drop(y,axis=1))
#  #Adding the predicted values to the df
#  y_predict=label_encoder.inverse_transform(y_predict)
#  y_predict=pd.Series(y_predict,index=predict_data.index)
#  series1=pd.Series(label_encoder.transform(train_data[train_data[y].notnull()][y]),index=train_data.index)
#  series2=pd.Series(label_encoder.transform(y_predict),index=X_predict.index)
#  series1, series2 = series1.align(series2, fill_value=0)
#  result = series1 + series2
#  result=[int(x) for x in result]
#  df[y]=label_encoder.inverse_transform(result)
#  #Adding the columns containing null values other than y
#  df = pd.concat([df, dropped], axis=1)

#  return df

def PredictStringMissingValues(df, y):
    # Find columns with null values
    columns_with_nulls = df.columns[df.isnull().any()].tolist()

    # Remove 'y' from the list of columns with null values
    columns_to_drop = [col for col in columns_with_nulls if col != y]
    dropped = df[columns_to_drop]
    
    # Drop the columns containing null values except for 'y'
    df = df.drop(columns=columns_to_drop)

    # Take training and data to be predicted
    predict_data = df[df[y].isnull()]
    train_data = df[df[y].notnull()]
    
    # Extract X_train (features) and y_train (target) from the training data
    X_train = train_data.drop(y, axis=1)
    y_train = train_data[y]

    # Take the categorical variables and train the encoder on the train data
    index = train_data.index
    object_vars = X_train.columns[X_train.dtypes == 'object']
    X_train_categorical = X_train[object_vars]
    
    # Initialize and fit a OneHotEncoder to transform categorical variables into numeric format
    encoder = OneHotEncoder(handle_unknown='ignore')
    encoder.fit(X_train_categorical)
    
    # Transform the categorical variables of X_train using the encoder and add them to the numerical columns from the original X_Train
    X_train_encoded_categorical = encoder.transform(X_train_categorical)
    X_train_encoded = pd.DataFrame(X_train_encoded_categorical.toarray(), columns=encoder.get_feature_names_out(object_vars), index=index)
    X_train = pd.concat([X_train.drop(object_vars, axis=1), X_train_encoded], axis=1)
    
    # LabelEncode the target variable (convert string labels to numeric values)
    label_encoder = LabelEncoder()
    label_encoder.fit(y_train)
    y_encoded = label_encoder.transform(y_train)

    # Train the Support Vector Machine (SVM) model with a radial basis function (RBF) kernel
    clf = svm.SVC(kernel='rbf')
    clf.fit(X_train, y_encoded)
    
    # Transform the predict data to the format compatible with the model
    X_pred = predict_data[object_vars]
    X_pred = encoder.transform(X_pred)
    X_pred = pd.DataFrame(X_pred.toarray(), columns=encoder.get_feature_names_out(object_vars), index=predict_data.index)
    X_predict = pd.concat([predict_data.drop(object_vars, axis=1), X_pred], axis=1)
    
    # Make predictions on the missing data
    y_predict = clf.predict(X_predict.drop(y, axis=1))
    
    # Decode the numeric predictions back to their original string labels
    y_predict = label_encoder.inverse_transform(y_predict)
    y_predict = pd.Series(y_predict, index=predict_data.index)
    
    # Align the predicted series with the original training data series for further processing
    series1 = pd.Series(label_encoder.transform(train_data[train_data[y].notnull()][y]), index=train_data.index)
    series2 = pd.Series(label_encoder.transform(y_predict), index=X_predict.index)
    series1, series2 = series1.align(series2, fill_value=0)
    
    # Add the predicted values to the original dataframe
    result = series1 + series2
    result = [int(x) for x in result]
    df[y] = label_encoder.inverse_transform(result)
    
    # Add the columns containing null values other than 'y' back to the dataframe
    df = pd.concat([df, dropped], axis=1)

    return df
def fill_missing_string_values(df):
    # Find columns with null values
    columns_with_nulls = df.columns[df.isnull().any()].tolist()

    # Create a helper function for the PredictStringMissingValues logic
    def predict_missing_string_value(df, y):
        # Find columns with null values
        columns_with_nulls = df.columns[df.isnull().any()].tolist()
    
        # Remove 'y' from the list of columns with null values
        columns_to_drop = [col for col in columns_with_nulls if col != y]
        dropped = df[columns_to_drop]
        
        # Drop the columns containing null values except for 'y'
        df = df.drop(columns=columns_to_drop)
    
        # Take training and data to be predicted
        predict_data = df[df[y].isnull()]
        train_data = df[df[y].notnull()]
        
        # Extract X_train (features) and y_train (target) from the training data
        X_train = train_data.drop(y, axis=1)
        y_train = train_data[y]
    
        # Take the categorical variables and train the encoder on the train data
        index = train_data.index
        object_vars = X_train.columns[X_train.dtypes == 'object']
        X_train_categorical = X_train[object_vars]
        
        # Initialize and fit a OneHotEncoder to transform categorical variables into numeric format
        encoder = OneHotEncoder(handle_unknown='ignore')
        encoder.fit(X_train_categorical)
        
        # Transform the categorical variables of X_train using the encoder and add them to the numerical columns from the original X_Train
        X_train_encoded_categorical = encoder.transform(X_train_categorical)
        X_train_encoded = pd.DataFrame(X_train_encoded_categorical.toarray(), columns=encoder.get_feature_names_out(object_vars), index=index)
        X_train = pd.concat([X_train.drop(object_vars, axis=1), X_train_encoded], axis=1)
        
        # LabelEncode the target variable (convert string labels to numeric values)
        label_encoder = LabelEncoder()
        label_encoder.fit(y_train)
        y_encoded = label_encoder.transform(y_train)
    
        # Train the Support Vector Machine (SVM) model with a radial basis function (RBF) kernel
        clf = svm.SVC(kernel='rbf')
        clf.fit(X_train, y_encoded)
        
        # Transform the predict data to the format compatible with the model
        X_pred = predict_data[object_vars]
        X_pred = encoder.transform(X_pred)
        X_pred = pd.DataFrame(X_pred.toarray(), columns=encoder.get_feature_names_out(object_vars), index=predict_data.index)
        X_predict = pd.concat([predict_data.drop(object_vars, axis=1), X_pred], axis=1)
        
        # Make predictions on the missing data
        y_predict = clf.predict(X_predict.drop(y, axis=1))
        
        # Decode the numeric predictions back to their original string labels
        y_predict = label_encoder.inverse_transform(y_predict)
        y_predict = pd.Series(y_predict, index=predict_data.index)
        
        # Align the predicted series with the original training data series for further processing
        series1 = pd.Series(label_encoder.transform(train_data[train_data[y].notnull()][y]), index=train_data.index)
        series2 = pd.Series(label_encoder.transform(y_predict), index=X_predict.index)
        series1, series2 = series1.align(series2, fill_value=0)
        
        # Add the predicted values to the original dataframe
        result = series1 + series2
        result = [int(x) for x in result]
        df[y] = label_encoder.inverse_transform(result)
        
        # Add the columns containing null values other than 'y' back to the dataframe
        df = pd.concat([df, dropped], axis=1)
    
        return df
    
    # Loop through columns with null values and fill missing strings
    for col in columns_with_nulls:
        df = predict_missing_string_value(df, col)

    return df