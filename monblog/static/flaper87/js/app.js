(function(/*! Brunch !*/) {
  'use strict';

  var globals = typeof window !== 'undefined' ? window : global;
  if (typeof globals.require === 'function') return;

  var modules = {};
  var cache = {};

  var has = function(object, name) {
    return ({}).hasOwnProperty.call(object, name);
  };

  var expand = function(root, name) {
    var results = [], parts, part;
    if (/^\.\.?(\/|$)/.test(name)) {
      parts = [root, name].join('/').split('/');
    } else {
      parts = name.split('/');
    }
    for (var i = 0, length = parts.length; i < length; i++) {
      part = parts[i];
      if (part === '..') {
        results.pop();
      } else if (part !== '.' && part !== '') {
        results.push(part);
      }
    }
    return results.join('/');
  };

  var dirname = function(path) {
    return path.split('/').slice(0, -1).join('/');
  };

  var localRequire = function(path) {
    return function(name) {
      var dir = dirname(path);
      var absolute = expand(dir, name);
      return globals.require(absolute);
    };
  };

  var initModule = function(name, definition) {
    var module = {id: name, exports: {}};
    definition(module.exports, localRequire(name), module);
    var exports = cache[name] = module.exports;
    return exports;
  };

  var require = function(name) {
    var path = expand(name, '.');

    if (has(cache, path)) return cache[path];
    if (has(modules, path)) return initModule(path, modules[path]);

    var dirIndex = expand(path, './index');
    if (has(cache, dirIndex)) return cache[dirIndex];
    if (has(modules, dirIndex)) return initModule(dirIndex, modules[dirIndex]);

    throw new Error('Cannot find module "' + name + '"');
  };

  var define = function(bundle, fn) {
    if (typeof bundle === 'object') {
      for (var key in bundle) {
        if (has(bundle, key)) {
          modules[key] = bundle[key];
        }
      }
    } else {
      modules[bundle] = fn;
    }
  };

  globals.require = require;
  globals.require.define = define;
  globals.require.register = define;
  globals.require.brunch = true;
})();

window.require.register("scripts/logo", function(exports, require, module) {
  var flashOffTimeout, flashOnTimeout, logo, logoText, random, replaceAt, replacements, turnOff, turnOn;

  if ((document.body.className.indexOf('is-home')) === -1) {
    return;
  }

  random = function(min, max) {
    return Math.round(Math.random() * (max - min) + min);
  };

  replaceAt = function(str, index, char) {
    return (str.substr(0, index)) + char + (str.substr(index + char.length));
  };

  logo = document.getElementById('logo');

  logoText = logo.innerHTML;

  flashOnTimeout = 500;

  flashOffTimeout = 2500;

  replacements = {
    e: '3',
    s: '5'
  };

  turnOn = function() {
    var index, letter;
    while (true) {
      index = random(0, logoText.length - 1);
      if ((letter = logoText[index]) in replacements) {
        break;
      }
    }
    logo.innerHTML = replaceAt(logoText, index, replacements[letter]);
    return setTimeout(turnOff, random(0, flashOnTimeout));
  };

  turnOff = function() {
    logo.innerHTML = logoText;
    return setTimeout(turnOn, random(0, flashOffTimeout));
  };

  turnOff();
  
});
