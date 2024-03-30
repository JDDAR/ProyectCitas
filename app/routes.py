from . import app, db
from .models import Medico, Paciente, Consultorio, Cita 
from flask import render_template, request, flash, redirect
from datetime import datetime

######### RUTAS INICIO _ PRINCIPALES ########################################
#############################################################################

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


############# SELECIONANDO DETALLES DEL USUARIO ############################
############################################################################

## Detalles de medico ##
@app.route('/medicos/<int:id>')
def get_medico_by_id(id):
    medico = Medico.query.get(id)
    if(request.method == 'GET'):
        flash("Detalles del Medico", 'menssageDetails')
        return render_template('medicos/medicos.html', medicoId = medico)

## Detalle de paciente ## 
@app.route('/pacientes/<int:id>', methods = ['GET', 'POST'])
def get_paciente_by_id(id):
    paciente = Paciente.query.get(id)
    if(request.method == 'GET'):
        flash("Detalles del paciente", 'menssageDetails')
        return render_template('/pacientes/pacientes.html', pacienteId = paciente)

## Detalle de consultorio ##
@app.route('/consultorios/<int:id>')
def get_consultorio_by_id(id):
    consultorio = Consultorio.query.get(id)
    if(request.method == 'GET'):
        flash('Detalles del consultorio', 'menssageDetails')
        return render_template('consultorios/consultorios.html', consultorioId = consultorio)

## Detalle de citas ##
@app.route('/citas/<int:id>', methods = ['GET', 'POST'])
def get_citas_by_id(id):
    citas = Cita.query.get(id)
    if(request.method == 'GET'):
        flash('Detalles de la cita', 'menssageDetails')
        return render_template('citas/citas.html', citaId = citas)


################ CREANDO USUARIOS ########################################
##########################################################################

## Creando Medico ##
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
    elif( request.method == 'POST'):
        medicoV = request.form['numeroID']
        medicos = Medico.query.all()
        nIdentificacion = [medico.numero_identificacion for medico in medicos]
        if medicoV in str(nIdentificacion):
            flash("El medico con identificacion: " + medicoV + " ya existe", 'existe')
            return redirect('/medicos/create')
        else:
            new_medico = Medico(nombres = request.form['nombres'],
                            apellidos = request.form['apellidos'],
                            tipo_identificacion = request.form['tipoID'],
                            numero_identificacion = request.form['numeroID'],
                            registro_medico = request.form['registroMedico'],
                            especialidad = request.form['especialidad']
                            )
            db.session.add(new_medico)
            db.session.commit()
            flash('Medico registrado exitosamente', 'exito')
            return redirect('/medicos/create')

## Creando Paciente ##
@app.route('/pacientes/create', methods = ['GET' , 'POST'])
def create_paciente():
    if(request.method == 'GET'):
        return render_template('pacientes/paciente_form.html' )
    elif(request.method == 'POST'):
        pacienteV = request.form['numeroID']
        pacientes = Paciente.query.all()
        ## Creando una lista para almacenar los numeros de idenificaciones
        nIdentificacion = [paciente.numero_identificacion for paciente in pacientes]
        ## Creo la condicional para 
        if pacienteV in str(nIdentificacion):
            flash("El paciente con identificacion:\n" + pacienteV + " ya existe", "existe" )
            return redirect('/pacientes/create')
        else:
            new_paciente = Paciente(nombres = request.form['nombres'],
                                apellidos = request.form['apellidos'],
                               tipo_identificacion = request.form['tipoID'],
                               numero_identificacion = request.form['numeroID'],
                               altura = request.form['altura'],
                               tipo_sangre = request.form['tipoSangre']
                                )
            db.session.add(new_paciente)
            db.session.commit()
            flash("Paciente registrado exitosamente", "exito")
            return redirect('/pacientes/create')

## creando Consultorio ## 
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

## Creando Citas ##
@app.route('/citas/create', methods = ['GET', 'POST'])
def get_cita_paciente():
    if(request.method == 'GET'): 
        return render_template('citas/cita_form.html' )
    elif(request.method == 'POST'):
        especialidad = [ 'Cardiologia', 'Pediatria', 'Psicologia']
        identPaciente = request.form['identificacion']
        paciente = Paciente.query.all()
        return render_template('citas/cita_formNext2.html', paciente = paciente, identPaciente = identPaciente, especialidad = especialidad)

@app.route('/citas/create/asignacion', methods = ['GET', 'POST'])
def get_cita_medico():
    if(request.method == 'GET'):
        return render_template('citas/cita_formNext2.html')
    elif(request.method == 'POST'):
        identPaciente = request.form['identificacion']
        especialidadSelect = request.form['especialidad']
        paciente = Paciente.query.all()
        medico = Medico.query.all()
        consul = Consultorio.query.all()
        return render_template('citas/cita_formNext3.html', 
                               identPaciente = identPaciente,
                               especialidadSelect = especialidadSelect,
                               paciente = paciente,
                               medico = medico, 
                               consultorios = consul               
                               )
@app.route('/citas/create/asignacionCreate', methods = ['GET', 'POST'])
def get_create_cita():
    if(request.method == 'GET'):
        return render_template('citas/cita_formNext3.html')
    elif(request.method == 'POST'):
        new_cita = Cita( fecha = datetime.strptime(request.form['data'], '%Y-%m-%dT%H:%M'),
                         paciente_id = str(request.form['idPaciente']),
                         medico_id = str(request.form['doctor']),
                         consultorio_id = str(request.form['consultorio'])
                        )
        db.session.add(new_cita)
        db.session.commit()
        flash('Cita asignada')
        return redirect('/citas')

############# ACTUALIZACION DE DATOS ##########################
#################################################################

##Actualizando Medicos ##
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
        flash("Medico actualizado exitosamente", 'upgrade')
        return redirect('/medicos')

## Actualizando Pacientes ##
@app.route('/pacientes/update/<int:id>', methods = ['GET', 'POST'])
def update_paciente(id):
    paciente_update = Paciente.query.get(id)
    if(request.method == 'GET'):
        return render_template('pacientes/paciente_update.html', paciente_update = paciente_update)
    elif(request.method == 'POST'):
        paciente_update.nombres = request.form['nombres']
        paciente_update.apellidos = request.form['apellidos']
        paciente_update.tipo_identificacion = request.form['tipoID']
        paciente_update.numero_identificacion = request.form['numeroID']
        paciente_update.altura = request.form['altura']
        paciente_update.tipo_sangre = request.form['tipoSangre']
        db.session.commit()
        flash("Paciente Actualizado", 'upgrade')
        return redirect('/pacientes')

## Actualizando Consultorios##
@app.route('/consultorios/update/<int:id>', methods = ['GET', 'POST'])
def update_consultorio(id):
    consultorio_update = Consultorio.query.get(id)
    if(request.method == 'GET'):
        return render_template('consultorios/consultorio_update.html', consultorio_update = consultorio_update)
    elif(request.method == 'POST'):
        consultorio_update.numero = request.form['nConsultorio']
        db.session.commit()
        flash('Consultorio Actualizado', 'upgrade')
        return redirect('/consultorios')

#actualizando Cita medica ##
@app.route('/citas/update/<int:id>', methods = ['GET', 'POST'])
def update_cita(id):
    cita_update = Cita.query.get(id)
    consultorios = Consultorio.query.all()
    if(request.method == 'GET'):
        return render_template('citas/citas_update.html', cita_update = cita_update, consultorios = consultorios)
    elif(request.method == 'POST'):
        cita_update.fecha = datetime.strptime(request.form['data'], '%Y-%m-%dT%H:%M')
        cita_update.consultorio_id = request.form['consultorio']
        db.session.commit()
        flash('Cita Medica Actualizada', 'upgrade')
        return redirect('/citas')


############## ELIMINACION DE REGISTROS ######################################
##########################################################################

##Eliminando Medico##
@app.route('/medicos/delete/<int:id>', methods = [ 'GET', 'POST'])
def delete_medico(id):
    medico_delete = Medico.query.get(id)
    if(request.method == 'GET'):
        flash("¿Desea eliminar al medico?", 'delete')
        return render_template('/medicos/medicos.html', medicoD = medico_delete)
    elif(request.method == 'POST'):
        idD = request.form['idDelete']
        if idD == str(medico_delete.id):
            db.session.delete(medico_delete)
            db.session.commit()
            flash('El Medico ha sido eliminado', 'deletetwo')
            return redirect('/medicos')

## Eliminando paciente ##
@app.route('/pacientes/delete/<int:id>', methods = ['GET', 'POST'])
def delete_paciente(id): 
    paciente_delete =  Paciente.query.get(id)
    if(request.method == 'GET'):
        flash("desea eliminar al paciente", 'delete')
        return render_template('/pacientes/pacientes.html', pacienteD = paciente_delete)
    elif(request.method == 'POST'):
        idD = request.form['idDelete']
        if idD == str(paciente_delete.id):
            db.session.delete(paciente_delete)
            db.session.commit()
            flash("El paciente ha sido eliminado", 'deletetwo')
            return redirect('/pacientes')

## Eliminando consultorio ## 
@app.route('/consultorios/delete/<int:id>', methods = ['GET', 'POST'])
def delete_consultorio(id):
    consultorio_delete = Consultorio.query.get(id)
    if(request.method == 'GET'):
        flash("¿Desea eliminar el Consultorio?", 'delete')
        return render_template('/consultorios/consultorios.html', consultorioD = consultorio_delete )
    elif(request.method == 'POST'):
        idD = request.form['idDelete']
        if idD == str(consultorio_delete.id):
            db.session.delete(consultorio_delete)
            db.session.commit()
            flash("El Consultorio ha sido eliminado", 'deletetwo')
            return  redirect('/consultorios')

## eliminar Cita medica ## 

@app.route('/citas/delete/<int:id>', methods = ['GET', 'POST'])
def delete_cita(id):
    cita_delete = Cita.query.get(id)
    if(request.method == 'GET'):
        flash("¿Desea eliminar la cita?", 'delete')
        return render_template('/citas/citas.html', citaD = cita_delete)
    elif(request.method == 'POST'):
        idD = request.form['idDelete']
        if idD  == str(cita_delete.id):
            db.session.delete(cita_delete)
            db.session.commit()
            flash("La cita Medica fue eliminada", 'deletetwo')
            return redirect('/citas')


































    
