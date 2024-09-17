from flask import Flask, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from libvirt_controller import list_vms, start_vm, shutdown_vm
from auth import auth_bp, login_manager

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'
app.register_blueprint(auth_bp)
login_manager.init_app(app)

@app.route('/')
@login_required
def index():
    vms = list_vms()
    return render_template('index.html', vms=vms)

@app.route('/start_vm/<vm_name>')
@login_required
def start_vm_route(vm_name):
    success = start_vm(vm_name)
    if not success:
        flash(f"Não foi possível iniciar a VM {vm_name}")
    return redirect(url_for('index'))

@app.route('/shutdown_vm/<vm_name>')
@login_required
def shutdown_vm_route(vm_name):
    success = shutdown_vm(vm_name)
    if not success:
        flash(f"Não foi possível desligar a VM {vm_name}")
    return redirect(url_for('index'))

# Outras rotas (criar_vm, deletar_vm, etc.) podem ser adicionadas aqui

@app.route('/create_vm', methods=['GET', 'POST'])
@login_required
def create_vm():
    if request.method == 'POST':
        vm_name = request.form['vm_name']
        cpu = request.form['cpu']
        ram = request.form['ram']
        disk_size = request.form['disk_size']
        os_type = request.form['os_type']
        # Implemente a lógica para criar a VM com os parâmetros fornecidos
        success = define_vm(vm_name, cpu, ram, disk_size, os_type)
        if success:
            flash(f"VM {vm_name} criada com sucesso!")
            return redirect(url_for('index'))
        else:
            flash(f"Erro ao criar a VM {vm_name}.")
    return render_template('create_vm.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
