import arcpy
import math

class LngLatTransfer():

    def __init__(self):
        self.x_pi = 3.14159265358979324 * 3000.0 / 180.0
        self.pi = math.pi  # π
        self.a = 6378245.0  # 长半轴
        self.es = 0.00669342162296594323  # 偏心率平方
        pass

    def GCJ02_to_BD09(self, gcj_lng, gcj_lat):
        """
        实现GCJ02向BD09坐标系的转换
        :param lng: GCJ02坐标系下的经度
        :param lat: GCJ02坐标系下的纬度
        :return: 转换后的BD09下经纬度
        """
        z = math.sqrt(gcj_lng * gcj_lng + gcj_lat * gcj_lat) + 0.00002 * math.sin(gcj_lat * self.x_pi)
        theta = math.atan2(gcj_lat, gcj_lng) + 0.000003 * math.cos(gcj_lng * self.x_pi)
        bd_lng = z * math.cos(theta) + 0.0065
        bd_lat = z * math.sin(theta) + 0.006
        return bd_lng, bd_lat


    def BD09_to_GCJ02(self, bd_lng, bd_lat):
        '''
        实现BD09坐标系向GCJ02坐标系的转换
        :param bd_lng: BD09坐标系下的经度
        :param bd_lat: BD09坐标系下的纬度
        :return: 转换后的GCJ02下经纬度
        '''
        x = bd_lng - 0.0065
        y = bd_lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * self.x_pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * self.x_pi)
        gcj_lng = z * math.cos(theta)
        gcj_lat = z * math.sin(theta)
        return gcj_lng, gcj_lat


    def WGS84_to_GCJ02(self, lng, lat):
        '''
        实现WGS84坐标系向GCJ02坐标系的转换
        :param lng: WGS84坐标系下的经度
        :param lat: WGS84坐标系下的纬度
        :return: 转换后的GCJ02下经纬度
        '''


        dlat = self._transformlat(lng - 105.0, lat - 35.0)
        dlng = self._transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * self.pi
        magic = math.sin(radlat)
        magic = 1 - self.es * magic * magic
        sqrtmagic = math.sqrt(magic)

        dlat = (dlat * 180.0) / ((self.a * (1 - self.es)) / (magic * sqrtmagic) * self.pi)
        dlng = (dlng * 180.0) / (self.a / sqrtmagic * math.cos(radlat) * self.pi)
        gcj_lat = lat + dlat
        gcj_lng = lng + dlng
        return gcj_lng, gcj_lat


    def GCJ02_to_WGS84(self, gcj_lng, gcj_lat):
        '''
        实现GCJ02坐标系向WGS84坐标系的转换
        :param gcj_lng: GCJ02坐标系下的经度
        :param gcj_lat: GCJ02坐标系下的纬度
        :return: 转换后的WGS84下经纬度
        '''
        dlat = self._transformlat(gcj_lng - 105.0, gcj_lat - 35.0)
        dlng = self._transformlng(gcj_lng - 105.0, gcj_lat - 35.0)
        radlat = gcj_lat / 180.0 * self.pi
        magic = math.sin(radlat)
        magic = 1 - self.es * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((self.a * (1 - self.es)) / (magic * sqrtmagic) * self.pi)
        dlng = (dlng * 180.0) / (self.a / sqrtmagic * math.cos(radlat) * self.pi)
        mglat = gcj_lat + dlat
        mglng = gcj_lng + dlng
        lng = gcj_lng * 2 - mglng
        lat = gcj_lat * 2 - mglat
        return lng, lat


    def BD09_to_WGS84(self, bd_lng, bd_lat):
        '''
        实现BD09坐标系向WGS84坐标系的转换
        :param bd_lng: BD09坐标系下的经度
        :param bd_lat: BD09坐标系下的纬度
        :return: 转换后的WGS84下经纬度
        '''
        lng, lat = self.BD09_to_GCJ02(bd_lng, bd_lat)
        return self.GCJ02_to_WGS84(lng, lat)


    def WGS84_to_BD09(self, lng, lat):
        '''
        实现WGS84坐标系向BD09坐标系的转换
        :param lng: WGS84坐标系下的经度
        :param lat: WGS84坐标系下的纬度
        :return: 转换后的BD09下经纬度
        '''
        lng, lat = self.WGS84_to_GCJ02(lng, lat)
        return self.GCJ02_to_BD09(lng, lat)


    def _transformlat(self, lng, lat):
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
              0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 *
                math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * self.pi) + 40.0 *
                math.sin(lat / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * self.pi) + 320 *
                math.sin(lat * self.pi / 30.0)) * 2.0 / 3.0
        return ret


    def _transformlng(self, lng, lat):
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
              0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 *
                math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * self.pi) + 40.0 *
                math.sin(lng / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * self.pi) + 300.0 *
                math.sin(lng / 30.0 * self.pi)) * 2.0 / 3.0
        return ret

    def WGS84_to_WebMercator(self, lng, lat):
        '''
        实现WGS84向web墨卡托的转换
        :param lng: WGS84经度
        :param lat: WGS84纬度
        :return: 转换后的web墨卡托坐标
        '''
        x = lng * 20037508.342789 / 180
        y = math.log(math.tan((90 + lat) * self.pi / 360)) / (self.pi / 180)
        y = y * 20037508.34789 / 180
        return x, y

    def WebMercator_to_WGS84(self, x, y):
        '''
        实现web墨卡托向WGS84的转换
        :param x: web墨卡托x坐标
        :param y: web墨卡托y坐标
        :return: 转换后的WGS84经纬度
        '''
        lng = x / 20037508.34 * 180
        lat = y / 20037508.34 * 180
        lat = 180 / self.pi * (2 * math.atan(math.exp(lat * self.pi / 180)) - self.pi / 2)
        return lng, lat
        
lnglatTransfer = LngLatTransfer()

ftClsNameList = arcpy.GetParameterAsText(0)
for ftCls in ftClsNameList.split(';'):
  feature_count = int(arcpy.GetCount_management(ftCls).getOutput(0))
  desc = arcpy.Describe(ftCls)
  feature_name = desc.name
  spatial_ref = desc.spatialReference
  oidFieldName = desc.oidFieldName
  shapefieldname = desc.shapeFieldName
  shapeType = desc.shapeType

  with arcpy.da.UpdateCursor(ftCls, (oidFieldName, 'SHAPE@')) as rows:
  # WGS84坐标转GCJ02火星坐标

    # 面要素
    if shapeType == "Polygon":
      rowCount = 0
      for row in rows:
        oid = row[0]
        try:
          feat = row[1]
          arr_feat = arcpy.Array()
          for part in feat:
            arr_part = arcpy.Array()
            for pnt in part:
              if pnt is not None:
                x = pnt.X
                y = pnt.Y
                x, y = lnglatTransfer.WGS84_to_GCJ02(x, y)
                arr_part.add(arcpy.Point(x, y))
              else:
                arr_part.add(None)
            arr_feat.add(arr_part)
          polygon = arcpy.Polygon(arr_feat, spatial_ref)
          row[1] = polygon
          rows.updateRow(row)
          rowCount += 1
          arcpy.SetProgressorLabel("%s:%d/%d" %(feature_name, rowCount, feature_count))
          arcpy.SetProgressorPosition(int(rowCount * 100 / feature_count))
        except Exception as e:
          arcpy.AddWarning("OID{%d}:%s" %(oid, str(e)));
    # 线要素
    elif shapeType == "Polyline":
      rowCount = 0
      for row in rows:
        oid = row[0]
        try:
          feat = row[1]
          arr_feat = arcpy.Array()
          for part in feat:
            arr_part = arcpy.Array()
            for pnt in part:
              x = pnt.X
              y = pnt.Y
              x, y = lnglatTransfer.WGS84_to_GCJ02(x, y)
              arr_part.add(arcpy.Point(x, y))
            arr_feat.add(arr_part)
          polyline = arcpy.Polyline(arr_feat, spatial_ref)
          row[1] = polyline
          rows.updateRow(row)
          rowCount += 1
          arcpy.SetProgressorLabel("%s:%d/%d" %(feature_name, rowCount, feature_count))
          arcpy.SetProgressorPosition(int(rowCount * 100 / feature_count))
        except Exception as e:
          arcpy.AddWarning("OID{%d}:%s" %(oid, str(e)));
    # 多点要素
    elif shapeType == "Multipoint":
      rowCount = 0
      for row in rows:
        oid = row[0]
        try:
          feat = row[1]
          arr_feat = arcpy.Array()
          for pnt in feat:
            x = pnt.X
            y = pnt.Y
            x, y = lnglatTransfer.WGS84_to_GCJ02(x, y)
            arr_feat.add(arcpy.Point(x, y))
          multipoint = arcpy.Multipoint(arr_feat, spatial_ref)
          row[1] = multipoint
          rows.updateRow(row)
          rowCount += 1
          arcpy.SetProgressorLabel("%s:%d/%d" %(feature_name, rowCount, feature_count))
          arcpy.SetProgressorPosition(int(rowCount * 100 / feature_count))
        except Exception as e:
          arcpy.AddWarning("OID{%d}:%s" %(oid, str(e)));
    elif shapeType == "Point":
      rowCount = 0
      for row in rows:
        oid = row[0]
        try:
          feat = row[1]
          x = feat.centroid.X
          y = feat.centroid.Y
          x, y = lnglatTransfer.WGS84_to_GCJ02(x, y)
          point = arcpy.PointGeometry(arcpy.Point(x, y), spatial_ref);
          row[1] = point
          rows.updateRow(row)
          rowCount += 1
          arcpy.SetProgressorLabel("%s:%d/%d" %(feature_name, rowCount, feature_count))
          arcpy.SetProgressorPosition(int(rowCount * 100 / feature_count))
        except Exception as e:
          arcpy.AddWarning("OID{%d}:%s" %(oid, str(e)));
