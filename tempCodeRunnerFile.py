        if menu_button.collidepoint((mouse.mx, mouse.my)):
            if click:
                problemGenerator.needsNewProblem = True
                main_menu()
                isProgramRunning = False
                break