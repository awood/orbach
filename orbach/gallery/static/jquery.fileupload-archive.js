(function (factory) {
  'use strict';
  if (typeof define === 'function' && define.amd) {
      // Register as an anonymous AMD module:
      define([
          'jquery',
          './jquery.fileupload-process'
      ], factory);
  } else if (typeof exports === 'object') {
      // Node/CommonJS:
      factory(require('jquery'));
  } else {
      // Browser globals:
      factory(
          window.jQuery
      );
  }
}(function ($) {
  'use strict';
  // Prepend to the default processQueue:
  $.blueimp.fileupload.prototype.options.processQueue.unshift(
    {
      action: 'loadArchive',
      // Use the action as prefix for the "@" options:
      prefix: true,
      fileTypes: '@',
      disabled: '@disableArchivePreview',
      classes: '@archivePreviewClasses'
    },
    {
      action: 'showArchive',
      name: '@archivePreviewName',
      disabled: '@disableArchivePreview'
    }
  );

  $.widget('blueimp.fileupload', $.blueimp.fileupload, {
    options: {
      loadArchiveFileTypes: /^application\/zip$/
    },

    _iconElement: document.createElement('span'),

    processActions: {
      loadArchive: function (data, options) {
        if (options.disabled) {
          return data;
        }
        var file = data.files[data.index];
        var archive = this._iconElement.cloneNode(false);
        if (options.classes) {
          $.each(options.classes, function(ix, val) {
            archive.classList.add(val);
          });
        } else {
          archive.classList.add('fileupload-archive');
        }
        data.archive = archive;
        return data;
      },

      showArchive: function(data, options) {
        if (data.archive && !options.disabled) {
          data.files[data.index][options.name || 'preview'] = data.archive;
        }
        return data;
      }
    }
  });
}));
