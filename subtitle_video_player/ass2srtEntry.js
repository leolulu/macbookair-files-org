/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./main.js":
/*!*****************!*\
  !*** ./main.js ***!
  \*****************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

eval("var ass2srt = __webpack_require__(/*! ass-to-srt */ \"./node_modules/ass-to-srt/index.js\");\r\n\r\n// 将 subsrt 暴露到全局作用域\r\nwindow.ass2srt = ass2srt;\n\n//# sourceURL=webpack:///./main.js?");

/***/ }),

/***/ "./node_modules/ass-to-srt/index.js":
/*!******************************************!*\
  !*** ./node_modules/ass-to-srt/index.js ***!
  \******************************************/
/***/ ((module) => {

eval("var re_ass = new RegExp('Dialogue:\\\\s\\\\d,' + // get time and subtitle\n        '(\\\\d+:\\\\d\\\\d:\\\\d\\\\d.\\\\d\\\\d),' +     // start time\n        '(\\\\d+:\\\\d\\\\d:\\\\d\\\\d.\\\\d\\\\d),' +     // end time\n        '([^,]*),' +                  // object\n        '([^,]*),' +                  // actor\n        '(?:[^,]*,){4}' +\n        '(.*)$', 'i');                // subtitle\nvar re_newline = /\\\\n/ig // replace \\N with newline\nvar re_style = /\\{[^}]+\\}/g // replace style\n\nmodule.exports = function(assText) {\n  var srts = [];\n  String(assText).split(/\\r*\\n/).forEach(function(line) {\n    var m = line.match(re_ass);\n    if(!m) return;\n\n    var start = m[1], end = m[2], what = m[3], actor = m[4], text = m[5];\n    text = text.replace(re_style, '').replace(re_newline, '\\r\\n');\n    srts.push({start: start, end: end, text: text});\n  });\n\n  var i = 1;\n  var output = srts.sort(function(d1, d2) {\n    var s1 = assTime2Int(d1.start);\n    var s2 = assTime2Int(d2.start);\n    var e1 = assTime2Int(d1.end);\n    var e2 = assTime2Int(d2.end);\n\n    return s1 != s2 ? s1 - s2 : e1 - e2;\n  }).map(function(srt) {\n    var start = assTime2SrtTime(srt.start);\n    var end = assTime2SrtTime(srt.end);\n    return (i++) + '\\n'\n      + start + ' --> ' + end + '\\n'\n      + srt.text + '\\n\\n';\n  }).join('');\n\n  return output;\n};\n\nfunction assTime2Int(assTime) {\n  return parseInt(assTime.replace(/[^0-9]/g, ''));\n}\n\nfunction assTime2SrtTime(assTime) {\n  var h = m = s = '00', ms = '000';\n  var t = assTime.split(':');\n  if(t.length > 0) h = t[0].length == 1 ? '0'+t[0] : t[0];\n  if(t.length > 1) m = t[1].length == 1 ? '0'+t[1] : t[1];\n  if(t.length > 2) {\n    var t2 = t[2].split('.');\n    if(t2.length > 0) s = t2[0].length == 1 ? '0'+t2[0] : t2[0];\n    if(t2.length > 0) ms = t2[1].length == 2 ? '0'+t2[1] : t2[1].length == 1 ? '00'+ t2[1] : t2[1];\n  }\n  return [h, m , s+','+ms].join(':');\n}\n\n\n\n\n//# sourceURL=webpack:///./node_modules/ass-to-srt/index.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = __webpack_require__("./main.js");
/******/ 	
/******/ })()
;