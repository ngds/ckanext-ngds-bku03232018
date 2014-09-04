this.ckan.module('ngds-contribute', function (jQuery, _) {
  return {
    initialize: function () {
      var message
        , form
        , button
        , ngdsPackage
        , ngdsRecord
        ;

      message = _('There are unsaved modifications to this form').fetch();
      this.el.incompleteFormWarning(message);
      // Internet Explorer 7 fix for forms with <button type="submit">
      if ($('html').hasClass('ie7')) {
        this.el.on('submit', function() {
          form = $(this);
          $('button', form).each(function() {
            button = $(this);
            $('<input type="hidden">').prop('name', button.prop('name')).prop('value', button.val()).appendTo(form);
          });
        });
      }

      ngdsPackage = {
        _id: 'undefined',
        Title: 'undefined',
        Description: 'undefined',
        PublicationDate: 'undefined',
        ResourceId: 'undefined',
        Authors: [{
          Name: 'undefined',
          OrganizationName: 'undefined',
          ContactInformation: {
            Phone: 'undefined',
            email: 'undefined',
            Address: {
              Street: 'undefined',
              City: 'undefined',
              State: 'undefined',
              Zip: 'undefined'
            }
          }
        }],
        Keywords: [],
        GeographicExtent: {
          NorthBound: 'undefined',
          SouthBound: 'undefined',
          EastBound: 'undefined',
          WestBound: 'undefined'
        },
        Distributors: [{
          Name: 'undefined',
          OrganizationName: 'undefined',
          ContactInformation: {
            Phone: 'undefined',
            email: 'undefined',
            Address: {
              Street: 'undefined',
              City: 'undefined',
              State: 'undefined',
              Zip: 'undefined'
            }
          }
        }],
        MetadataContact: {
          Name: 'undefined',
          OrganizationName: 'undefined',
          ContactInformation: {
            Phone: 'undefined',
            email: 'undefined',
            Address: {
              Street: 'undefined',
              City: 'undefined',
              State: 'undefined',
              Zip: 'undefined'
            }
          }
        }
      };

      ngdsRecord = {
        URL: 'undefined',
        Name: 'undefined',
        Description: 'undefined',
        Distributor: 'undefined',
        ServiceType: 'undefined',
        Layer: 'undefined',
        ContentModelURI: 'undefined',
        ContentModelVersion: 'undefined'
      };

      $('#ngds-dataset-edit').submit(function (e) {
        console.log(e);
        return true;
      })
    }
  };
});