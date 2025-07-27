import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class EDAAgent:
    def summarize(self, df: pd.DataFrame) -> str:
        buffer = []
        buffer.append('<h4>Data Info</h4>')
        buffer.append(df.info(verbose=True, buf=None))
        buffer.append('<h4>Head</h4>')
        buffer.append(df.head().to_html(index=False))
        buffer.append('<h4>Data Dictionary</h4>')
        data_dict = pd.DataFrame({'Column': df.columns, 'Type': df.dtypes.astype(str)})
        buffer.append(data_dict.to_html(index=False))
        buffer.append('<h4>Missing Values</h4>')
        missing = df.isnull().sum()
        missing_percent = (missing / len(df)) * 100
        missing_df = pd.DataFrame({'Missing': missing, 'Percent': missing_percent})
        buffer.append(missing_df.to_html())
        buffer.append('<h4>Describe</h4>')
        buffer.append(df.describe(include='all').to_html())
        return ''.join([str(x) for x in buffer])

    def generate_visuals(self, df: pd.DataFrame):
        os.makedirs("outputs", exist_ok=True)
        image_paths = []
        numeric_cols = df.select_dtypes(include='number').columns
        # Histograms
        for col in numeric_cols:
            plt.figure(figsize=(8, 5))
            sns.histplot(df[col].dropna(), kde=True)
            plt.title(f"Histogram of {col}")
            img_path = f"outputs/histogram_{col}.png"
            plt.savefig(img_path)
            plt.close()
            image_paths.append(img_path)
        # Line chart: Total by Year
        if 'Year' in df.columns and len(numeric_cols) > 0:
            plt.figure(figsize=(10, 6))
            for col in numeric_cols:
                yearly = df.groupby('Year')[col].sum().sort_index()
                plt.plot(yearly.index, yearly.values, marker='o', label=col)
            plt.title('Total by Year')
            plt.xlabel('Year')
            plt.ylabel('Total')
            plt.legend()
            img_path = 'outputs/line_total_by_year.png'
            plt.savefig(img_path)
            plt.close()
            image_paths.append(img_path)
        # Bar chart: Top 10 by first categorical column
        cat_cols = df.select_dtypes(include='object').columns
        if len(cat_cols) > 0 and len(numeric_cols) > 0:
            plt.figure(figsize=(12, 6))
            top_cat = df.groupby(cat_cols[0])[numeric_cols[0]].sum().sort_values(ascending=False).head(10)
            sns.barplot(x=top_cat.values, y=top_cat.index, orient='h')
            plt.title(f'Top 10 {cat_cols[0]} by {numeric_cols[0]}')
            plt.xlabel(numeric_cols[0])
            plt.ylabel(cat_cols[0])
            img_path = f'outputs/bar_top10_{cat_cols[0]}.png'
            plt.savefig(img_path)
            plt.close()
            image_paths.append(img_path)
        # Box plot: Value by first categorical column
        if len(cat_cols) > 0 and len(numeric_cols) > 0:
            plt.figure(figsize=(14, 6))
            top_cats = df[cat_cols[0]].value_counts().head(10).index.tolist()
            box_data = df[df[cat_cols[0]].isin(top_cats)]
            if not box_data.empty:
                sns.boxplot(x=cat_cols[0], y=numeric_cols[0], data=box_data)
                plt.title(f'{numeric_cols[0]} Distribution by Top 10 {cat_cols[0]}')
                plt.xticks(rotation=45, ha='right')
                img_path = f'outputs/boxplot_{numeric_cols[0]}_by_{cat_cols[0]}.png'
                plt.savefig(img_path, bbox_inches='tight')
                plt.close()
                image_paths.append(img_path)
        # Correlation heatmap
        if len(numeric_cols) > 1:
            plt.figure(figsize=(8, 6))
            corr = df[numeric_cols].corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
            plt.title('Correlation Heatmap')
            img_path = 'outputs/corr_heatmap.png'
            plt.savefig(img_path)
            plt.close()
            image_paths.append(img_path)
        return image_paths 