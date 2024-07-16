import pandas as pd
import matplotlib.pyplot as plt
from plotnine import ggplot, aes, geom_bar, labs, theme, element_text

# Load the data
data = pd.read_csv('2006-2023_yearly_statistics.csv')

# Combine categories into '기타 혐오_count' (Other Hate)
data['기타 혐오_count'] += data['남성_count'] + data['성소수자_count'] + data['연령_count'] + data['지역_count'] + data['종교_count'] + data['기타 혐오_count']

# Keep only the necessary columns
data = data[['year', '여성/가족_count', '인종/국적_count', '악플/욕설_count', '기타 혐오_count']]

# Melt the data to long format
data_melted = data.melt(id_vars=['year'], 
                        value_vars=['여성/가족_count', '인종/국적_count', '악플/욕설_count', '기타 혐오_count'], 
                        var_name='Category', 
                        value_name='Count')

# Define category labels in English for clarity in the graph
category_labels = {
    '여성/가족_count': 'Women/Family',
    '인종/국적_count': 'Race/Nationality',
    '악플/욕설_count': 'Abusive/Insult',
    '기타 혐오_count': 'Other Hate'
}

data_melted['Category'] = data_melted['Category'].map(category_labels)

# Plot the stacked bar chart using ggplot
plot = (ggplot(data_melted, aes(x='factor(year)', y='Count', fill='Category')) +
        geom_bar(stat='identity', position='stack') +
        labs(title='Yearly Statistics (2006-2023)', x='Year', y='Count') +
        theme(axis_text_x=element_text(rotation=90, hjust=1)))

# Display the plot
print(plot);
