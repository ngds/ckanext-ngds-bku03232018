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
      'class':function() {
        return 'distributor-fake';
      },
      'tag':'input',
      'additional':function() {
        return 'type=text';
      },
      'additional_content':function() {
        // return '<span class="ngds-slug" style="display:none;"></span><br/><a href="javascript:create_distributor();" class="new-distributor form-anchor">Add Distributor</a>';
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
      'additional':function() {
        return 'type=text';
      },
      'additional_content':function() {
        // return '<span class="ngds-slug" style="display:none;"></span><br/><a href="javascript:create_distributor();" class="new-distributor form-anchor">Add Distributor</a>';
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
        // return '<span class="ngds-slug" style="display:none;"></span><br/><a href="javascript:create_distributor();" class="new-distributor form-anchor">Add Distributor</a>';
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
    'name':'layer_name',
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


// var create_distributor = function() {
//   var distributor_anch = $(".distributor>a");
//   $(".create_distributor_form").remove();
//   $(".distributor-fake").val("");
//   $(".new-distributor").hide();
//   distributor_anch.hide();
//   var responsible_parties = {
//     'responsible_parties':[
//       {
//         'label':'Name',
//         'name':'responsible_party_name',
//         'class':'create_distributor_form',
//         'type':'text'
//       },
//       {
//         'label':'Email',
//         'name':'responsible_party_email',
//         'class':'create_distributor_form',
//         'type':'text'
//       },
//       {
//         'button':'Create',
//         'class':'create_distributor_form create_distributor'
//       },
//        {
//         'button':'Cancel',
//         'class':'create_distributor_form cancel_create_distributor'
//       },
//       {
//         'span':'distributor_create_status',
//         'class':'create_distributor_form',
//         'style':'color:green;font-size:13px;'
//       }
//     ]
//   };

//   distributor_anch.after(Mustache.render(ngds.add_responsible_party_template,responsible_parties));

//   $('.create_distributor').on('click',function(ev) {
//       var name = $("[name=responsible_party_name]").val();
//       var email = $("[name=responsible_party_email]").val();

//       $.ajax({
//         'url':'/api/action/additional_metadata',
//         'type':'POST',
//         'data':JSON.stringify({
//           "process":"create",
//           "model":"ResponsibleParty",
//           "data":{
//             "name":name,
//             "email":email
//           }
//         }),
//         'success':function(response) {
//           $(".distributor_name").val(response.result.name);
//           $(".distributor_email").val(response.result.email);
//           $(".distributor_create_status").html("Success");
//           $(".create_distributor_form").fadeOut(1500,function() {
//              $(".create_distributor_form").remove();
//              $(".distributor-fake").val(response.result.name);
//              distributor_blur_handler();
//           });
//         }
//   });
//   });

//   $(".cancel_create_distributor").on('click',function(ev) {
//     $(".new-distributor").show();
//     $(".create_distributor_form").remove();
//   });

// }
// var edit_distributor = function()  {
//   $(".distributor-fake").show();
//   $(".ngds-slug").hide();
//   $(".distributor-edit").remove();
//   $(".new-distributor").show();
// };
// $(".ngds-slug").on('click',edit_distributor);
// var distributor_blur_handler = function(ev) {
//   if($(".distributor-fake").is(":focus")===true) {
//     return;
//   }

//   if($(".distributor-fake").val()==="") {
//     $(".distributor_name").val("");
//     $(".distributor_email").val("");
//     $(".ngds-slug").html("");
//     $(".ngds-slug").hide();
//     $(".distributor-fake").show();
//   }

//   if(typeof ev!=='undefined' && typeof $(ev.target).attr('class') !=='undefined' && $(ev.target).attr('class').indexOf('ngds-slug')!==-1) {
//     edit_distributor();
//     return;
//   }

//   var distributor_name = $(".distributor_name").val();
//   var distributor_email = $(".distributor_email").val();

//   if(distributor_name!==null && typeof distributor_name !=='undefined' && distributor_name!=='' && distributor_email!==null && distributor_email!=='' && typeof distributor_email !=='undefined') {
//     $(".distributor-fake").hide();
//     $(".new-distributor").hide();
//     $(".ngds-slug").show();
//     $(".ngds-slug").html(distributor_name);
//     $(".ngds-slug").attr("title",distributor_name+", "+distributor_email);
//   }
// };


// $(document).on('click',distributor_blur_handler);
// $(document).on('blur',".distributor-fake",distributor_blur_handler);