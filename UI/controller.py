import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.selectedForma = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []
        self.selectedAnno=None

    def fillDD(self):
        self._view.ddyear.options.clear()
        anni=self._model.getAnni()
        anniDD=list(map(lambda x: ft.dropdown.Option(key=x,on_click=self.getSelectedAnno),anni))
        self._view.ddyear.options=anniDD
        self._view.update_page()
        pass

    def fillDDForme(self):
        self._view.ddshape.options.clear()
        forme=self._model.getForme(self.selectedAnno)
        formeDD=list(map(lambda x: ft.dropdown.Option(key=x,on_click=self.getSelectedForma),forme))
        self._view.ddshape.options=formeDD
        self._view.update_page()


    def handle_graph(self, e):
        self._view.txt_result.clean()
        if self.selectedAnno is None:
            self._view.create_alert("Inserire anno")
            return
        if self.selectedForma is None:
            self._view.create_alert("Inserire forma")
            return
        res=self._model.creaGrafo(self.selectedAnno, self.selectedForma)
        n,a= self._model.getDetails()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con {n} nodi e {a} archi"))
        for a in res.keys():
            self._view.txt_result.controls.append(ft.Text(f"Nodo: {a}. Somma: {res[a]}"))
        self._view.update_page()
        pass
    def handle_path(self, e):
        res,maxD=self._model.cammino()
        self._view.txtOut2.controls.append(ft.Text(f"Distanza max: {maxD}"))
        for a in res:
            self._view.txtOut2.controls.append(ft.Text(f"{a[0]} -- {a[1]}, peso: {a[2]}, distanza: {a[3]}"))
        self._view.update_page()
        pass

    def getSelectedAnno(self,e):
        if e.control.key is None:
            pass
        else:
            self.selectedAnno=e.control.key
            self.fillDDForme()


    def getSelectedForma(self,e):
        if e.control.key is None:
            pass
        else:
            self.selectedForma=e.control.key