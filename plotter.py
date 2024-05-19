import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_all_graphs(evaluation_results_path, recognition_results_path, output_folder):
    # Load the evaluation and recognition results CSV files
    evaluation_results = pd.read_csv(evaluation_results_path)
    recognition_results = pd.read_csv(recognition_results_path)

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Plot for Basic Pixelization
    basic_pixelization = evaluation_results[evaluation_results['Pixelation Type'] == 'Basic Pixelization']
    block_sizes = basic_pixelization['Block Size'].dropna().unique()
    ssim_values_basic = [basic_pixelization[basic_pixelization['Block Size'] == size]['SSIM'].mean() for size in block_sizes]
    psnr_values_basic = [basic_pixelization[basic_pixelization['Block Size'] == size]['PSNR'].mean() for size in block_sizes]

    plt.figure()
    sns.scatterplot(x=block_sizes, y=ssim_values_basic)
    sns.regplot(x=block_sizes, y=ssim_values_basic, scatter=False, ci=None, color='red')
    plt.title('Block Size vs SSIM for Basic Pixelization')
    plt.xlabel('Block Size')
    plt.ylabel('SSIM')
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, 'block_size_vs_ssim_basic_pixelization.png'))
    plt.close()

    plt.figure()
    sns.scatterplot(x=block_sizes, y=psnr_values_basic)
    sns.regplot(x=block_sizes, y=psnr_values_basic, scatter=False, ci=None, color='red')
    plt.title('Block Size vs PSNR for Basic Pixelization')
    plt.xlabel('Block Size')
    plt.ylabel('PSNR (dB)')
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, 'block_size_vs_psnr_basic_pixelization.png'))
    plt.close()

    # Bar Plot for Recognition Accuracy for Basic Pixelization
    basic_recognition = recognition_results[recognition_results['Pixelation Type'] == 'Basic Pixelization']
    recognition_accuracy_basic = [basic_recognition[basic_recognition['Block Size'] == size]['Recognition Result'].mean() for size in block_sizes]

    plt.figure()
    sns.barplot(x=block_sizes, y=recognition_accuracy_basic)
    plt.title('Block Size vs Recognition Accuracy for Basic Pixelization')
    plt.xlabel('Block Size')
    plt.ylabel('Recognition Accuracy')
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, 'block_size_vs_recognition_accuracy_basic_pixelization.png'))
    plt.close()

    # Scatter Plot with Trend Line for Adaptive Pixelization
    adaptive_pixelization = evaluation_results[evaluation_results['Pixelation Type'] == 'Adaptive Pixelization']
    min_block_sizes = adaptive_pixelization['Min Block Size'].dropna().unique()
    ssim_values_adaptive = [adaptive_pixelization[adaptive_pixelization['Min Block Size'] == size]['SSIM'].mean() for size in min_block_sizes]
    psnr_values_adaptive = [adaptive_pixelization[adaptive_pixelization['Min Block Size'] == size]['PSNR'].mean() for size in min_block_sizes]

    plt.figure()
    sns.scatterplot(x=min_block_sizes, y=ssim_values_adaptive)
    sns.regplot(x=min_block_sizes, y=ssim_values_adaptive, scatter=False, ci=None, color='red')
    plt.title('Min Block Size vs SSIM for Adaptive Pixelization')
    plt.xlabel('Min Block Size')
    plt.ylabel('SSIM')
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, 'min_block_size_vs_ssim_adaptive_pixelization.png'))
    plt.close()

    plt.figure()
    sns.scatterplot(x=min_block_sizes, y=psnr_values_adaptive)
    sns.regplot(x=min_block_sizes, y=psnr_values_adaptive, scatter=False, ci=None, color='red')
    plt.title('Min Block Size vs PSNR for Adaptive Pixelization')
    plt.xlabel('Min Block Size')
    plt.ylabel('PSNR (dB)')
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, 'min_block_size_vs_psnr_adaptive_pixelization.png'))
    plt.close()

    # Scatter Plot with Regression Line for Recognition Accuracy for Adaptive Pixelization
    adaptive_recognition = recognition_results[recognition_results['Pixelation Type'] == 'Adaptive Pixelization']
    recognition_accuracy_adaptive = [adaptive_recognition[adaptive_recognition['Min Block Size'] == size]['Recognition Result'].mean() for size in min_block_sizes]

    plt.figure()
    sns.scatterplot(x=min_block_sizes, y=recognition_accuracy_adaptive)
    sns.regplot(x=min_block_sizes, y=recognition_accuracy_adaptive, scatter=False, ci=None, color='red')
    plt.title('Min Block Size vs Recognition Accuracy for Adaptive Pixelization')
    plt.xlabel('Min Block Size')
    plt.ylabel('Recognition Accuracy')
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, 'min_block_size_vs_recognition_accuracy_adaptive_pixelization.png'))
    plt.close()

    # Scatter Plot with Trend Line for Gaussian Blur
    gaussian_blur = evaluation_results[evaluation_results['Pixelation Type'] == 'Gaussian Blur']
    kernel_sizes = gaussian_blur['Kernel Size'].dropna().unique()
    ssim_values_blur = [gaussian_blur[gaussian_blur['Kernel Size'] == size]['SSIM'].mean() for size in kernel_sizes]
    psnr_values_blur = [gaussian_blur[gaussian_blur['Kernel Size'] == size]['PSNR'].mean() for size in kernel_sizes]

    plt.figure()
    sns.scatterplot(x=kernel_sizes, y=ssim_values_blur)
    sns.regplot(x=kernel_sizes, y=ssim_values_blur, scatter=False, ci=None, color='red')
    plt.title('Kernel Size vs SSIM for Gaussian Blur')
    plt.xlabel('Kernel Size')
    plt.ylabel('SSIM')
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, 'kernel_size_vs_ssim_gaussian_blur.png'))
    plt.close()

    plt.figure()
    sns.scatterplot(x=kernel_sizes, y=psnr_values_blur)
    sns.regplot(x=kernel_sizes, y=psnr_values_blur, scatter=False, ci=None, color='red')
    plt.title('Kernel Size vs PSNR for Gaussian Blur')
    plt.xlabel('Kernel Size')
    plt.ylabel('PSNR (dB)')
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, 'kernel_size_vs_psnr_gaussian_blur.png'))
    plt.close()

    # Box Plot for Recognition Accuracy for Gaussian Blur
    gaussian_recognition = recognition_results[recognition_results['Pixelation Type'] == 'Gaussian Blur']
    recognition_accuracy_blur = [gaussian_recognition[gaussian_recognition['Kernel Size'] == size]['Recognition Result'].mean() for size in kernel_sizes]

    plt.figure()
    sns.boxplot(x=kernel_sizes, y=recognition_accuracy_blur)
    plt.title('Kernel Size vs Recognition Accuracy for Gaussian Blur')
    plt.xlabel('Kernel Size')
    plt.ylabel('Recognition Accuracy')
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, 'kernel_size_vs_recognition_accuracy_gaussian_blur.png'))
    plt.close()

    # Scatter Plot with Trend Line for Clustering with Pixelization
    clustering_pixelization = evaluation_results[evaluation_results['Pixelation Type'] == 'Clustering with Pixelization']
    num_clusters = clustering_pixelization['Num Clusters'].dropna().unique()
    ssim_values_clustering = [clustering_pixelization[clustering_pixelization['Num Clusters'] == num]['SSIM'].mean() for num in num_clusters]
    psnr_values_clustering = [clustering_pixelization[clustering_pixelization['Num Clusters'] == num]['PSNR'].mean() for num in num_clusters]

    plt.figure()
    sns.scatterplot(x=num_clusters, y=ssim_values_clustering)
    sns.regplot(x=num_clusters, y=ssim_values_clustering, scatter=False, ci=None, color='red')
    plt.title('Number of Clusters vs SSIM for Clustering Pixelization')
    plt.xlabel('Number of Clusters')
    plt.ylabel('SSIM')
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, 'num_clusters_vs_ssim_clustering_pixelization.png'))
    plt.close()

    plt.figure()
    sns.scatterplot(x=num_clusters, y=psnr_values_clustering)
    sns.regplot(x=num_clusters, y=psnr_values_clustering, scatter=False, ci=None, color='red')
    plt.title('Number of Clusters vs PSNR for Clustering Pixelization')
    plt.xlabel('Number of Clusters')
    plt.ylabel('PSNR (dB)')
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, 'num_clusters_vs_psnr_clustering_pixelization.png'))
    plt.close()

    # Heatmap for Recognition Accuracy for Clustering with Pixelization
    clustering_recognition = recognition_results[recognition_results['Pixelation Type'] == 'Clustering with Pixelization']
    recognition_accuracy_clustering = [clustering_recognition[clustering_recognition['Num Clusters'] == num]['Recognition Result'].mean() for num in num_clusters]
    
    clustering_data = pd.DataFrame({'Num Clusters': num_clusters, 'Recognition Accuracy': recognition_accuracy_clustering})
    clustering_pivot = clustering_data.pivot_table(index='Num Clusters', values='Recognition Accuracy')

    plt.figure()
    sns.heatmap(clustering_pivot, annot=True, cmap="YlGnBu")
    plt.title('Number of Clusters vs Recognition Accuracy for Clustering Pixelization')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Recognition Accuracy')
    plt.savefig(os.path.join(output_folder, 'num_clusters_vs_recognition_accuracy_clustering_pixelization.png'))
    plt.close()
# Call the function with paths
plot_all_graphs('Evaluation/cleaned_evaluation_results.csv', 'Evaluation/cleaned_recognition_results.csv', 'images')
