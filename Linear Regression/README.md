# Olympic Medal Prediction Using Linear Regression

## Overview
This project predicts the probable number of Olympic medals a country might win based on historic data. By using a Linear Regression model, we analyze trends and patterns in medal counts and make future predictions. The dataset was split into training and testing data (80/20 split) to ensure accurate and robust predictions.

## Author
Thato Seluku

## Repository
The project is hosted under my Data Science repository on GitHub.

## Dataset
The dataset contains historical records of Olympic medals won by various countries. It includes features such as:
- **Country**: The name of the country.
- **Year**: The Olympic year.
- **Medals**: The total number of medals won by the country.

## Project Workflow
1. **Data Cleaning and Preparation**:
   - Ensured no missing values in the dataset.
   - Standardized and normalized features as needed.
2. **Data Splitting**:
   - The data was split into 80% training and 20% testing subsets.
3. **Model Training**:
   - A Linear Regression model was implemented to learn from the training dataset.
4. **Evaluation**:
   - The model was evaluated on the test dataset using metrics such as Mean Absolute Error (MAE).
5. **Prediction**:
   - Probable medal counts for countries were predicted based on their historical performance.

## Results
- **Model Accuracy**: Varying insights. Countries with the most medals have shown consistent correct results. Although we may have to use a different method for countries with less medals.

- **Key Insights**:
   - Countries with consistent Olympic participation tend to have predictable medal counts.
   - Countries with more athletes participating are likely to have more medals.

## How to Run the Project
1. Clone the repository:
   ```bash
   git clone https://github.com/thatoseluku/datascience-repo.git
   ```
2. Navigate to the project directory:
   ```bash
   cd datascience-repo/olympic-medals
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Jupyter Notebook:
   ```bash
   jupyter notebook OlympicMedalsPrediction.ipynb
   ```

## Requirements
- Python 3.8 or above
- Jupyter Notebook
- Libraries: pandas, numpy, matplotlib, seaborn, scikit-learn

## Files in Repository
- **OlympicMedalsPrediction.ipynb**: Main notebook containing code for the project.
- **teams.csv**: The dataset used for training and testing.

## Future Improvements
- Incorporate additional features such as GDP, population, and sports infrastructure to improve predictions.
- Experiment with advanced machine learning models like Random Forests or Gradient Boosting.
- Visualize country-wise trends using interactive tools like Plotly or Tableau.

## Contributing
Feel free to fork the repository and submit pull requests for improvements or additional features.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Thank you for exploring this project. For any questions or feedback, please reach out via the Issues section on GitHub.

