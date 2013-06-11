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
      'name':'distributor-fake',
      'id':function() {
        return "id=distributor-fake";
      },
      'top_classes':function() {
        return "distributor";
      },
      'tag':'input',
      'additional':function() {
        return 'type=text';
      },
      'additional_content':function() {
        return '<a href="javascript:create_responsible_party();" class="new-responsible-party">Add Distributor</a>';
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
  ],
  'custom':[
    {
      'tag':'input',
      'name':'distributor_name',
      'id':'distributor_name',
      'type':'hidden'
    },
     {
      'tag':'input',
      'name':'distributor_email',
      'id':'distributor_email',
      'type':'hidden'
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

$.ajax({
  'url':'/scripts/contribute/resource_form_template.tmf',
  'success':function(response) {
    ngds.structured_form_template = response;
  }

});

$.ajax({
  'url':'/scripts/contribute/add_responsible_party.tmf',
  'success':function(response) {
    ngds.add_responsible_party_template = response;
  }

});

var create_responsible_party = function() {
  var distributor_anch = $(".distributor>a");
  distributor_anch.hide();
  var responsible_parties = {
    'responsible_parties':[
      {
        'label':'Name',
        'name':'responsible_party_name',
        'type':'text'
      },
      {
        'label':'Email',
        'name':'responsible_party_email',
        'type':'text'
      },
      {
        'button':'Create',
        'class':'create_responsible_party'
      },
       {
        'button':'Cancel',
        'class':'cancel_responsible_party'
      }
    ]
  };

  distributor_anch.after(Mustache.render(ngds.add_responsible_party_template,responsible_parties));
  
  $('.create_responsible_party').on('click',function(ev) {
      var name = $("[name=responsible_party_name]").val();
      var email = $("[name=responsible_party_email]").val();

      $.ajax({
        'url':'/api/action/additional_metadata',
        'type':'POST',
        'data':JSON.stringify({
          "process":"create",
          "model":"ResponsibleParty",
          "data":{
            "name":name,
            "email":email
          }
        })
  });

  });
}

$(".form-body").on('blur',"#distributor-fake",function(ev) {
  var distributor_name = $("#distributor_name").val();
  var distributor_email = $("#distributor_email").val();
  console.log(distributor_name);
  console.log(distributor_email);

});