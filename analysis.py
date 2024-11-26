import pandas as pd
import plotly.express as px
from pandasgui import show
from sklearn.preprocessing import LabelEncoder
from statsmodels.stats.power import TTestIndPower
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def o_score(df):
    # Define correct answers for each category
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

    # Apply the scoring function to each row and create a new column 'o_score'
    df['o_score'] = df.apply(calculate_score, axis=1)

    return df

def encode_column_names(columns):
    encoded_mapping = {}

    # Encode the first 18 columns as SQ1 to SQ18
    for i in range(1, 19):
        encoded_mapping[f"SQ{i}"] = columns[i]

    # Encode the next 5 columns as BQ1 to BQ5
    for i, col in enumerate(columns[19:24], start=1):
        encoded_mapping[f"BQ{i}"] = col

    # Encode the next 5 columns as DQ1 to DQ5
    for i, col in enumerate(columns[24:29], start=1):
        encoded_mapping[f"DQ{i}"] = col

    # Encode the last 5 columns as MQ1 to MQ5
    for i, col in enumerate(columns[29:], start=1):
        encoded_mapping[f"MQ{i}"] = col

    return encoded_mapping

def preprocessing(responses_df):
    # Get the original column names and generate the mapping
    original_columns = responses_df.columns.tolist()
    encoded_mapping = encode_column_names(original_columns)

    # Rename columns in the DataFrame
    responses_df.rename(columns={v: k for k, v in encoded_mapping.items()}, inplace=True)

    # Step 2: Fill Missing Values
    responses_df.fillna('Not Taken', inplace=True)

    # Step 3: Encode Student IDs in 'SQ1'
    label_encoder = LabelEncoder()
    responses_df['SQ1'] = label_encoder.fit_transform(responses_df['SQ1'])
    responses_df.rename(columns={'SQ1': 'SQ1_encoded'}, inplace=True)

    # Save mapping for later use
    id_mapping = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))

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

    # Normalize 'SQ2' and apply replacements
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

#-------
def pow_analysis():
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
    # Combine text from columns S9 and S12 into a single string
    text = ' '.join(responses_df['SQ9'].dropna().astype(str)) + ' ' + ' '.join(responses_df['SQ12'].dropna().astype(str))

    # Generate WordCloud
    print_wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        max_words=200
    ).generate(text)

    # Display the WordCloud
    plt.figure(figsize=(10, 5))
    plt.imshow(print_wordcloud, interpolation='bilinear')
    plt.axis('off')  # Hide axes
    plt.title('Wordcloud for SQ9 and 12')
    plt.show()

def print_violin(responses_df):
    fig = px.violin(data_frame=responses_df, x=None, y=['SQ8', 'SQ11', 'SQ15', 'SQ17'],
    color=None, facet_row=None, facet_col=None, )
    fig.update_layout(
        title="Violin of SQ8, SQ11, SQ15, and SQ17",
    )
    fig.show()

def print_contour_map(responses_df):
    fig = px.density_contour(
        data_frame=responses_df, 
        x='SQ5', 
        y='SQ10', 
        z=None,
        facet_row=None, 
        facet_col=None
    )
    fig.update_traces(contours_coloring='fill', contours_showlabels=True)

    # Adjust layout to make the figure square and update text color
    fig.update_layout(
        width=600,  # Set the width
        height=600,  # Set the height
        xaxis=dict(scaleanchor="y"),  # Make x-axis and y-axis scales equal
        font=dict(color="black"),  # Set text color to white
        title="Contour Map of SQ5 and SQ10"
    )

    # Display the figure
    fig.show()

def print_histo_10_13_o_score(responses_df):
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

    # Update layout to make it more suitable for a Python notebook
    fig.update_layout(
        width=800,  # Set a width for the figure
        height=600,  # Set a height for the figure
        font=dict(size=12),  # Adjust font size for better readability
        paper_bgcolor="white",  # Set background to white
        plot_bgcolor="white",  # Set plot area background to white
        title="Histogram of SQ10, SQ13, and Objective Score",
    )

    # Display the figure
    fig.show()

def print_scatter_6_13_o_score(responses_df):
    df = responses_df[responses_df['o_score'] != 0]

    # Create a 3D scatter plot
    fig = px.scatter_3d(
        data_frame=df, 
        x='SQ6', 
        y='SQ13', 
        z='o_score', 
        color=None
    )

    # Update layout for better visualization
    fig.update_layout(
        width=800,  # Set the width of the plot
        height=600,  # Set the height of the plot
        font=dict(size=12),  # Adjust font size for readability
        paper_bgcolor="white",  # Set the background to white
        plot_bgcolor="white",  # Set the plot area background to white
        title="3D Scatter Plot of SQ6, SQ13, and Objective Score"
    )

    # Display the figure
    fig.show()

def print_scatter_7_13_o_score(responses_df):
    df = responses_df[responses_df['o_score'] != 0]

    # Create a 3D scatter plot
    fig = px.scatter_3d(
        data_frame=df, 
        x='SQ7', 
        y='SQ13', 
        z='o_score', 
        color=None
    )

    # Update layout for better visualization
    fig.update_layout(
        width=800,  # Set the width of the plot
        height=600,  # Set the height of the plot
        font=dict(size=12),  # Adjust font size for readability
        paper_bgcolor="white",  # Set the background to white
        plot_bgcolor="white"  # Set the plot area background to white
    )

    fig.update_layout(
        title="3D Scatter Plot of SQ7, SQ13, and Objective Score",
    )

    # Display the figure
    fig.show()

def print_pie_chart(responses_df):
    # Check for None conditions (raise error if implemented logic fails)
    if None is not None or None is not None:
        raise NotImplementedError("Condition not implemented.")

    # Create a pie chart
    fig = px.pie(
        data_frame=responses_df, 
        names='SQ18', 
        values=None, 
        color=None
    )

    fig.update_layout(
        title="Pie Chart of SQ18"
    )

    # Display the figure
    fig.show()

def print_scatter_2_to_6(responses_df):
    # Drop rows with NaN values in specific columns (replace None with actual column names)
    df = responses_df.dropna(subset=['SQ5', 'SQ2'])

    # Create a scatter plot
    fig = px.scatter(
        data_frame=df,
        x='SQ5', 
        y='SQ2', 
        color='SQ3',  # Replace with an appropriate column name or remove if not needed
        symbol='SQ4',  # Replace with an appropriate column name or remove if not needed
        size='SQ6',    # Replace with an appropriate column name or remove if not needed
        trendline=None, 
        marginal_x=None, 
        marginal_y=None,
        facet_row=None, 
        facet_col=None,
        render_mode='auto'  # Replace with the appropriate value if needed
    )

    # Update figure layout (customize if necessary)
    fig.update_layout(
        title="Scatter Plot of SQ5 vs SQ2",
        xaxis_title="SQ5",
        yaxis_title="SQ2"
    )

    # Display the figure inline in the notebook
    fig.show()

def print_scatter_14_16(responses_df):
    # Drop rows with NaN values in specific columns (replace None with actual column names)
    if None is not None:  # Replace None with the column to check for NaN values
        responses_df = responses_df.dropna(subset=['SQ16', 'SQ14'])  # Adjust column names as needed

    # Create a scatter plot
    fig = px.scatter(
        data_frame=responses_df,
        x='SQ16',  # Replace with the correct x-axis column name
        y='SQ14',  # Replace with the correct y-axis column name
        color=None,  # Replace with a column name for coloring, or keep as None
        symbol=None,  # Replace with a column name for symbol mapping, or keep as None
        size=None,  # Replace with a column name for point size, or keep as None
        trendline=None,  # Add a trendline type (e.g., "ols") if needed
        marginal_x=None,  # Add "box" or "violin" for marginal plots on x-axis
        marginal_y=None,  # Add "box" or "violin" for marginal plots on y-axis
        facet_row=None,  # Replace with a column name to create row facets, or keep as None
        facet_col=None,  # Replace with a column name to create column facets, or keep as None,
        render_mode='auto'  # Auto works for most cases
    )

    # Update figure layout (optional customization)
    fig.update_layout(
        title="Scatter Plot of SQ16 vs SQ14",
        xaxis_title="SQ16",
        yaxis_title="SQ14",
        autosize=True
    )

    # Display the figure in the notebook
    fig.show()
#-------

def main():
    responses_df = pd.read_csv('./responses_df_with_scores.csv')
    show(responses_df)

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