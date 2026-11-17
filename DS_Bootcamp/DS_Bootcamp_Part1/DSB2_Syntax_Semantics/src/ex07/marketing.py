import sys
def clients_set():
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
    'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
    'elon@paypal.com', 'jessica@gmail.com']
    return set(clients)

def participants_set():
    participants = ['walter@heisenberg.com', 'vasily@mail.ru',
    'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
    'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
    return set(participants)

def recipients_set():
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']
    return set(recipients)

def call_center(clients_s, recipients_s):
    return (clients_s - recipients_s)

def potential_clients(clients_s, participants_s):
    return (participants_s - clients_s)

def loyalty_program(clients_s, participants_s):
    return (clients_s - participants_s)

def process():
    inp = sys.argv
    if len(inp) != 2:
        raise ValueError("ошибка")
    if inp[1] == 'call_center':
        print(call_center(clients_set(), recipients_set()))
    elif inp[1] == 'potential_clients':
        print(potential_clients(clients_set(), participants_set()))
    elif inp[1] == 'loyalty_program':
        print(loyalty_program(clients_set(), participants_set()))
    else:
        raise ValueError("ошибка")

if __name__ == '__main__':
    process()