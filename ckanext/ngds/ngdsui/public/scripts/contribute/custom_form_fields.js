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

                        var lvalue = L.geoJson(value);
                        lvalue.addTo(map);

                        var layers = lvalue._layers;

                        map.panTo(lvalue.getBounds().getCenter());

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