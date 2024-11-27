# AI Chatbots vs. Students' Learning Perception
Evaluating AI Chatbots' Impact on Student Learning at Duke


### __Executive Summary:__
When brainstorming ideas for this final project, it dawned on me that the use of chatbots to facilitate rapid learning of new topics is a viewpoint that many detractors towards AI have constantly challenged. Through the curation of responses from Duke students, I believed there was a way to truly address this. As such, a problem was formulated: __"Can AI chatbots be effectively integrated into university settings to enhance student learning outcomes?"__. With AI chatbots in their infancy, addressing this problem would provide a basis for examining the long-term effects of their introduction in education. Fully realizing the positive and negative trends in the data could very well lead to beneficial insights for various educational settings in the future.

__Previous Work Done to Solve the Problem:__
Notably, _"Perceived Satisfaction of University Students with the Use of Chatbots as a Tool for Self-Regulated Learning"_ by Manzanares et al. (2023) in __Heliyon__ addresses the problem. I found this high-impact paper using DeepScholar, which indicated significant citations. The paper provided an η² value of 0.15 that was associated with Cohen's d of 0.84; thus, I used __d = 0.8__. The study found that master's degree students used chatbots more frequently and reported better learning outcomes and satisfaction compared to undergraduate students. 

Some notable datasets that exist in this space include the __Student Performance Prediction ([kaggle.com](https://www.kaggle.com/datasets/souradippal/student-performance-prediction))__ and __Chatbots' Impact on University Learning ([kaggle.com](https://www.kaggle.com/datasets/jocelyndumlao/chatbots-impact-on-university-learning?resource=download))__. The data for both of these is collected via questionnaires, and are designed primarily for classification tasks and the efficacy of chatbots in supporting mathematics learning at the university level, respectively. The student performance prediction dataset contains 40,000 records of students, with attributes including study habits, attendance rates, previous grades, and more. The other dataset focuses on AI chatbot experience based on criteria such as frequency of use, perceived usefulness, trust and security, and facilitating conditions.

__IRB Process:__
Before collecting the data, I had to be "cleared" for gathering data from other students. By contacting Duke Campus IRB Resources, I filled out the IRB form and was subsequently assigned to protocol #2025-0140.

__Tools Needed:__
I collected data from Duke University students using a structured [Google Forms questionnaire](https://forms.gle/MZoBVN3F4fpKvKDL7). Responses were recorded in Google Sheets, converted to CSV, and analyzed in Python with a Jupyter notebook, initially. Some further tools were developed to clean the data further within the notebook, which were— the **`o_score`** function,   **`encode_column_names`** function, and the **`preprocessing`** function. The first calculates the overall correctness score for each respondent by evaluating their answers to specific categories: modeling (`MQ`), business (`BQ`), and data (`DQ`) questions. The second standardizes column names by mapping them to structured keys like `SQ1`, `BQ1`, and `MQ5` for consistency and ease of analysis. Finally, the **`preprocessing`** function prepares the dataset by renaming columns, normalizing student majors (`SQ2`) using a predefined mapping, filling missing values, and encoding identifiers (`SQ1`) into anonymized numerical labels. Together, these "tools" ensure the dataset is clean, standardized, and ready for analysis.

__Data Collection:__
The data was collected from Duke University students across various academic programs and years, using surveys/questionnaires and synthetic data. The survey was administered through messaging apps (Discord, GroupMe, and WhatsApp). I reached out to Duke students in AIPI (Artificial Intelligence in Product Innovation) program student groups, gathering information on their engagement with AI chatbots, perceived usefulness, learning experiences, and academic performance metrics such as GPA and course grades. Synthetic data, although initially believed to be needed, was dropped due to having a sufficient sample size. All participants were anonymized to protect their privacy.

### __Dataset Description & Structure:__
The dataset uniquely provides a direct correlation between a Duke student's __objective score__ on a short quiz in their most confident class and their feelings and general habits involving generative AI tools, which is seldom addressed in public datasets.

The dataset contains several feature columns:

1. **Timestamp**: No encoding (remains as-is).  
2. **What’s your Duke Student ID?**: Encoded as **SQ1_encoded** (anonymized with numerical encoding).  
3. **What’s your major?**: Encoded as **SQ2**.  
4. **Are you an AIPI Student at Duke?**: Encoded as **SQ3**.  
5. **Are you an Undergraduate or Graduate Student?**: Encoded as **SQ4**.  
6. **Study Time Spent per day in Hours?**: Encoded as **SQ5**.  
7. **How much do you feel you have participated in class?**: Encoded as **SQ6**.  
8. **How much do you feel you use what you have learned outside of class?**: Encoded as **SQ7**.  
9. **How comfortable are you with using generative AI tools like ChatGPT to assist with your learning?**: Encoded as **SQ8**.  
10. **In which aspects of your learning have you used generative AI tools?**: Encoded as **SQ9**.  
11. **How frequently do you use generative AI tools for learning-related tasks?**: Encoded as **SQ10**.  
12. **To what extent do you feel generative AI has improved your academic performance?**: Encoded as **SQ11**.  
13. **What concerns, if any, do you have about using generative AI in your learning process?**: Encoded as **SQ12**.  
14. **How would you rate your overall academic performance in the past few weeks of the semester?**: Encoded as **SQ13**.  
15. **How have your grades in assignments changed as the semester has progressed?**: Encoded as **SQ14**.  
16. **How closely do your current grades align with your expectations?**: Encoded as **SQ15**.  
17. **Have you noticed any specific trends in your grades across different subjects throughout the semester?**: Encoded as **SQ16**.  
18. **How much do you believe your study habits or external factors have influenced your grades this semester?**: Encoded as **SQ17**.  
19. **If you are an AIPI student, indicate which class you feel you understand the most...**: Encoded as **SQ18**.  

### MENG570-Related Questions:
20. **In the Lean Canvas, what is the purpose of the Unique Value Proposition (UVP)?**: Encoded as **BQ1**.  
21. **What is the main role of early adopters in the Lean Start-Up approach?**: Encoded as **BQ2**.  
22. **What does market segmentation help a business achieve?**: Encoded as **BQ3**.  
23. **According to the Lean Canvas, what is an "Unfair Advantage"?**: Encoded as **BQ4**.  
24. **What does "customer discovery" aim to achieve in the Lean Start-Up process?**: Encoded as **BQ5**. 

### AIPI510-Related Questions:
25. **What is the primary purpose of sourcing data for analytics?**: Encoded as **DQ1**.  
26. **Which of the following is a key challenge when sourcing data from external sources?**: Encoded as **DQ2**.  
27. **What is a common reason for using APIs in data sourcing?**: Encoded as **DQ3**.  
28. **What is one advantage of using web scraping to source data for analytics?**: Encoded as **DQ4**.  
29. **Which type of data source is best suited for real-time analytics?**: Encoded as **DQ5**. 

### AIPI520-Related Questions:
30. **What does the 'no free lunch theorem' imply when it comes to algorithm selection?**: Encoded as **MQ1**.  
31. **Which of the following is NOT a key assumption in linear regression models?**: Encoded as **MQ2**.  
32. **In a residual plot, what does a 'hill-shaped' pattern of residuals indicate?**: Encoded as **MQ3**.  
33. **When constructing a confidence interval, what does a 95% confidence level mean?**: Encoded as **MQ4**.  
34. **Which of the following is a common reason why a model might underfit the data?**: Encoded as **MQ5**.

**o_score**: The metric that represents the respondent's correctness in their category of choice, summarizing their overall understanding of said topic.

__Power Analysis & Hypothesis:__
The code provided in [Introduction to Power Analysis in Python - GeeksforGeeks](https://www.geeksforgeeks.org/introduction-to-power-analysis-in-python/) calculates that approximately 25.525 subjects are needed in each group for a two-sided independent t-test with an effect size of 0.8, alpha of 0.05, and power of 0.8, using `TTestIndPower` from the `statsmodels.stats.power` module. Thus, one could make the hypothesis that a sample size of at least 26 subjects per group (in our case, Duke students as a whole constitute as a group) is sufficient to detect a large effect size (Cohen's d = 0.8) with a power of 0.8 and alpha of 0.05 in a two-sided independent t-test.

### __Exploratory Data Analysis:__
The code provides a comprehensive pipeline for preprocessing, analyzing, and visualizing survey data (initially separated in the earlier python notebook configurations). It starts by defining key preprocessing functions: `o_score`, `encode_column_names`, and `preprocessing`. The `pow_analysis` function calculates the required sample size for statistical significance using effect size and power. Visualization functions include creating word clouds (`print_wordcloud`), violin plots (`print_violin`), density contours (`print_contour_map`), histograms (`print_histo_10_13_o_score`), scatter plots (`print_scatter_*`), and pie charts (`print_pie_chart`), all of which visually explore patterns and relationships in the survey data. Here are the visualizations that were made:

_ALL PLOTS CAN BE VIEWED UPON RUNNING `analysis.py`_

### 1. **Scatter Plot of SQ16 vs SQ14**
This plot visualizes the relationship between students' consistency across subjects (SQ16) and their perception of improvement or decline in performance (SQ14). Categories like "Consistently strong in all subjects" and "Varied significantly across different subjects" are plotted against responses such as "Improved" or "Declined". This plot indicated that students who reported being "Consistently strong in all subjects" tend to associate their performance with "Improved" outcomes, while those who indicated they are "Varied significantly across different subjects" often show a mix of "Stayed mostly the same" or "Declined" perceptions.

### 2. **Scatter Plot of SQ5 vs SQ2**
This scatter plot examines the relationship between students' self-reported time spent using AI tools (SQ5) and their normalized major (SQ2). Markers are colored and shaped based on the respondents' college level and whether they used AI chatbots/tools, distinguishing undergraduates and graduates and showcasing variations in usage patterns across disciplines like AIPI, Business, and Linguistics & Spanish. AIPI students reported higher hours of AI tool usage compared to majors like Business or Linguistics, with those majors exhibiting less consistent engagement with AI tools.

### 3. **Pie Chart of SQ18**
This chart represents the distribution of survey participants across different courses (SQ18). Categories like "AIPI 520 - Modeling Process & Algorithms" and "MENG 570 - Business Fundamentals for Engineers" dominate, indicating which courses contributed most to the dataset. It provides an overview of the courses influencing the dataset's results. There is a notable participation from other technical and business-oriented courses, which is good for the sampling of the dataset.

### 4. **3D Scatter Plot of SQ7, SQ13, and Objective Score**
This visualization explores the relationship between students' responses to their consistency in AI tool usage (SQ7), their study habits (SQ13), and their objective performance score (o_score). Students who reported consistent AI usage (SQ7) and focused study habits (SQ13) tend to score higher on objective measures.

### 5. **3D Scatter Plot of SQ6, SQ13, and Objective Score**
This plot similarly analyzes the interplay between students' perceptions of AI's impact on their learning (SQ6), their study habits (SQ13), and their objective scores (o_score). It identifies whether perceptions of AI's impact align with objective outcomes, offering potential insights into how subjective and objective measures relate.

### 6. **Histogram of SQ10, SQ13, and Objective Score**
This histogram compares the distributions of responses for time spent studying (SQ10), study habits (SQ13), and the objective score (o_score). The marginal box plots at the top highlight spread and outliers for each variable, providing a comprehensive view of how these metrics vary across respondents. Perfect o_scores are associated with significantly higher study times and better study habits (SQ13), implying that effective time management and disciplined study contribute to performance.

### 7. **Contour Map of SQ5 and SQ10**
This density contour map illustrates the relationship between time spent using AI tools (SQ5) and time spent studying (SQ10). Areas of higher density (highlighted in yellow and orange) show where respondents tend to cluster, revealing common patterns in AI usage and study time allocation. This shows clusters around moderate time spent on both activities, suggesting that students balance their study time with AI tools rather than being over-reliant on one.

### 8. **Violin Plot of SQ8, SQ11, SQ15, and SQ17**
This violin plot visualizes the distribution of responses for various survey questions: SQ8 (confidence levels), SQ11 (academic satisfaction), SQ15 (study focus), and SQ17 (learning outcomes). The width of the violins at each value reflects the density of responses, providing insights into how these variables are distributed among the participants. Study focus (SQ15) and learning outcomes (SQ17) show narrower distributions compared to the higher variability when AI is involved.

### 9. **Word Cloud for SQ9 and SQ12**
This word cloud highlights the most frequent terms in responses to SQ9 (concerns about AI) and SQ12 (preferences for AI usage). Larger words like "Problem," "Solving," and "Information" suggest key areas of interest or concern among students.

### __Ethics Statement:__
This dataset was curated ethically in accordance with Duke Campus IRB, ensuring voluntary participation, anonymization of student IDs, and exclusion of sensitive personal data. Survey questions were designed to respect respondents' well-being, with majors normalized for clarity and inclusivity. The dataset is for research purposes only, aiming to enhance AI-driven learning while upholding fairness, transparency, and participant privacy.

### __Link to Kaggle-Hosted Dataset:__
https://www.kaggle.com/datasets/ykh2020/ai-chatbots-vs-students-learning-perception/data

### __Open Source License:__
__MIT License__ -> full description in the LICENSE file at the root of this repo.