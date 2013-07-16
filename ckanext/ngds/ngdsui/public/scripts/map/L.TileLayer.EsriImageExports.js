/* When creating a layer pass the ESRI Service's Export URL. e.g.:
 *  https://eia-ms.esri.com/arcgis/rest/services/20130301StateEnergyProfilesMap/MapServer/export
 */

L.TileLayer.EsriImageExports = L.TileLayer.WMS.extend({
    getTileUrl: function (tilePoint) {
        // Get the URL if this was just a WMS
        var wmsUrl = L.TileLayer.WMS.prototype.getTileUrl.call(this, tilePoint),
            base = wmsUrl.split("?")[0],
            params = wmsUrl.split("?")[1].split("&");

        // Look through the params and pick on the ones we need
        var bbox = "", layers = "", height = 0, width = 0;

        for (var i = 0; i < params.length; i++) {
            var param = params[i],
                key = param.split("=")[0],
                val = param.split("=")[1];

            switch (key.toLowerCase()) {
                case "bbox":
                    bbox = val;
                    break;
                case "height":
                    height = val;
                    break;
                case "width":
                    width = val;
                    break;
                case "layers":
                    layers = val;
                    break;
            }
        }

        // Rebuild the ESRI export URL
        var esriUrl = base + "?" + "f=image&format=png32&transparent=true&bboxSR=3857&bbox=" + bbox + "&layers=show:" + layers + "&size=" + width + "," + height;
        return esriUrl;
    }
  });