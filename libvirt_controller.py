import libvirt
import xml.etree.ElementTree as ET

def connect_libvirt():
    try:
        conn = libvirt.open('qemu:///system')
        return conn
    except libvirt.libvirtError as e:
        print(f"Erro ao conectar com o LibVirt: {e}")
        return None

def list_vms():
    conn = connect_libvirt()
    if conn:
        domains = conn.listAllDomains(0)
        vms = []
        for domain in domains:
            state, reason = domain.state()
            vm_info = {
                'name': domain.name(),
                'id': domain.ID(),
                'state': state,
            }
            vms.append(vm_info)
        conn.close()
        return vms
    else:
        return []

def start_vm(vm_name):
    conn = connect_libvirt()
    if conn:
        try:
            domain = conn.lookupByName(vm_name)
            domain.create()
            conn.close()
            return True
        except libvirt.libvirtError as e:
            print(f"Erro ao iniciar a VM {vm_name}: {e}")
            conn.close()
            return False

def shutdown_vm(vm_name):
    conn = connect_libvirt()
    if conn:
        try:
            domain = conn.lookupByName(vm_name)
            domain.shutdown()
            conn.close()
            return True
        except libvirt.libvirtError as e:
            print(f"Erro ao desligar a VM {vm_name}: {e}")
            conn.close()
            return False

# Continue implementando outras funções (definir_vm, delete_vm, etc.)
