import pandas as pd
from sklearn.impute import SimpleImputer

class DataPreparationAgent:
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df_clean = df.copy()
        # Convert all columns that look numeric
        for col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='ignore')
        # Impute numeric columns
        imputer = SimpleImputer(strategy="mean")
        num_cols = df_clean.select_dtypes(include='number').columns
        df_clean[num_cols] = imputer.fit_transform(df_clean[num_cols])
        # Drop duplicates
        df_clean.drop_duplicates(inplace=True)
        # Remove outliers (IQR method) for all numeric columns
        for col in num_cols:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            df_clean = df_clean[(df_clean[col] >= lower) & (df_clean[col] <= upper)]
        return df_clean 