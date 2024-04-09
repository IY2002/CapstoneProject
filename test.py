import webbrowser
import os

def call_printer(html_path):
    absolute_path = os.path.abspath(html_path)
    webbrowser.open(absolute_path)
    return


call_printer('CapStone_Print_Ark.html')
call_printer('CapStone_Print_Rollo.html')