Author: Lukas Geiger
Date: October 8, 2019
Description: ClickTime Taco Assembler

Initialization:
Run 'python tacoAssembly.py' in your unix commandline and run on localhost
Requirments: Flask (not provided) and Bootstrap (provided)

Workflow:

1 - Welcome: User arrives at welcome page and clicks 'Get Started' or 'Random Taco'
2 - Taco Assembly: Launch Taco Assembly Workflow (Guides the user through a series of options)
3 - Shopping Cart: Show final product in a window and allow user to delete item
    This step uses global variables to track items in user's shopping cart which creates problems when the
    cart page is refreshed. To make this more stable I would use SQLite or some other SQL database to store user's tacos.
4 - Checkout: thank the user and says goodbye
