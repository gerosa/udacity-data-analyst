## P6: Make Effective Data Visualization

### Summary
When Brazilian consumers need to resolve a dispute with business the first step is to go to a local Procon (Consumer Protection Agency) and file a complaint. The Procon assists the consumer and intermediates the resolution with the company.

Depending on the state where the complaint was filled, the consumer could have a much better chance to resolve his issue. For example, in Parana (PR) the resolution rate is only 50% while in Paraiba consumers resolve more than 80% of their issues. Also, the state could determine how much time the consumer will have to wait. For example, in the Rio de Janeiro (RJ) the median time to resolve an issue is only 3 weeks while in Distrito Federal (DF) is more than one year.

![Static Chart](https://raw.githubusercontent.com/gerosa/udacity-data-analyst/master/P6/static_chart.png)

### Design
A [bubble chart](https://datavizcatalogue.com/methods/bubble_chart.html) was chosen as the final chart type because it allows the comparasion between the resolution rate and the median time to resolve issues for each state. The size of the bubble represents the number of complaints filed in each state. The vertical line represents the weighted mean resolution rate and the horizontal line represents the weighted mean resolution time. The color of the bubbles represents the region where the state is located.

The chart could be divided into four quadrants:

| Quadrant     | Resolution Rate  | Resolution time  |
|--------------|------------------|------------------|
| Bottom left  | Low              | Fast             | 
| Bottom right | High             | Fast             |
| Upper left   | Low              | Slow             |
| Upper right  | High             | Slow             |

### Feedback

## Feedback 1
The reader was not sure about the meaning of each quadrant in the chart. 

Changes: I added labels in the four quadrants (slow/fast or low/high).

## Feedback 2
 > I did not understand what the area of the circles means. Is it the total amount of complaints? And I did not understand the dashed lines of red. I think it's the average or median of all states, but I was in doubt. One last thing: have you tried to leave all circles of one color alone? Maybe it does not need color. It was just these comments. I found the animation great.

Changes: I added legend explaning that the size of the circle represents is proportional with the number of complaints in the state. I added the labels and the values in the red lines. I made all bubbles with the same color.

## Feedback 3
The reader missed the source of the data in the chart.

Changes: the sources was included.

### Resources

- [dados.gov.br](http://dados.gov.br/dataset/cadastro-nacional-de-reclamacoes-fundamentadas-procons-sindec1)
- [2015 Brazilian Business Complaints EDA](https://www.kaggle.com/gerosa/brazilian-consumer-2015-complaints-eda)
- [Dimple](http://dimplejs.org/)

