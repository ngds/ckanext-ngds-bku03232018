/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */

(function () {

var drawings = new L.FeatureGroup();

ngds.Map = {
    map: L.map('map-container', {center: [39.977, -97.646], zoom: 4,
        maxBounds: [[-84, -179], [84, 179]], attributionControl: true, minZoom: 2}),
    layers: {
        baseLayer: L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpeg', {
            subdomains: '1234',
            attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Map data &copy; ' +
                '<a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.' +
                'org/licenses/by-sa/2.0/">CC-BY-SA</a>',
            detectRetina: true
        }),
        searchResultsGroup: {"Search Results": L.layerGroup()},
        dataExtentsGroup: {"Data Extents": new Array()},
        wmsLayersGroup: new Array()
    },
    controls: {
        loading: L.Control.loading({separate: true, position: 'topleft'}),
        doodle: new L.Control.Draw({position: 'topleft',
            draw:{polyline: false, circle: false, marker: false, polygon: false},
            edit: {featureGroup: drawings, remove: false, edit: false}
        }),
        reset: L.Control.extend({options: {position: 'topleft'}, onAdd: function (){
            var container = L.DomUtil.create('div', 'ngds-custom-control reset-control');
            L.DomEvent.on(container, 'click', L.DomEvent.stopPropagation)
                .on(container, 'dblclick', L.DomEvent.stopPropagation)
                .on(container, 'mousedown', L.DomEvent.stopPropagation)
                .addListener(container, 'click', function () {
                    ngds.Map.map.setView([39.977, -97.46], 4);
                });
            $(container).append('<a class="glyphicon icon-globe" href="#" title="Reset extent"></a>')
            return container;
        }})
    },
    searchParameters: {'q': '', 'extras': 'undefined', 'page': 'undefined'}
};

ngds.Map.topLevelSearch = function (parameters) {
    if (!(parameters)) {parameters = ngds.Map.searchParameters};
    if (parameters['page'] === 'undefined') {parameters['page'] = 1};
    if (parameters['extras'] === 'undefined') {parameters['extras'] = {'ext_bbox': "-180,-90,180,90"}};
    var theseLayers = ngds.Map.layers.searchResultsGroup["Search Results"];
    if (theseLayers.getLayers().length > 1) {theseLayers.clearLayers();}
    $('#query-results #search-results').empty();

    if (parameters['q'].length === 0) {
        var searchQuery = $('#map-search-query').val();
        parameters['q'] = searchQuery;
    } else {
        $('#map-search-query').val(parameters['q']);
    }

    ngds.Map.makeSearch(parameters);
    $('#content-legend-menu').addClass('shown');
};

ngds.Map.makeSearch = function (parameters) {
    var action = ngds.ckanlib.package_search,
        rows = 50,
        page = parseInt(parameters['page']),
        start = (page - 1)*rows,
        query = parameters['q'],// + '+res_url:*+',
        extras = parameters['extras'],
        fields = ['tags', 'data_type', 'res_protocol', 'res_format', 'res_resource_format', 'Source', 'author_string', 'status', 'res_content_model', 'private'],
        fq = '+dataset_type:dataset';

    action({'q': query, 'rows': rows, 'start': start, 'extras': extras}, function (response) {
        var count = response['result']['count'],
            nextPage = (page + 1),
            nextRows = (nextPage*rows)

        if (count === 0) {
            var html = '<div class="top-showing-results">No Search Results</div>';
            $('#query-results .query-hit-count').empty();
            $('#query-results .query-hit-count').append(html);
        } else if (count < 50 && page === 1) {
            var html = '<div class="top-showing-results">Results 1 - ' + count + ' of ' + count + '</div>';
            $('#query-results .query-hit-count').empty();
            $('#query-results .query-hit-count').append(html);
        } else if (count != 0 && page === 1) {
            var html = '<div class="top-showing-results">Results 1 - 50 of ' + count + '</div>';
            $('#query-results .query-hit-count').empty();
            $('#query-results .query-hit-count').append(html);
        } else {
            var html = '<div class="top-showing-results"> '+ count + ' Total Results</div>';
            $('#query-results .query-hit-count').empty();
            $('#query-results .query-hit-count').append(html);
        }

        _.each(response.result.packages, function (rec) {
            var randomNumber = Math.floor(Math.random()*1000000000000000000000),
                coords = JSON.parse(rec.bbox[0]),
                geoData = {'sw_lat': coords.coordinates[0][0][1], 'sw_lon': coords.coordinates[0][0][0],
                    'ne_lat': coords.coordinates[0][2][1], 'ne_lon': coords.coordinates[0][2][0]},
                geoString = geoData['sw_lat'] + ',' + geoData['sw_lon'] + ',' + geoData['ne_lat'] + ',' + geoData['ne_lon'];
                bounds = L.latLngBounds([[geoData.sw_lon, geoData.sw_lat],[geoData.ne_lon, geoData.ne_lat]]),
                center = bounds.getCenter(),
                geojson = {'type': 'Feature', 'properties': {'feature_id': randomNumber, 'title': rec.title},
                    'geometry': {'type': 'Point', 'coordinates': [center.lat, center.lng]}},
                reqData = {'title': rec.title, 'name': rec.name, 'notes': rec.notes, 'pkg_id': rec.id,
                    'resources': rec.resources, 'geoData': geoData, 'geojson': geojson, 'geoString': geoString};
            ngds.Map.returnSearchResult(reqData);
        });

        if (count > 0 && rows < count && response.result.packages.length > 0) {
            var html = '<div id="load-results-' + nextPage + '" class="load-more-results">';
                html += '<a href="javascript:void(0)" value="' + nextPage + '-' + nextRows + '-' + rows + '" onclick="ngds.Map.doPagination(this)">Load Results ' + (rows*(nextPage-1) + 1) + ' - ' + (nextRows) + '</a>';
                html += '</div>';
            $('#query-results #search-results').append(html);
        } else {
            var html = '<div class="top-showing-results">No More Search Results</div>'
            $('#query-results #search-results').append(html);
        }
    })
    /*
    Empty the search query here.  This isn't really a hack, it's just kind of sloppy.  If we don't empty the search
    query here, then you won't be able to make any new searches.  A refactor of the map search object is definitely
    needed to clean this up.  We should have one object that can handle the search query.
    */
    parameters['q'] = '';
};

ngds.Map.returnSearchResult = function (result) {
    var thisResult = [result];
    var vanillaOptions = _.map(thisResult, function (data) {
        if (data.geoData) {
            html = '<div class="accordion-group" id="accordion-search-result">';
            html += '<div class="accordion-heading">';
            html += '<a id=bbox-handle' + data.pkg_id + ' class="toggle-layer-extent extent-absent" value="' + result.geoString + '" href="javascript:void(0)" onclick="ngds.Map.addBbox(this)">Show Area on Map</a>';
            html += '</div></div>';
            return html;
        }
    }).join('');

    var wmsLayerOption = _.map(result.resources, function (data) {
        var layerName = function (data) {
            if ('layer_name' in data && data.layer_name.length > 0 && typeof data.layer_name === 'string') {
                return data.layer_name;
            } else if ('layer' in data && data.layer.length > 0 && typeof data.layer === 'string') {
                return data.layer;
            } else if (data.name) {
                var unHyphen = data.name.replace(/\s*-\s*/g, ' ');
                return unHyphen.replace(/\b./g, function (m) {return m.toUpperCase()});
            } else {
                return 'Undefined Layer';
            }
        };
        data['smartLayer'] = layerName(data);

        if (data.protocol === 'OGC:WMS') {
            html = '<div class="accordion-group" id="accordion-search-result">';
            html += '<div class="accordion-heading">';
            html += '<a id="' + result.pkg_id + '" class="toggle-layer-wms wms-absent" value="' + data.smartLayer + '" href="javascript:void(0)" onclick="ngds.Map.addWmsLayer(this)">Show Web Map Service</a>'
            html += '</div></div>';
            return html;
        }
    }).join('');

    var datasetDetailsOption = _.map(thisResult, function(data) {
        var link = '/dataset/' + data.name;
        html = '<div class="accordion-group" id="accordion-search-result">';
        html += '<div class="accordion-heading">';
        html += '<a class="data-details-link" target="_blank" href="' + link + '">Go To Dataset Details Page</a>';
        html += '</div></div>';
        return html;
    }).join(',');

    var resources = _.map(result.resources, function (data) {
        var versionUri = data.content_model_version,
            baseUri = data.content_model_uri;
        if (baseUri || versionUri) {
            var getThisUri = function (data) {
                if (versionUri && baseUri || versionUri && !(baseUri)) {
                    return '<a class="data-uri-link" href="' + versionUri + '">Go To Content Model URI</a>';
                } else if (baseUri && !(versionUri)) {
                    return '<a class="data-uri-link" href="' + baseUri + '">Go To Content Model URI</a>';
                }
            };
            data['smartUri'] = getThisUri(data);
        };

        if (data.protocol && data.protocol.search('OGC') != -1 && data.url) {
            var getThisRequest = function (data) {
                if (data.url.search('getcapabilities') != -1 || data.url.search('GetCapabilities') != -1
                    || data.url.search('getCapabilities') != -1 || data.url.search('Getcapabilities') != -1) {
                    return data.url;
                } else {
                    return data.url + 'request=GetCapabilities&service=WMS';
                }
            }
            data['smartRequest'] = getThisRequest(data);
        }

        if (data.protocol === 'OGC:WMS' || data.format === 'wms') {
            html = '<div class="accordion-group" id="accordion-search-result">';
            html += '<div class="accordion-heading">';
            html += '<a class="data-ogc" target="_blank" href="' + data.smartRequest + '">Web Map Service Capabilities</a>';
            html += '</div></div>';
            return html;
        } else if (data.protocol === 'OGC:WFS' || data.format === 'wfs') {
            html = '<div class="accordion-group" id="accordion-search-result">';
            html += '<div class="accordion-heading">';
            html += '<a class="data-ogc" target="_blank" href="' + data.smartRequest + '">Web Feature Service Capabilities</a>';
            html += '</div></div>';
            return html;
        } else if (data.protocol === 'OGC:WCS' || data.format === 'wcs') {
            html = '<div class="accordion-group" id="accordion-search-result">';
            html += '<div class="accordion-heading">';
            html += '<a class="data-ogc" target="_blank" href="' + data.url + '">Web Coverage Service Capabilities</a>';
            html += '</div></div>';
            return html;
        } else if (data.format === 'CSV') {
            html = '<div class="accordion-group" id="accordion-search-result">';
            html += '<div class="accordion-heading">';
            html += '<a class="data-ogc" href="' + data.url + '">Download CSV Resource</a>';
            html += '</div></div>';
            return html;
        } else if (data.format === 'PDF') {
            html = '<div class="accordion-group" id="accordion-search-result">';
            html += '<div class="accordion-heading">';
            html += '<a class="data-ogc" href="' + data.url + '">Download PDF Resource</a>';
            html += '</div></div>';
            return html;
        } else if (data.format === 'ZIP') {
            html = '<div class="accordion-group" id="accordion-search-result">';
            html += '<div class="accordion-heading">';
            html += '<a class="data-ogc" href="' + data.url + '">Download Zipfile Resource</a>';
            html += '</div></div>';
            return html;
        } else if (data.format.indexOf('ms-excel') !== -1) {
            html = '<div class="accordion-group" id="accordion-search-result">';
            html += '<div class="accordion-heading">';
            html += '<a class="data-ogc" href="' + data.url + '">Download Microsoft Excel Resource</a>';
            html += '</div></div>';
            return html;
        } else if (data.format.indexOf('openxml') !== -1) {
            html = '<div class="accordion-group" id="accordion-search-result">';
            html += '<div class="accordion-heading">';
            html += '<a class="data-ogc" href="' + data.url + '">Download Open XML Resource</a>';
            html += '</div></div>';
            return html;
        } else if (!(data.format) && data.url.indexOf("notifications.usgin.org") !== -1) {
            html = '<div class="accordion-group" id="accordion-search-result">';
            html += '<div class="accordion-heading">';
            html += '<a class="data-ogc" target="_blank" href="' + data.url + '">Service Notifications</a>';
            html += '</div></div>';
            return html;
        } else if (data.format === 'HTML' && data.url) {
            html = '<div class="accordion-group" id="accordion-search-result">';
            html += '<div class="accordion-heading">';
            html += '<a class="data-ogc" target="_blank" href="' + data.url + '">External Website</a>';
            html += '</div></div>';
            return html;
        } else if (data.url.indexOf('.tif') !== -1 || data.url.indexOf('.tiff') !== -1) {
            html = '<div class="accordion-group" id="accordion-search-result">';
            html += '<div class="accordion-heading">';
            html += '<a class="data-ogc" target="_blank" href="' + data.url + '">Download TIFF Image</a>';
            html += '</div></div>';
            return html;
        } else if (!(data.format) && data.url) {
            html = '<div class="accordion-group" id="accordion-search-result">';
            html += '<div class="accordion-heading">';
            html += '<a class="data-ogc" target="_blank" href="' + data.url + '">External Website</a>';
            html += '</div></div>';
            return html;
        }
    }).join('');

    var getPackageDescription = function (data) {
        if (data.length > 200) {
            return {'preview': data.substr(0,200) + '...', 'full': data}
        } else if (data.length <= 200) {
            return data
        } else {
            return ''
        }
    };

    var determineResources = function (data) {
        if (data.length > 0) {
            return data;
        } else {
            html = '<div class="accordion-group" id="accordion-search-result">';
            html += '<div id="no-results" class="accordion-heading">';
            html += '<div class="data-no-results">This package doesn\'t have any resources</div>';
            html += '</div></div>';
            return html;
        }
    }

    var feature_id = result.geojson.properties.feature_id,
        packageDescription = getPackageDescription(result.notes),
        html = '<li class="map-search-result result-' + feature_id + '" >';
        html += '<div class="accordion" id="accordion-search">';
        html += '<div class="accordion-group">';
        html += '<div class="accordion-heading">';
        html += '<table>';
        html += '<a class="accordion-toggle feature-id-' + feature_id + '" data-toggle="collapse" data-parent="#accordion-search" href=#collapse' + feature_id + '>' + result.title + '</td>';
        html += '</td></tr></table>';
        html += '<div class="package-description"><p>' + packageDescription['preview'] + '</p></div></div>';
        html += '<div id=collapse' + feature_id + ' class="accordion-body collapse">';
        html += '<div class="resource-content">' + vanillaOptions + '</div>';
        html += '<div class="resource-content">' + wmsLayerOption + '</div>';
        html += '<div class="resource-content">' + datasetDetailsOption + '</div>';
        html += '<div class="resource-content">Available Resources' + determineResources(resources) + '</div>';
        html += '</div></div></div></li>';
    $('#query-results #search-results').append(html);

    var defaultStyle = {radius: 8, fillColor: '#ff5500', color: '#b23b00',
            weight: 2, opacity: 1, fillOpacity: 0.5},
         highlightStyle = {radius: 8, fillColor: '#00aaff', color: '#0076b2',
            weight: 2, opacity: 1, fillOpacity: 1};

    var circles = L.geoJson(result.geojson, {pointToLayer: function (f,ll) {
        return L.circleMarker(ll, defaultStyle)
        },
        onEachFeature: function (feature, layer) {
            var feature_id = layer.feature.properties.feature_id,
                popupText = layer.feature.properties.title,
                thisPopup = L.popup().setLatLng(feature).setContent(popupText),
                searchResult = $('.map-search-result.result-' + feature_id);
            layer.bindPopup(thisPopup);
            layer.on('click', function() {
                var toggleId = $('#collapse' + feature_id),
                    collapseId = $('.feature-id-' + feature_id),
                    firstResult = $('#query-results #search-results li').first();

                if (firstResult.hasClass('map-active')) { firstResult.removeClass('map-active') }

                $('#query-results #search-results').prepend(searchResult);
                $('#query-results #search-results').animate({scrollTop:0}, 'fast');

                if (collapseId.hasClass('collapsed')) {
                    toggleId.addClass('in');
                    collapseId.removeClass('collapsed');
                    searchResult.addClass('map-active');
                } else if (toggleId.hasClass('in')) {
                    toggleId.removeClass('in');
                    collapseId.addClass('collapsed');
                    searchResult.addClass('map-active');
                } else {
                    toggleId.addClass('in');
                    searchResult.addClass('map-active');
                }
            }),
            layer.on('mouseover', function () {
                layer.setStyle(highlightStyle);
                var resultId = $('.result-' + feature_id);
                resultId.addClass('result-highlight');
            }),
            layer.on('mouseout', function () {
                layer.setStyle(defaultStyle);
                var resultId = $('.result-' + feature_id);
                resultId.removeClass('result-highlight');
            })

            searchResult.hover(function () {
                $(searchResult).addClass('result-highlight');
                layer.setStyle(highlightStyle);
            }, function () {
                $(searchResult).removeClass('result-highlight');
                layer.setStyle(defaultStyle);
            })
        }}
    );

    ngds.Map.layers.searchResultsGroup["Search Results"].addLayer(circles).addTo(ngds.Map.map);

};

ngds.Map.map.on('draw:created', function (e) {
    var layer = e.layer,
        theseBounds = layer.getBounds().toBBoxString(),
        ext_bbox = {'ext_bbox': theseBounds};
    ngds.Map.searchParameters['extras'] = ext_bbox;
    ngds.Map.topLevelSearch(ngds.Map.searchParameters);
    ngds.Map.map.fitBounds(layer.getBounds());
});

ngds.Map.doPagination = function (event) {
    var thisValue = event.getAttribute('value'),
        nextPage = parseInt(thisValue.split('-')[0]),
        nextRows = parseInt(thisValue.split('-')[1]),
        baseRows = parseInt(thisValue.split('-')[2]),
        parameters = ngds.Map.searchParameters,
        parentID = $("#load-results-" + nextPage),
        html = '<div class="showing-results">Results ' + (baseRows*(nextPage-1) + 1) + ' - ' + nextRows + '</div>';

        parameters['page'] = nextPage;
        ngds.Map.makeSearch(parameters);
        parentID.empty().append(html);
};

ngds.Map.addWmsLayer = function (event) {
    var thisElement = $('#' + event.getAttribute('id')),
        thisId = thisElement[0].id,
        thisValue = event.getAttribute('value');
    if (thisElement.hasClass('wms-absent')) {
        ngds.ckanlib.get_wms_urls(thisId, function (wmsMapping) {
            _.each(wmsMapping, function (wms) {
                var params = {
                    'layers': wms['layer'],
                    'format': wms['format'],
                    'transparent': true,
                    'version': '1.1.1'
                    },
                    bbox = [[wms.bbox[1], wms.bbox[0]],[wms.bbox[3], wms.bbox[2]]],
                    wmsLayer = L.tileLayer.wms(wms['service_url'], params);
                ngds.Map.layers.wmsLayersGroup[thisId] = wmsLayer;
                var thisWms = ngds.Map.layers.wmsLayersGroup[thisId];
                layersControl.addOverlay(thisWms, thisValue);
                ngds.Map.map.addLayer(thisWms);
                ngds.Map.map.fitBounds(bbox);
            })
        })
        thisElement.removeClass('wms-absent').addClass('wms-present');
        thisElement.text('Hide Web Map Service');
    } else if (thisElement.hasClass('wms-present')) {
        var thisWms = ngds.Map.layers.wmsLayersGroup[thisId];
        ngds.Map.map.removeLayer(thisWms);
        layersControl.removeLayer(thisWms);
        thisElement.removeClass('wms-present').addClass('wms-absent');
        thisElement.text('Show Web Map Service');
    }
};

ngds.Map.addBbox = function (event) {
    var thisId = $('#' + event.getAttribute('id')),
        thisUID = thisId[0].id.split('bbox-handle')[1];
    if (thisId.hasClass('extent-absent')) {
        var theseValues = event.getAttribute('value').split(','),
            theseCoords = [];
        _.each(theseValues, function (value) {
            var coord = parseFloat(value);
            theseCoords.push(coord);
        });
        var theseBounds = [[theseCoords[0], theseCoords[1]], [theseCoords[2], theseCoords[3]]],
            boundingBox = L.rectangle(theseBounds, {color: 'red', opacity: 1, fillOpacity: 0.2, weight: 1});
            bboxGroup = ngds.Map.layers.dataExtentsGroup;
        bboxGroup['Data Extents'][thisUID] = boundingBox;
        bboxGroup['Data Extents'][thisUID].addTo(ngds.Map.map).bringToBack();
        ngds.Map.map.fitBounds(bboxGroup['Data Extents'][thisUID], {maxZoom: 6, padding: [200, 200]});
        thisId.removeClass('extent-absent').addClass('extent-present');
        thisId.text('Hide Area on Map');
    } else if (thisId.hasClass('extent-present')) {
        var thisLayer = bboxGroup['Data Extents'][thisUID];
        ngds.Map.map.removeLayer(thisLayer);
        thisId.removeClass('extent-present').addClass('extent-absent');
        thisId.text('Show Area on Map');
    }
};

ngds.Map.toggleContentMenu = function () {
    if ($('#content-legend-menu').hasClass('shown')) {
        $('#content-legend-menu').removeClass('shown');
        $('#line-triangle').removeClass('left-triangle');
        $('#line-triangle').addClass('right-triangle');
    } else {
        $('#content-legend-menu').addClass('shown');
        $('#line-triangle').removeClass('right-triangle');
        $('#line-triangle').addClass('left-triangle');
    }
};

var overlayPane = ngds.Map.layers.searchResultsGroup,
    layersControl = L.control.layers(null, overlayPane, {position: 'topleft'});

drawings.addTo(ngds.Map.map);
ngds.Map.layers.baseLayer.addTo(ngds.Map.map);
ngds.Map.map.addControl(ngds.Map.controls.doodle);
ngds.Map.map.addControl(new ngds.Map.controls.reset);
layersControl.addTo(ngds.Map.map);
ngds.Map.map.addControl(ngds.Map.controls.loading);

$('.leaflet-draw-toolbar-top').removeClass('leaflet-draw-toolbar');
$('.leaflet-draw-draw-rectangle').addClass('glyphicon icon-pencil');

}).call(this);
