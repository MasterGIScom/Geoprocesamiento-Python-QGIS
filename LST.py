import ee
from ee_plugin import Map 

#Tradicional print 
print("Hola Mundo")

#Earth Engine object
print(ee.String('Hello World from Earth Engine!').getInfo())

#Area de estudio
Cordi_blanca = ee.FeatureCollection('users/mastergis01/Cordil_Blanca')
Map.addLayer(Cordi_blanca, {'color': 'red'}, 'Coordillera_Blanca')

#Funcion de fintrado de image collection 
Id = ["LANDSAT/LT05/C01/T1_SR", "LANDSAT/LC08/C01/T1_SR"]
Date = ['2010-01-01','2011-01-01','2020-01-01','2021-01-01']
def fun_medTOA(id, date01, date02):
    img = ee.ImageCollection(id)\
            .filterBounds(Cordi_blanca)\
            .filterDate(date01, date02)\
            .filterMetadata('CLOUD_COVER', 'less_than', 10)\
            .median()\
            .clip(Cordi_blanca)
            
    return img

#Cargar las imagenes del 2010 y 2020
img_2010 = fun_medTOA(Id[0],Date[0], Date[1])
img_2020 = fun_medTOA(Id[1], Date[2], Date[3])
Map.addLayer(img_2010, {'min': 100, 'max': 2000, 'bands': ['B3', 'B2', 'B1']}, 'Img_2010')
Map.addLayer(img_2020, {'min': 100, 'max': 2000, 'bands': ['B4', 'B3', 'B2']}, 'Img_2020')

## Calculo del Indice NDVI para el año 2010 y 2020
#Calculo del NDVI
ndvi_2010 = img_2010.normalizedDifference(['B4', 'B3'])
ndvi_2020 = img_2020.normalizedDifference(['B5', 'B4'])

#Parametros de visualizacion ndvi
vis_parandvi ={
    'min':0,
    'max':0.6, 
    'palette':["#051852", "#FFFFFF", "#C7B59B", "#A8B255", "#A3C020", "#76AD00","#429001", "#006400", "#003B00", "#000000"]
}
Map.addLayer(ndvi_2010, vis_parandvi, 'ndvi_2010')
Map.addLayer(ndvi_2020, vis_parandvi, 'ndvi_2020')

## Seleccion de las bandas térmicas 6 y 10 (con temperatura de brillo), sin cálculo
#Banda termica 
thermal_2010 = img_2010.select('B6').multiply(0.1)
thermal_2020 = img_2020.select('B10').multiply(0.1)

#Parametros de visualizacion 
vis_parathermal ={
    'min':291.918,
    'max':302.382, 
    'palette':['042333', '2c3395', '744992', 'b15f82', 'eb7958', 'fbb43d', 'e8fa5b']
}

Map.addLayer(thermal_2010, vis_parathermal, 'thermal_2010')
Map.addLayer(thermal_2020, vis_parathermal, 'thermal_2020')

## Calculo de la Vegetacion fracturada (fv)
#Vegetacion fracturada del 2010 ((NDVI-minNDVI)/(maxNDVI-minNDVI))^2
fv_2010 = (ndvi_2010.subtract(ee.Number(-1)).divide(ee.Number(1).subtract(ee.Number(-1)))).pow(ee.Number(2)).rename('fv')
fv_2020 = (ndvi_2020.subtract(ee.Number(-1)).divide(ee.Number(1).subtract(ee.Number(-1)))).pow(ee.Number(2)).rename('fv')
#Parametros de visualizacion 
para_fv ={
    'min':0, 
    'max':0.6,
    'palette':['blue', 'white', 'green']
}
Map.addLayer(fv_2010, para_fv, 'fv_2010')
Map.addLayer(fv_2020, para_fv, 'fv_2020')

## Emissivity EM = Fv * 0.04 + 0.986
#Asignacion de valores
a= ee.Number(0.004)
b= ee.Number(0.986)

#Calculo de la emisibidad 
EMM_2010 = fv_2010.multiply(a).add(b).rename('EMM')
EMM_2020 = fv_2020.multiply(a).add(b).rename('EMM')

#Parametros de visualizacion 
Para_EMM = {
    'min':  0.9865619146722164,
    'max': 0.989699971371314, 
    'palette':['181c43', '0c5ebe', '75aabe', 'f1eceb', 'd08b73', 'a52125', '3c0912']
}

#Visualizacion de resultados 
Map.addLayer(EMM_2010, Para_EMM, 'EMM_2010')
Map.addLayer(EMM_2020, Para_EMM, 'EMM_2020')

############### Temperatura de la superficie terrestre(LST) en grados Celsius ################
# Land Surface Temperature
def fun_lst(thermal,EMM, Banda):
    lst = thermal.expression(
    '(Tb/(1 + (0.00115* (Tb / 1.438))*log(Ep)))-273.15', {
        'Tb': thermal.select(Banda),
        'Ep': EMM.select('EMM')
    }
    ).rename('LST')
    return lst
#Calculo 
LST_2010 = fun_lst(thermal_2010, EMM_2010, 'B6' )
LST_2020 = fun_lst(thermal_2020, EMM_2020, 'B10' )

#Parametros de visualizacion 
Para_LST = {
    'min':0, 
    'max':10, 
    'palette':[
                '040274', '040281', '0502a3', '0502b8', '0502ce', '0502e6',
                '0602ff', '235cb1', '307ef3', '269db1', '30c8e2', '32d3ef',
                '3be285', '3ff38f', '86e26f', '3ae237', 'b5e22e', 'd6e21f',
                'fff705', 'ffd611', 'ffb613', 'ff8b13', 'ff6e08', 'ff500d',
                'ff0000', 'de0101', 'c21301', 'a71001', '911003'
 ]
}

#Visualizacion de resultados LST
Map.addLayer(LST_2010, Para_LST, 'LST_2010')
Map.addLayer(LST_2020, Para_LST, 'LST_2020')