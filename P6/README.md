## P6: Make Effective Data Visualization
*Create a data visualization from a data set that tells a story or highlights trends or patterns in the data. Use either dimple.js or d3.js to create the visualization. Your work should be a reflection of the theory and practice of data visualization, such as visual encodings, design principles, and effective communication.*

### Summary
When Brazilian consumers need to resolve a dispute with business the first step is to go to a local Procon (Consumer Protection Agency) and file a complaint. The Procon assists the consumer and intermediates the resolution with the company. The goal of this visulation is to compare how fast and how often consumers can resolve their issues in each state.

### Design
A scatter plot was chosen as the final chart type because it allows the comparasion between the resolution rate and the median time to resolve issues for each state. The size of the bubble represents the number of complaints filed in each state. The vertical line represents the weighted mean resolution rate and the horizontal line represents the weighted mean resolution time. 

The chart could be divided into four quadrants:

| Quadrant     | Resolution Rate  | Resolution time  |
|--------------|------------------|------------------|
| Bottom left  | Low              | Fast             | 
| Bottom right | High             | Fast             |
| Upper left   | Low              | Slow             |
| Upper right  | High             | Slow             |

### Feedback

## Feedback 1
The reader was not sure about the meaning of each quadrant in the chart. I added labels in the four quadrants (slow/fast or low/high).

### Resources

- [Brazilian Business Complaints](https://www.kaggle.com/gerosa/procon)
- [2015 Brazilian Business Complaints EDA](https://www.kaggle.com/gerosa/brazilian-consumer-2015-complaints-eda)
- [Dimple](http://dimplejs.org/)

