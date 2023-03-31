# Junior Data Analyst Test Task

This repository contains the solution to the Junior Data Analyst Test Task. The task is divided into two parts: data processing and data visualization.

## **Part 1: Data Processing**

The data processing task involves preparing and processing the source data to be used in the second part of the task. The requirements for the output data are specified in the problem statement. The implementation for this part can be found in **`solution1.py`**.

### **Data Processing Steps:**

1. Load the input data
2. Keep the required columns
3. Assign colors to phrases based on clusters
4. Remove duplicates of keywords in the same area
5. Rename columns if needed
6. Sort the output data
7. Save the output data to a CSV file or a Google Spreadsheet

### **Libraries used:**

- pandas

## **Part 2: Data Visualization**

The data visualization task involves creating scatter plots based on the processed data. Each scatter plot represents one area. The implementation for this part can be found in **`solution2.py`**.

### **Data Visualization Steps:**

1. Define a function to split long phrases
2. Load the output data from Part 1
3. Create scatter plots for each area
4. Save the scatter plots as PNG files

### **Libraries used:**

- pandas
- matplotlib

## **Repository Structure**

- **`solution1.py`**: Python script for Part 1: Data Processing
- **`solution2.py`**: Python script for Part 2: Data Visualization
- **`scatter_plots/`**: Folder containing scatter plot images for each area
- **`Тестовое задание.xlsx`**: Input data in Excel format
- **`output_data.csv`**: Processed data saved as a CSV file

## **Usage**

1. Install required dependencies:

```bash
pip install pandas matplotlib
```

1. Run the **`solution1.py`** script to process the input data and generate the output data:

```bash
python solution1.py
```

1. Run the **`solution2.py`** script to create scatter plots based on the processed data:

```bash
shCopy code
python solution2.py
```

The scatter plots will be saved as PNG files in the **`scatter_plots/`** folder.
