/**
 * Created by kaffeine on 11/3/13.
 */
$(document).ready(function () {
    var ngds_notify = (function () {
        var p_notify = ckan.notify;

        var ngds_notify = function notify(title, message, type) {
            $(".flash-messages").empty();
            p_notify(title, message, type);
        };
        return ngds_notify;
    }());

    ckan.notify = ngds_notify;
    ckan.sandbox.extend({'notify': ngds_notify});
});