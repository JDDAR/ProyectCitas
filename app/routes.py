from . import app, db
from .models import Medico, Paciente, Consultorio, Cita 
from flask import render_template, request, flash, redirect

##Creando ruta inicio home index 

@app.route('/')
def home_index():
    return render_template('home/index.html')


@app.route('/medicos')
def get_all_medicos():
    medicos = Medico.query.all()
    return render_template('medicos/medicos.html', medicos = medicos) 

@app.route('/pacientes')
def get_all_pacientes():
    pacientes = Paciente.query.all()
    return render_template('pacientes/pacientes.html', pacientes = pacientes)

@app.route('/consultorios')
def get_all_consultorios():
    consultorios = Consultorio.query.all()
    return render_template('consultorios/consultorios.html', consultorios = consultorios )

@app.route('/citas')
def get_all_citas():
    citas = Cita.query.all()
    return render_template("citas/citas.html", citas = citas)


############# rutas para selecionar detalles 

@app.route('/medicos/<int:id>')
def get_medico_by_id(id):
    ##return 'id del medico: ' + str(id)
    #traer el medico por id utilizando la entidad medico 
    medico = Medico.query.get(id)
    return render_template('medicos/medico.html', medicoId = medico)

@app.route('/pacientes/<int:id>')
def get_paciente_by_id(id):
    paciente = Paciente.query.get(id)
    return render_template('pacientes/paciente.html', pacienteId = paciente)

@app.route('/consultorios/<int:id>')
def get_consultorio_by_id(id):
    consultorio = Consultorio.query.get(id)
    return render_template('consultorios/consultorio.html', consultorioId = consultorio)

@app.route('/citas/<int:id>')
def get_citas_by_id(id):
    citas = Cita.query.get(id)
    return render_template('citas/cita.html', citaId = citas)


################ Creando rutas pra nuevo medico 
@app.route('/medicos/create' , methods = [ 'GET' , 'POST'])
def create_medico():
    ##Mostrar el formulario: metodo GET  
    if( request.method == 'GET' ):
        especialidades = [
            'Cardiologia',
            'Pediatria',
            'Psicologia'
        ]
        return render_template('medicos/medico_form.html', especialidades = especialidades)
    ##cuando el usuario preiona el boton de guardar 
    ##los datos del formulario viajan al servidor utilisando el metodo POST
    elif( request.method == 'POST'):
        #cuando se presiona 'crear'
        ##return request.form['especialidad']
        new_medico = Medico(nombres = request.form['nombres'],
                            apellidos = request.form['apellidos'],
                            tipo_identificacion = request.form['tipoID'],
                            numero_identificacion = request.form['numeroID'],
                            registro_medico = request.form['registroMedico'],
                            especialidad = request.form['especialidad']
                            )
        ##añadirlo a sqlalchemy 
        db.session.add(new_medico)
        db.session.commit()
        flash('Medico registrado exitosamente', 'actualizado')
        return redirect('/medicos')

############### Creando rutas para nuevo paciente 
@app.route('/pacientes/create', methods = ['GET' , 'POST'])
def create_paciente():
    if(request.method == 'GET'):
        return render_template('pacientes/paciente_form.html')
    elif(request.method == 'POST'):
        new_paciente = Paciente(nombres = request.form['nombres'],
                                apellidos = request.form['apellidos'],
                                tipo_identificacion = request.form['tipoID'],
                                numero_identificacion = request.form['numeroID'],
                                altura = request.form['altura'],
                                tipo_sangre = request.form['tipoSangre']
                                )
        db.session.add(new_paciente)
        db.session.commit()
        flash("Paciente registrado exitosamente")
        return redirect('/Pacientes')

############## Creando Nuevos consultorios 

@app.route('/consultorios/create', methods = ['GET', 'POST'])
def create_consultorio():
    if(request.method == 'GET'):
        return render_template('consultorios/consultorio_form.html')
    elif(request.method == 'POST'):
        new_consultorio = Consultorio( numero = request.form['numero'] )
    db.session.add(new_consultorio)
    db.session.commit()
    flash("Consultorio registrado exitosamente")
    return redirect('/consultorios')

############## Creando nuevas citas  

@app.route('/citas/create', methods = ['GET', 'POST'])
def create_cita():
    if(request.method == 'GET'):
        return render_template('citas/cita_form.html') 

############# Actualizaciones de datos  
@app.route('/medicos/update/<int:id>', methods = ['GET', 'POST'])
def update_medico(id):
    especialidades = [ 'Cardiologia', 'Pediatria','Psicologia']
    medico_update = Medico.query.get(id)
    if(request.method == 'GET'):
        return render_template('medicos/medico_update.html', medico_update = medico_update, especialidades = especialidades)
    elif(request.method == 'POST'):
        medico_update.nombres = request.form['nombres']
        medico_update.apellidos = request.form['apellidos']
        medico_update.tipo_identificacion = request.form['tipoID']
        medico_update.numero_identificacion = request.form['numeroID']
        medico_update.registro_medico = request.form['registroMedico']
        medico_update.especialidad = request.form['especialidad']
        db.session.commit()
        flash("Medico actualizado exitosamente")
        return redirect('/medicos')

@app.route('/pacientes/update/<int:id>', methods = ['GET', 'POST'])
def update_paciente(id):
    paciente_update = Paciente.query.get(id)
    if(request.method == 'GET'):
        return render_template('pacientes/paciente_update.html', paciente_update = paciente_update)


############## Eliminando registro 

@app.route('/medicos/delete/<int:id>')
def delete_medico(id):
    medico_delete = Medico.query.get(id)
    db.session.delete(medico_delete)
    db.session.commit()
    flash('Eliminado exitosamente', 'delete')
    return redirect('/medicos')



    
