import pandas as pd
import plotly.express as px
from pandasgui import show
from sklearn.preprocessing import LabelEncoder
from statsmodels.stats.power import TTestIndPower
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ----------------------------
# Data Preprocessing Functions
# ----------------------------
def o_score(df):
    '''
    Appends the objective score feature column to the dataframe df.

    Args:
        df (pd.Dataframe): Any dataframe, in this case [the original responses.csv]

    Returns:
        pd.Dataframe: A dataframe that adds the o_score computed columns for an input dataframe df.
    '''
    correct_answers = {
        'MQ': {
            'MQ1': 'No single algorithm performs best across all tasks',
            'MQ2': 'There are significant multicollinearity issues in the data',
            'MQ3': 'The model is violating the assumption of linearity',
            'MQ4': 'The true population parameter lies within the interval 95% of the time',
            'MQ5': "The model is too simple to capture the data's underlying patterns"
        },
        'BQ': {
            'BQ1': 'To define a clear, compelling message that differentiates your product',
            'BQ2': 'To provide feedback and help validate the product-market fit',
            'BQ3': 'Target specific customer groups with tailored marketing strategies',
            'BQ4': 'A unique feature that cannot be easily copied or bought by competitors',
            'BQ5': 'Understanding customer needs and validating business assumptions'
        },
        'DQ': {
            'DQ1': 'To collect data from various sources for analysis and decision-making',
            'DQ2': 'Verifying the quality and accuracy of the data',
            'DQ3': 'To extract real-time data from various online platforms',
            'DQ4': 'It can extract data from websites without needing API access',
            'DQ5': 'Streaming data sources'
        }
    }

    # Function to calculate score
    def calculate_score(row):
        '''
        Calculates the score of the objective score questions that a participant had taken.

        Args:
            row (pd.Row) The row of a dataframe df.

        Returns:
            int: The score out of 5 that is achieved from the answers in the columns.
        '''
        score = 0
        if row['SQ18'] == 'AIPI 520 - Modeling Process & Algorithms':
            for i in range(1, 6):
                question = f'MQ{i}'
                if row[question] == correct_answers['MQ'][question]:
                    score += 1
        elif row['SQ18'] == 'MENG 570 - Business Fundamentals for Engineers':
            for i in range(1, 6):
                question = f'BQ{i}'
                if row[question] == correct_answers['BQ'][question]:
                    score += 1
        elif row['SQ18'] == 'AIPI 510 - Sourcing Data for Analytics':
            for i in range(1, 6):
                question = f'DQ{i}'
                if row[question] == correct_answers['DQ'][question]:
                    score += 1
        return score

    df['o_score'] = df.apply(calculate_score, axis=1)

    return df

def encode_column_names(columns):
    '''
    Encodes column names to make the feature names much more concise.

    Args:
        columns (list of str): A list of column names.

    Returns:
        dict: A dictionary where keys are the new encoded names and values are the original column names.
    '''
    encoded_mapping = {}

    # Takes the first 18 questions in the original columns and encodes them.
    for i in range(1, 19):
        encoded_mapping[f"SQ{i}"] = columns[i]

    # Takes the next 5 questions that have been answered in the original columns and encodes them.
    for i, col in enumerate(columns[19:24], start=1):
        encoded_mapping[f"BQ{i}"] = col

    # Takes the next 5 questions that have been answered in the original columns and encodes them.
    for i, col in enumerate(columns[24:29], start=1):
        encoded_mapping[f"DQ{i}"] = col

    # Takes the next 5 questions that have been answered in the original columns and encodes them.
    for i, col in enumerate(columns[29:], start=1):
        encoded_mapping[f"MQ{i}"] = col

    return encoded_mapping

def preprocessing(responses_df):
    '''
    Preprocesses a survey responses DataFrame.

    Args:
        responses_df (pd.DataFrame): The input DataFrame containing survey responses.

    Returns:
        tuple:
            - encoded_mapping (dict): A mapping of new encoded column names to their original names.
            - id_mapping (dict): A mapping of original 'SQ1' values to their encoded numerical values.
    '''
    original_columns = responses_df.columns.tolist()
    encoded_mapping = encode_column_names(original_columns)

    responses_df.rename(columns={v: k for k, v in encoded_mapping.items()}, inplace=True)

    responses_df.fillna('Not Taken', inplace=True)

    label_encoder = LabelEncoder()
    responses_df['SQ1'] = label_encoder.fit_transform(responses_df['SQ1'])
    responses_df.rename(columns={'SQ1': 'SQ1_encoded'}, inplace=True)

    id_mapping = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))

    # Some names that were recorded for a participant's major was too long, so they needed to be shortened.
    replacement_map = {
        'ARTIFICIAL INTELLIGENCE IN PRODUCT INNOVATION': 'AIPI',
        'ARTIFICIAL INTELLIGENCE': 'AIPI',
        'AI': 'AIPI',
        'M.ENG AIPI': 'AIPI',
        'MENG IN AIPI': 'AIPI',
        'COMPUTER SCIENCE, PHYSICS': 'CS & PHYSICS',
        'PHYSICS, COMPUTER SCIENCE': 'CS & PHYSICS',
        'ECONOMIC S': 'ECON',
        'UNDECLARED - STATISTICAL SCIENCE': 'UNDECLARED/STATSCI',
        'LINGUISTICS AND SPANISH': 'LINGUISTICS & SPANISH',
        'MECHANICAL ENGINEERING': 'MECHE',
        'FGG': 'UNDECLARED'
    }

    # Normalized 'SQ2' and applied the above map to the users' inputs.
    responses_df['SQ2'] = (
        responses_df['SQ2']
        .str.strip()
        .str.upper()
        .replace(replacement_map)
    )

    print("\nMapping of Encoded Column Names:")
    print(encoded_mapping)

    print("\nMapping of Original IDs to Encoded Values:")
    print(id_mapping)

    return encoded_mapping, id_mapping

# ----------------------------
# Visualizations
# ----------------------------
def pow_analysis():
    '''
    [Taken from GeeksforGeeks/Lecture Slides]
    Performs a general power analysis to find the sample size required (achieved 25.525 and got 31 survey responses)
    '''
    # factors for power analysis
    alpha = 0.05
    power = 0.8

    # perform power analysis to find sample size 
    # for given effect 
    obj = TTestIndPower() 
    n = obj.solve_power(effect_size=0.8, alpha=alpha, power=power, 
                        ratio=1, alternative='two-sided') 

    print('Sample size/Number needed in each group: {:.3f}'.format(n))

def print_wordcloud(responses_df):
    '''
    Prints out the wordcloud of combined responses for SQ9 and SQ12.

    Args:
        responses_df (pd.DataFrame): The input DataFrame containing survey responses.
    '''
    # Combines responses for columns S9 and S12 into a single string.
    text = ' '.join(responses_df['SQ9'].dropna().astype(str)) + ' ' + ' '.join(responses_df['SQ12'].dropna().astype(str))

    print_wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        max_words=200
    ).generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(print_wordcloud, interpolation='bilinear')
    plt.axis('off')  # Hide axes
    plt.title('Wordcloud for SQ9 and 12')
    plt.show()

def print_violin(responses_df):
    '''
    Prints out the violin visualization of combined responses for SQ8, SQ11, SQ15, and SQ17.

    Args:
        responses_df (pd.DataFrame): The input DataFrame containing survey responses.
    '''

    # Specifies dataframe, the columns, and leaves defaults facet row and col.
    fig = px.violin(data_frame=responses_df, x=None, y=['SQ8', 'SQ11', 'SQ15', 'SQ17'],
    color=None, facet_row=None, facet_col=None, )
    fig.update_layout(
        title="Violin of SQ8, SQ11, SQ15, and SQ17",
    )
    fig.show()

def print_contour_map(responses_df):
    '''
    Prints out the contour map visualization of combined responses for SQ5 and SQ10.

    Args:
        responses_df (pd.DataFrame): The input DataFrame containing survey responses.
    '''
    fig = px.density_contour(
        data_frame=responses_df, 
        x='SQ5', 
        y='SQ10', 
        z=None,
        facet_row=None, 
        facet_col=None
    )

    # Constantly updates the contours and fills in diverging colors.
    fig.update_traces(contours_coloring='fill', contours_showlabels=True)

    fig.update_layout(
        width=600,
        height=600,
        xaxis=dict(scaleanchor="y"),
        font=dict(color="black"),
        title="Contour Map of SQ5 and SQ10"
    )

    # Display the figure
    fig.show()

def print_histo_10_13_o_score(responses_df):
    '''
    Prints out the histogram of combined responses for SQ10, SQ13, and Objective score.

    Args:
        responses_df (pd.DataFrame): The input DataFrame containing survey responses.
    '''

    # Specify the objective scores not equal to 0.
    df = responses_df[(responses_df[['o_score', 'SQ10', 'SQ13']] != 0).all(axis=1)]

    fig = px.histogram(
        data_frame=df, 
        x=['o_score', 'SQ10', 'SQ13'], 
        color=None,
        facet_row=None, 
        facet_col=None, 
        marginal='box', 
        cumulative=False
    )

    fig.update_layout(
        width=800, 
        height=600,
        font=dict(size=12),
        paper_bgcolor="white",
        plot_bgcolor="white",
        title="Histogram of SQ10, SQ13, and Objective Score",
    )

    fig.show()

def print_scatter_6_13_o_score(responses_df):
    '''
    Prints out the 3D Scatterplot of combined responses for SQ6, SQ13, and Objective score.

    Args:
        responses_df (pd.DataFrame): The input DataFrame containing survey responses.
    '''
    df = responses_df[responses_df['o_score'] != 0]

    fig = px.scatter_3d(
        data_frame=df, 
        x='SQ6', 
        y='SQ13', 
        z='o_score', 
        color=None
    )

    fig.update_layout(
        width=800,
        height=600,
        font=dict(size=12),
        paper_bgcolor="white",
        plot_bgcolor="white", 
        title="3D Scatter Plot of SQ6, SQ13, and Objective Score"
    )

    fig.show()

def print_scatter_7_13_o_score(responses_df):
    '''
    Prints out the 3D Scatterplot of combined responses for SQ7, SQ13, and Objective score.

    Args:
        responses_df (pd.DataFrame): The input DataFrame containing survey responses.
    '''
    df = responses_df[responses_df['o_score'] != 0]

    fig = px.scatter_3d(
        data_frame=df, 
        x='SQ7', 
        y='SQ13', 
        z='o_score', 
        color=None
    )

    fig.update_layout(
        width=800,
        height=600,
        font=dict(size=12), 
        paper_bgcolor="white", 
        plot_bgcolor="white" 
    )

    fig.update_layout(
        title="3D Scatter Plot of SQ7, SQ13, and Objective Score",
    )

    fig.show()

def print_pie_chart(responses_df):
    '''
    Prints out the Pie chart of SQ18.

    Args:
        responses_df (pd.DataFrame): The input DataFrame containing survey responses.
    '''
    # Check for None conditions in the distribution.
    if None is not None or None is not None:
        raise NotImplementedError("Condition not implemented.")

    fig = px.pie(
        data_frame=responses_df, 
        names='SQ18', 
        values=None, 
        color=None
    )

    fig.update_layout(
        title="Pie Chart of SQ18"
    )

    fig.show()

def print_scatter_2_to_6(responses_df):
    '''
    Prints out Scatterplot of combined responses for SQ2 - SQ6.

    Args:
        responses_df (pd.DataFrame): The input DataFrame containing survey responses.
    '''
    # Drop rows with NaN values in the cols.
    df = responses_df.dropna(subset=['SQ5', 'SQ2'])

    fig = px.scatter(
        data_frame=df,
        x='SQ5', 
        y='SQ2', 
        color='SQ3', 
        symbol='SQ4',
        size='SQ6', 
        trendline=None, 
        marginal_x=None, 
        marginal_y=None,
        facet_row=None, 
        facet_col=None,
        render_mode='auto'
    )

    fig.update_layout(
        title="Scatter Plot of SQ5 vs SQ2",
        xaxis_title="SQ5",
        yaxis_title="SQ2"
    )

    fig.show()

def print_scatter_14_16(responses_df):
    '''
    Prints out Scatterplot of combined responses for SQ14 and SQ16.

    Args:
        responses_df (pd.DataFrame): The input DataFrame containing survey responses.
    '''
    # Drop rows with NaN values in specific cols.
    if None is not None:
        responses_df = responses_df.dropna(subset=['SQ16', 'SQ14'])

    fig = px.scatter(
        data_frame=responses_df,
        x='SQ16',
        y='SQ14', 
        color=None,
        symbol=None,
        size=None,
        trendline=None,
        marginal_x=None,
        marginal_y=None,
        facet_row=None,
        facet_col=None,
        render_mode='auto'
    )

    fig.update_layout(
        title="Scatter Plot of SQ16 vs SQ14",
        xaxis_title="SQ16",
        yaxis_title="SQ14",
        autosize=True
    )

    fig.show()

# ----------------------------
# Main
# ----------------------------
def main():
    '''
    The Main function.
    '''
    responses_df = pd.read_csv('./responses_df_with_scores.csv')

    # PandasGUI for easier visualization tampering for new data scientists!
    show(responses_df)

    # Power Analysis and Visualization functions
    pow_analysis()
    print_wordcloud(responses_df)
    print_violin(responses_df)
    print_contour_map(responses_df)
    print_histo_10_13_o_score(responses_df)
    print_scatter_6_13_o_score(responses_df)
    print_scatter_7_13_o_score(responses_df)
    print_pie_chart(responses_df)
    print_scatter_2_to_6(responses_df)
    print_scatter_14_16(responses_df)

if __name__ == '__main__':
    main()