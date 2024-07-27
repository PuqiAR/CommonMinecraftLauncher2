import sys
import os


file_header = """
#############################
# Common Minecraft Launcher #
# %s module,part of CMCL    #
# copyright PuqiAR@2024     #
#############################
"""

env = os.path.dirname(os.path.dirname(__file__))
os.chdir(env)
def exit_console():
    sys.exit(0)
def new_form():
    form_name = input(' enter form name:')
    with open(f"QtUi/{form_name}.py","w") as _:
        if (os.path.exists(f'QtUi/{form_name}.ui')):
            print('making py file from ui file...')
            os.system(f'pyuic5 -x QtUi/{form_name}.ui -o QtUi/{form_name}.py')
        else:
            print('No ui file found,create a ui file first')
            with open(f"QtUi/{form_name}.py","w") as f1:
                f1.write('')
            print('making py file from ui file...')
            os.system(f'pyuic5 -x QtUi/{form_name}.ui -o QtUi/{form_name}.py')
    print(f'New form {form_name}.ui created')
def convert_ui():
    form_name = input(' enter form name:')
    print('making py file from ui file...')
    os.system(f'pyuic5 -x QtUi/{form_name}.ui -o QtUi/{form_name}.py')
def new_code_file():
    file_name = input(' enter code file name:')
    with open(f"CMCL/{file_name}.py","w") as f:
        f.write(file_header % file_name)
text:str = ''
commands = {
    'exit': exit_console,
    'newf': new_form,
    'uic': convert_ui,
    'newc': new_code_file,

}

print('CMCL Dev Console 1.0 by PuqiAR')
print('Env path:',env)
print('Starting repl...')
while True:
    text = input('>>>')
    if text in commands:
        commands[text]()
    else:
        print('Command not found')