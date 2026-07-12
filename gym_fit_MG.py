"""
=============================================================
  GymFit - Sistema de Gestión GYM FIT
  Pantallas: Principal → Menú → Clientes / Membresías /
             Pagos / Asistencia / Reportes e Indicadores
=============================================================
"""


from datetime import date ,timedelta 





class Persona :
    """Clase padre — encapsula datos comunes de cualquier persona."""


    def __init__ (self ,dni :str ,nombre :str ,apellido :str ,telefono :str ):


        self .__dni =dni 
        self .__nombre =nombre 
        self .__apellido =apellido 
        self .__telefono =telefono 



    def get_dni (self )->str :return self .__dni 
    def get_nombre (self )->str :return self .__nombre 
    def get_apellido (self )->str :return self .__apellido 
    def get_telefono (self )->str :return self .__telefono 
    def get_nombre_completo (self )->str :return f"{self .__nombre } {self .__apellido }"



    def set_nombre (self ,nombre :str ):

        if not nombre .strip ():
            raise ValueError ("El nombre no puede estar vacío.")
        self .__nombre =nombre .strip ()

    def set_apellido (self ,apellido :str ):
        if not apellido .strip ():
            raise ValueError ("El apellido no puede estar vacío.")
        self .__apellido =apellido .strip ()

    def set_telefono (self ,telefono :str ):

        if not telefono .isdigit ()or len (telefono )!=9 :
            raise ValueError ("El teléfono debe tener exactamente 9 dígitos numéricos.")
        self .__telefono =telefono 


    def __str__ (self )->str :
        return (f"[Persona] DNI: {self .__dni } | "
        f"{self .get_nombre_completo ()} | Tel: {self .__telefono }")





class Membresia :
    """Clase base — define la interfaz de todas las membresías."""


    PRECIO_BASE :float =0.0 
    DURACION_DIAS :int =0 

    def __init__ (self ):

        self ._fecha_inicio :date =date .today ()

        self ._fecha_fin :date =date .today ()+timedelta (days =self .DURACION_DIAS )

    def calcular_costo (self ,descuento :float =0.0 )->float :
        """Polimorfismo: cada subclase usa su propio PRECIO_BASE."""

        return round (self .PRECIO_BASE *(1 -descuento ),2 )

    def esta_vigente (self )->bool :

        return date .today ()<=self ._fecha_fin 

    def dias_restantes (self )->int :

        return max ((self ._fecha_fin -date .today ()).days ,0 )

    def tipo (self )->str :

        return self .__class__ .__name__ 

    def get_fecha_inicio (self )->date :
        return self ._fecha_inicio 

    def get_fecha_fin (self )->date :
        return self ._fecha_fin 

    def __str__ (self )->str :
        estado ="Vigente ✓"if self .esta_vigente ()else "Vencida ✗"
        return (f"{self .tipo ():22} | S/ {self .PRECIO_BASE :>7.2f} | "
        f"{self ._fecha_inicio } → {self ._fecha_fin } | "
        f"{estado } ({self .dias_restantes ()}d restantes)")



class MembresiaBasica (Membresia ):
    """Mensual — sala de máquinas."""
    PRECIO_BASE =80.0 
    DURACION_DIAS =30 

class MembresiaTrimestral (Membresia ):
    """Trimestral — acceso total + 1 clase grupal/semana."""
    PRECIO_BASE =210.0 
    DURACION_DIAS =90 

class MembresiaAnual (Membresia ):
    """Anual — acceso total + clases grupales ilimitadas."""
    PRECIO_BASE =720.0 
    DURACION_DIAS =365 





class Pago :
    """Registra un pago realizado por un socio."""


    _correlativo :int =1 

    def __init__ (self ,dni_socio :str ,nombre_socio :str ,monto :float ,plan :str ):

        self .__numero =Pago ._correlativo 
        Pago ._correlativo +=1 

        self .__dni_socio =dni_socio 
        self .__nombre_socio =nombre_socio 
        self .__monto =monto 
        self .__plan =plan 
        self .__fecha =date .today ()


    def get_numero (self )->int :return self .__numero 
    def get_dni_socio (self )->str :return self .__dni_socio 
    def get_nombre_socio (self )->str :return self .__nombre_socio 
    def get_monto (self )->float :return self .__monto 
    def get_plan (self )->str :return self .__plan 
    def get_fecha (self )->date :return self .__fecha 

    def comprobante (self )->str :

        sep ="─"*46 
        return (f"\n  {'COMPROBANTE DE PAGO':^44}\n"
        f"  {'GYM FIT':^44}\n"
        f"  {sep }\n"
        f"  N° Comprobante : {self .__numero :04d}\n"
        f"  Fecha          : {self .__fecha }\n"
        f"  DNI cliente    : {self .__dni_socio }\n"
        f"  Nombre         : {self .__nombre_socio }\n"
        f"  Plan           : {self .__plan }\n"
        f"  Monto pagado   : S/ {self .__monto :.2f}\n"
        f"  {sep }\n"
        f"  ¡Gracias por su preferencia! 💪\n")

    def __str__ (self )->str :
        return (f"  #{self .__numero :04d} | {self .__fecha } | "
        f"{self .__nombre_socio :<22} | {self .__plan :<22} | "
        f"S/ {self .__monto :.2f}")





class RegistroAsistencia :
    """Almacena un ingreso diario de un socio."""

    def __init__ (self ,dni_socio :str ,nombre_socio :str ):
        self .__dni_socio =dni_socio 
        self .__nombre_socio =nombre_socio 
        self .__fecha =date .today ()

    def get_dni_socio (self )->str :return self .__dni_socio 
    def get_nombre_socio (self )->str :return self .__nombre_socio 
    def get_fecha (self )->date :return self .__fecha 

    def __str__ (self )->str :
        return (f"  {self .__fecha } | DNI: {self .__dni_socio } | "
        f"{self .__nombre_socio }")





class Socio (Persona ):
    """Socio del gimnasio vinculado a una membresía."""

    def __init__ (self ,dni :str ,nombre :str ,apellido :str ,telefono :str ,membresia :Membresia ):


        super ().__init__ (dni ,nombre ,apellido ,telefono )


        self .__membresia :Membresia =membresia 
        self .__deuda :float =membresia .calcular_costo ()
        self .__pagado :bool =False 
        self .__historial_mem :list [Membresia ]=[membresia ]
        self .__fecha_registro :date =date .today ()


    def get_membresia (self )->Membresia :return self .__membresia 
    def get_deuda (self )->float :return self .__deuda 
    def esta_al_dia (self )->bool :return self .__pagado 
    def get_historial_mem (self )->list :return list (self .__historial_mem )
    def get_fecha_registro (self )->date :return self .__fecha_registro 


    def registrar_pago (self )->Pago :
        """Marca la membresía como pagada y retorna el objeto Pago."""
        monto =self .__deuda 
        self .__pagado =True 
        self .__deuda =0.0 

        return Pago (self .get_dni (),self .get_nombre_completo (),monto ,self .__membresia .tipo ())

    def renovar_membresia (self ,nueva :Membresia ):

        self .__membresia =nueva 
        self .__deuda =nueva .calcular_costo ()
        self .__pagado =False 
        self .__historial_mem .append (nueva )

    def modificar_datos (self ,nombre :str =None ,apellido :str =None ,telefono :str =None ):

        if nombre :self .set_nombre (nombre )
        if apellido :self .set_apellido (apellido )
        if telefono :self .set_telefono (telefono )


    def __str__ (self )->str :
        estado ="Al día ✓"if self .__pagado else f"Deuda: S/ {self .__deuda :.2f}"
        return (f"[Socio    ] DNI: {self .get_dni ()} | "
        f"{self .get_nombre_completo ():<22} | {estado }\n"
        f"            Membresía → {self .__membresia }")





class SocioVIP (Socio ):
    """Socio con 15 % de descuento permanente y entrenador asignado."""

    DESCUENTO =0.15 

    def __init__ (self ,dni :str ,nombre :str ,apellido :str ,telefono :str ,membresia :Membresia ,entrenador :str ):

        super ().__init__ (dni ,nombre ,apellido ,telefono ,membresia )
        self .__entrenador :str =entrenador 



        self ._Socio__deuda =membresia .calcular_costo (self .DESCUENTO )

    def get_entrenador (self )->str :
        return self .__entrenador 

    def renovar_membresia (self ,nueva :Membresia ):

        super ().renovar_membresia (nueva )
        self ._Socio__deuda =nueva .calcular_costo (self .DESCUENTO )

    def __str__ (self )->str :

        return (super ().__str__ ()
        .replace ("[Socio    ]","[Socio VIP]")+
        f"\n            Entrenador: {self .__entrenador } | Desc: 15 %")





class Entrenador (Persona ):
    """Personal trainer con especialidad y bono por socios asignados."""

    BONO_POR_SOCIO =50.0 

    def __init__ (self ,dni :str ,nombre :str ,apellido :str ,telefono :str ,especialidad :str ,sueldo_base :float ):
        super ().__init__ (dni ,nombre ,apellido ,telefono )
        self .__especialidad :str =especialidad 
        self .__sueldo_base :float =sueldo_base 
        self .__socios_asignados :list [str ]=[]

    def get_especialidad (self )->str :return self .__especialidad 
    def get_socios (self )->list :return list (self .__socios_asignados )

    def calcular_sueldo (self )->float :

        bono =len (self .__socios_asignados )*self .BONO_POR_SOCIO 
        return round (self .__sueldo_base +bono ,2 )

    def asignar_socio (self ,dni_socio :str ):

        if dni_socio not in self .__socios_asignados :
            self .__socios_asignados .append (dni_socio )

    def __str__ (self )->str :
        return (f"[Entrenador] DNI: {self .get_dni ()} | "
        f"{self .get_nombre_completo ():<22} | "
        f"{self .__especialidad :<20} | "
        f"Socios: {len (self .__socios_asignados ):>2} | "
        f"Sueldo: S/ {self .calcular_sueldo ():.2f}")





class GymManager :
    """Gestiona socios, membresías, pagos, asistencia y reportes. 
       Es el cerebro central (Controlador) que une todas las piezas."""

    def __init__ (self ,nombre :str ):
        self .__nombre :str =nombre 

        self .__socios :list [Socio ]=[]
        self .__entrenadores :list [Entrenador ]=[]
        self .__pagos :list [Pago ]=[]
        self .__asistencias :list [RegistroAsistencia ]=[]




    def mostrar_dashboard (self ):

        total =len (self .__socios )
        activos =sum (1 for s in self .__socios if s .get_membresia ().esta_vigente ())
        morosos =sum (1 for s in self .__socios if not s .esta_al_dia ())
        ingresos =self .calcular_ingresos_esperados ()
        vencen =self ._socios_por_vencer (7 )

        sep ="─"*60 
        print (f"\n{sep }")
        print (f"  SISTEMA DE GESTIÓN — {self .__nombre .upper ()}")
        print (sep )
        print (f"  Socios totales         : {total }")
        print (f"  Membresías activas     : {activos }")
        print (f"  Membresías vencidas    : {total -activos }")
        print (f"  Socios morosos         : {morosos }")
        print (f"  Ingresos pendientes    : S/ {ingresos :.2f}")
        print (f"  Vencen en 7 días       : {vencen }")
        print (f"  Total asistencias hoy  : {self ._asistencias_hoy ()}")
        print (sep )




    def registrar_socio (self ,socio :Socio ):

        if any (s .get_dni ()==socio .get_dni ()for s in self .__socios ):
            raise ValueError (f"DNI {socio .get_dni ()} ya está registrado.")
        self .__socios .append (socio )
        print (f"  ✔ Socio '{socio .get_nombre_completo ()}' registrado.")

    def buscar_socio (self ,dni :str )->"Socio | None":

        return next ((s for s in self .__socios if s .get_dni ()==dni ),None )

    def buscar_socio_nombre (self ,texto :str )->list [Socio ]:
        """Búsqueda rápida por nombre o apellido (insensible a mayúsculas)."""
        texto =texto .lower ()
        return [s for s in self .__socios if texto in s .get_nombre_completo ().lower ()]

    def modificar_socio (self ,dni :str ,nombre :str =None ,apellido :str =None ,telefono :str =None ):
        s =self .buscar_socio (dni )
        if not s :
            raise ValueError ("Socio no encontrado.")
        s .modificar_datos (nombre ,apellido ,telefono )
        print (f"  ✔ Datos de {s .get_nombre_completo ()} actualizados.")

    def consultar_historial_membresias (self ,dni :str ):
        s =self .buscar_socio (dni )
        if not s :
            print ("  Socio no encontrado.")
            return 
        print (f"\n  HISTORIAL DE MEMBRESÍAS — {s .get_nombre_completo ()}")
        print (f"  {'─'*56 }")

        for i ,m in enumerate (s .get_historial_mem (),1 ):
            print (f"  {i }. {m }")

    def listar_socios (self ):
        if not self .__socios :
            print ("  Sin socios registrados.");return 
        print (f"\n{'─'*60 }")
        print (f"  SOCIOS ({len (self .__socios )})")
        print (f"{'─'*60 }")
        for s in self .__socios :
            print (s );print ()

    def listar_socios_morosos (self ):

        morosos =[s for s in self .__socios if not s .esta_al_dia ()]
        if not morosos :
            print ("  🎉 Todos los socios están al día.");return 
        print (f"\n  ⚠ MOROSOS ({len (morosos )}):")
        for s in morosos :
            print (f"    → {s .get_nombre_completo ():<22} | DNI: {s .get_dni ()} | Debe: S/ {s .get_deuda ():.2f}")

    def calcular_ingresos_esperados (self )->float :

        return round (sum (s .get_deuda ()for s in self .__socios ),2 )




    def listar_planes_vigentes (self ):
        """Controla fechas de vencimiento de todas las membresías."""
        print (f"\n  {'─'*60 }")
        print (f"  {'CONTROL DE MEMBRESÍAS':^60}")
        print (f"  {'─'*60 }")
        print (f"  {'Socio':<22} {'Plan':<22} {'Vence':<12} {'Estado'}")
        print (f"  {'─'*60 }")
        for s in self .__socios :
            m =s .get_membresia ()
            estado ="✓ Vigente"if m .esta_vigente ()else "✗ Vencida"
            print (f"  {s .get_nombre_completo ():<22} {m .tipo ():<22} {str (m .get_fecha_fin ()):<12} {estado }")

    def alertas_vencimiento (self ,dias :int =7 ):
        """Genera alertas automáticas de membresías por vencer."""

        alertas =[(s ,s .get_membresia ().dias_restantes ())
        for s in self .__socios 
        if 0 <s .get_membresia ().dias_restantes ()<=dias ]
        if not alertas :
            print (f"  ✓ No hay membresías que venzan en los próximos {dias } días.")
            return 
        print (f"\n  ⚠ ALERTAS — Membresías que vencen en ≤ {dias } días:")
        print (f"  {'─'*56 }")

        for s ,d in sorted (alertas ,key =lambda x :x [1 ]):
            print (f"  🔔 {s .get_nombre_completo ():<22} | Tel: {s .get_telefono ()} | Vence en {d } día(s)")

    def _socios_por_vencer (self ,dias :int )->int :

        return sum (1 for s in self .__socios if 0 <s .get_membresia ().dias_restantes ()<=dias )

    def renovar_membresia_socio (self ,dni :str ,nueva :Membresia ):
        s =self .buscar_socio (dni )
        if not s :
            raise ValueError ("Socio no encontrado.")
        s .renovar_membresia (nueva )
        print (f"  ✔ Membresía renovada para {s .get_nombre_completo ()}.")




    def registrar_pago_socio (self ,dni :str )->Pago |None :
        """Registra el pago y genera comprobante."""
        s =self .buscar_socio (dni )
        if not s :
            print ("  Socio no encontrado.");return None 
        if s .esta_al_dia ():
            print (f"  ℹ {s .get_nombre_completo ()} ya tiene su membresía pagada.")
            return None 


        pago =s .registrar_pago ()
        self .__pagos .append (pago )
        print (pago .comprobante ())
        return pago 

    def historial_pagos (self ,dni :str =None ):
        """Consulta historial de ingresos, filtrable por socio."""
        pagos =self .__pagos 
        if dni :
            pagos =[p for p in pagos if p .get_dni_socio ()==dni ]
        if not pagos :
            print ("  Sin pagos registrados.");return 

        titulo =f"HISTORIAL DE PAGOS — {dni }"if dni else "HISTORIAL DE INGRESOS"
        print (f"\n  {titulo }")
        print (f"  {'─'*60 }")
        for p in pagos :
            print (p )
        total =sum (p .get_monto ()for p in pagos )
        print (f"  {'─'*60 }")
        print (f"  Total cobrado: S/ {total :.2f}")




    def registrar_asistencia (self ,dni :str ):
        """Registra ingreso diario de un socio."""
        s =self .buscar_socio (dni )
        if not s :
            print ("  Socio no encontrado.");return 
        if not s .get_membresia ().esta_vigente ():

            print (f"  ⚠ La membresía de {s .get_nombre_completo ()} está vencida. No puede ingresar.")
            return 

        reg =RegistroAsistencia (s .get_dni (),s .get_nombre_completo ())
        self .__asistencias .append (reg )
        print (f"  ✔ Ingreso registrado para {s .get_nombre_completo ()} — {date .today ()}")

    def listar_asistencias_hoy (self ):

        hoy =[a for a in self .__asistencias if a .get_fecha ()==date .today ()]
        if not hoy :
            print ("  Sin asistencias registradas hoy.");return 
        print (f"\n  ASISTENCIAS DE HOY ({date .today ()}) — Total: {len (hoy )}")
        print (f"  {'─'*50 }")
        for a in hoy :print (a )

    def _asistencias_hoy (self )->int :
        return sum (1 for a in self .__asistencias if a .get_fecha ()==date .today ())

    def frecuencia_asistencia (self ):
        """Controla la frecuencia de uso por socio usando Diccionarios."""
        conteo :dict [str ,int ]={}
        nombres :dict [str ,str ]={}
        for a in self .__asistencias :


            conteo [a .get_dni_socio ()]=conteo .get (a .get_dni_socio (),0 )+1 
            nombres [a .get_dni_socio ()]=a .get_nombre_socio ()

        if not conteo :
            print ("  Sin registros de asistencia.");return 
        print (f"\n  FRECUENCIA DE ASISTENCIA")
        print (f"  {'─'*50 }")
        print (f"  {'Socio':<25} {'DNI':<10} {'Visitas':>7}")
        print (f"  {'─'*50 }")

        for dni ,visitas in sorted (conteo .items (),key =lambda x :-x [1 ]):
            print (f"  {nombres [dni ]:<25} {dni :<10} {visitas :>7}")

    def identificar_clientes_inactivos (self ,dias_sin_visita :int =15 ):
        """Identifica socios que no asisten desde hace N días."""
        ultima_visita :dict [str ,date ]={}

        for a in self .__asistencias :
            d =a .get_dni_socio ()
            if d not in ultima_visita or a .get_fecha ()>ultima_visita [d ]:
                ultima_visita [d ]=a .get_fecha ()

        hoy =date .today ()
        inactivos =[]
        for s in self .__socios :
            if s .get_membresia ().esta_vigente ():
                uv =ultima_visita .get (s .get_dni ())

                if uv is None or (hoy -uv ).days >=dias_sin_visita :
                    dias =(hoy -uv ).days if uv else None 
                    inactivos .append ((s ,uv ,dias ))

        if not inactivos :
            print (f"  ✓ No hay socios inactivos por más de {dias_sin_visita } días.");return 

        print (f"\n  CLIENTES INACTIVOS (≥{dias_sin_visita } días sin visita):")
        print (f"  {'─'*60 }")
        for s ,uv ,dias in inactivos :
            ultima =str (uv )if uv else "Nunca ha asistido"
            info =f"{dias } días"if dias is not None else "—"
            print (f"  {s .get_nombre_completo ():<22} | Tel: {s .get_telefono ()} | Última visita: {ultima } ({info })")




    def reporte_clientes_activos (self ):
        activos =[s for s in self .__socios if s .get_membresia ().esta_vigente ()]
        print (f"\n  CLIENTES ACTIVOS — {len (activos )} socio(s)")
        print (f"  {'─'*56 }")
        for s in activos :
            print (f"  ✓ {s .get_nombre_completo ():<22} | DNI: {s .get_dni ()} | Tel: {s .get_telefono ()}")

    def reporte_clientes_inactivos (self ):
        inactivos =[s for s in self .__socios if not s .get_membresia ().esta_vigente ()]
        print (f"\n  CLIENTES INACTIVOS (membresía vencida) — {len (inactivos )} socio(s)")
        print (f"  {'─'*56 }")
        if not inactivos :
            print ("  (ninguno)");return 
        for s in inactivos :
            print (f"  ✗ {s .get_nombre_completo ():<22} | DNI: {s .get_dni ()} | Venció: {s .get_membresia ().get_fecha_fin ()}")

    def reporte_ingresos_mensuales (self ):
        """Agrupa los pagos cobrados por mes."""
        mensuales :dict [str ,float ]={}
        for p in self .__pagos :

            clave =p .get_fecha ().strftime ("%Y-%m")
            mensuales [clave ]=mensuales .get (clave ,0.0 )+p .get_monto ()

        if not mensuales :
            print ("  Sin pagos registrados aún.");return 
        print (f"\n  INGRESOS MENSUALES")
        print (f"  {'─'*40 }")
        for mes in sorted (mensuales ):
            print (f"  {mes }   S/ {mensuales [mes ]:>9.2f}")
        print (f"  {'─'*40 }")
        print (f"  TOTAL  S/ {sum (mensuales .values ()):>9.2f}")

    def reporte_renovaciones (self ):
        """Socios con más de una membresía en el historial."""

        renovados =[(s ,len (s .get_historial_mem ()))for s in self .__socios if len (s .get_historial_mem ())>1 ]
        print (f"\n  RENOVACIONES DE MEMBRESÍAS — {len (renovados )} socio(s)")
        print (f"  {'─'*56 }")
        if not renovados :
            print ("  (sin renovaciones registradas)");return 
        for s ,total in sorted (renovados ,key =lambda x :-x [1 ]):
            print (f"  {s .get_nombre_completo ():<22} | Renovaciones: {total -1 }")

    def reporte_vencimientos_proximos (self ,dias :int =30 ):
        proximos =[(s ,s .get_membresia ().dias_restantes ())
        for s in self .__socios if 0 <s .get_membresia ().dias_restantes ()<=dias ]
        print (f"\n  VENCIMIENTOS PRÓXIMOS (≤{dias } días)")
        print (f"  {'─'*56 }")
        if not proximos :
            print (f"  Ninguna membresía vence en los próximos {dias } días.");return 
        for s ,d in sorted (proximos ,key =lambda x :x [1 ]):
            print (f"  {s .get_nombre_completo ():<22} | Vence en: {d } día(s) ({s .get_membresia ().get_fecha_fin ()})")

    def reporte_tendencia_crecimiento (self ):
        """Socios registrados por mes."""
        por_mes :dict [str ,int ]={}
        for s in self .__socios :
            clave =s .get_fecha_registro ().strftime ("%Y-%m")
            por_mes [clave ]=por_mes .get (clave ,0 )+1 

        print (f"\n  TENDENCIA DE CRECIMIENTO DE CLIENTES")
        print (f"  {'─'*40 }")
        if not por_mes :
            print ("  Sin datos.");return 

        acum =0 
        for mes in sorted (por_mes ):
            acum +=por_mes [mes ]
            barra ="█"*por_mes [mes ]
            print (f"  {mes }  {barra :<15} +{por_mes [mes ]:>2} (total: {acum })")

    def reporte_ranking_planes (self ):
        """Planes más vendidos según membresía actual."""
        conteo :dict [str ,int ]={}
        for s in self .__socios :
            plan =s .get_membresia ().tipo ()
            conteo [plan ]=conteo .get (plan ,0 )+1 

        print (f"\n  RANKING DE PLANES MÁS VENDIDOS")
        print (f"  {'─'*40 }")
        if not conteo :
            print ("  Sin datos.");return 
        for i ,(plan ,cant )in enumerate (sorted (conteo .items (),key =lambda x :-x [1 ]),1 ):
            barra ="█"*cant 
            print (f"  {i }. {plan :<22} {barra :<10} {cant } socio(s)")




    def registrar_entrenador (self ,e :Entrenador ):
        self .__entrenadores .append (e )
        print (f"  ✔ Entrenador '{e .get_nombre_completo ()}' registrado.")

    def listar_entrenadores (self ):
        if not self .__entrenadores :
            print ("  Sin entrenadores.");return 
        print (f"\n  PLANILLA DE ENTRENADORES:")
        total =0.0 
        for e in self .__entrenadores :
            print (f"  {e }");total +=e .calcular_sueldo ()
        print (f"\n  Total planilla: S/ {total :.2f}")








def limpiar ():
    print ("\n"+"═"*60 )

def seleccionar_membresia ()->Membresia :

    print ("  Tipo de membresía:")
    print ("  [1] Básica Mensual     – S/  80.00")
    print ("  [2] Trimestral         – S/ 210.00")
    print ("  [3] Anual              – S/ 720.00")
    while True :
        op =input ("  Seleccione [1-3]: ").strip ()
        if op =="1":return MembresiaBasica ()
        if op =="2":return MembresiaTrimestral ()
        if op =="3":return MembresiaAnual ()
        print ("  Opción inválida, intente de nuevo.")





def mostrar_pantalla_principal ():
    print ("""
╔══════════════════════════════════════════╗
║                                          ║
║      SISTEMA DE GESTIÓN GYM FIT          ║
║                                          ║
╚══════════════════════════════════════════╝
  Presione Enter para continuar...""")
    input ()

def mostrar_menu ():
    print ("""
╔══════════════════════════════════════════╗
║      GYM FIT – Menú Principal            ║
╠══════════════════════════════════════════╣
║  1. Clientes                             ║
║  2. Membresías                           ║
║  3. Pagos                                ║
║  4. Asistencia                           ║
║  5. Reportes e Indicadores               ║
║  0. Salir                                ║
╚══════════════════════════════════════════╝""")

def menu_clientes (gym :GymManager ):
    while True :
        print ("""
╔══════════════════════════════════════════╗
║           CLIENTES                       ║
╠══════════════════════════════════════════╣
║  1. Registrar nuevo cliente              ║
║  2. Modificar información                ║
║  3. Consultar historial de membresías    ║
║  4. Buscar cliente rápidamente           ║
║  5. Listar todos los clientes            ║
║  6. Ver clientes morosos                 ║
║  0. Volver                               ║
╚══════════════════════════════════════════╝""")
        op =input ("  Opción: ").strip ()
        limpiar ()
        try :
            if op =="1":
                print ("── REGISTRAR CLIENTE ──────────────────")
                dni =input ("  DNI (8 dígitos): ").strip ()
                nombre =input ("  Nombre         : ").strip ()
                apellido =input ("  Apellido       : ").strip ()
                telefono =input ("  Teléfono       : ").strip ()
                es_vip =input ("  ¿Es VIP? (s/n) : ").lower ()=="s"
                mem =seleccionar_membresia ()


                if es_vip :
                    entrenador =input ("  Entrenador asignado: ").strip ()
                    socio =SocioVIP (dni ,nombre ,apellido ,telefono ,mem ,entrenador )
                else :
                    socio =Socio (dni ,nombre ,apellido ,telefono ,mem )
                gym .registrar_socio (socio )

            elif op =="2":
                print ("── MODIFICAR INFORMACIÓN ──────────────")
                dni =input ("  DNI del cliente: ").strip ()
                print ("  (Dejar en blanco para no modificar)")

                nombre =input ("  Nuevo nombre   : ").strip ()or None 
                apellido =input ("  Nuevo apellido : ").strip ()or None 
                telefono =input ("  Nuevo teléfono : ").strip ()or None 
                gym .modificar_socio (dni ,nombre ,apellido ,telefono )

            elif op =="3":
                print ("── HISTORIAL DE MEMBRESÍAS ────────────")
                dni =input ("  DNI del cliente: ").strip ()
                gym .consultar_historial_membresias (dni )

            elif op =="4":
                print ("── BÚSQUEDA RÁPIDA ────────────────────")
                texto =input ("  Nombre o apellido: ").strip ()
                resultado =gym .buscar_socio_nombre (texto )
                if resultado :
                    print (f"\n  Se encontraron {len (resultado )} resultado(s):")
                    for s in resultado :print (f"\n{s }")
                else :
                    print ("  No se encontraron coincidencias.")

            elif op =="5":
                gym .listar_socios ()
            elif op =="6":
                gym .listar_socios_morosos ()
            elif op =="0":
                break 
            else :
                print ("  Opción no válida.")

        except ValueError as e :

            print (f"  ⚠ Error: {e }")

        input ("\n  Presione Enter para continuar…")





def menu_membresias (gym :GymManager ):
    while True :
        print ("""
╔══════════════════════════════════════════╗
║           MEMBRESÍAS                     ║
╠══════════════════════════════════════════╣
║  1. Listar planes vigentes               ║
║  2. Ver alertas de vencimiento           ║
║  3. Renovar membresía                    ║
║  0. Volver                               ║
╚══════════════════════════════════════════╝""")

        op =input ("  Opción: ").strip ()
        limpiar ()

        try :
            if op =="1":
                gym .listar_planes_vigentes ()
            elif op =="2":
                gym .alertas_vencimiento ()
            elif op =="3":
                print ("── RENOVAR MEMBRESÍA ──────────────────")
                dni =input ("  DNI del cliente: ").strip ()
                nueva_membresia =seleccionar_membresia ()
                gym .renovar_membresia_socio (dni ,nueva_membresia )
            elif op =="0":
                break 
            else :
                print ("  Opción no válida.")
        except ValueError as e :
            print (f"  ⚠ Error: {e }")

        input ("\n  Presione Enter para continuar…")


def menu_pagos (gym :GymManager ):
    while True :
        print ("""
╔══════════════════════════════════════════╗
║              PAGOS                       ║
╠══════════════════════════════════════════╣
║  1. Registrar pago                       ║
║  2. Ver historial de pagos               ║
║  3. Consultar pagos por cliente          ║
║  0. Volver                               ║
╚══════════════════════════════════════════╝""")

        op =input ("  Opción: ").strip ()
        limpiar ()

        if op =="1":
            print ("── REGISTRAR PAGO ─────────────────────")
            dni =input ("  DNI del cliente: ").strip ()
            gym .registrar_pago_socio (dni )
        elif op =="2":
            gym .historial_pagos ()
        elif op =="3":
            dni =input ("  DNI del cliente: ").strip ()
            gym .historial_pagos (dni )
        elif op =="0":
            break 
        else :
            print ("  Opción no válida.")

        input ("\n  Presione Enter para continuar…")


def menu_asistencia (gym :GymManager ):
    while True :
        print ("""
╔══════════════════════════════════════════╗
║            ASISTENCIA                    ║
╠══════════════════════════════════════════╣
║  1. Registrar asistencia                 ║
║  2. Ver asistencias de hoy               ║
║  3. Ver frecuencia de asistencia         ║
║  4. Identificar clientes inactivos       ║
║  0. Volver                               ║
╚══════════════════════════════════════════╝""")

        op =input ("  Opción: ").strip ()
        limpiar ()

        if op =="1":
            dni =input ("  DNI del cliente: ").strip ()
            gym .registrar_asistencia (dni )
        elif op =="2":
            gym .listar_asistencias_hoy ()
        elif op =="3":
            gym .frecuencia_asistencia ()
        elif op =="4":
            gym .identificar_clientes_inactivos ()
        elif op =="0":
            break 
        else :
            print ("  Opción no válida.")

        input ("\n  Presione Enter para continuar…")


def menu_reportes (gym :GymManager ):
    while True :
        print ("""
╔══════════════════════════════════════════╗
║        REPORTES E INDICADORES            ║
╠══════════════════════════════════════════╣
║  1. Clientes activos                     ║
║  2. Clientes inactivos                   ║
║  3. Ingresos mensuales                   ║
║  4. Renovaciones                         ║
║  5. Vencimientos próximos                ║
║  6. Tendencia de crecimiento             ║
║  7. Ranking de planes                    ║
║  8. Planilla de entrenadores             ║
║  0. Volver                               ║
╚══════════════════════════════════════════╝""")

        op =input ("  Opción: ").strip ()
        limpiar ()

        if op =="1":
            gym .reporte_clientes_activos ()
        elif op =="2":
            gym .reporte_clientes_inactivos ()
        elif op =="3":
            gym .reporte_ingresos_mensuales ()
        elif op =="4":
            gym .reporte_renovaciones ()
        elif op =="5":
            gym .reporte_vencimientos_proximos ()
        elif op =="6":
            gym .reporte_tendencia_crecimiento ()
        elif op =="7":
            gym .reporte_ranking_planes ()
        elif op =="8":
            gym .listar_entrenadores ()
        elif op =="0":
            break 
        else :
            print ("  Opción no válida.")

        input ("\n  Presione Enter para continuar…")




def main ():

    gym =GymManager ("GymFit S.A.C.")



    gym .registrar_socio (Socio ("12345678","Ana","Torres","987654321",MembresiaBasica ()))
    gym .registrar_socio (SocioVIP ("87654321","Carlos","Mendoza","912345678",MembresiaAnual (),"Luis Quispe"))
    gym .registrar_socio (Socio ("45678901","Lucia","Vargas","934567890",MembresiaTrimestral ()))
    gym .registrar_socio (Socio ("11223344","Pedro","Rojas","956789012",MembresiaBasica ()))
    gym .registrar_entrenador (Entrenador ("11111111","Luis","Quispe","911111111","Musculación",1500.0 ))


    carlos =gym .buscar_socio ("87654321")
    if carlos :carlos .registrar_pago ()


    ana =gym .buscar_socio ("12345678")
    if ana :gym .registrar_pago_socio ("12345678")


    gym .registrar_asistencia ("12345678")
    gym .registrar_asistencia ("87654321")


    mostrar_pantalla_principal ()

    while True :
        mostrar_menu ()
        opcion =input ("  Opción: ").strip ()
        limpiar ()

        try :

            if opcion =="1":menu_clientes (gym )
            elif opcion =="2":menu_membresias (gym )
            elif opcion =="3":menu_pagos (gym )
            elif opcion =="4":menu_asistencia (gym )
            elif opcion =="5":menu_reportes (gym )
            elif opcion =="0":
                print ("  ¡Hasta luego! 💪")
                break 
            else :
                print ("  Opción no válida.")
                input ("\n  Presione Enter para continuar…")

        except ValueError as e :
            print (f"  ⚠ Error de validación: {e }")
            input ("\n  Presione Enter para continuar…")
        except Exception as e :

            print (f"  ✗ Error inesperado: {e }")
            input ("\n  Presione Enter para continuar…")



if __name__ =="__main__":
    main ()