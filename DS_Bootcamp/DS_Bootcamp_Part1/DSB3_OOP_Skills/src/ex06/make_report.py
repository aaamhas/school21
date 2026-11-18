
from analytics import Research
import config
def main():
    research = Research(config.data_file)
    try:
        reader = research.file_reader()
        analytic = research.Analytics(reader)
        template_1 = len(reader)
        template_3, template_2 = analytic.counts()
        template_4, template_5 = analytic.fractions(template_2, template_3)
        randoms = analytic.predict_random(config.num_of_steps)
        template_6 = 0 
        template_7 = 0
        for i in randoms:
            template_6 += i[0]
            template_7 += i[1]
        analytic.save_file(config.report_template.format(template_1, template_2, template_3, template_4*100, template_5*100, config.num_of_steps, template_6, template_7), 'file', 'txt')
        research.send_telegram_message(config.text_good)
    except ValueError as e:
        research.send_telegram_message(config.text_bad)
        print(e)
    except FileNotFoundError:
        research.send_telegram_message(config.text_bad)
        print("ошибка")
    except PermissionError:
        research.send_telegram_message(config.text_bad)
        print("ошибка")

    
    
if __name__ == '__main__':
    main()

