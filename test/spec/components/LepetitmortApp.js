'use strict';

describe('Main', function () {
  var LepetitmortApp, component;

  beforeEach(function () {
    var container = document.createElement('div');
    container.id = 'content';
    document.body.appendChild(container);

    LepetitmortApp = require('../../../src/scripts/components/LepetitmortApp.jsx');
    component = LepetitmortApp();
  });

  it('should create a new instance of LepetitmortApp', function () {
    expect(component).toBeDefined();
  });
});
