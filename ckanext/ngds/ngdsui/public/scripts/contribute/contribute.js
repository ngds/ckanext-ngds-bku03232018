/* Copyright (c) 2014, Siemens Coporate Technology and Arizona Geological Survey */
var ngds = ngds || { };


(function() {
	$(document).ready(function() {

        $('#datasetfile_path').attr("readonly","readonly");
        $('#resourcefile_path').attr("readonly","readonly");

        $('#datasetfile').change(function(){

            if(validate_extension($(this).val(),'.xls')){
                alert("Can only upload .xls files.");
                $(this).val("");
                $('#datasetfile_path').val("");
                $('#upload-submit-button').attr('disabled',true);
            }else{
                $('#datasetfile_path').val($(this).val());
                $('#upload-submit-button').attr('disabled',false);
            }
        });
        $('#resourceszip').change(function(){
            if(validate_extension($(this).val(),'.zip')){
                alert("Can only upload .zip files.");
                $(this).val("");
                $('#resourcefile_path').val("");
            }else{
                $('#resourcefile_path').val($(this).val());
            }
        });

        function validate_extension(file_path,valid_extension){
            ext = file_path.slice(file_path.lastIndexOf(".")).toLowerCase();

            if (ext !== valid_extension.toLowerCase()){
                return true;
            }
            return false;
        }

    });

})();

