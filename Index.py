import ee
from ee_plugin import Map 

#Definir la region de interes 
peru=ee.FeatureCollection("FAO/GAUL/2015/level0")\
.filter(ee.Filter.eq('ADM0_NAME', 'Peru'))
#Visualizacion del area de interes 
Map.addLayer(peru, {'color': 'red'}, 'peru')

#Filtrar imagaCollection 
ColLand8=ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")\
.filterBounds(peru)\
.filterDate('2019-01-01', '2020-01-01')\
.filterMetadata('CLOUD_COVER', 'less_than', 40)\
.median().clip(peru)

#Parametros de visualizacion 
visParams={
    'bands':['B4','B3', 'B2'],
    'min':0,
    'max':0.4
}
Map.addLayer(ColLand8, visparams, 'Median_LanTOA')
#Calculo del NDVI
ndvi=ColLand8.normalizedDifference(['B5','B4'])
ndvi_palette= [
    'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901',
    '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01',
    '012E01', '011D01', '011301'
  ]
#calculo del NDSI
ndsi=ColLand8.normalizedDifference(['B6', 'B2'])
ndsi_palette = ['white','000088', '0000FF', '8888FF', 'FFFFFF']

Map.addLayer(ndvi, {'palette':ndvi_palette, 'min':0, 'max':1} , 'NDVI', 0)
Map.addLayer(ndsi, {'palette':ndsi_palette} , 'NDSI')