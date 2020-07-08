from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile, askopenfilename
from PIL import Image, ImageTk
import sqlite3
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfile
from Modulos import LeituraArquivos,ConfusionMatrix, ProcessamentoDoSinal, LeituraEventos, AssociaTrechoEvento, CriaImagen, CNN

#from ../ProcessamentoSinais/Python/main.py import 


# FILES
sinal_eeg = []
eventos = []


# ------------  HOME SCREEN   ---------------------------------------------
raiz = Tk()
raiz.title("Epilepsy Detection")
raiz.resizable(0, 0)
raiz.geometry("1024x768")
raiz.config(bg="#DFEBE9")

# ------------------ IMAGES AND LOGOS INTO HOME SCREEN -------------------


logo_cerebro = PhotoImage(file="logos/cerebrito.png")
Label(raiz, image=logo_cerebro, bg="#DFEBE9").place(x=64, y=55)

logo_ufmg= Image.open("logos/ufmg _logo.png")
resized_ufmg= logo_ufmg.resize((100,42), Image.ANTIALIAS)
logo_ufmg_resized=ImageTk.PhotoImage(resized_ufmg)
Label(raiz, image=logo_ufmg_resized,bg="#DFEBE9").place(x=670,y=691)

logo_labbio = Image.open("logos/labbio_logo.png")
resized_labbio = logo_labbio.resize((100, 52), Image.ANTIALIAS)
logo_labbio_resized = ImageTk.PhotoImage(resized_labbio)
Label(raiz, image=logo_labbio_resized, bg="#DFEBE9").place(x=840, y=686)

# ------------------ Images and logos into Information Screen ------------

logo_cerebro_solo = Image.open("logos/cerebro_solo.png")
resized_cerebro = logo_cerebro_solo.resize((400, 400), Image.ANTIALIAS)
logo_cerebro_resized = ImageTk.PhotoImage(resized_cerebro)

resized_ufmg2= logo_ufmg.resize((150,63), Image.ANTIALIAS)
logo_ufmg_resized2=ImageTk.PhotoImage(resized_ufmg2)


resized_labbio2 = logo_labbio.resize((150, 78), Image.ANTIALIAS)
logo_labbio_resized2 = ImageTk.PhotoImage(resized_labbio2)



# -----------------  Open Information Screen ------------------------------
def info():
    Ventana_info = Toplevel()
    Ventana_info.geometry("1024x768")
    Ventana_info.config(bg="#DFEBE9")
    Ventana_info.title("About")
    Label(Ventana_info, image=logo_cerebro_resized, bg="#DFEBE9").place(x=550, y=55)
    Label(Ventana_info, image=logo_ufmg_resized2, bg="#DFEBE9").place(x=709, y=465)
    Label(Ventana_info, image=logo_labbio_resized2, bg="#DFEBE9").place(x=709, y=574)
    titulo_info = Label(Ventana_info, text="About Project",
                        font=("AvantGarde", 40, "bold"), bg="#DFEBE9",
                        fg="#14787A").place(x=10, y=20)
    Boton_home = Button(Ventana_info, text="Home", command=Ventana_info.destroy,
                        font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                        width="15", height="1", cursor="hand2").place(x=660, y=700)


# -----------------  Open Add Patient Screen ------------------------------
def add_patient():
    Ventana_add = Toplevel()
    Ventana_add.geometry("1024x768")
    Ventana_add.config(bg="#DFEBE9")
    Ventana_add.title("Patient Registration Form")
    
    reg = Frame(Ventana_add)

    Fullname = StringVar()
    Informations = StringVar()

    conn = sqlite3.connect('Form.db')
    with conn:
        cursor = conn.cursor()

    def database():
        name = Fullname.get()
        Informations = Informations.get()
        gender = var.get()
        age = c.get()
        #prog = var1.get()+var2.get()+var3.get()
        cursor.execute('CREATE TABLE IF NOT EXISTS Patient ( Fullname TEXT,Informations TEXT,Gender TEXT,Age TEXT,Programming TEXT)')
        cursor.execute('INSERT INTO Patient (Fullname,Informations,Gender,Age) VALUES(?,?,?,?)',(name,informations,gender,age))
        conn.commit()
        showinfo( title = "Patient Reacord", message = "Data inserted sucessfully")
     
    def display():
        cursor.execute('SELECT * FROM Patient')
        data = cursor.fetchall()
        print(data)
        output = ''
        for x in data:
            output = output+x[0]+'  '+x[1]+'  '+x[2]+'  '+x[3]+'  '+x[4]+'\n'
        print(output)
        return output

    def delete(conn,task):
        sql ='DELETE FROM Patient WHERE Fullname =?'
        cursor = conn.cursor()
        cursor.execute(sql,task)
        conn.commit()
        showinfo( title = "Patient Reacord", message = "Data deleted sucessfully")
        
    def update(task):
        sql = 'UPDATE Patient SET Email=?, Gender=?, Age=? WHERE Fullname = ?'
        cursor.execute(sql,task)
        conn.commit()
        showinfo( title = "Patient Reacord", message = "Data updated sucessfully")

    def delete_task():
        database = r"Form.db"
        conn = sqlite3.connect(database)
        name = Fullname.get()
        with conn:
            delete_task(conn, name)

    canvas1 = Canvas(Ventana_add, width = 1000, height = 500,  relief = 'raised', bg="#DFEBE9")
    canvas1.pack()

    label1 = Label(Ventana_add, text='Registration Form')
    label1.config(font=("bold", 18),bg="#DFEBE9")
    canvas1.create_window(250, 30, window=label1)
    
    label2 = Label(Ventana_add, text='Fullname :')
    label2.config(font=('helvetica',14),bg="#DFEBE9")
    canvas1.create_window(65, 90, window=label2)

    entry1 = Entry(Ventana_add, textvar = Fullname, font = (14), borderwidth=2, width = 30)
    canvas1.create_window(320, 90, window=entry1)

    label3 = Label(Ventana_add, text='Info:')
    label3.config(font=('helvetica',14),bg="#DFEBE9")
    canvas1.create_window(65, 140, window=label3)

    entry2 = Entry (Ventana_add, textvar = Informations, font = (14), borderwidth=2, width = 30) 
    canvas1.create_window(320, 140, window=entry2)

    label4 = Label(Ventana_add, text='Gender :')
    label4.config(font=('helvetica',14),bg="#DFEBE9")
    canvas1.create_window(65, 190, window=label4)

    var = StringVar()
    rd1 = Radiobutton(Ventana_add ,text="Male" ,padx = 5, variable = var, value = "Male  ")
    rd1.config(font=('helvetica',14),bg="white")
    canvas1.create_window(200,190, window = rd1)

    rd2 = Radiobutton(Ventana_add ,text="Female" ,padx = 20, variable = var, value = "Female")
    rd2.config(font=('helvetica',14),bg="white")
    canvas1.create_window(350,190, window = rd2)

    label5 = Label(Ventana_add, text='Age :')
    label5.config(font=('helvetica',14),bg="#DFEBE9")
    canvas1.create_window(65, 240, window=label5)

    list1 = ['0-21','22-45','46-70','71-']
    c=StringVar()
    droplist = OptionMenu(Ventana_add,c,*list1)
    droplist.config(font=('helvetica',14),bg="white",width = 27)
    c.set('Select age')
    canvas1.create_window(320,240, window = droplist)

    label6 = Label(Ventana_add, text='Update file EDF:')
    label6.config(font=('helvetica',14),bg="#DFEBE9")
    canvas1.create_window(65, 300, window=label6)

    var = StringVar()
    rd3 = Button(Ventana_add ,text="File" ,padx = 5, command = lambda:open_file(sinal_eeg))
    rd3.config(font=('helvetica',14),bg="white")
    canvas1.create_window(200,300, window = rd3)

    label7 = Label(Ventana_add, text='Update file TSE:')
    label7.config(font=('helvetica',14),bg="#DFEBE9")
    canvas1.create_window(65, 350, window=label7)

    var = StringVar()
    rd4 = Button(Ventana_add ,text="File" ,padx = 5, command = lambda:open_file_tse(eventos))
    if sinal_eeg !=  None:
        print("Existe")
    rd4.config(font=('helvetica',14),bg="white")
    canvas1.create_window(200,350, window = rd4)


    # DOIS ARQUIVOS : .edf .tse
    def open_file(sinal_eeg):
        aux = LeituraArquivos.ImportarSinalEEG()
        sinal_eeg.append(aux)
        #return sinal_eeg

    # DOIS ARQUIVOS : .edf .tse
    def open_file_tse(eventos):
        aux = LeituraEventos.importar_evento()
        eventos.append(aux)
        #return eventos


    def main():
        name = Fullname.get()
        Informations = Informations.get()
        gender = var.get()
        age = c.get()
        #prog = var1.get()+var2.get()+var3.get()    
        update(name,Informations,gender,age)


    # Clasificação 
    # daqui vai para a outra tela, com os resultados
    # depois pegar os resultados e os dados do paciente e colocar no database
    # enviar mensagem de registro concluido

    button1 = Button(Ventana_add, text='   Classificar   ',command=lambda :classificacao(sinal_eeg,eventos), bg="#14787A", fg="#ffffff", font=('helvetica', 12, 'bold'))
    canvas1.create_window(150, 450, window=button1)

    # Colocar esta parte na Open Pat.
    button2 = Button(Ventana_add, text='   Update   ',command=lambda :(text.delete(1.0,END),text.insert(END,display())), bg="#14787A", fg="#ffffff", font=('helvetica', 12, 'bold'))
    canvas1.create_window(300, 450, window=button2)


    text = Text(Ventana_add,  height=25, width=50)
    text.config(font=('helvetica',12),bg="white")
    canvas1.create_window(750, 270, window=text)

    lblDisplay = Label(Ventana_add,  text = "Patient Data")
    lblDisplay.config(font=('Helvetica',18,'bold'),fg='black',justify=CENTER,bg="#DFEBE9")
    canvas1.create_window(750, 25, window=lblDisplay)
  
    Boton_home = Button(Ventana_add, text="Home", command=Ventana_add.destroy,
                        font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                        width="15", height="1", cursor="hand2").place(x=700, y=700)


# -----------------  Open Open Patient Screen ------------------------------
def open_patient():
    #raiz.withdraw()
    Ventana_open = Toplevel()
    Ventana_open.geometry("1024x768")
    Ventana_open.config(bg="#DFEBE9")
    Ventana_open.title("Open Patient")
    Boton_home = Button(Ventana_open, text="Home", command=Ventana_open.destroy,
                        font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                        width="15", height="1", cursor="hand2").place(x=700, y=700)


#--------------------- TELA DE CLASSIFICAÇÃO --------------------------------
# TODO Juntar com o código do Arthur
# def main_processamento(sinal_eeg, eventos):

# Criar gráficos
# Criar animação do processo -> que está processando (barra de progre.)
# -----------------  Open Open Patient Screen ------------------------------
def classificacao(sinal_eeg,eventos):
    #raiz.withdraw()
    print("Aqui estou")
    Ventana_open = Toplevel()
    Ventana_open.geometry("1024x768")
    Ventana_open.config(bg="#DFEBE9")
    Ventana_open.title("Classificacao")
    # Recebe código do arthur e executa
    sinal_eeg = sinal_eeg[0]
    eventos = eventos[0]
    print(sinal_eeg)

    fs = sinal_eeg.frequencia_de_amostragem

    sinal_delta_theta = sinal_eeg.decomporSinalEmFaixaDeFrequencia([1, 7])
    sinal_alpha_beta = sinal_eeg.decomporSinalEmFaixaDeFrequencia([8, 30])
    sinal_gama = sinal_eeg.decomporSinalEmFaixaDeFrequencia([31, 100])

    delta_theta_dividido = ProcessamentoDoSinal.dividir_sinal(sinal_delta_theta, fs)
    alpha_beta_dividido = ProcessamentoDoSinal.dividir_sinal(sinal_alpha_beta, fs)
    gama_dividido = ProcessamentoDoSinal.dividir_sinal(sinal_gama, fs)

    AssociaTrechoEvento.associa_trecho_evento(delta_theta_dividido, eventos)
    AssociaTrechoEvento.associa_trecho_evento(alpha_beta_dividido, eventos)
    AssociaTrechoEvento.associa_trecho_evento(gama_dividido, eventos)

    dados = CriaImagen.cria_imagens_saidas(gama_dividido, delta_theta_dividido, alpha_beta_dividido)

    classification_info = CNN.CNN_fit(dados[0], dados[1])

    # classification_info é um array com a estrutura [accuracy, precision, cm]

    print("\nAccuracy:")
    print(classification_info[0])

    print("\nPrecision:")
    print(classification_info[1])

    cm_plot_labels = ["Normal", "Epilepsy"]
    ConfusionMatrix.plot_confusion_matrix(classification_info[2], cm_plot_labels, title="Confusion Matrix")

    # Colocar uma animação enquanto estiver rodando de um timer (já está quase pronta)
    # Quando terminar de executar colocar um botão ver resultados
    #button7 = Button(Ventana_add, text='   Ver resultado   ',command=resultado, bg="#14787A", fg="#ffffff", font=('helvetica', 12, 'bold'))
    #canvas3.create_window(150, 450, window=button1)
    Boton_home = Button(Ventana_open, text="Home", command=Ventana_open.destroy,
                        font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                        width="15", height="1", cursor="hand2").place(x=700, y=700)

#------------------ TELA Informações da rede ---------------------------------
# TODO mostrar parte da detecção e outras informações do resultado
def resultado():
    #raiz.withdraw()
    Ventana_open = Toplevel()
    Ventana_open.geometry("1024x768")
    Ventana_open.config(bg="#DFEBE9")
    Ventana_open.title("Resultados")
    # Recebe código do arthur e executa (código receve content e content2 como entrada)
    # Colocar uma animação enquanto estiver rodando de um timer (já está quase pronta)
    Boton_home = Button(Ventana_open, text="Home", command=Ventana_open.destroy,
                        font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                        width="15", height="1", cursor="hand2").place(x=700, y=700)

    #Adicionar botão que vai para a outra ventana de informações

    # Botão para salvar no dataset




# ---------------  Buttons into home screen ----------------------------------


Boton_info = Button(raiz, text="Abaut", command=info,
                    font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                    width="15", height="1", cursor="hand2").place(x=700, y=101)

Boton_add = Button(raiz, text="Add Pacient", command=add_patient,
                   font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                   width="15", height="1", cursor="hand2").place(x=700, y=230)

Boton_open = Button(raiz, text="Open Patient", command=open_patient,
                    font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                    width="15", height="1", cursor="hand2").place(x=700, y=359)

Boton_close = Button(raiz, text="Close", command=raiz.quit,
                     font=("AvantGarde", 20, "bold"), bg="#14787A", fg="#ffffff",
                     width="15", height="1", cursor="hand2").place(x=700, y=488)






raiz.mainloop()