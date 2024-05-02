import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

# Load the data from the CSV file
file_path = 'evaluation/cleaned_evaluation_results.csv'  # Update the path accordingly
data = pd.read_csv(file_path)

# Setting up the aesthetic for the plots using set_theme
sns.set_theme(style="whitegrid")

# Optional: Set to False to disable displaying plots in windows
display_in_windows = False

# Open a PDF file to save the plots
with PdfPages('pixelation_analysis.pdf') as pdf:
    # Creating visualizations for each pixelation type
    for pixelation_type in data['Pixelation Type'].unique():
        type_data = data[data['Pixelation Type'] == pixelation_type]

        # Boxplot for SSIM and PSNR
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=type_data, x='Pixelation Type', y='SSIM')
        plt.title(f'SSIM Distribution for {pixelation_type}')
        plt.ylabel('SSIM')
        plt.xlabel('Pixelation Type')
        pdf.savefig()  # Save the current figure to pdf
        if display_in_windows:
            plt.show()
        else:
            plt.close()

        plt.figure(figsize=(12, 6))
        sns.boxplot(data=type_data, x='Pixelation Type', y='PSNR')
        plt.title(f'PSNR Distribution for {pixelation_type}')
        plt.ylabel('PSNR')
        plt.xlabel('Pixelation Type')
        pdf.savefig()
        if display_in_windows:
            plt.show()
        else:
            plt.close()

        # Histograms for SSIM and PSNR
        plt.figure(figsize=(12, 6))
        sns.histplot(data=type_data, x='SSIM', kde=True)
        plt.title(f'Histogram of SSIM for {pixelation_type}')
        plt.xlabel('SSIM')
        plt.ylabel('Frequency')
        pdf.savefig()
        if display_in_windows:
            plt.show()
        else:
            plt.close()

        plt.figure(figsize=(12, 6))
        sns.histplot(data=type_data, x='PSNR', kde=True)
        plt.title(f'Histogram of PSNR for {pixelation_type}')
        plt.xlabel('PSNR')
        plt.ylabel('Frequency')
        pdf.savefig()
        if display_in_windows:
            plt.show()
        else:
            plt.close()

        # Scatter plots and Line graphs for parameters
        param_cols = [col for col in type_data.columns if 'Size' in col or 'Threshold' in col or 'Clusters' in col]
        for param in param_cols:
            # Scatter plot SSIM vs PSNR for each parameter value
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=type_data, x='SSIM', y='PSNR', hue=param)
            plt.title(f'Relationship between SSIM and PSNR for {pixelation_type} by {param}')
            plt.xlabel('SSIM')
            plt.ylabel('PSNR')
            plt.legend(title=param)
            pdf.savefig()
            if display_in_windows:
                plt.show()
            else:
                plt.close()

            # Line plot for trends of SSIM and PSNR by parameter
            plt.figure(figsize=(12, 6))
            sns.lineplot(data=type_data, x=param, y='SSIM', label='SSIM', marker='o')
            sns.lineplot(data=type_data, x=param, y='PSNR', label='PSNR', marker='o', color='red')
            plt.title(f'Trends of SSIM and PSNR by {param} in {pixelation_type}')
            plt.xlabel(param)
            plt.ylabel('Metric Value')
            plt.legend()
            pdf.savefig()
            if display_in_windows:
                plt.show()
            else:
                plt.close()

print("Plots have been saved to 'pixelation_analysis.pdf'")
