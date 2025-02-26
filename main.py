from controllers.Controller import Controller
from models.Model import Model
from views.View import View

if __name__ == '__main__':
    model = Model()
    view = View(model, None)
    controller = Controller(model, view)
    view.set_controller(controller)
    view.mainloop() # Koodi "viimane" rida