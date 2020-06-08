'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = errorAttr;

var _ruleError = require('./ruleError');

var _ruleError2 = _interopRequireDefault(_ruleError);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function errorAttr(element) {
  var errors = element.errors;


  if (!errors) return null;

  return errors.map(function (error) {
    switch (error.type) {
      case 'include':
        {
          var _error$params = error.params,
              file = _error$params.file,
              partialPath = _error$params.partialPath;


          return (0, _ruleError2.default)('mj-include fails to read file : ' + file + ' at ' + partialPath, element);
        }
      default:
        return null;
    }
  });
}
module.exports = exports['default'];