'use strict';

var main = function () {
  var _ref = _asyncToGenerator( /*#__PURE__*/regeneratorRuntime.mark(function _callee() {
    var response, loaderEl, fingerprints, i, fingerprint, hash;
    return regeneratorRuntime.wrap(function _callee$(_context) {
      while (1) {
        switch (_context.prev = _context.next) {
          case 0:
            _context.next = 2;
            return fetch('/validate/' + token, {
              method: 'post'
            });

          case 2:
            response = _context.sent;

            if (!(response.status !== 204)) {
              _context.next = 6;
              break;
            }

            alert('Invalid token');
            return _context.abrupt('return');

          case 6:
            loaderEl = document.querySelector('.loader');

            loaderEl.appendChild(document.createTextNode('Loading... Please do not close this window.'));

            fingerprints = [];
            i = 0;

          case 10:
            if (!(i < 5)) {
              _context.next = 19;
              break;
            }

            _context.next = 13;
            return getFingerprint();

          case 13:
            fingerprint = _context.sent;
            hash = objectHash(fingerprint);

            fingerprints.push({ hash: hash, fingerprint: fingerprint });

          case 16:
            i += 1;
            _context.next = 10;
            break;

          case 19:
            _context.next = 21;
            return fetch('/fingerprints', {
              method: 'post',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ token: token, fingerprints: fingerprints })
            });

          case 21:

            while (loaderEl.firstChild) {
              loaderEl.removeChild(loaderEl.firstChild);
            }

            loaderEl.appendChild(document.createTextNode("That's it! You may close this window."));

          case 23:
          case 'end':
            return _context.stop();
        }
      }
    }, _callee, this);
  }));

  return function main() {
    return _ref.apply(this, arguments);
  };
}();

function _asyncToGenerator(fn) { return function () { var gen = fn.apply(this, arguments); return new Promise(function (resolve, reject) { function step(key, arg) { try { var info = gen[key](arg); var value = info.value; } catch (error) { reject(error); return; } if (info.done) { resolve(value); } else { return Promise.resolve(value).then(function (value) { step("next", value); }, function (err) { step("throw", err); }); } } return step("next"); }); }; }

function getFingerprint() {
  return new Promise(function (resolve) {
    if (window.requestIdleCallback) {
      requestIdleCallback(function () {
        Fingerprint2.get(resolve);
      });
    } else {
      setTimeout(function () {
        Fingerprint2.get(resolve);
      }, 500);
    }
  });
}

main();