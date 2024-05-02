from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Modelos
from .forms import C_Intermediario2, form_CotizadorTAR, form_Blindaje
import datetime
from reportlab.pdfgen import canvas
from io import BytesIO
import locale
import os
from decimal import Decimal
import base64
from django.core.mail import EmailMessage
from django.conf import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph

# Create your views here.

def es_bisiesto(año):
    return año % 4 == 0 and (año % 100 != 0 or año % 400 == 0)
def calcular_variable(año):
    if es_bisiesto(año + 1) and datetime.date(año, 3, 1) <= datetime.date.today() <= datetime.date(año + 1, 2, 29):
        return 1.0027397260274
    else:
        return 1

def CotizadorA(request):
    form_intermediario = C_Intermediario2()
    form_cotizador = form_CotizadorTAR()
    form_blindaje = form_Blindaje()

    if request.method == 'POST':
        buffer = BytesIO()
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        # Crear un objeto PDF
        pdf = canvas.Canvas(buffer)
        #Estilo de Letra
        pdf.setFont("Helvetica", 9)
        #Trabajo con Variables
        Nom = request.POST.get('Nombre', None)
        In = request.POST.get('Int', None)
        Te = request.POST.get('Tel', None)
        Cor = request.POST.get('Correo', None)
        Identificacion = request.POST.get('Id', None)
        Solicitante = request.POST.get('Sol', None)
        Suma = request.POST.get('Sum', None)
        Marca = request.POST.get('Marc', None)
        Modelo = request.POST.get('Model', None)
        Ag = request.POST.get('Agen', None)
        Repuesto = request.POST.get('Rep', None)
        Blindaje = request.POST.get('Blind', None)
        Año_F = request.POST.get('Año', None)
        Placa = request.POST.get('Plac', None)

        Mails = request.POST.get('Mail', None)
        Cellphones = request.POST.get('Cellphone', None)

        fecha_actual = datetime.datetime.now().strftime("%d de %B de %Y")
        image_path = os.path.join('cotizador_autos', 'static', 'satlan.png')

        # Agregando contenido al PDF
        pdf.setFont("Helvetica", 9)
        pdf.drawString(480, 820, fecha_actual)

        pdf.drawImage(image_path, x=50, y=750, width=127, height=67)

        pdf.setFont("Helvetica-Bold", 12)
            
        pdf.drawString(222, 775, "OFERTA DE SEGURO DE AUTOMOTORES")

        pdf.setFont("Helvetica", 9)

        pdf.drawString(25, 745, "Presentamos la oferta para el seguro de su vehículo, en el que mostramos algunos de los beneficios al contratarlo con Seguros Atlántida:")

        altura_solicitante = 720
        altura_suma = 707
        altura_categoria = 694
        altura_marca = 681
        altura_modelo = 720
        altura_año = 707
        altura_placa = 694
        altura_agencia = 681

        pdf.drawString(30, altura_solicitante, "SOLICITANTE:")
        pdf.drawString(30, altura_suma, "SUMA ASEGURADA:")
        pdf.drawString(30, altura_categoria, "CATEGORÍA:")
        pdf.drawString(30, altura_marca, "MARCA:")
        pdf.drawString(355, altura_modelo, "MODELO:")
        pdf.drawString(355, altura_año, "AÑO:")
        pdf.drawString(355, altura_placa, "PLACA:")
        pdf.drawString(355, altura_agencia, "AGENCIA:")

        #SOLICITANTE
        Solicitante_Mayus = Solicitante.upper()
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(140, altura_solicitante - 2, 200, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(142, altura_solicitante, Solicitante_Mayus)
        #SUMA ASEGURADA
        SumaAsegurada = "{:,.2f}".format(float(Suma))
        SumaA = "$" + SumaAsegurada
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(140, altura_suma - 2, 200, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(142, altura_suma, "$" + SumaAsegurada)
        #CATEGORÍA
        cat = Modelos.objects.get(modelo=Modelo).clase
        if cat == 'A':
            categoria = 'SEDÁN O HATCHBACK'
            deducible = "2%"
        elif cat == 'B':
            categoria = 'CAMIONETAS O PICKUP'
            deducible = "3%"
        else:
            categoria = ''
            deducible = ""
        
        if Blindaje == "" or Blindaje == "$" or Blindaje == "undefined":
            Bld = ""
        else:
            Bl = "{:,.2f}".format(float(Blindaje))
            Bld = "$" + Bl

        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(140, altura_categoria - 2, 200, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(142, altura_categoria, categoria)
        #MARCA
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(140, altura_marca - 2, 200, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(142, altura_marca, Marca)
        #MODELO
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(415, altura_modelo - 2, 152, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(417, altura_modelo, Modelo)
        #AÑO
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(415, altura_año - 2, 152, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(417, altura_año, Año_F)
        #PLACA
        placa_mayus = Placa.upper()
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(415, altura_placa - 2, 152, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(417, altura_placa, placa_mayus)
        #AGENCIA
        Agencia_mayus = Ag.upper()
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(415, altura_agencia - 2, 152, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(417, altura_agencia, Agencia_mayus)
        #ENCABEZADO
        pdf.setFillColorRGB(0.89, 0.12, 0.19)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(30, 640, 535, 28, fill=True, stroke=False)
        pdf.setFillColorRGB(1, 1, 1)
        pdf.setFont("Helvetica-Bold", 9)
    
        pdf.drawString(50, 650, "COBERTURAS / PLANES:")
        pdf.drawString(202, 650, "FULL COVER")
        pdf.drawString(290, 650, "AUTO RENTABLE")
        pdf.drawString(400, 650, "BÁSICO")
        pdf.drawString(465, 655, "RESPONSABILIDAD")
        pdf.drawString(498, 645, "CIVIL")
        #DAÑO Y ROBO
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0.65, 0.65, 0.65)
        pdf.rect(30, 626, 153, 12, fill=False, stroke=True)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica", 9)
        pdf.drawString(32, 628, "Daños y Robo al Vehículo")
        #RANGOS DE AÑOS
        current_year = datetime.datetime.now().year
        rango_FC1 = [str(year) for year in range(current_year + 1, current_year - 8, -1)]
        rango_FC2 = [str(year) for year in range(current_year + 1, current_year - 6, -1)]

        rango_ARB1 = [str(year) for year in range(current_year + 1, current_year - 16, -1)]
        rango_ARB2 = [str(year) for year in range(current_year + 1, current_year - 11, -1)]

        factor_añobisiesto = calcular_variable(current_year)

        #DAÑO Y ROBO - FULL COVER
        pdf.rect(183, 626, 100, 12, fill=False, stroke=True)

        if Repuesto == "Si":
            Rp = "Incluido"
            Llanta = "$30.00"
            LlantaR = 30
        else:
            Rp = "No Incluido"
            Llanta = "$0.00"
            LlantaR = 0
        
        if (str(Año_F) in rango_FC1) and Ag == "Si":
            SumaFC = SumaA
            DeducibleFC1 = "Ahorro hasta el 100%"
            DeducibleFC2 = "del Deducible"
            RBienesFC = "$12,000.00"
            RBienesUFC = "$6,000.00"
            RExcesoFC = "$50,000.00"
            GMVariasFC = "10,000.00"
            GMUnaFC = "$2,000.00"
            GFunerariosFC = "$2,000.00"
            LimiteFC1 = "Centroámerica"
            LimiteFC2 = "incluyendo México,"
            LimiteFC3 = "Panamá y Belice."
            MAConductorFC = "$10,000.00"
            MAOcupanteFC = "$5,000.00"
            IConductorFC = "$10,000.00"
            RpFC = Rp
            AsistenciaFC = "Incluido"
            AsistenciaHFC = "Incluido"
            AutoFC = "1 evento / $150.00"
            ConductorFC = "2 eventos"
            MinoriaFC = "Incluido"
            DañosFC = "Incluido"
            GruaFC = "$1,500.00"
            LegalesFC = "$1,500.00"
            BlFC = Bld

            
            descuentosFC1 = {}
            for year in rango_FC1:
                if current_year - 3 <= int(year) <= current_year + 1:
                    descuentosFC1[year] = 0.47
                elif current_year - 6 <= int(year) <= current_year - 4:
                    descuentosFC1[year] = 0.42
                else:
                    descuentosFC1[year] = 0.37
            
            descuento_FC1 = descuentosFC1[Año_F]
            
            if Blindaje == "" or Blindaje == "$" or Blindaje == "undefined":
                SumaP = float(Suma)
                PrimaFCA = Decimal(SumaP) * Decimal(0.0550090561502465) * Decimal(factor_añobisiesto)
                PrimaFCB = Decimal(12000) * Decimal(0.0100018112300493) * Decimal(factor_añobisiesto)
                PrimaFCC = Decimal(12000) * Decimal(0.00500090561502464) * Decimal(factor_añobisiesto)
                PrimaFCD = Decimal(10000) * Decimal(0.0100018112300493) * Decimal(factor_añobisiesto)
                PrimaTotalFC = (PrimaFCA + PrimaFCB + PrimaFCC + PrimaFCD)
                PrimaFC = PrimaTotalFC - (PrimaTotalFC * Decimal(descuento_FC1))
            else:
                SumaP = float(Suma) + float(Blindaje)
                PrimaFCA = (Decimal(SumaP) * Decimal(0.0550090561502465)) * Decimal(1.5) * Decimal(factor_añobisiesto)
                PrimaFCB = (Decimal(12000) + Decimal(Blindaje)) * Decimal(0.0100018112300493) * Decimal(1.5) * Decimal(factor_añobisiesto)
                PrimaFCC = (Decimal(12000)) * Decimal(0.00500090561502464) * Decimal(factor_añobisiesto)
                PrimaFCD = (Decimal(10000)) * Decimal(0.0100018112300493) * Decimal(factor_añobisiesto)
                PrimaTotalFC = (PrimaFCA + PrimaFCB + PrimaFCC + PrimaFCD)
                PrimaFC = PrimaTotalFC - (PrimaTotalFC * Decimal(descuento_FC1))
            
            Prima_FC = "{:,.2f}".format(float(PrimaFC))
            Prima_FC = "$" + Prima_FC
            
            LlantaRepuesto_FC = Llanta

            IVA_Total = (PrimaFC + LlantaR) * Decimal(0.13)

            IVA_TotalFC = "{:,.2f}".format(float(IVA_Total))
            IVA_TotalFC = "$" + IVA_TotalFC

            Prima_Total = PrimaFC + LlantaR + IVA_Total

            Prima_TotalFC = "{:,.2f}".format(float(Prima_Total))
            Prima_TotalFC = "$" + Prima_TotalFC

            Prima_Mensual = (Prima_Total * Decimal(1.07))/12

            Prima_MensualFC = "{:,.2f}".format(float(Prima_Mensual))
            Prima_MensualFC = "$" + Prima_MensualFC 

            
        elif (str(Año_F) in rango_FC2) and Ag == "No":
            SumaFC = SumaA
            DeducibleFC1 = "Ahorro hasta el 100%"
            DeducibleFC2 = "del Deducible"
            RBienesFC = "$12,000.00"
            RBienesUFC = "$6,000.00"
            RExcesoFC = "$50,000.00"
            GMVariasFC = "$10,000.00"
            GMUnaFC = "$2,000.00"
            GFunerariosFC = "$2,000.00"
            LimiteFC1 = "Centroamérica"
            LimiteFC2 = "incluyendo México,"
            LimiteFC3 = "Panamá y Belice."
            MAConductorFC = "$10,000.00"
            MAOcupanteFC = "$5,000.00"
            IConductorFC = "$10,000.00"
            RpFC = Rp
            AsistenciaFC = "Incluido"
            AsistenciaHFC = "Incluido"
            AutoFC = "1 evento / $150.00"
            ConductorFC = "2 eventos"
            MinoriaFC = "Incluido"
            DañosFC = "Incluido"
            GruaFC = "$1,500.00"
            LegalesFC = "$1,500.00"
            BlFC = Bld

            descuentosFC2 = {}
            for year in rango_FC2:
                if current_year - 3 <= int(year) <= current_year + 1:
                    descuentosFC2[year] = 0.46
                else:
                    descuentosFC2[year] = 0.40
                        
            descuento_FC2 = descuentosFC2[Año_F]

            if Blindaje == "" or Blindaje == "$":
                SumaP = float(Suma)
                PrimaFCA = Decimal(SumaP) * Decimal(0.0550090561502465) * Decimal(factor_añobisiesto)
                PrimaFCB = Decimal(12000) * Decimal(0.0100018112300493) * Decimal(factor_añobisiesto)
                PrimaFCC = Decimal(12000) * Decimal(0.00500090561502464) * Decimal(factor_añobisiesto)
                PrimaFCD = Decimal(10000) * Decimal(0.0100018112300493) * Decimal(factor_añobisiesto)
                PrimaTotalFC = (PrimaFCA + PrimaFCB + PrimaFCC + PrimaFCD)
                PrimaFC = PrimaTotalFC - (PrimaTotalFC * Decimal(descuento_FC2))
            else:
                SumaP = float(Suma) + float(Blindaje)
                PrimaFCA = (Decimal(SumaP) * Decimal(0.0550090561502465)) * Decimal(1.5) * Decimal(factor_añobisiesto)
                PrimaFCB = (Decimal(12000) + Decimal(Blindaje)) * Decimal(0.0100018112300493) * Decimal(1.5) * Decimal(factor_añobisiesto)
                PrimaFCC = (Decimal(12000)) * Decimal(0.00500090561502464) * Decimal(factor_añobisiesto)
                PrimaFCD = (Decimal(10000)) * Decimal(0.0100018112300493) * Decimal(factor_añobisiesto)
                PrimaTotalFC = (PrimaFCA + PrimaFCB + PrimaFCC + PrimaFCD)
                PrimaFC = PrimaTotalFC - (PrimaTotalFC * Decimal(descuento_FC2))

            Prima_FC = "{:,.2f}".format(float(PrimaFC))
            Prima_FC = "$" + Prima_FC

            LlantaRepuesto_FC = Llanta
            
            IVA_Total = (PrimaFC + LlantaR) * Decimal(0.13)

            IVA_TotalFC = "{:,.2f}".format(float(IVA_Total))
            IVA_TotalFC = "$" + IVA_TotalFC

            Prima_Total = PrimaFC + LlantaR + IVA_Total

            Prima_TotalFC = "{:,.2f}".format(float(Prima_Total))
            Prima_TotalFC = "$" + Prima_TotalFC

            Prima_Mensual = (Prima_Total * Decimal(1.07))/12

            Prima_MensualFC = "{:,.2f}".format(float(Prima_Mensual))
            Prima_MensualFC = "$" + Prima_MensualFC

        else:
            SumaFC = ""
            DeducibleFC1 = ""
            DeducibleFC2 = ""
            RBienesFC = ""
            RBienesUFC = ""
            RExcesoFC = ""
            GMVariasFC = ""
            GMUnaFC = ""
            GFunerariosFC = ""
            LimiteFC1 = ""
            LimiteFC2 = ""
            LimiteFC3 = ""
            MAConductorFC = ""
            MAOcupanteFC = ""
            IConductorFC = ""
            RpFC = ""
            AsistenciaFC = ""
            AsistenciaHFC = ""
            AutoFC = ""
            ConductorFC = ""
            MinoriaFC = ""
            DañosFC = ""
            GruaFC = ""
            LegalesFC = ""
            BlFC = ""
            Prima_FC = ""
            LlantaRepuesto_FC = ""
            IVA_TotalFC = ""
            Prima_TotalFC = ""
            Prima_MensualFC = ""
        
        ancho_texto1 = pdf.stringWidth(SumaFC, "Helvetica", 9)
        x_centro1 = 183 + (100 - ancho_texto1)/2
        pdf.drawString(x_centro1, 628, SumaFC)
        #DAÑO Y ROBO - AR
        pdf.rect(283, 626, 90, 12, fill=False, stroke=True)
        if (str(Año_F) in rango_ARB1) and Ag == "Si":
            SumaAR = SumaA
            DeducibleAR1 = "Ahorro hasta el 50%"
            DeducibleAR2 = "del Deducible"
            RBienesAR = "$10,000.00"
            RBienesUAR = "$5,000.00"
            RExcesoAR = "$35,000.00"
            GMVariasAR = "$10,000.00"
            GMUnaAR = "$2,000.00"
            GFunerariosAR = "$2,000.00"
            LimiteAR1 = "Centroamérica"
            LimiteAR2 = "incluyendo México,"
            LimiteAR3 = "Panamá y Belice."
            MAConductorAR = "$10,000.00"
            MAOcupanteAR = "$5,000.00"
            IConductorAR = "$10,000.00"
            RpAR = Rp
            AsistenciaAR = "Incluido"
            AsistenciaHAR = "N/A"
            AutoAR = "1 evento / $150.00"
            ConductorAR = "2 eventos"
            MinoriaAR = "Incluido"
            DañosAR = "Incluido"
            GruaAR = "$1,500.00"
            LegalesAR = "$1,500.00"
            BlAR = Bld

            descuentosARB1 = {}
            for year in rango_ARB1:
                if current_year - 3 <= int(year) <= current_year + 1:
                    descuentosARB1[year] = 0.47
                elif current_year - 6 <= int(year) <= current_year - 4:
                    descuentosARB1[year] = 0.42
                elif current_year - 9 <= int(year) <= current_year - 7:
                    descuentosARB1[year] = 0.37
                else:
                    descuentosARB1[year] = 0.28
                        
            descuento_ARB1 = descuentosARB1[Año_F]

            if Blindaje == "" or Blindaje == "$" or Blindaje == "undefined":
                SumaP = float(Suma)
                PrimaABA = Decimal(SumaP) * Decimal(0.0550090561502465) * Decimal(factor_añobisiesto)
                PrimaABB = Decimal(10000) * Decimal(0.0100018112300493) * Decimal(factor_añobisiesto)
                PrimaABC = Decimal(10000) * Decimal(0.00500090561502464) * Decimal(factor_añobisiesto)
                PrimaABD = Decimal(10000) * Decimal(0.0100018112300493) * Decimal(factor_añobisiesto)
                PrimaTotalAB = (PrimaABA + PrimaABB + PrimaABC + PrimaABD)
                PrimaAB = PrimaTotalAB - (PrimaTotalAB * Decimal(descuento_ARB1))
            else:
                SumaP = float(Suma) + float(Blindaje)
                PrimaABA = (Decimal(SumaP) * Decimal(0.0550090561502465)) * Decimal(1.5) * Decimal(factor_añobisiesto)
                PrimaABB = (Decimal(10000) + Decimal(Blindaje)) * Decimal(0.0100018112300493) * Decimal(1.5) * Decimal(factor_añobisiesto)
                PrimaABC = (Decimal(10000)) * Decimal(0.00500090561502464) * Decimal(factor_añobisiesto)
                PrimaABD = (Decimal(10000)) * Decimal(0.0100018112300493) * Decimal(factor_añobisiesto)
                PrimaTotalAB = (PrimaABA + PrimaABB + PrimaABC + PrimaABD)
                PrimaAB = PrimaTotalAB - (PrimaTotalAB * Decimal(descuento_ARB1))

            Prima_AB = "{:,.2f}".format(float(PrimaAB))
            Prima_AB = "$" + Prima_AB

            LlantaRepuesto_AB = Llanta
            
            IVA_Total = (PrimaAB + LlantaR) * Decimal(0.13)

            IVA_TotalAB = "{:,.2f}".format(float(IVA_Total))
            IVA_TotalAB = "$" + IVA_TotalAB

            Prima_Total = PrimaAB + LlantaR + IVA_Total

            Prima_TotalAB = "{:,.2f}".format(float(Prima_Total))
            Prima_TotalAB = "$" + Prima_TotalAB

            Prima_Mensual = (Prima_Total * Decimal(1.07))/12

            Prima_MensualAB = "{:,.2f}".format(float(Prima_Mensual))
            Prima_MensualAB = "$" + Prima_MensualAB

        elif (str(Año_F) in rango_ARB2) and Ag == "No":
            SumaAR = SumaA
            DeducibleAR1 = "Ahorro hasta el 50%"
            DeducibleAR2 = "del Deducible"
            RBienesAR = "$10,000.00"
            RBienesUAR = "$5,000.00"
            RExcesoAR = "$35,000.00"
            GMVariasAR = "$10,000.00"
            GMUnaAR = "$2,000.00"
            GFunerariosAR = "$2,000.00"
            LimiteAR1 = "Centroamérica"
            LimiteAR2 = "incluyendo México,"
            LimiteAR3 = "Panamá y Belice."
            MAConductorAR = "$10,000.00"
            MAOcupanteAR = "$5,000.00"
            IConductorAR = "$10,000.00"
            RpAR = Rp
            AsistenciaAR = "Incluido"
            AsistenciaHAR = "N/A"
            AutoAR = "1 evento / $150.00"
            ConductorAR = "2 eventos"
            MinoriaAR = "Incluido"
            DañosAR = "Incluido"
            GruaAR = "$1,500.00"
            LegalesAR = "$1,500.00"
            BlAR = Bld

            descuentosARB2 = {}
            for year in rango_ARB2:
                if current_year - 3 <= int(year) <= current_year + 1:
                    descuentosARB2[year] = 0.46
                elif current_year - 6 <= int(year) <= current_year - 4:
                    descuentosARB2[year] = 0.40
                elif current_year - 9 <= int(year) <= current_year - 7:
                    descuentosARB2[year] = 0.35
                else:
                    descuentosARB2[year] = 0.26
                        
            descuento_ARB2 = descuentosARB2[Año_F]

            if Blindaje == "" or Blindaje == "$":
                SumaP = float(Suma)
                PrimaABA = Decimal(SumaP) * Decimal(0.0550090561502465) * Decimal(factor_añobisiesto)
                PrimaABB = Decimal(10000) * Decimal(0.0100018112300493) * Decimal(factor_añobisiesto)
                PrimaABC = Decimal(10000) * Decimal(0.00500090561502464) * Decimal(factor_añobisiesto)
                PrimaABD = Decimal(10000) * Decimal(0.0100018112300493) * Decimal(factor_añobisiesto)
                PrimaTotalAB = (PrimaABA + PrimaABB + PrimaABC + PrimaABD)
                PrimaAB = PrimaTotalAB - (PrimaTotalAB * Decimal(descuento_ARB2))
            else:
                SumaP = float(Suma) + float(Blindaje)
                PrimaABA = (Decimal(SumaP) * Decimal(0.0550090561502465)) * Decimal(1.5) * Decimal(factor_añobisiesto)
                PrimaABB = (Decimal(10000) + Decimal(Blindaje)) * Decimal(0.0100018112300493) * Decimal(1.5) * Decimal(factor_añobisiesto)
                PrimaABC = (Decimal(10000)) * Decimal(0.00500090561502464) * Decimal(factor_añobisiesto)
                PrimaABD = (Decimal(10000)) * Decimal(0.0100018112300493) * Decimal(factor_añobisiesto)
                PrimaTotalAB = (PrimaABA + PrimaABB + PrimaABC + PrimaABD)
                PrimaAB = PrimaTotalAB - (PrimaTotalAB * Decimal(descuento_ARB2))

            Prima_AB = "{:,.2f}".format(float(PrimaAB))
            Prima_AB = "$" + Prima_AB

            LlantaRepuesto_AB = Llanta
            
            IVA_Total = (PrimaAB + LlantaR) * Decimal(0.13)

            IVA_TotalAB = "{:,.2f}".format(float(IVA_Total))
            IVA_TotalAB = "$" + IVA_TotalAB

            Prima_Total = PrimaAB + LlantaR + IVA_Total

            Prima_TotalAB = "{:,.2f}".format(float(Prima_Total))
            Prima_TotalAB = "$" + Prima_TotalAB

            Prima_Mensual = (Prima_Total * Decimal(1.07))/12

            Prima_MensualAB = "{:,.2f}".format(float(Prima_Mensual))
            Prima_MensualAB = "$" + Prima_MensualAB

        else:
            SumaAR = ""
            DeducibleAR1 = ""
            DeducibleAR2 = ""
            RBienesAR = ""
            RBienesUAR = ""
            RExcesoAR = ""
            GMVariasAR = ""
            GMUnaAR = ""
            GFunerariosAR = ""
            LimiteAR1 = ""
            LimiteAR2 = ""
            LimiteAR3 = ""
            MAConductorAR = ""
            MAOcupanteAR = ""
            IConductorAR = ""
            RpAR = ""
            AsistenciaAR = ""
            AsistenciaHAR = ""
            AutoAR = ""
            ConductorAR = ""
            MinoriaAR = ""
            DañosAR = ""
            GruaAR = ""
            LegalesAR = ""
            BlAR = ""
            Prima_AB = ""
            LlantaRepuesto_AB = ""
            IVA_TotalAB = ""
            Prima_TotalAB = ""
            Prima_MensualAB = ""

        
        ancho_texto2 = pdf.stringWidth(SumaAR, "Helvetica", 9)
        x_centro2 = 283 + (90 - ancho_texto2)/2
        pdf.drawString(x_centro2, 628, SumaAR)
        #DAÑO Y ROBO - BÁSICO
        pdf.rect(373, 626, 88, 12, fill=False, stroke=True)
        if (str(Año_F) in rango_ARB1) and Ag == "Si":
            SumaB = SumaA
            DeducibleB1 = "Participación del"
            DeducibleB2 = "100% del Deducible"
            RBienesB = "$8,000.00"
            RBienesUB = "$4,000.00"
            RExcesoB = "N/A"
            GMVariasB = "$5,000.00"
            GMUnaB = "$1,000.00"
            GFunerariosB = "$2,000.00"
            LimiteB1 = "Centroamérica"
            LimiteB2 = "incluyendo México,"
            LimiteB3 = "Panamá y Belice."
            MAConductorB = "$5,000.00"
            MAOcupanteB = "$2,500.00"
            IConductorB = "$5,000.00"
            RpB = Rp
            AsistenciaB = "Incluido"
            AsistenciaHB = "N/A"
            AutoB = "1 evento / $150.00"
            ConductorB = "2 eventos"
            MinoriaB = "N/A"
            DañosB = "N/A"
            GruaB = "$1,500.00"
            LegalesB = "$1,500.00"
            BlB = Bld

            descuentosB1 = {}
            for year in rango_ARB1:
                if current_year - 3 <= int(year) <= current_year + 1:
                    descuentosB1[year] = 0.47
                elif current_year - 6 <= int(year) <= current_year - 4:
                    descuentosB1[year] = 0.42
                elif current_year - 9 <= int(year) <= current_year - 7:
                    descuentosB1[year] = 0.37
                else:
                    descuentosB1[year] = 0.28
                        
            descuento_B1 = descuentosB1[Año_F]

            if Blindaje == "" or Blindaje == "$" or Blindaje == "undefined":
                SumaP = float(Suma)
                PrimaBA = Decimal(SumaP) * Decimal(0.0550090561502465) * Decimal(factor_añobisiesto)
                PrimaBB = Decimal(8000) * Decimal(0.0100018112300493) * Decimal(factor_añobisiesto)
                PrimaBC = Decimal(8000) * Decimal(0.00500090561502464) * Decimal(factor_añobisiesto)
                PrimaBD = Decimal(5000) * Decimal(0.0100018112300493) * Decimal(factor_añobisiesto)
                PrimaTotalB = (PrimaBA + PrimaBB + PrimaBC + PrimaBD)
                PrimaB = PrimaTotalB - (PrimaTotalB * Decimal(descuento_B1))
            else:
                SumaP = float(Suma) + float(Blindaje)
                PrimaBA = (Decimal(SumaP) * Decimal(0.0550090561502465)) * Decimal(1.5) * Decimal(factor_añobisiesto)
                PrimaBB = (Decimal(8000) + Decimal(Blindaje)) * Decimal(0.0100018112300493) * Decimal(1.5) * Decimal(factor_añobisiesto)
                PrimaBC = (Decimal(8000)) * Decimal(0.00500090561502464) * Decimal(factor_añobisiesto)
                PrimaBD = (Decimal(5000)) * Decimal(0.0100018112300493) * Decimal(factor_añobisiesto)
                PrimaTotalB = (PrimaBA + PrimaBB + PrimaBC + PrimaBD)
                PrimaB = PrimaTotalB - (PrimaTotalB * Decimal(descuento_B1))

            Prima_B = "{:,.2f}".format(float(PrimaB))
            Prima_B = "$" + Prima_B

            LlantaRepuesto_B = Llanta
            
            IVA_Total = (PrimaB + LlantaR) * Decimal(0.13)

            IVA_TotalB = "{:,.2f}".format(float(IVA_Total))
            IVA_TotalB = "$" + IVA_TotalB

            Prima_Total = PrimaB + LlantaR + IVA_Total

            Prima_TotalB = "{:,.2f}".format(float(Prima_Total))
            Prima_TotalB = "$" + Prima_TotalB 

            Prima_Mensual = (Prima_Total * Decimal(1.07))/12

            Prima_MensualB = "{:,.2f}".format(float(Prima_Mensual))
            Prima_MensualB = "$" + Prima_MensualB

        elif (str(Año_F) in rango_ARB2) and Ag == "No":
            SumaB = SumaA
            DeducibleB1 = "Participación del"
            DeducibleB2 = "100% del Deducible"
            RBienesB = "$8,000.00"
            RBienesUB = "$4,000.00"
            RExcesoB = "N/A"
            GMVariasB = "$5,000.00"
            GMUnaB = "$1,000.00"
            GFunerariosB = "$2,0000.00"
            LimiteB1 = "Centroamérica"
            LimiteB2 = "incluyendo México,"
            LimiteB3 = "Panamá y Belice."
            MAConductorB = "$5,000.00"
            MAOcupanteB = "$2,500.00"
            IConductorB = "$5,000.00"
            RpB = Rp
            AsistenciaB = "Incluido"
            AsistenciaHB = "N/A"
            AutoB = "1 evento / $150.00"
            ConductorB = "2 eventos"
            MinoriaB = "N/A"
            DañosB = "N/A"
            GruaB = "$1,500.00"
            LegalesB = "$1,500.00"
            BlB = Bld

            descuentosB2 = {}
            for year in rango_ARB2:
                if current_year - 3 <= int(year) <= current_year + 1:
                    descuentosB2[year] = 0.46
                elif current_year - 6 <= int(year) <= current_year - 4:
                    descuentosB2[year] = 0.40
                elif current_year - 9 <= int(year) <= current_year - 7:
                    descuentosB2[year] = 0.35
                else:
                    descuentosB2[year] = 0.26
                        
            descuento_B2 = descuentosB2[Año_F]

            if Blindaje == "" or Blindaje == "$":
                SumaP = float(Suma)
                PrimaBA = Decimal(SumaP) * Decimal(0.0550090561502465) * Decimal(factor_añobisiesto)
                PrimaBB = Decimal(8000) * Decimal(0.0100018112300493) * Decimal(factor_añobisiesto)
                PrimaBC = Decimal(8000) * Decimal(0.00500090561502464) * Decimal(factor_añobisiesto)
                PrimaBD = Decimal(5000) * Decimal(0.0100018112300493) * Decimal(factor_añobisiesto)
                PrimaTotalB = (PrimaBA + PrimaBB + PrimaBC + PrimaBD)
                PrimaB = PrimaTotalB - (PrimaTotalB * Decimal(descuento_B2))
            else:
                SumaP = float(Suma) + float(Blindaje)
                PrimaBA = (Decimal(SumaP) * Decimal(0.0550090561502465)) * Decimal(1.5) * Decimal(factor_añobisiesto)
                PrimaBB = (Decimal(8000) + Decimal(Blindaje)) * Decimal(0.0100018112300493) * Decimal(1.5) * Decimal(factor_añobisiesto)
                PrimaBC = (Decimal(8000)) * Decimal(0.00500090561502464) * Decimal(factor_añobisiesto)
                PrimaBD = (Decimal(5000)) * Decimal(0.0100018112300493) * Decimal(factor_añobisiesto)
                PrimaTotalB = (PrimaBA + PrimaBB + PrimaBC + PrimaBD)
                PrimaB = PrimaTotalB - (PrimaTotalB * Decimal(descuento_B2))

            Prima_B = "{:,.2f}".format(float(PrimaB))
            Prima_B = "$" + Prima_B

            LlantaRepuesto_B = Llanta
            
            IVA_Total = (PrimaB + LlantaR) * Decimal(0.13)

            IVA_TotalB = "{:,.2f}".format(float(IVA_Total))
            IVA_TotalB = "$" + IVA_TotalB

            Prima_Total = PrimaB + LlantaR + IVA_Total

            Prima_TotalB = "{:,.2f}".format(float(Prima_Total))
            Prima_TotalB = "$" + Prima_TotalB

            Prima_Mensual = (Prima_Total * Decimal(1.07))/12

            Prima_MensualB = "{:,.2f}".format(float(Prima_Mensual))
            Prima_MensualB = "$" + Prima_MensualB
        else:
            SumaB = ""
            DeducibleB1 = ""
            DeducibleB2 = ""
            RBienesB = ""
            RBienesUB = ""
            RExcesoB = ""
            GMVariasB = ""
            GMUnaB = ""
            GFunerariosB = ""
            LimiteB1 = ""
            LimiteB2 = ""
            LimiteB3 = ""
            MAConductorB = ""
            MAOcupanteB = ""
            IConductorB = ""
            RpB = ""
            AsistenciaB = ""
            AsistenciaHB = ""
            AutoB = ""
            ConductorB = ""
            MinoriaB = ""
            DañosB = ""
            GruaB = ""
            LegalesB = ""
            BlB = ""
            Prima_B = ""
            LlantaRepuesto_B = ""
            IVA_TotalB = ""
            Prima_TotalB = ""
            Prima_MensualB = ""
        

        ancho_texto3 = pdf.stringWidth(SumaB, "Helvetica", 9)
        x_centro3 = 373 + (88 - ancho_texto3)/2
        pdf.drawString(x_centro3, 628, SumaB)
        #DAÑO Y ROBO - RESP. CIVIL
        pdf.rect(461, 626, 104, 12, fill=False, stroke=True)
        pdf.drawString(505, 628, "N/A")
        #DEDUCIBLE
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0.65, 0.65, 0.65)
        pdf.rect(30, 601, 153, 25, fill=False, stroke=True)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica", 9)
        pdf.drawString(32, 611, "Deducible del " + deducible)
        #DEDUCIBLE - FC
        pdf.rect(183, 601, 100, 25, fill=False, stroke=True)
        pdf.drawString(190, 614, DeducibleFC1)
        pdf.drawString(205, 605, DeducibleFC2)
        #DEDUCIBLE - AR
        pdf.rect(283, 601, 90, 25, fill=False, stroke=True)
        pdf.drawString(287, 614, DeducibleAR1)
        pdf.drawString(301, 605, DeducibleAR2)
        #DEDUCIBLE - B
        pdf.rect(373, 601, 88, 25, fill=False, stroke=True)
        pdf.drawString(384, 614, DeducibleB1)
        pdf.drawString(377, 605, DeducibleB2)
        #DEDUCIBLE - RESP. CIVIL
        pdf.rect(461, 601, 104, 25, fill=False, stroke=True)
        pdf.drawString(502, 611, "$200")
        #RESP. BIENES
        pdf.rect(30, 589, 153, 12, fill=False, stroke=True)
        pdf.drawString(32, 591, "Responsabilidad Civil en Bienes")
        #RESP. BIENES FC
        pdf.rect(183, 589, 100, 12, fill=False, stroke=True)
        pdf.drawString(211, 591, RBienesFC)
        #RESP. BIENES AR
        pdf.rect(283, 589, 90, 12, fill=False, stroke=True)
        pdf.drawString(306, 591, RBienesAR)
        #RESP. BIENES B
        pdf.rect(373, 589, 88, 12, fill=False, stroke=True)
        pdf.drawString(398, 591, RBienesB)
        #RESP. BIENES RC
        pdf.rect(461, 589, 104, 12, fill=False, stroke=True)
        pdf.drawString(493, 591, "$6,000.00")
        #RESP. PERSONASV
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0.65, 0.65, 0.65)
        pdf.rect(30, 564, 153, 25, fill=False, stroke=True)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica", 9)
        pdf.drawString(32, 578, "Responsabilidad Civil en Personas")
        pdf.drawString(32, 567, "(Varias personas)")
        #RESP. PERSONASV FC
        pdf.rect(183, 564, 100, 25, fill=False, stroke=True)
        pdf.drawString(211, 573, RBienesFC)
        #RESP. PERSONASV AR
        pdf.rect(283, 564, 90, 25, fill=False, stroke=True)
        pdf.drawString(306, 573, RBienesAR)
        #RESP. PERSONASV B
        pdf.rect(373, 564, 88, 25, fill=False, stroke=True)
        pdf.drawString(398, 573, RBienesB)
        #RESP. PERSONASV RC
        pdf.rect(461, 564, 104, 25, fill=False, stroke=True)
        pdf.drawString(493, 573, "$6,000.00")
        #RESP. PERSONASU
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0.65, 0.65, 0.65)
        pdf.rect(30, 539, 153, 25, fill=False, stroke=True)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica", 9)
        pdf.drawString(32, 553, "Responsabilidad Civil en Personas")
        pdf.drawString(32, 542, "(Por una persona)")
        #RESP. PERSONASU FC
        pdf.rect(183, 539, 100, 25, fill=False, stroke=True)
        pdf.drawString(214, 548, RBienesUFC)
        #RESP. PERSONASU AR
        pdf.rect(283, 539, 90, 25, fill=False, stroke=True)
        pdf.drawString(309, 548, RBienesUAR)
        #RESP. PERSONASU B
        pdf.rect(373, 539, 88, 25, fill=False, stroke=True)
        pdf.drawString(399, 548, RBienesUB)
        #RESP. PERSONASU RC
        pdf.rect(461, 539, 104, 25, fill=False, stroke=True)
        pdf.drawString(493, 548, "$3,000.00")

        #RESP. EN EXCESO
        pdf.rect(30, 527, 153, 12, fill=False, stroke=True)
        pdf.drawString(32, 529, "Responsabilidad Civil en exceso")
        #RESP. EN EXCESO FC
        pdf.rect(183, 527, 100, 12, fill=False, stroke=True)
        pdf.drawString(212, 529, RExcesoFC)
        #RESP. EN EXCESO AR
        pdf.rect(283, 527, 90, 12, fill=False, stroke=True)
        pdf.drawString(307, 529, RExcesoAR)
        #RESP. EN EXCESO B
        pdf.rect(373, 527, 88, 12, fill=False, stroke=True)
        pdf.drawString(412, 529, RExcesoB)
        #RESP. EN EXCESO RC
        pdf.rect(461, 527, 104, 12, fill=False, stroke=True)
        pdf.drawString(507, 529, "N/A")
        #GM - V
        pdf.rect(30, 515, 153, 12, fill=False, stroke=True)
        pdf.drawString(32, 517, "Gastos Médicos (Varias personas)")
        #GM - VFC
        pdf.rect(183, 515, 100, 12, fill=False, stroke=True)
        pdf.drawString(212, 517, GMVariasFC)
        #GM - VAR
        pdf.rect(283, 515, 90, 12, fill=False, stroke=True)
        pdf.drawString(307, 517, GMVariasAR)
        #GM - VB
        pdf.rect(373, 515, 88, 12, fill=False, stroke=True)
        pdf.drawString(399, 517, GMVariasB)
        #GM - VRC
        pdf.rect(461, 515, 104, 12, fill=False, stroke=True)
        pdf.drawString(507, 517, "N/A")
        #GM - U
        pdf.rect(30, 503, 153, 12, fill=False, stroke=True)
        pdf.drawString(32, 505, "Gastos Médicos (Por una persona)")
        #GM - UFC
        pdf.rect(183, 503, 100, 12, fill=False, stroke=True)
        pdf.drawString(215, 505, GMUnaFC)
        #GM - UAR
        pdf.rect(283, 503, 90, 12, fill=False, stroke=True)
        pdf.drawString(310, 505, GMUnaAR)
        #GM - UB
        pdf.rect(373, 503, 88, 12, fill=False, stroke=True)
        pdf.drawString(400, 505, GMUnaB)
        #GM - RC
        pdf.rect(461, 503, 104, 12, fill=False, stroke=True)
        pdf.drawString(507, 505, "N/A")
        #GF
        pdf.rect(30, 491, 153, 12, fill=False, stroke=True)
        pdf.drawString(32, 493, "Gastos Funerarios")
        #GF - FC
        pdf.rect(183, 491, 100, 12, fill=False, stroke=True)
        pdf.drawString(215, 493, GFunerariosFC)
        #GF - AR
        pdf.rect(283, 491, 90, 12, fill=False, stroke=True)
        pdf.drawString(310, 493, GFunerariosAR)
        #GF - B
        pdf.rect(373, 491, 88, 12, fill=False, stroke=True)
        pdf.drawString(400, 493, GFunerariosB)
        #GF - RC
        pdf.rect(461, 491, 104, 12, fill=False, stroke=True)
        pdf.drawString(507, 493, "N/A")

        #ENCABEZADO2
        pdf.setFillColorRGB(0.89, 0.12, 0.19)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(30, 454, 535, 28, fill=True, stroke=False)
        pdf.setFillColorRGB(1, 1, 1)
        pdf.setFont("Helvetica-Bold", 9)
    
        pdf.drawString(48, 465, "BENEFICIOS ADICIONALES:")

        #LÍMITE TERRITORIAL
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0.65, 0.65, 0.65)
        pdf.rect(30, 418, 153, 33, fill=False, stroke=True)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica", 9)
        pdf.drawString(32, 431, "Límite Territorial")
        #LÍMITE TERRITORIAL - FC
        pdf.rect(183, 418, 100, 33, fill=False, stroke=True)
        pdf.drawString(201, 440, LimiteFC1)
        pdf.drawString(194, 431, LimiteFC2)
        pdf.drawString(198, 421, LimiteFC3)
        #LÍMITE TERRITORIAL - AR
        pdf.rect(283, 418, 90, 33, fill=False, stroke=True)
        pdf.drawString(297, 440, LimiteAR1)
        pdf.drawString(291, 431, LimiteAR2)
        pdf.drawString(295, 421, LimiteAR3)
        #LÍMITE TERRITORIAL - B
        pdf.rect(373, 418, 88, 33, fill=False, stroke=True)
        pdf.drawString(387, 440, LimiteB1)
        pdf.drawString(379, 431, LimiteB2)
        pdf.drawString(384, 421, LimiteB3)
        #LÍMITE TERRITORIAL - RC
        pdf.rect(461, 418, 104, 33, fill=False, stroke=True)
        pdf.drawString(481, 440, "Centroamérica")
        pdf.drawString(474, 431, "incluyendo México,")
        pdf.drawString(478, 421, "Panamá y Belice.")

        #MUERTE EN ACCIDENTE CONDUCTOR
        pdf.rect(30, 393, 153, 25, fill=False, stroke=True)
        pdf.drawString(32, 406, "Muerte en Accidente de Tránsito")
        pdf.drawString(32, 395, "del Conductor")
        #MUERTE EN ACCIDENTE CONDUCTOR - FC
        pdf.rect(183, 393, 100, 25, fill=False, stroke=True)
        pdf.drawString(210, 402, MAConductorFC)
        #MUERTE EN ACCIDENTE CONDUCTOR - AR
        pdf.rect(283, 393, 90, 25, fill=False, stroke=True)
        pdf.drawString(305, 402, MAConductorAR)
        #MUERTE EN ACCIDENTE CONDUCTOR - B
        pdf.rect(373, 393, 88, 25, fill=False, stroke=True)
        pdf.drawString(397, 402, MAConductorB)
        #MUERTE EN ACCIDENTE CONDUCTOR - RC
        pdf.rect(461, 393, 104, 25, fill=False, stroke=True)
        pdf.drawString(504, 402, "N/A")

        #MUERTE EN ACCIDENTE OCUPANTE
        pdf.rect(30, 368, 153, 25, fill=False, stroke=True)
        pdf.drawString(32, 381, "Muerte en Accidente de Tránsito")
        pdf.drawString(32, 370, "por Ocupante")
        #MUERTE EN ACCIDENTE OCUPANTE - FC
        pdf.rect(183, 368, 100, 25, fill=False, stroke=True)
        pdf.drawString(214, 377, MAOcupanteFC)
        #MUERTE EN ACCIDENTE OCUPANTE - AR
        pdf.rect(283, 368, 90, 25, fill=False, stroke=True)
        pdf.drawString(309, 377, MAOcupanteAR)
        #MUERTE EN ACCIDENTE OCUPANTE - B
        pdf.rect(373, 368, 88, 25, fill=False, stroke=True)
        pdf.drawString(397, 377, MAOcupanteB)
        #MUERTE EN ACCIDENTE OCUPANTE - RC
        pdf.rect(461, 368, 104, 25, fill=False, stroke=True)
        pdf.drawString(504, 377, "N/A")

        #INCAPACIDAD
        pdf.rect(30, 343, 153, 25, fill=False, stroke=True)
        pdf.drawString(32, 358, "Incapacidad Total y Permanente por")
        pdf.drawString(32, 347, "Accidente de Tránsito del conductor")
        #INCAPACIDAD - FC
        pdf.rect(183, 343, 100, 25, fill=False, stroke=True)
        pdf.drawString(211, 352, IConductorFC)
        #INCAPACIDAD - AR
        pdf.rect(283, 343, 90, 25, fill=False, stroke=True)
        pdf.drawString(306, 352, IConductorAR)
        #INCAPACIDAD - B
        pdf.rect(373, 343, 88, 25, fill=False, stroke=True)
        pdf.drawString(397, 352, IConductorB)
        #INCAPACIDAD - RC
        pdf.rect(461, 343, 104, 25, fill=False, stroke=True)
        pdf.drawString(504, 352, "N/A")

        #LLANTA DE REPUESTO
        pdf.rect(30, 331, 153, 12, fill=False, stroke=True)
        pdf.drawString(32, 333, "Llanta de Repuesto")
        #LLANTA DE REPUESTO - FC
        pdf.rect(183, 331, 100, 12, fill=False, stroke=True)
        pdf.drawString(218, 333, RpFC)
        #LLANTA DE REPUESTO - AR
        pdf.rect(283, 331, 90, 12, fill=False, stroke=True)
        pdf.drawString(313, 333, RpAR)
        #LLANTA DE REPUESTO - B
        pdf.rect(373, 331, 88, 12, fill=False, stroke=True)
        pdf.drawString(402, 333, RpB)
        #LLANTA DE REPUESTO - RC
        pdf.rect(461, 331, 104, 12, fill=False, stroke=True)
        pdf.drawString(505, 333, "N/A")

        #SERVICIO DE ASISTENCIA VIAL
        pdf.rect(30, 306, 153, 25, fill=False, stroke=True)
        pdf.drawString(32, 319, "Servicio de asistencia vial (Cambio")
        pdf.drawString(32, 309, "de llanta, paso de corriente, otros).")
        #SERVICIO DE ASISTENCIA VIAL - FC
        pdf.rect(183, 306, 100, 25, fill=False, stroke=True)
        pdf.drawString(219, 315, AsistenciaFC)
        #SERVICIO DE ASISTENCIA VIAL - AR
        pdf.rect(283, 306, 90, 25, fill=False, stroke=True)
        pdf.drawString(314, 315, AsistenciaAR)
        #SERVICIO DE ASISTENCIA VIAL - B
        pdf.rect(373, 306, 88, 25, fill=False, stroke=True)
        pdf.drawString(402, 315, AsistenciaB)
        #SERVICIO DE ASISTENCIA VIAL - RC
        pdf.rect(461, 306, 104, 25, fill=False, stroke=True)
        pdf.drawString(498, 315, "Incluido")

        #ASISTENCIA HOGAR
        pdf.rect(30, 294, 153, 12, fill=False, stroke=True)
        pdf.drawString(32, 296, "Servicio de Asistencia en el Hogar")
        #ASISTENCIA HOGAR - FC
        pdf.rect(183, 294, 100, 12, fill=False, stroke=True)
        pdf.drawString(219, 296, AsistenciaHFC)
        #ASISTENCIA HOGAR - AR
        pdf.rect(283, 294, 90, 12, fill=False, stroke=True)
        pdf.drawString(320, 296, AsistenciaHAR)
        #ASISTENCIA HOGAR - B
        pdf.rect(373, 294, 88, 12, fill=False, stroke=True)
        pdf.drawString(410, 296, AsistenciaHB)
        #ASISTENCIA HOGAR - RC
        pdf.rect(461, 294, 104, 12, fill=False, stroke=True)
        pdf.drawString(505, 296, "N/A")

        #AUTO POR ROBO 
        pdf.rect(30, 282, 153, 12, fill=False, stroke=True)
        pdf.drawString(32, 284, "Auto por robo de vehículo")
        #AUTO POR ROBO - FC
        pdf.rect(183, 282, 100, 12, fill=False, stroke=True)
        pdf.drawString(195, 284, AutoFC)
        #AUTO POR ROBO - AR
        pdf.rect(283, 282, 90, 12, fill=False, stroke=True)
        pdf.drawString(290, 284, AutoAR)
        #AUTO POR ROBO - B
        pdf.rect(373, 282, 88, 12, fill=False, stroke=True)
        pdf.drawString(380, 284, AutoB)
        #AUTO POR ROBO - RC
        pdf.rect(461, 282, 104, 12, fill=False, stroke=True)
        pdf.drawString(505, 284, "N/A")

        #CONDUCTOR DESIGNADO 
        pdf.rect(30, 270, 153, 12, fill=False, stroke=True)
        pdf.drawString(32, 272, "Conductor Designado")
        #CONDUCTOR DESIGNADO - FC
        pdf.rect(183, 270, 100, 12, fill=False, stroke=True)
        pdf.drawString(216, 272, ConductorFC)
        #CONDUCTOR DESIGNADO - AR
        pdf.rect(283, 270, 90, 12, fill=False, stroke=True)
        pdf.drawString(312, 272, ConductorAR)
        #CONDUCTOR DESIGNADO - B
        pdf.rect(373, 270, 88, 12, fill=False, stroke=True)
        pdf.drawString(398, 272, ConductorB)
        #CONDUCTOR DESIGNADO - RC
        pdf.rect(461, 270, 104, 12, fill=False, stroke=True)
        pdf.drawString(505, 272, "N/A")

        #MINORÍA 
        pdf.rect(30, 258, 153, 12, fill=False, stroke=True)
        pdf.drawString(32, 260, "Minoría de edad y/o inexperiencia")
        #MINORÍA - FC
        pdf.rect(183, 258, 100, 12, fill=False, stroke=True)
        pdf.drawString(218, 260, MinoriaFC)
        #MINORÍA - AR
        pdf.rect(283, 258, 90, 12, fill=False, stroke=True)
        pdf.drawString(314, 260, MinoriaAR)
        #MINORÍA - B
        pdf.rect(373, 258, 88, 12, fill=False, stroke=True)
        pdf.drawString(410, 260, MinoriaB)
        #MINORÍA - RC
        pdf.rect(461, 258, 104, 12, fill=False, stroke=True)
        pdf.drawString(505, 260, "N/A")

        #DAÑOS EN MALOS CAMINOS 
        pdf.rect(30, 233, 153, 25, fill=False, stroke=True)
        pdf.drawString(32, 247, "Daños o pérdidas cuando el vehículo")
        pdf.drawString(32,  235, "transite en malos caminos")
        #DAÑOS EN MALOS CAMINOS - FC
        pdf.rect(183, 233, 100, 25, fill=False, stroke=True)
        pdf.drawString(218, 242, DañosFC)
        #DAÑOS EN MALOS CAMINOS - AR
        pdf.rect(283, 233, 90, 25, fill=False, stroke=True)
        pdf.drawString(314, 242, DañosAR)
        #DAÑOS EN MALOS CAMINOS - B
        pdf.rect(373, 233, 88, 25, fill=False, stroke=True)
        pdf.drawString(410, 242, DañosB)
        #DAÑOS EN MALOS CAMINOS - RC
        pdf.rect(461, 233, 104, 25, fill=False, stroke=True)
        pdf.drawString(505, 242, "N/A")

        #GASTOS DE GRÚA 
        pdf.rect(30, 221, 153, 12, fill=False, stroke=True)
        pdf.drawString(32, 223, "Gastos de grúa")
        #GASTOS DE GRÚA - FC
        pdf.rect(183, 221, 100, 12, fill=False, stroke=True)
        pdf.drawString(214, 223, GruaFC)
        #GASTOS DE GRÚA - AR
        pdf.rect(283, 221, 90, 12, fill=False, stroke=True)
        pdf.drawString(310, 223, GruaAR)
        #GASTOS DE GRÚA - B
        pdf.rect(373, 221, 88, 12, fill=False, stroke=True)
        pdf.drawString(398, 223, GruaB)
        #GASTOS DE GRÚA - RC
        pdf.rect(461, 221, 104, 12, fill=False, stroke=True)
        pdf.drawString(494, 223, "$1,500.00")

        #GASTOS LEGALES 
        pdf.rect(30, 209, 153, 12, fill=False, stroke=True)
        pdf.drawString(32, 211, "Gastos de grúa")
        #GASTOS LEGALES - FC
        pdf.rect(183, 209, 100, 12, fill=False, stroke=True)
        pdf.drawString(214, 211, LegalesFC)
        #GASTOS LEGALES - AR
        pdf.rect(283, 209, 90, 12, fill=False, stroke=True)
        pdf.drawString(310, 211, LegalesAR)
        #GASTOS LEGALES - B
        pdf.rect(373, 209, 88, 12, fill=False, stroke=True)
        pdf.drawString(398, 211, LegalesB)
        #GASTOS LEGALES - RC
        pdf.rect(461, 209, 104, 12, fill=False, stroke=True)
        pdf.drawString(494, 211, "$1,500.00")

        #BLINDAJE 
        pdf.rect(30, 197, 153, 12, fill=False, stroke=True)
        pdf.drawString(32, 199, "Blindaje")
        #BLINDAJE - FC
        pdf.rect(183, 197, 100, 12, fill=False, stroke=True)
        ancho_texto4 = pdf.stringWidth(BlFC, "Helvetica", 9)
        x_centro4 = 183 + (100 - ancho_texto4)/2
        pdf.drawString(x_centro4, 199, BlFC)
        #BLINDAJE - AR
        pdf.rect(283, 197, 90, 12, fill=False, stroke=True)
        ancho_texto5 = pdf.stringWidth(BlAR, "Helvetica", 9)
        x_centro5 = 283 + (90 - ancho_texto5)/2
        pdf.drawString(x_centro5, 199, BlAR)
        #BLINDAJE - B
        pdf.rect(373, 197, 88, 12, fill=False, stroke=True)
        ancho_texto6 = pdf.stringWidth(BlB, "Helvetica", 9)
        x_centro6 = 373 + (88 - ancho_texto6)/2
        pdf.drawString(x_centro6, 199, BlB)
        #BLINDAJE - RC
        pdf.rect(461, 197, 104, 12, fill=False, stroke=True)
        pdf.drawString(506, 199, "N/A")

        #ENCABEZADO3
        pdf.setFillColorRGB(0.89, 0.12, 0.19)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(30, 167, 535, 20, fill=True, stroke=False)
        pdf.setFillColorRGB(1, 1, 1)
        pdf.setFont("Helvetica-Bold", 9)
    
        pdf.drawString(90, 173, "PRIMA:")

        #PRIMA
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0.65, 0.65, 0.65)
        pdf.rect(30, 150, 153, 12, fill=False, stroke=True)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica", 9)
        pdf.drawString(32, 152, "Prima")
        #PRIMA - FC
        pdf.rect(183, 150, 100, 12, fill=False, stroke=True)
        ancho_texto7 = pdf.stringWidth(Prima_FC, "Helvetica", 9)
        x_centro7 = 183 + (100 - ancho_texto7)/2
        pdf.drawString(x_centro7, 152, Prima_FC)
        #PRIMA - AR
        pdf.rect(283, 150, 90, 12, fill=False, stroke=True)
        ancho_texto12 = pdf.stringWidth(Prima_AB, "Helvetica", 9)
        x_centro12 = 283 + (90 - ancho_texto12)/2
        pdf.drawString(x_centro12, 152, Prima_AB)
        #PRIMA - B
        pdf.rect(373, 150, 88, 12, fill=False, stroke=True)
        ancho_texto17 = pdf.stringWidth(Prima_B, "Helvetica", 9)
        x_centro17 = 373 + (88 - ancho_texto17)/2
        pdf.drawString(x_centro17, 152, Prima_B)
        #PRIMA - RC
        PrimaRCA = Decimal(6000) * (Decimal(0.0100018112300493)/Decimal(0.20)) * Decimal(factor_añobisiesto)
        PrimaRCB = Decimal(6000) * Decimal(0.00500090561502464) * Decimal(factor_añobisiesto)

        Prima_RCA = PrimaRCA + PrimaRCB

        PrimaRCA_Total = Prima_RCA - (Prima_RCA * Decimal(0.54678))

        Prima_RC_Total = "{:,.2f}".format(float(PrimaRCA_Total))
        
        IVATotalRC = PrimaRCA_Total * Decimal(0.13)

        IVA_TotalRC = "{:,.2f}".format(float(IVATotalRC))

        PrimaTotalRC = PrimaRCA_Total + IVATotalRC

        Prima_TotalRC = "{:,.2f}".format(float(PrimaTotalRC))

        PrimaMensualRC = (PrimaTotalRC * Decimal(1.07))/12

        Prima_MensualRC = "{:,.2f}".format(float(PrimaMensualRC))

        pdf.rect(461, 150, 104, 12, fill=False, stroke=True)
        ancho_texto22 = pdf.stringWidth("$" + Prima_RC_Total, "Helvetica", 9)
        x_centro22 = 461 + (104 - ancho_texto22)/2
        pdf.drawString(x_centro22, 152, "$" + Prima_RC_Total)

        #LLANTA DE REPUESTO $
        pdf.rect(30, 138, 153, 12, fill=False, stroke=True)
        pdf.drawString(32, 140, "Llanta de Repuesto")
        #LLANTA DE REPUESTO $ - FC
        pdf.rect(183, 138, 100, 12, fill=False, stroke=True)
        ancho_texto8 = pdf.stringWidth(LlantaRepuesto_FC, "Helvetica", 9)
        x_centro8 = 183 + (100 - ancho_texto8)/2
        pdf.drawString(x_centro8, 140, LlantaRepuesto_FC)
        #LLANTA DE REPUESTO $ - AR
        pdf.rect(283, 138, 90, 12, fill=False, stroke=True)
        ancho_texto13 = pdf.stringWidth(LlantaRepuesto_AB, "Helvetica", 9)
        x_centro13 = 283 + (90 - ancho_texto13)/2
        pdf.drawString(x_centro13, 140, LlantaRepuesto_AB)
        #LLANTA DE REPUESTO $ - B
        pdf.rect(373, 138, 88, 12, fill=False, stroke=True)
        ancho_texto18 = pdf.stringWidth(LlantaRepuesto_B, "Helvetica", 9)
        x_centro18 = 373 +(88 - ancho_texto18)/2
        pdf.drawString(x_centro18, 140, LlantaRepuesto_B)
        #LLANTA DE REPUESTO $ - RC
        pdf.rect(461, 138, 104, 12, fill=False, stroke=True)
        pdf.drawString(502, 140, "$0.00")

        #IVA
        pdf.rect(30, 126, 153, 12, fill=False, stroke=True)
        pdf.drawString(32, 128, "IVA")
        #IVA - FC
        pdf.rect(183, 126, 100, 12, fill=False, stroke=True)
        ancho_texto9 = pdf.stringWidth(IVA_TotalFC, "Helvetica", 9)
        x_centro9 = 183 + (100 - ancho_texto9)/2
        pdf.drawString(x_centro9, 128, IVA_TotalFC)
        #IVA - AR
        pdf.rect(283, 126, 90, 12, fill=False, stroke=True)
        ancho_texto14 = pdf.stringWidth(IVA_TotalAB, "Helvetica", 9)
        x_centro14 = 283 + (90 - ancho_texto14)/2
        pdf.drawString(x_centro14, 128, IVA_TotalAB)
        #IVA - B
        pdf.rect(373, 126, 88, 12, fill=False, stroke=True)
        ancho_texto19 = pdf.stringWidth(IVA_TotalB, "Helvetica", 9)
        x_centro19 = 373 + (88 - ancho_texto19)/2
        pdf.drawString(x_centro19, 128, IVA_TotalB)
        #IVA - RC
        pdf.rect(461, 126, 104, 12, fill=False, stroke=True)
        ancho_texto23 = pdf.stringWidth("$" + IVA_TotalRC, "Helvetica", 9)
        x_centro23 = 461 + (104 - ancho_texto23)/2
        pdf.drawString(x_centro23, 128, "$" + IVA_TotalRC)

        #PRIMA TOTAL
        pdf.rect(30, 114, 153, 12, fill=False, stroke=True)
        pdf.drawString(32, 116, "Prima Total")
        #PRIMA TOTAL - FC
        pdf.rect(183, 114, 100, 12, fill=False, stroke=True)
        ancho_texto10 = pdf.stringWidth(Prima_TotalFC, "Helvetica", 9)
        x_centro10 = 183 + (100 - ancho_texto10)/2
        pdf.drawString(x_centro10, 116, Prima_TotalFC)
        #PRIMA TOTAL - AR
        pdf.rect(283, 114, 90, 12, fill=False, stroke=True)
        ancho_texto15 = pdf.stringWidth(Prima_TotalAB, "Helvetica", 9)
        x_centro15 = 283 + (90 - ancho_texto15)/2
        pdf.drawString(x_centro15, 116, Prima_TotalAB)
        #PRIMA TOTAL - B
        pdf.rect(373, 114, 88, 12, fill=False, stroke=True)
        ancho_texto20 = pdf.stringWidth(Prima_TotalB, "Helvetica", 9)
        x_centro20 = 373 + (88 - ancho_texto20)/2
        pdf.drawString(x_centro20, 116, Prima_TotalB)
        #PRIMA TOTAL - RC
        pdf.rect(461, 114, 104, 12, fill=False, stroke=True)
        ancho_texto24 = pdf.stringWidth("$" + Prima_TotalRC, "Helvetica", 9)
        x_centro24 = 461 + (104 - ancho_texto24)/2
        pdf.drawString(x_centro24, 116, "$" + Prima_TotalRC)

        #PRIMA MENSUAL
        pdf.setFont("Helvetica-Bold", 9)
        pdf.rect(30, 102, 153, 12, fill=False, stroke=True)
        pdf.drawString(32, 104, "Prima Mensual")
        #PRIMA MENSUAL - FC
        pdf.rect(183, 102, 100, 12, fill=False, stroke=True)
        ancho_texto11 = pdf.stringWidth(Prima_MensualFC, "Helvetica", 9)
        x_centro11 = 183 + (100 - ancho_texto11)/2
        pdf.drawString(x_centro11, 104, Prima_MensualFC)
        #PRIMA MENSUAL - AR
        pdf.rect(283, 102, 90, 12, fill=False, stroke=True)
        ancho_texto16 = pdf.stringWidth(Prima_MensualAB, "Helvetica", 9)
        x_centro16 = 283 + (90 - ancho_texto16)/2
        pdf.drawString(x_centro16, 104, Prima_MensualAB)
        #PRIMA MENSUAL - B
        pdf.rect(373, 102, 88, 12, fill=False, stroke=True)
        ancho_texto21 = pdf.stringWidth(Prima_MensualB, "Helvetica", 9)
        x_centro21 = 373 + (88 - ancho_texto21)/2
        pdf.drawString(x_centro21, 104, Prima_MensualB)
        #PRIMA MENSUAL - RC
        pdf.rect(461, 102, 104, 12, fill=False, stroke=True)
        ancho_texto25 = pdf.stringWidth("$" + Prima_MensualRC)
        x_centro25 = 461 + (104 - ancho_texto25)/2
        pdf.drawString(x_centro25, 104, "$" + Prima_MensualRC)

        #SELECCIONE EL PLAN
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(30, 77, 535, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica-Bold", 9)
    
        pdf.drawString(250, 80, "SELECCIONE EL PLAN")

        pdf.setFont("Helvetica", 9)
        #PLAN FULL COVER
        pdf.drawString(45, 65, "PLAN FULL COVER")
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(138, 63, 13, 10, fill=False, stroke=True)
        #PLAN AUTO RENTABLE
        pdf.drawString(160, 65, "PLAN AUTO RENTABLE")
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(274, 63, 13, 10, fill=False, stroke=True)
        #PLAN BÁSICO
        pdf.drawString(300, 65, "PLAN BÁSICO")
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(369, 63, 13, 10, fill=False, stroke=True)
        #PLAN RESPONSABILIDAD CIVIL
        pdf.drawString(390, 65, "PLAN RESPONSABILIDAD CIVIL")
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(537, 63, 13, 10, fill=False, stroke=True)
        pdf.setFont("Helvetica", 9)
        # Guardar el PDF en el buffer
        pdf.showPage()
        
        #Página 2
        pdf.setFont("Helvetica", 9)
        pdf.drawString(30, 770, "Oferta válida por 15 días de la fecha de su emisión:")
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(240, 770, fecha_actual)

        pdf.setFont("Helvetica", 9)
        pdf.drawString(30, 750, "La presente cotización no constituye aceptación del riesgo por parte de Seguros Atlántida S.A. En caso de aceptar la presente")
        pdf.drawString(30, 738, " cotización, favor remitirse a nuestros medios de comunicación o acercarse a nuestra Oficina Principal.")
        pdf.drawString(30, 718, "La Aseguradora realizará la inspección del vehículo, antes de otorgar la cobertura y emisión de la respectiva póliza. Nos")
        pdf.drawString(30, 706, "reservamos el derecho de retirar y/o modificar los términos cotizados.")
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(30, 676, "Procedimiento para aplicar al Cero Deducible / Dependerá de su Plan contratado.")
        pdf.setFont("Helvetica", 9)
        pdf.drawString(30, 646, "Al utilizar la ")
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(80, 646, "Red de talleres (No agencias),")
        pdf.setFont("Helvetica", 9)
        pdf.drawString(210, 646, " el deducible será descontado al 100%, siempre y cuando cumpla con los siguientes")
        pdf.drawString(30, 634, "requisitos:")
        pdf.drawString(30, 616, "1. El siniestro sea por colisión.")
        pdf.drawString(30, 604, "2. Llame al número de Asistencia al ####-#### en el momento y lugar de accidente para que sea asistido.")
        pdf.drawString(30, 592, "3. Si los daños son leves y está obstruyendo la libre circulación, toma fotografías del incidente (lateral, frontal y trasera)")
        pdf.drawString(30, 580, "4. Si los daños no permiten mover su vehículo o hay personas lesionadas, deberá permanecer en el lugar de accidente.")
        pdf.drawString(30, 568, "5. El vehículo deberá ser reparado en un Taller de Red autorizado por Seguros Atlántida.")
        pdf.drawString(30, 556, "6. El monto del reclamo sea mayor a USD100.00, este beneficio no aplica en caso de Pérdida Total por accidente o robo.")
        pdf.drawString(30, 544, "7. Llevar el vehículo al taller dentro de los 30 días siguientes a la fecha del siniestro para la elaboración de presupuesto")
        pdf.drawString(30, 532, "y reparación de vehículo.")
        pdf.drawString(30, 512, "En caso de utilizar ")
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(105, 512, "Agencias Distribuidoras")
        pdf.setFont("Helvetica", 9)
        pdf.drawString(210, 512, " de vehículos, siempre y cuando se satisfagan los requisitos detallados anteriormente,")
        pdf.drawString(30, 500, "El Cero Deducible aplica únicamente en caso de accidente para vehículos no mayores a cinco años de antiguedad y cuando el")
        pdf.drawString(30, 488, "presupuesto ajustado sea mayor a USD200.00.")
        pdf.drawString(30, 468, "Para los vehículos Sedán o hatchback, camionetas y Pick-up con suma asegurada mayor o igual a $40,000.00 requieren instalación")
        pdf.drawString(30, 456, "de dispositivo de seguridad y la participación del Asegurado en caso de robo total se disminuirá al 5/95. Este beneficio se otorgará")
        pdf.drawString(30, 444, "mientras el sistema de seguridad se encuentre instalado y activado. El dispositivo será en comodato para el Asegurado y sólamente")
        pdf.drawString(30, 432, "pagará el costo del monitoreo de USD180.00 más IVA.")

        pdf.drawString(100, 327, "__________________________")
        pdf.drawString(110, 315, "Firma de aceptación cliente")
        pdf.drawString(360, 327, "__________________________")
        pdf.drawString(380, 315, "Fecha de aceptación")
        pdf.drawString(100, 240, "__________________________")
        pdf.drawString(116, 228, "Firma de intermediario")

        #Pie de página
        if Nom == "" and In == "":
            pdf.setFillColorRGB(0.87, 0.87, 0.87)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(50, 70, 497, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(50, 72, "Intermediario, Empresa: Oficina Principal, Atlántida Vida S.A. Seguro de Personas")
            pdf.drawString(500, 72, "V.01.2024")

            pdf.setFillColorRGB(0.87, 0.87, 0.87)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(50, 57, 497, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(50, 59, "Correo Electrónico: " + str(Cor))
            pdf.drawString(460, 59, "Teléfono: " + str(Te))
        else:
            pdf.setFillColorRGB(0.87, 0.87, 0.87)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(50, 70, 497, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(50, 72, "Intermediario, Empresa: " + str(In) + ", " + str(Nom))
            pdf.drawString(500, 72, "V.01.2024")

            pdf.setFillColorRGB(0.87, 0.87, 0.87)
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.rect(50, 57, 497, 14, fill=True, stroke=False)
            pdf.setFillColorRGB(0, 0, 0)
            pdf.drawString(50, 59, "Correo Electrónico: " + str(Cor))
            pdf.drawString(460, 59, "Teléfono: " + str(Te))
        pdf.setFillColorRGB(0.87, 0.87, 0.87)
        pdf.setStrokeColorRGB(0, 0, 0)
        pdf.rect(50, 43, 497, 14, fill=True, stroke=False)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(50, 45, "Atención al cliente: (503)2283-0800")
        pdf.drawString(332, 45, "Correo electrónico: aseguradoatlantida@seatlan.sv")

        pdf.showPage()

        pdf.setTitle('OFERTA_DE_SAUTOMOTORES_INDIVIDUAL.pdf')
        pdf.save()

        # Obtener el contenido del buffer y devolverlo como una respuesta HTTP
        #buffer.seek(0)

        pdf_bytes = buffer.getvalue()
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

        #response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'inline; filename="Oferta_TemporalRenovable.pdf"'
        #response.write(buffer.read())

        correos = [correo for correo in [Cor, Mails] if correo]  # Filtrar correos válidos

        # Si hay correos válidos, enviar el correo
        if correos:
            enviar_correo(correos, Solicitante, Cellphones, pdf_bytes)
        
        return render(request, 'Oferta_autos.html', 
            {'pdf_base64': pdf_base64,
             'Solicitante': Solicitante,
             })
    else:
        
        marca_seleccionada = request.GET.get('marca', None)
        Agencia = request.GET.get('Agencia', None)
        current_year = datetime.datetime.now().year
        # Si hay una marca seleccionada, filtramos los modelos correspondientes
        if marca_seleccionada:
            modelos = Modelos.objects.filter(marca=marca_seleccionada).values_list('modelo', flat=True)
            return JsonResponse({'modelos':list(modelos)})
        
        if Agencia:
            if Agencia == 'Si':
                años = [str(year) for year in range(current_year + 1, current_year - 21, -1)]
            else:
                años = [str(year) for year in range(current_year + 1, current_year - 11, -1)]
            
            return JsonResponse({'años': list(años)})

        #return JsonResponse({'error': 'No se pudo completar la solicitud'}, status=400)

        return render(request, 'S_autos.html', {
            'form_intermediario2': form_intermediario,
            'form_CotizadorTAR': form_cotizador,
            'form_Blindaje': form_blindaje,
        })
def enviar_correo(correos, Solicitante, Cellphones, pdf_bytes):
    # Configuración del servidor SMTP
    smtp_server = 'smtp.gmail.com'
    port = 587
    sender_email = 'henriquezricardo459@gmail.com'
    password = 'omou bfpf amij afcw'  # Recuerda almacenar la contraseña de manera segura
    
    # Crear el objeto del mensaje
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(correos)
    msg['Subject'] = 'Oferta de Automotores Individual'

    cuerpo_mensaje = f"""Información del cliente:

- Nombre: {Solicitante}
- Teléfono: {Cellphones}
    
Es un placer saludarle. Adjuntamos la oferta del Seguro de Automotores Individual, así cómo los documentos adicionales necesarios en caso de que acepte nuestra cotización.

Cualquier consulta, no dude en responder a este correo o comunicarse con nosotros al 2283-0800. Quedamos a su disposición para cualquier consulta adicional.

Saludos cordiales

Atentamente,

Seguros Atlántida S.A., de C.V.
    """
    msg.attach(MIMEText(cuerpo_mensaje, 'plain'))
    # Adjuntar el PDF generado
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(pdf_bytes)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename='Oferta de Automotores Individual.pdf')
    msg.attach(attachment)

    # Adjuntar otros archivos PDF
    for documento in ['Declaracion_Jurada_Persona_Natural.pdf', 'Hoja_de_Vinculacion_Persona_Natural.pdf']:
        with open(os.path.join('cotizador_autos/static', documento), 'rb') as f:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment', filename=documento)
            msg.attach(attachment)

    # Iniciar la conexión SMTP y enviar el correo
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
