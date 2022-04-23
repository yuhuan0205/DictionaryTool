from App import App

                
if __name__ == "__main__":
    app = App.App()
    app.after(500,app.change)
    app.run()


