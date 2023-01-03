# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Yunus Emre Onder -2022
# Description: Dataset ve Tablo Olusturma, kolon ekleme
# ---------------------------------------------------------------------------
import arcpy

sdeFolder = "sdeFolderPath"  # sde connectionlarin bulundugu klasör
sdeNames = ['TEST1.sde',
            'TEST2.sde'
            ]
print "islemler basliyor..."
tm42 = "PROJCS['Aksa_Itrf_TM42',GEOGCS['D_GRS_1980',DATUM['D_GRS_1980',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',42.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]];-5123200 -10002100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision"
tm39 = "PROJCS['Aksa_Itrf_TM39',GEOGCS['D_GRS_1980',DATUM['D_GRS_1980',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',39.0],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]];-5123200 -10002100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision"
dataset = '.TEST2' # tek dataset olusturacaksak dogrudan degisken olarak tanimlanir
#datasetNames = ['.TEST2', # birden fazla datasetle calisilacaksa liste yapılır ve asagidaki dongu kullanilir
#               '.TEST3']
featureNames = ['a_alan',
               'b_cizgi',
               'c_nokta']
columnNames = ['a_kolonu',
               'b_kolonu',
               'c_kolonu',
               'd_kolonu']
def koordinatBul(owner):
    if owner == 'TEST1' or owner == 'TEST2':
        return tm42
    else:
        return tm39
for sde in sdeNames:
    sdePath = sdeFolder + '\\' + sde  # sde yolu
    owner = sde.split(".")[0].split("_")[-1]
    try:
        arcpy.AcceptConnections(sdePath, False)  # yeni baglanti yapilmasini engelle
        print owner + " icin yeni baglantilar engellendi"
        arcpy.DisconnectUser(sdePath, "ALL")  # bütün kullanicilarin baglantilarini kes
        print owner + " icin tum userlar kill edidi"
        #for dataset in datasetNames: # birden fazla dataset olusturulacagi zaman kullanilir
        try:
            print owner + " Dataset olusturma islemi basladi..."
            arcpy.CreateFeatureDataset_management(sdePath, dataset, koordinatBul(owner)) # Dataset olusturur
            print "Dataset olusturma islemi basarili " + owner
        except Exception as err:
            raise err
        for feature in featureNames:
            createFeature = sdePath + "\\" + owner + dataset
            try:
                print owner + " Feature olusturma islemi basladi"
                if feature == "a_alan":
                    arcpy.CreateFeatureclass_management(createFeature, feature, "POLYGON", "", "DISABLED", "DISABLED", koordinatBul(owner)) # Feature olusturur
                elif feature == "b_cizgi":
                    arcpy.CreateFeatureclass_management(createFeature, feature, "POLYLINE", "", "DISABLED", "DISABLED", koordinatBul(owner))
                else:
                    arcpy.CreateFeatureclass_management(createFeature, feature, "POINT", "", "DISABLED", "DISABLED", koordinatBul(owner))
                print "Feature olusturma islemi basarili " + owner
            except Exception as err:
                raise err
            for column in columnNames:
                tablename = createFeature + "\\" + owner + "." + feature
                try:
                    print owner + " Kolon ekleme islemi basladi"
                    if column == "a_kolonu":
                        arcpy.AddField_management(tablename, column, "DOUBLE", "14", "", "", "", "NULLABLE", "NON_REQUIRED", "")  # kolon ekler
                    elif column == "b_kolonu":
                        arcpy.AddField_management(tablename, column, "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
                    elif column == "c_kolonu":
                        arcpy.AddField_management(tablename, column, "DATE", "14", "", "", "", "NULLABLE", "NON_REQUIRED", "")
                    else:
                        arcpy.AddField_management(tablename, column, "LONG", "10", "", "", "", "NULLABLE", "NON_REQUIRED", "")
                    print "kolon ekleme islemi basarili"
                except Exception as err:
                    raise err
    except Exception as err:
        print owner + " connection kill vb islemi tamamlanamadi!!!"
        print err
        pass
        arcpy.AcceptConnections(sdePath, True)  # yeni baglanti engelini kaldirr
        print owner + " icin yeni baglanti kabul edilebilir hale getirildi"
print "islemler tamamlandi"
