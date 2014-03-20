/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
/* Copyright (c) 2014, Siemens Corporate Technology and Arizona Geological Survey */
$(document).ready(function () {
    $("#field-language").select2({
        'minimumInputLength': 3
    });

    $("[data-restore-spatial]").each(function () {
        var pkg_id = $(this).attr("data-pkg-id");
        var key = $(this).attr("data-key");
        var dom_key = $(this).attr("data-dom-key");

        $.ajax({
            'url': '/api/action/package_show',
            'data': JSON.stringify({
                'id': pkg_id
            }),
            'type': 'POST',
            'success': function (response) {
                var extras = response.result.extras;
                for (var i = 0; i < extras.length; i++) {
                    if (extras[i]['key'] === key) {
                        var value = JSON.parse(extras[i]['value']);
                        $("#" + dom_key).val(extras[i]['value']);

                        map.originalExtent = L.geoJson(value);
                        map.originalExtent.addTo(map);

                        var layers = map.originalExtent._layers;

                        map.panTo(map.originalExtent.getBounds().getCenter());

                        for (var index in layers) {
                            if (layers[index].feature.type === 'Point') {
                                map.setZoom(5);
                            }
                        }
                    }
                }
            }
        })
    });
});
