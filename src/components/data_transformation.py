import os
import sys


import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer #this is used to create a pipeline
from sklearn.impute import SimpleImputer # for missing values
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


 
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts', "preprocessor.pkl")
    
    
class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
           
    def get_data_transformation_object(self): # this function is created to create all the pickle file
        '''
        This function is responsible for data transformation based on the different types of data
        
        '''
        logging.info("Entered the data transformation method or component")
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ]
            # this pipeline under training dataset
            num_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )
            cat_pipeline=Pipeline(
                
                # to handle the missing values
                # create a numerical pipeline to solve the missing values.Imputer helps in handling missing values
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
                
            )
            logging.info("Numerical columns standard scaling completed")
            
            logging.info("Categorical columns encoding completed")
            
            # combining the numerical pipeiline with the categorical pipeline by using column transformer
            # the column transformer will be having the combination of two things 1) the numerica pieline 2) numerical_columns
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipelines", cat_pipeline, categorical_columns)
                    
                ]
                
            )
            
            return preprocessor
                 
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        
        try:
            train_df = pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            
            logging.info("Read train and test data completed")
            
            logging.info("obtaining preprocessing object")
            
            preprocessing_obj = self.get_data_transformation_object() # this needs to be converted into a pickle file
            
            target_column_name = "math_score"
            numerical_columns = ["writing_score", "reading_score"]
            
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df=train_df[target_column_name]
            
            input_feature_test_df=test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df=test_df[target_column_name]
            
            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe"
            )
            
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)
            
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)]
            
            logging.info(f"Saved preprocessing object.")
            
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        except Exception as e: 
            raise CustomException(e, sys)
    