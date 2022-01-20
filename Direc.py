from qgis.core import QgsVectorLayer

#Remover las capas del mapa
QgsProject.instance().removeAllMapLayers()

#añadiendo layer 
layer = QgsVectorLayer('E:/MASTERGIS/MODULO 01/shapefile/Limite_provincial.shp', 'Limite_provincial', 'ogr')
QgsProject.instance().addMapLayer(layer)

#Numero de entidades 
n_featur = layer.featureCount()
print(n_featur )

#La ruta de la capa
print("Link: ", layer.source())
#help(iface)
#act_lay = iface.activeLayer()
#Tabla de atributos 
#iface.showAttributeTable(act_lay)

#Cuadro de propiedades
#iface.showLayerProperties(act_lay)

#Sistema de referencia de coordenadas
crs = layer.crs()
print(crs)
print(crs.description())

#visualizacion de campos
campos = layer.fields()
print(campos)
for campo in campos:
    print(campo.name(), campo.typeName())

#Poniendo en una lista
nombres = [campo.name() for campo in layer.fields()]
print(nombres)














