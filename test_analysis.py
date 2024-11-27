import pytest
import pandas as pd
from analysis import o_score, encode_column_names, pow_analysis

@pytest.fixture
def sample_df():
    '''
    Creates a sample df for testing.

    Returns:
        pd.Dataframe: The dataframe created from the synthetic data.
    '''
    data = {
        'SQ18': [
            'AIPI 520 - Modeling Process & Algorithms',
            'MENG 570 - Business Fundamentals for Engineers',
            'AIPI 510 - Sourcing Data for Analytics'
        ],
        'MQ1': ['No single algorithm performs best across all tasks', 'Invalid Answer', 'Invalid Answer'],
        'MQ2': ['There are significant multicollinearity issues in the data', 'Invalid Answer', 'Invalid Answer'],
        'MQ3': ['The model is violating the assumption of linearity', 'Invalid Answer', 'Invalid Answer'],
        'MQ4': ['The true population parameter lies within the interval 95% of the time', 'Invalid Answer', 'Invalid Answer'],
        'MQ5': ["The model is too simple to capture the data's underlying patterns", 'Invalid Answer', 'Invalid Answer'],
        'BQ1': ['Invalid Answer', 'To define a clear, compelling message that differentiates your product', 'Invalid Answer'],
        'BQ2': ['Invalid Answer', 'To provide feedback and help validate the product-market fit', 'Invalid Answer'],
        'BQ3': ['Invalid Answer', 'Target specific customer groups with tailored marketing strategies', 'Invalid Answer'],
        'BQ4': ['Invalid Answer', 'A unique feature that cannot be easily copied or bought by competitors', 'Invalid Answer'],
        'BQ5': ['Invalid Answer', 'Understanding customer needs and validating business assumptions', 'Invalid Answer'],
        'DQ1': ['Invalid Answer', 'Invalid Answer', 'To collect data from various sources for analysis and decision-making'],
        'DQ2': ['Invalid Answer', 'Invalid Answer', 'Verifying the quality and accuracy of the data'],
        'DQ3': ['Invalid Answer', 'Invalid Answer', 'To extract real-time data from various online platforms'],
        'DQ4': ['Invalid Answer', 'Invalid Answer', 'It can extract data from websites without needing API access'],
        'DQ5': ['Invalid Answer', 'Invalid Answer', 'Streaming data sources'],
        'SQ1': ['Student1', 'Student2', 'Student3'],
        'SQ2': ['ARTIFICIAL INTELLIGENCE', 'ECONOMIC S', 'LINGUISTICS AND SPANISH']
    }
    return pd.DataFrame(data)

def test_o_score(sample_df):
    '''Ensure 'o_score' column is created and scores are calculated correctly.'''
    result = o_score(sample_df)
    assert 'o_score' in result.columns, "o_score column was not created"
    assert result['o_score'].iloc[0] == 5, "o_score calculation is incorrect for AIPI 520"
    assert result['o_score'].iloc[1] == 5, "o_score calculation is incorrect for MENG 570"
    assert result['o_score'].iloc[2] == 5, "o_score calculation is incorrect for AIPI 510"

def test_encode_column_names():
    '''Tests the column name encoding.'''
    columns = [f"Column{i}" for i in range(34)]
    encoded_mapping = encode_column_names(columns)

    # Validates encoded keys.
    assert "SQ1" in encoded_mapping, "SQ1 encoding is missing"
    assert "SQ18" in encoded_mapping, "SQ18 encoding is missing"
    assert "BQ1" in encoded_mapping, "BQ1 encoding is missing"
    assert "DQ5" in encoded_mapping, "DQ5 encoding is missing"
    assert "MQ5" in encoded_mapping, "MQ5 encoding is missing"
    assert len(encoded_mapping) == 33, f"Unexpected number of encoded columns: {len(encoded_mapping)}"

def test_power_analysis(capsys):
    '''Test the power analysis function.'''
    pow_analysis()
    captured = capsys.readouterr()
    assert "Sample size/Number needed in each group" in captured.out, "Power analysis output is missing"