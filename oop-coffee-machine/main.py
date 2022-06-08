# used libraries
from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

# objects that perform functions of a coffee machine
coffee_maker = CoffeeMaker()
money_machine = MoneyMachine()
menu = Menu()

# turn on coffee machine
is_on = True

# while coffee machine is on...
while is_on:
    # show available items
    options = menu.get_items()
    choice = input(f"What would you like? ({options}): ")
    # secret code to turn off the machine
    if choice == "off":
        is_on = False
    # secret code to see amount of resources and money
    elif choice == "report":
        coffee_maker.report()
        money_machine.report()
    else:
        # make a drink from the menu if enough resources
        drink = menu.find_drink(choice)
        if coffee_maker.is_resource_sufficient(drink) and money_machine.make_payment(drink.cost):
            coffee_maker.make_coffee(drink)
