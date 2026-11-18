num_of_steps = 3
report_template = ("""В нашем эксперименте с подбрасыванием монеты из {} """
"""наблюдений {} раз выпала решка и {} раз — орёл. Вероятности составляют """
"""{}% и {}% соответственно. Мы прогнозируем, что в следующих {} наблюдениях решка """
"""выпадет {} раз, а орёл — {} раза.""")
data_file = 'data.csv'
token = ""
chat_id = ""
text_good = 'The report has been successfully created'
text_bad = "The report hasn't been created due to an error."