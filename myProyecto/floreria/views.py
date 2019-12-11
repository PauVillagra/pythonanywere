from django.shortcuts import render
from .models import Flores 
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login as auth_login
from django.contrib.auth.decorators import login_required
from .clases import elemento
from .forms import CustomUserForm


# Create your views here.
def home_administrador(request):
    return render(request,'core/home_administrador.html')

def home_usuario(request):
    return render(request,'core/home_usuario.html')

def galeria_administrador(request):
    flores=Flores.objects.all()
    return render(request,'core/galeria_administrador.html',{'listaFlores':flores})

def galeria_usuario(request):
    flores=Flores.objects.all()
    #SE TOMAN LAS FLORES QUE SE HAYAN INGRESADO A LA LISTA 
    return render(request,'core/galeria_usuario.html',{'listaFlores':flores})

def formulario(request):
    florr=Flores.objects.all()
    if request.POST:
        Name=request.POST.get("txtNombre")
        Valor=request.POST.get("txtValor")
        Descripcion=request.POST.get("txtDesc")
        Estado=request.POST.get("txtEstado")
        Stock=request.POST.get("txtStock")
        Imagen=request.FILES.get("txtImagen")
        flor=Flores(
            name=Name,
            valor=Valor,
            descripcion=Descripcion,
            estado=Estado,
            stock=Stock,
            imagen=Imagen
        )
        flor.save() #graba el objeto e bdd
        return render(request,'core/formulario.html',{'lista':florr,'msg':'grabo','sw':True})
    return render(request,'core/formulario.html',{'lista':florr})#pasan los datos a la web

def eliminar_flor(request,id): 
    flor=Flores.objects.get(name=id)
    flor.delete()
        
    return HttpResponse("<script> ;window.location.href='/galeria/';</script>")

def login_inicio(request):
    if request.POST:
        u=request.POST.get("txtUsuario")
        c=request.POST.get("txtPassword")
        #VALIDACION DEL USUARIO
        usu=authenticate(request,username=u,password=c)
        msg=''
        request.session["carrito"] = []        
        request.session["carritox"] = []   
        if usu is not None and usu.is_active:
            if usu.is_staff:
                auth_login(request, usu)
                arreglo={'nombre':u, 'contrasena':c, 'tipo':'administrador'}
                return render(request,'core/home_administrador.html',arreglo)
            else:
                arreglo={'nombre':u, 'contrasena':c, 'tipo':'cliente'}
                return render(request,'core/home_usuario.html',arreglo)
        variables={
            'msg':'no existe nada'
        }
    return render(request,'core/login.html',variables)

def login(request):
    return render(request,'core/login.html')

def cerrar_sesion(request):
    logout(request)
    return HttpResponse("<script>;window.location.href='/';</script>")

def carrito(request):
    
    x=request.session["carritox"]
    suma=0
    for item in x:
        suma=suma+int(item["total"])           
    return render(request,'core/carrito.html',{'x':x,'total':suma})

def agregar_carro(request,id):

    f=Flores.objects.get(name=id)
    
    x=request.session["carritox"]
    el=elemento(1,f.name,f.valor,1)
    sw=0
    suma=0
    clon=[]
    for item in x:        
        cantidad=item["cantidad"]
        if item["nombre"]==f.name:
            sw=1
            cantidad=int(cantidad)+1
        ne=elemento(1,item["nombre"],item["valor"],cantidad)
        suma=suma+int(ne.total())
        clon.append(ne.toString())
    

    if sw==0:
        clon.append(el.toString())
    x=clon    
    request.session["carritox"]=x
    flores=Flores.objects.all()
    return HttpResponse("<script> ;window.location.href='/galeria_usuario/',{'flores':flores,'total':suma};</script>")

def vaciar_carrito(request):
    request.session["carritox"]=""
    lista=request.session.get("caritox","")
    return render(request,"core/carrito.html",{'contenido':lista})
    
def grabar_carro(request):
    x=request.session["carritox"]    
    usuario=request.user.username
    suma=0
    try:
        for item in x:        
            producto=item["nombre"]
            valor=int(item["valor"])
            cantidad=int(item["cantidad"])
            total=int(item["total"])        
            compra=Compra(
                usuario=usuario,
                producto=producto,
                valor=valor,
                cantidad=cantidad,
                total=total,
                fecha=datetime.date.today()
            )
            compra.save()
            suma=suma+int(total)  
            print("reg grabado")                 
        mensaje="Grabado"
        request.session["carritox"] = []
    except:
        mensaje="error al grabar"            
    return render(request,'core/carrito.html',{'x':x,'total':suma,'mensaje':mensaje})

def carro_compras_mas(request,id):
    f=Flores.objects.get(name=id)
    x=request.session["carritox"]
    suma=0
    clon=[]
    for item in x:        
        cantidad=item["cantidad"]
        if item["nombre"]==f.name:
            cantidad=int(cantidad)+1
        ne=elemento(1,item["nombre"],item["valor"],cantidad)
        suma=suma+int(ne.total())
        clon.append(ne.toString())
    x=clon    
    request.session["carritox"]=x
    x=request.session["carritox"]        
    return render(request,'core/carrito.html',{'x':x,'total':suma})

def carro_compras_menos(request,id):
    f=Flores.objects.get(name=id)
    x=request.session["carritox"]
    suma=0
    clon=[]
    for item in x:        
        cantidad=item["cantidad"]
        if item["nombre"]==f.name:
            cantidad=int(cantidad)-1
        ne=elemento(1,item["nombre"],item["valor"],cantidad)
        suma=suma+int(ne.total())
        clon.append(ne.toString())
    x=clon    
    request.session["carritox"]=x
    x=request.session["carritox"]        
    return render(request,'core/carrito.html',{'x':x,'total':suma})

def registro(request):
    data={
        'form':CustomUserForm()
    }
    if request.method=='POST': 
        formulario=CustomUserForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            username=formulario.cleaned_data['username']
            password=formulario.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            login(request)
            return redirect(to='home_usuario')
    return render(request,'core/registro.html',data)   