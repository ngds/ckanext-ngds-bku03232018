var structured_form = {
  'form':[
    {
      'label':'Resource URL',
      'name':'url',
      'tag':'input',
      'additional':function() {
        return 'type=text id=url';
      }
    },
    {
      'label':'Name',
      'name':'name',
      'tag':'input',
      'additional':function() {
        return 'type=text';
      }
    },
    {
      'label':'Content Model',
      'name':'content_model',
      'top_classes':function() {
        return "content_model_marker";
      },
      'tag':'select',
      'id':function() {
        return 'id=content_model';
      }
    },
    {
      'label':'Description',
      'name':'description',
      'tag':'textarea',
      'id':function() {
        return 'id=description';
      },
      'additional':function() {
        return 'rows=4 cols=1'
      },
      'classes':function() {
        return 'description-label-div';
      }
    },
    {
      'label':'Distributor',
      'name':'distributor',
      'tag':'input',
      'additional':function() {
        return 'type=text';
      }
    },
    {
    'label':'Format',
    'name':'format',
    'tag':'input',
    'additional':function() {
      return 'type=text';
      }
    }
  ]
};

var unstructured_form = {
  'form':[
    {
      'label':'Resource URL',
      'name':'url',
      'tag':'input',
      'additional':function() {
        return 'type=text id=url';
      }
    },
    {
      'label':'Name',
      'name':'name',
      'tag':'input',
      'additional':function() {
        return 'type=text';
      }
    },
    {
      'label':'Description',
      'name':'description',
      'tag':'textarea',
      'id':function() {
        return 'id=description';
      },
      'additional':function() {
        return 'rows=4 cols=1'
      },
      'classes':function() {
        return 'description-label-div';
      }
    },
    {
      'label':'Distributor',
      'name':'distributor',
      'tag':'input',
      'additional':function() {
        return 'type=text';
      }
    },
    {
    'label':'Format',
    'name':'format',
    'tag':'input',
    'additional':function() {
      return 'type=text';
      }
    }
  ]
};


var offline_resource_form = {
  'form':[
    {
      'label':'Resource URL',
      'name':'url',
      'tag':'input',
      'additional':function() {
        return 'type=text id=url';
      }
    },
    {
      'label':'Name',
      'name':'name',
      'tag':'input',
      'additional':function() {
        return 'type=text';
      }
    },
    {
      'label':'Description',
      'name':'description',
      'tag':'textarea',
      'id':function() {
        return 'id=description';
      },
      'additional':function() {
        return 'rows=4 cols=1'
      },
      'classes':function() {
        return 'description-label-div';
      }
    },
    {
    'label':'Ordering Procedure',
    'name':'ordering_procedure',
    'tag':'textarea',
    'additional':function() {
        return 'rows=4 cols=1'
      },
    'classes':function() {
        return 'description-label-div';
      }
    }
  ]
};

var link_data_service_form = {
  'form':[
    {
      'label':'Resource URL',
      'name':'url',
      'tag':'input',
      'additional':function() {
        return 'type=text id=url';
      }
    },
    {
      'label':'Name',
      'name':'name',
      'tag':'input',
      'additional':function() {
        return 'type=text';
      }
    },
    {
      'label':'Description',
      'name':'description',
      'tag':'textarea',
      'id':function() {
        return 'id=description';
      },
      'additional':function() {
        return 'rows=4 cols=1'
      },
      'classes':function() {
        return 'description-label-div';
      }
    },
    {
      'label':'Distributor',
      'name':'distributor',
      'tag':'input',
      'additional':function() {
        return 'type=text';
      }
    },
    {
    'label':'Protocol',
    'name':'protocol',
    'tag':'input',
    'additional':function() {
      return 'type=text';
      }
    },
    {
    'label':'Layer',
    'name':'layer',
    'tag':'input',
    'additional':function() {
      return 'type=text';
      }
    }
  ]
};


var position_file_uploader = function(selector) {
  if(typeof selector==='undefined') {
    $("#file-upload").hide();
    return;
  }
  var ref = $(selector);
  var r_width = ref.width();
  var file_upload = $("#file-upload");
  file_upload.css("position","absolute");
  ref.css("width",r_width-60);
  file_upload.css("left",ref.position().left+ref.width()+5);
  file_upload.css("top",ref.position().top);
  file_upload.show();
};

var structured_form_template = "{{#form}}\
        <div class=\"input-group {{top_classes}}\">\
            <div class=\"sp-label {{classes}}\"><label>{{label}}</label></div>\
            <{{tag}} {{additional}} name=\"{{name}}\" {{id}} class=\"structured-input\" {{placeholder}}>{{inner}}</{{tag}}>\
        </div>\
{{/form}}";