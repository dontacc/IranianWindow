
import random


counter = 0

while True:

    dice1 = random.randint(1, 6) # 3
    dice2 = random.randint(1, 6) # 2


    print(dice1, dice2)

    if dice1 == dice2:
        counter += 1
        if counter == 3:
            break

    


