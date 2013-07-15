var structured_form = {
  'form':[
    {
      'label':'Resource URL',
      'name':'url',
      'tag':'input',
      'additional':function() {
        return 'type=text id=url';
      },
      'title':'A URL for this resource or upload a file'
    },
    {
      'label':'Name',
      'name':'name',
      'tag':'input',
      'additional':function() {
        return 'type=text';
      },
      'title':'A name for this resource'
    },
    {
      'label':'Content Model',
      'name':'content_model_uri',
      'top_classes':function() {
        return "content_model_marker";
      },
      'tag':'select',
      'class':function() {
        return 'content_model';
      },
      'title':'A content model that this resource conforms to'
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
      },
      'title':'Describe this resource'
    },
    {
      'label':'Distributor',
      'top_classes':function() {
        return "distributor";
      },
      'id':'distributor_fake',
      'tag':'input',
      'additional':function() {
        return 'type=text';
      },
      'additional_content':function() {
        return '<div class="distributor-tag retreived-tags""></div>';
      },
      'title':'The distributor for this resource'
    },
    {
    'label':'Format',
    'name':'format',
    'tag':'input',
    'additional':function() {
      return 'type=text';
      },
      'title':'The file format of this resource'
    }
  ],
  'custom':[
    {
      'tag':'input',
      'name':'distributor',
      'class':'distributor',
      'type':'hidden'
    },
     {
      'tag':'input',
      'class':'distributor_name',
      'type':'hidden'
    },
     {
      'tag':'input',
      'class':'distributor_email',
      'type':'hidden'
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
      },
      'title':'A URL for this resource or upload a file'
    },
    {
      'label':'Name',
      'name':'name',
      'tag':'input',
      'additional':function() {
        return 'type=text';
      },
      'title':'A name for this resource'
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
      },
      'title':'Describe this resource'
    },
    {
      'label':'Distributor',
      'top_classes':function() {
        return "distributor";
      },
      'class':function() {
        return "distributor-fake";
      },
      'name':'distributor',
      'tag':'input',
      'id':'distributor_fake',
      'additional':function() {
        return 'type=text';
      },
      'additional_content':function() {
        return '<div class="distributor-tag retreived-tags""></div>';
      },
      'title':'The distributor for this resource'
    },
    {
    'label':'Format',
    'name':'format',
    'tag':'input',
    'additional':function() {
      return 'type=text';
      },
      'title':'The file format of this resource'
    }
  ],
  'custom':[
    {
      'tag':'input',
      'name':'distributor',
      'class':'distributor',
      'type':'hidden'
    },
     {
      'tag':'input',
      'class':'distributor_name',
      'type':'hidden'
    },
     {
      'tag':'input',
      'class':'distributor_email',
      'type':'hidden'
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
      },
      'title':'A URL for this resource or upload a file'
    },
    {
      'label':'Name',
      'name':'name',
      'tag':'input',
      'additional':function() {
        return 'type=text';
      },
      'title':'A name for this resource'
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
      },
      'title':'Describe this resource'
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
      },
      'title':'How this resource can be obtained'
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
var link_data_service_form = {
  'form':[
    {
      'label':'Resource URL',
      'name':'url',
      'tag':'input',
      'additional':function() {
        return 'type=text id=url';
      },
      'title':'A URL for this resource or upload a file'
    },
    {
      'label':'Name',
      'name':'name',
      'tag':'input',
      'additional':function() {
        return 'type=text';
      },
      'title':'A name for this resource'
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
      },
      'title':'Describe this resource'
    },
    {
      'label':'Distributor',
      'top_classes':function() {
        return "distributor";
      },
      'id':'distributor_fake',
      'tag':'input',
      'additional':function() {
        return 'type=text';
      },
      'additional_content':function() {
        return '<div class="distributor-tag retreived-tags""></div>';
      },
      'title':'The distributor for this resource'
    },
    {
    'label':'Protocol',
    'name':'protocol',
    'tag':'select',
    'additional':function() {
      return 'type=text';
      },
      'title':'What protocol is used to access this resource?',
      'dnt':"someval",
      'options':[
        {
          'label':'WMS',
          'value':'wms'
        },
        {
          'label':'WFS',
          'value':'wfs'
        },
        {
          'label':'WCS',
          'value':'wcs'
        },
        {
          'label':'ESRI Map Service',
          'value':'esri_map_service'
        },
        {
          'label':'CSW',
          'value':'csw'
        },
        {
          'label':'SOS',
          'value':'sos'
        },
        {
          'label':'Open DAP',
          'value':'opendap'
        },
        {
          'label':'Other',
          'value':'other'
        }
      ]
    },
    {
    'label':'Layer',
    'name':'layer',
    'tag':'input',
    'additional':function() {
      return 'type=text';
      },
      'title':'Layer name if any for this resource'
    }
  ],
  'custom':[
    {
      'tag':'input',
      'id':'distributor',
      'name':'distributor',
      'type':'hidden'
    },
     {
      'tag':'input',
      'id':'distributor_name',
      'type':'hidden'
    },
     {
      'tag':'input',
      'id':'distributor_email',
      'type':'hidden'
    }
  ]
};
$(document).tooltip({
  position:{
    at:'right top+5',
    collision:'none'
  }
});